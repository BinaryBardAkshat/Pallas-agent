import click
from rich.console import Console
from rich.panel import Panel
from pallas_constants import PROJECT_NAME, VERSION

from pallas_cli.banner import display_banner

console = Console()

@click.group()
@click.version_option(version=VERSION)
def cli():
    pass

@cli.command()
def start():
    display_banner(console)
    console.print("[bold]Welcome, Operator.[/bold] How can I assist you today?\n")

@cli.command()
def doctor():
    console.print("[yellow]Running system diagnostics...[/yellow]")
    # Basic check for environment variables
    import os
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    if anthropic_key:
        console.print("[green]✔[/green] Anthropic API Key found.")
    else:
        console.print("[red]✘[/red] Anthropic API Key missing.")
        
    if google_key:
        console.print("[green]✔[/green] Google API Key found.")
    else:
        console.print("[red]✘[/red] Google API Key missing.")

def main():
    cli()

if __name__ == "__main__":
    main()
