import click
import os
import time
from rich.console import Console
from dotenv import load_dotenv, set_key

from pallas_core.pallas_constants import PROJECT_NAME, VERSION
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
        from pallas_core.pallas_constants import (
            PROVIDER_ANTHROPIC, PROVIDER_GOOGLE, PROVIDER_OPENAI,
            PROVIDER_OPENROUTER, PROVIDER_OLLAMA
        )
        import questionary
        from pallas_core.pallas_state import PallasState
        
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
    from pallas_cli.commands import _register_all_tools

    agent = AgentLoop(provider=provider, model=model, human_in_loop=False)
    _register_all_tools(agent)
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
    elif platform == "whatsapp":
        from gateway.platforms.whatsapp import WhatsAppPlatform
        bot = WhatsAppPlatform(on_message=on_message)
        console.print(f"[bold blue]⚡ Initiating WhatsApp (Twilio) Gateway...[/bold blue]")
        bot.connect()
        console.print("[dim]WhatsApp gateway ready. Waiting for webhook events...[/dim]")
        import time
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            bot.disconnect()
    elif platform == "signal":
        from gateway.platforms.signal import SignalPlatform
        bot = SignalPlatform(on_message=on_message)
        console.print(f"[bold blue]⚡ Initiating Signal Gateway...[/bold blue]")
        bot.connect()
        console.print("[dim]Signal gateway ready. Listening for messages...[/dim]")
        import time
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            bot.disconnect()
    elif platform == "email":
        from gateway.platforms.email import EmailPlatform
        bot = EmailPlatform(on_message=on_message)
        console.print(f"[bold blue]⚡ Initiating Email (IMAP/SMTP) Gateway...[/bold blue]")
        bot.connect()
        console.print("[dim]Email gateway polling. Press Ctrl+C to stop.[/dim]")
        import time
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            bot.disconnect()
    elif platform == "homeassistant":
        from gateway.platforms.homeassistant import HomeAssistantPlatform
        bot = HomeAssistantPlatform(on_message=on_message)
        console.print(f"[bold blue]⚡ Initiating Home Assistant Gateway...[/bold blue]")
        bot.connect()
        console.print("[dim]Home Assistant gateway ready. Press Ctrl+C to stop.[/dim]")
        import time
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            bot.disconnect()
    else:
        console.print(f"[red]Error: Platform '{platform}' is not supported.[/red]")
        console.print("[dim]Supported: telegram, discord, slack, whatsapp, signal, email, homeassistant[/dim]")


@cli.command()
@click.argument("action", type=click.Choice(["list", "search", "install", "create"]), default="list", required=False)
@click.argument("query", required=False)
@click.option("--optional", is_flag=True, default=False, help="Show optional skills")
def skills(action, query, optional):
    """Browse, search, install, and create skills."""
    import shutil
    from pathlib import Path
    from rich.table import Table

    project_root = Path(__file__).parent.parent
    builtin_skills_dir = project_root / ("optional-skills" if optional else "skills")
    user_skills_dir = Path.home() / ".pallas" / "skills"

    if action == "list":
        table = Table(title="Available Skills" + (" (optional)" if optional else ""), show_header=True)
        table.add_column("Name", style="cyan")
        table.add_column("Category")
        table.add_column("Installed", style="green")

        if builtin_skills_dir.exists():
            for category_dir in sorted(builtin_skills_dir.iterdir()):
                if not category_dir.is_dir():
                    continue
                for skill_dir in sorted(category_dir.iterdir()):
                    if not skill_dir.is_dir():
                        continue
                    skill_md = skill_dir / "SKILL.md"
                    if skill_md.exists():
                        installed = "✓" if (user_skills_dir / skill_dir.name).exists() else ""
                        table.add_row(skill_dir.name, category_dir.name, installed)
        console.print(table)

    elif action == "search":
        if not query:
            console.print("[red]Usage: pallas skills search <query>[/red]")
            return
        found = False
        for skills_root in [project_root / "skills", project_root / "optional-skills"]:
            if not skills_root.exists():
                continue
            for skill_md in skills_root.rglob("SKILL.md"):
                content = skill_md.read_text(encoding="utf-8", errors="replace")
                if query.lower() in content.lower() or query.lower() in skill_md.parent.name.lower():
                    console.print(f"  [cyan]{skill_md.parent.name}[/cyan] ({skill_md.parent.parent.parent.name}/{skill_md.parent.parent.name})")
                    found = True
        if not found:
            console.print(f"[dim]No skills matching '{query}'.[/dim]")

    elif action == "install":
        if not query:
            console.print("[red]Usage: pallas skills install <skill-name>[/red]")
            return
        for skills_root in [project_root / "skills", project_root / "optional-skills"]:
            for skill_dir in skills_root.rglob(query):
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    dest = user_skills_dir / query
                    shutil.copytree(str(skill_dir), str(dest), dirs_exist_ok=True)
                    console.print(f"[green]✓ Installed '{query}' to ~/.pallas/skills/{query}[/green]")
                    return
        console.print(f"[red]Skill '{query}' not found.[/red]")

    elif action == "create":
        if not query:
            console.print("[red]Usage: pallas skills create <skill-name>[/red]")
            return
        skill_dir = user_skills_dir / query
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / "SKILL.md"
        template = f"""# {query.replace('-', ' ').title()}

## Description
[Describe what this skill does in 2-3 sentences.]

## When to Use
- [Use case 1]
- [Use case 2]

## Instructions
[Detailed instructions for the agent. This content is injected into the system prompt when the skill is active.]

## Examples
- "[Example prompt 1]"
- "[Example prompt 2]"

## Requirements
- [Any tools or env vars needed]
"""
        skill_file.write_text(template, encoding="utf-8")
        console.print(f"[green]✓ Created skill scaffold at ~/.pallas/skills/{query}/SKILL.md[/green]")
        console.print(f"[dim]Edit the file to add your skill instructions.[/dim]")


