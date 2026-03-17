from rich.console import Console
from rich.panel import Panel
from rich.align import Align

BANNER_TEXT = """
██████╗  █████╗ ██╗     ██╗      █████╗ ███████╗
██╔══██╗██╔══██╗██║     ██║     ██╔══██╗██╔════╝
██████╔╝███████║██║     ██║     ███████║███████╗
██╔═══╝ ██╔══██║██║     ██║     ██╔══██║╚════██║
██║     ██║  ██║███████╗███████╗██║  ██║███████║
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝
"""

SUBTITLE = "Pallas Agent — Built to evolve with you."
VINKURA_BRAND = "VINKURA AI"
STATUS_LINE = "● System: Ready | Mode: Autonomous"

def display_banner(console: Console):
    banner = Align.center(f"[bold blue]{BANNER_TEXT}[/bold blue]", vertical="middle")
    subtitle = Align.center(f"[italic white]{SUBTITLE}[/italic white]")
    brand = Align.center(f"[bold cyan]<{VINKURA_BRAND}>[/bold cyan]")
    status = Align.center(f"[dim white]{STATUS_LINE}[/dim white]")
    
    console.print(banner)
    console.print(subtitle)
    console.print(brand)
    console.print(status)
    console.print("\n")
