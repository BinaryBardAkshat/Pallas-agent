#!/usr/bin/env python3
import sys
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    provider = os.getenv("PALLAS_PROVIDER", "anthropic")
    model = os.getenv("PALLAS_MODEL", None)
    human_in_loop = os.getenv("PALLAS_NO_APPROVAL", "").lower() not in ("1", "true", "yes")

    from pallas_cli.banner import display_banner
    from pallas_cli.commands import chat_session
    from rich.console import Console

    console = Console()
    display_banner(console)
    console.print("[bold]Pallas Agent running. Type your task below.[/bold]\n")
    chat_session(provider=provider, model=model, human_in_loop=human_in_loop)


if __name__ == "__main__":
    main()
