import click
import os
import time
from rich.console import Console
from dotenv import load_dotenv, set_key

from pallas_constants import PROJECT_NAME, VERSION
from pallas_cli.banner import display_banner
from pallas_cli.commands import chat_session, show_config
from pallas_cli.doctor import run_doctor as _run_doctor

# Attempt to load local project .env first, fallback to global user .env
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
    load_dotenv(dotenv_path=os.path.expanduser("~/.pallas/.env"))

console = Console()


@click.group()
@click.version_option(version=VERSION, prog_name=PROJECT_NAME)
def cli():
    pass


@cli.command()
@click.option("--provider", "-p", default=None, help="LLM provider to use.")
@click.option("--model", "-m", default=None, help="Specific model ID to use.")
@click.option("--no-approval", is_flag=True, default=False, help="Skip human-in-loop tool approval.")
@click.option("--session", "-s", default=None, help="Resume a specific session ID.")
def start(provider, model, no_approval, session):
    with console.status("[bold cyan]Initializing Pallas Core modules...[/bold cyan]", spinner="dots"):
        time.sleep(1.2)  # Simulate module bootstrapping
        from pallas_constants import (
            PROVIDER_ANTHROPIC, PROVIDER_GOOGLE, PROVIDER_OPENAI,
            PROVIDER_OPENROUTER, PROVIDER_OLLAMA
        )
        import questionary
        from pallas_state import PallasState
        
    display_banner(console)
    state = PallasState()
    
    saved_provider = state.get("default_provider", None)
    
    if not provider:
        if saved_provider and saved_provider != "None":
            provider = saved_provider
        else:
            provider = questionary.select(
                "Select your LLM Provider Operator:",
                choices=[
                    questionary.Choice("Anthropic (Claude 3.7+ - Recommended)", value=PROVIDER_ANTHROPIC),
                    questionary.Choice("Google (Gemini 2.5 Pro)", value=PROVIDER_GOOGLE),
                    questionary.Choice("OpenAI (GPT-5.4)", value=PROVIDER_OPENAI),
                    questionary.Choice("OpenRouter (Multi-model)", value=PROVIDER_OPENROUTER),
                    questionary.Choice("Ollama (Local/Offline)", value=PROVIDER_OLLAMA),
                ]
            ).ask()
            if provider:
                state.set("default_provider", provider)
        
    if not provider:
        provider = PROVIDER_ANTHROPIC

    env_path = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(env_path):
        env_path = os.path.expanduser("~/.pallas/.env")
        if not os.path.exists(env_path):
            os.makedirs(os.path.dirname(env_path), exist_ok=True)
            with open(env_path, "w") as f:
                f.write("")
                
    key_map = {
        PROVIDER_ANTHROPIC: "ANTHROPIC_API_KEY",
        PROVIDER_GOOGLE: "GOOGLE_API_KEY",
        PROVIDER_OPENAI: "OPENAI_API_KEY",
        PROVIDER_OPENROUTER: "OPENROUTER_API_KEY"
    }

    env_var = key_map.get(provider)
    if env_var and not os.getenv(env_var):
        api_key = questionary.password(f"Please enter your {env_var} (will be saved securely):").ask()
        if api_key:
            set_key(env_path, env_var, api_key)
            os.environ[env_var] = api_key
            console.print(f"[green]✔ Saved {env_var} securely![/green]")

    console.print("\n[bold]Welcome, Operator.[/bold] Type your task. Press Ctrl+C to exit.\n")
    chat_session(provider=provider, model=model, human_in_loop=not no_approval, session_id=session)


@cli.command()
def info():
    from pallas_core.model_metadata import suggest_model
    display_banner(console)
    console.print("\n[bold cyan]Pallas Agent System v0.1.0[/bold cyan]")
    console.print("Pallas is an elite autonomous AI coding system and research environment.")
    
    console.print("\n[bold]LLM Optimized Use Cases:[/bold]")
    console.print(f" • [green]Coding:[/green]     {suggest_model('coding')} (Ultra Logic)")
    console.print(f" • [green]Research:[/green]   {suggest_model('research')} (Long Context)")
    console.print(f" • [green]Heavy:[/green]      {suggest_model('heavy')} (Reasoning Focus)")
    console.print(f" • [green]Local:[/green]      {suggest_model('local')} (Offline Mode)")

    console.print("\n[bold]The 5-Brain Architecture:[/bold]")
    console.print(" 1. [yellow]Conversation Layer[/yellow] - Immersive CLI and Multi-Platform Gateways.")
    console.print(" 2. [yellow]Agent Loop[/yellow] - Sequential Perception-Action-Reflection cycle.")
    console.print(" 3. [yellow]Tool Sandbox[/yellow] - Native OS control (Terminal, File, Browser).")
    console.print(" 4. [yellow]Learning Memory[/yellow] - FTS5 SQL persistent history & skill codification.")
    console.print(" 5. [yellow]Infrastructure Layer[/yellow] - Execution sandboxes (Docker, SSH, Shell).")
    
    console.print("\n[dim]Commands: pallas start | pallas ask | pallas doctor | pallas keys[/dim]\n")


@cli.command()
@click.argument("provider_name")
@click.argument("key_value")
def keys(provider_name, key_value):
    """Securely set an API key for a provider."""
    env_path = os.path.expanduser("~/.pallas/.env")
    os.makedirs(os.path.dirname(env_path), exist_ok=True)
    
    key_map = {
        "anthropic": "ANTHROPIC_API_KEY",
        "google": "GOOGLE_API_KEY",
        "openai": "OPENAI_API_KEY",
        "openrouter": "OPENROUTER_API_KEY"
    }
    
    var_name = key_map.get(provider_name.lower())
    if not var_name:
        console.print(f"[red]Error: Unknown provider '{provider_name}'.[/red]")
        return
        
    set_key(env_path, var_name, key_value)
    console.print(f"[green]✔ Locked in {var_name} securely in ~/.pallas/.env[/green]")



@cli.command()
def doctor():
    _run_doctor(console)


@cli.command()
def config():
    show_config(console)


@cli.command()
@click.argument("message")
@click.option("--provider", "-p", default="anthropic")
@click.option("--model", "-m", default=None)
def ask(message, provider, model):
    from environments.agent_loop import AgentLoop
    from toolsets import register_all

    agent = AgentLoop(provider=provider, model=model, human_in_loop=False)
    register_all(agent, agent.memory)
    agent.run(message)


@cli.command()
@click.argument("platform")
def gateway(platform):
    from gateway.session import get_router
    router = get_router()

    def on_message(chat_id, text, platform_name):
        return router.route(str(chat_id), platform_name, text)

    platform = platform.lower()
    if platform == "telegram":
        from gateway.platforms.telegram import TelegramPlatform
        bot = TelegramPlatform(on_message=on_message)
        console.print(f"[bold blue]⚡ Initiating Telegram Unified Gateway...[/bold blue]")
        bot.start()
    elif platform == "discord":
        from gateway.platforms.discord import DiscordPlatform
        bot = DiscordPlatform(on_message=on_message)
        console.print(f"[bold blue]⚡ Initiating Discord Unified Gateway...[/bold blue]")
        bot.start()
    elif platform == "slack":
        from gateway.platforms.slack import SlackPlatform
        bot = SlackPlatform(on_message=on_message)
        console.print(f"[bold blue]⚡ Initiating Slack Unified Gateway...[/bold blue]")
        bot.start()
    else:
        console.print(f"[red]Error: Platform '{platform}' is not supported yet.[/red]")


def main():
    cli()


if __name__ == "__main__":
    main()
