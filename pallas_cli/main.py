import click
import os
from rich.console import Console
from dotenv import load_dotenv

from pallas_constants import PROJECT_NAME, VERSION
from pallas_cli.banner import display_banner
from pallas_cli.commands import chat_session, show_config
from pallas_cli.doctor import run_doctor as _run_doctor

load_dotenv()
console = Console()


@click.group()
@click.version_option(version=VERSION, prog_name=PROJECT_NAME)
def cli():
    pass


@cli.command()
@click.option("--provider", "-p", default="anthropic", help="LLM provider to use.")
@click.option("--model", "-m", default=None, help="Specific model ID to use.")
@click.option("--no-approval", is_flag=True, default=False, help="Skip human-in-loop tool approval.")
@click.option("--session", "-s", default=None, help="Resume a specific session ID.")
def start(provider, model, no_approval, session):
    display_banner(console)
    console.print("[bold]Welcome, Operator.[/bold] Type your task. Press Ctrl+C to exit.\n")
    chat_session(provider=provider, model=model, human_in_loop=not no_approval, session_id=session)


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

    if platform == "telegram":
        from gateway.platforms.telegram import TelegramPlatform
        bot = TelegramPlatform(on_message=on_message)
        console.print(f"[bold]Starting Telegram gateway...[/bold]")
        bot.start()
    else:
        console.print(f"[red]Unknown platform: {platform}[/red]")


def main():
    cli()


if __name__ == "__main__":
    main()