@cli.command()
def setup():
    """Interactive onboarding wizard for first-time setup."""
    import questionary
    from pallas_core.pallas_constants import (
        PROVIDER_ANTHROPIC, PROVIDER_GOOGLE, PROVIDER_OPENAI,
        PROVIDER_OPENROUTER, PROVIDER_OLLAMA
    )
    from pallas_core.pallas_state import PallasState
    from dotenv import set_key
    import shutil
    from pathlib import Path

    display_banner(console)
    console.print("\n[bold cyan]Pallas Setup Wizard[/bold cyan]\n")

    env_path = Path.home() / ".pallas" / ".env"
    env_path.parent.mkdir(parents=True, exist_ok=True)
    if not env_path.exists():
        env_path.touch()

    # Step 1: Choose provider
    provider = questionary.select(
        "Select your default LLM provider:",
        choices=[
            questionary.Choice("Anthropic (Claude - Recommended)", value=PROVIDER_ANTHROPIC),
            questionary.Choice("Google (Gemini)", value=PROVIDER_GOOGLE),
            questionary.Choice("OpenAI (GPT)", value=PROVIDER_OPENAI),
            questionary.Choice("OpenRouter (Multi-model)", value=PROVIDER_OPENROUTER),
            questionary.Choice("Ollama (Local/Offline)", value=PROVIDER_OLLAMA),
        ]
    ).ask()

    if not provider:
        console.print("[red]Setup cancelled.[/red]")
        return

    # Step 2: Enter API key
    key_map = {
        PROVIDER_ANTHROPIC: "ANTHROPIC_API_KEY",
        PROVIDER_GOOGLE: "GOOGLE_API_KEY",
        PROVIDER_OPENAI: "OPENAI_API_KEY",
        PROVIDER_OPENROUTER: "OPENROUTER_API_KEY",
    }
    env_var = key_map.get(provider)
    if env_var:
        existing = os.getenv(env_var, "")
        if existing:
            console.print(f"[dim]{env_var} already set.[/dim]")
        else:
            api_key = questionary.password(f"Enter your {env_var}:").ask()
            if api_key:
                set_key(str(env_path), env_var, api_key)
                os.environ[env_var] = api_key
                console.print(f"[green]✓ {env_var} saved.[/green]")

    # Step 3: Test connection
    console.print(f"\n[dim]Testing connection to {provider}...[/dim]")
    try:
        from pallas_core.provider_adapter import ProviderAdapter
        adapter = ProviderAdapter(provider)
        result = adapter.completion(
            messages=[{"role": "user", "content": "Say 'ok' in one word."}],
            max_tokens=10,
        )
        if result.get("error"):
            console.print(f"[red]✗ Connection failed: {result['error']}[/red]")
        else:
            console.print(f"[green]✓ Connection successful![/green]")
    except Exception as e:
        console.print(f"[red]✗ Connection error: {e}[/red]")

    # Step 4: Save default provider
    state = PallasState()
    state.set("default_provider", provider)
    set_key(str(env_path), "PALLAS_PROVIDER", provider)

    # Step 5: Copy default skills
    project_root = Path(__file__).parent.parent
    builtin_skills = project_root / "skills"
    user_skills = Path.home() / ".pallas" / "skills"
    if builtin_skills.exists():
        shutil.copytree(str(builtin_skills), str(user_skills), dirs_exist_ok=True)
        console.print(f"[green]✓ Default skills installed.[/green]")

    console.print(f"\n[bold green]✅ Setup complete! Run:[/bold green] [bold cyan]pallas start[/bold cyan]\n")


@cli.command()
def uninstall():
    """Remove Pallas and all associated data."""
    import questionary
    import shutil
    from pathlib import Path

    console.print("[bold red]Pallas Uninstall[/bold red]")
    console.print("[dim]This will delete ~/.pallas/ and uninstall the pallas CLI.[/dim]\n")

    confirmed = questionary.confirm(
        "Are you sure you want to uninstall Pallas? This cannot be undone.",
        default=False,
    ).ask()

    if not confirmed:
        console.print("[dim]Uninstall cancelled.[/dim]")
        return

    pallas_home = Path.home() / ".pallas"
    if pallas_home.exists():
        shutil.rmtree(str(pallas_home))
        console.print(f"[green]✓ Removed ~/.pallas/[/green]")

    # Try uv tool uninstall first, fall back to pip
    import subprocess
    result = subprocess.run(
        ["uv", "tool", "uninstall", "pallas-agent"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        console.print("[green]✓ Uninstalled via uv.[/green]")
    else:
        result2 = subprocess.run(
            ["pip", "uninstall", "pallas-agent", "-y"],
            capture_output=True, text=True
        )
        if result2.returncode == 0:
            console.print("[green]✓ Uninstalled via pip.[/green]")
        else:
            console.print("[yellow]Could not auto-uninstall. Run manually: uv tool uninstall pallas-agent[/yellow]")

    console.print("\n[bold]Pallas has been removed. Goodbye.[/bold]")


def main():
    cli()


if __name__ == "__main__":
    main()
