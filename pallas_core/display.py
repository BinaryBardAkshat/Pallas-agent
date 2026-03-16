from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.text import Text
from typing import Any, Dict, List, Optional


console = Console()


def print_response(content: str, title: str = "Pallas"):
    md = Markdown(content)
    console.print(Panel(md, title=f"[bold cyan]{title}[/bold cyan]", border_style="dim white"))


def print_tool_call(name: str, args: Dict[str, Any]):
    console.print(f"[dim]  > Tool: [bold]{name}[/bold] | args: {args}[/dim]")


def print_tool_result(name: str, result: str, error: bool = False):
    style = "red" if error else "dim green"
    console.print(f"[{style}]  < {name}: {result[:200]}[/{style}]")


def print_thinking(text: str = "Thinking..."):
    console.print(f"[dim italic]  {text}[/dim italic]")


def print_usage(summary: Dict[str, Any]):
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_row("[dim]Tokens[/dim]", str(summary.get("total_tokens", 0)))
    table.add_row("[dim]Cost[/dim]", f"${summary.get('total_cost_usd', 0):.4f}")
    table.add_row("[dim]Calls[/dim]", str(summary.get("calls", 0)))
    console.print(table)


def print_memories(memories: List[Dict[str, Any]]):
    if not memories:
        return
    console.print("\n[dim]Recalled memories:[/dim]")
    for m in memories:
        console.print(f"  [dim]- {m['content'][:120]}[/dim]")
