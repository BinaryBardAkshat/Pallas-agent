"""
display.py — Pallas terminal UI v2.
Rich, clean, and a little mysterious.
"""
import random
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
from rich.tree import Tree

# ── Theme ─────────────────────────────────────────────────────────────────────

_THEME = Theme({
    "pallas.user":    "bold cyan",
    "pallas.agent":   "bold white",
    "pallas.tool":    "yellow",
    "pallas.result":  "green",
    "pallas.error":   "bold red",
    "pallas.memory":  "magenta",
    "pallas.dim":     "dim white",
    "pallas.step":    "bold blue",
    "pallas.accent":  "bold cyan",
    "pallas.subtle":  "dim cyan",
    "pallas.warn":    "bold yellow",
    "pallas.success": "bold green",
})

console = Console(theme=_THEME, highlight=False)

# ── Flavour text ──────────────────────────────────────────────────────────────

_THINKING_QUIPS = [
    "Consulting the oracle…",
    "Running the inference engine…",
    "Deep thought in progress…",
    "The owl ponders…",
    "Processing with intent…",
    "Traversing the knowledge graph…",
    "Connecting the dots…",
    "Signal acquired. Reasoning…",
    "Weighing all possibilities…",
    "Almost there…",
]

_FAREWELL_QUIPS = [
    "Until next time, Operator.",
    "The owl returns to the dark.",
    "Memory persists. See you soon.",
    "Pallas never truly sleeps.",
    "Session saved. Goodbye.",
    "Stay curious.",
    "The work continues.",
]

_STARTUP_QUIPS = [
    "The owl watches. The agent thinks.",
    "Forged by Vinkura. Deployed by you.",
    "Memory loaded. Tools armed. Ready.",
    "Autonomous and aware.",
    "Self-evolving since birth.",
    "Built to grow with you.",
]

# ── Easter egg content ────────────────────────────────────────────────────────

OWL_ASCII = r"""
      .     .
    .  \   /  .
      . \ / .
   .----(   )----.
  /   .' --- '.   \
 |  .'  (o)|(o) '. |
  \ '.   --=--   .' /
   '-.___'---'___.-'
        |     |
        '-----'
"""

COFFEE_ASCII = r"""
     ( (
      ) )
   ._______.
   |       |]
   \       /
    `-----'
  ☕  BREAK  ☕
"""

MATRIX_CHARS = "ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ01"

FORTUNES = [
    "A complex system that works is invariably found to have evolved from a simple system that worked.",
    "The best tool is the one you actually use.",
    "Any sufficiently advanced technology is indistinguishable from magic.",
    "The purpose of abstracting is not to be vague, but to create a new semantic level.",
    "First, solve the problem. Then, write the code.",
    "Premature optimisation is the root of all evil.",
    "Make it work. Make it right. Make it fast.",
    "The most dangerous thought you can have is that you know what you're doing.",
    "If debugging is the process of removing bugs, then programming must be the process of putting them in.",
    "Wisdom begins with knowing what you don't know.",
    "The owl who flies farthest sees the most.",
    "Every great system starts with 'hello world' and ends with 'what have I built?'",
]

# ── Core display functions ────────────────────────────────────────────────────

def print_response(content: str, title: str = "Pallas") -> None:
    """Render the agent response in a styled markdown panel."""
    if not content or not content.strip():
        return
    md = Markdown(content, code_theme="monokai")
    console.print(
        Panel(
            md,
            title=f"[pallas.agent] {title} [/pallas.agent]",
            title_align="left",
            border_style="blue",
            padding=(1, 2),
        )
    )


def print_tool_call(name: str, args: Dict[str, Any]) -> None:
    """Print a tool invocation line."""
    display_args = {}
    for k, v in args.items():
        sv = str(v)
        display_args[k] = (sv[:100] + "…") if len(sv) > 100 else sv

    arg_parts = []
    for k, v in display_args.items():
        # escape brackets so Rich doesn't interpret them as markup
        safe_v = str(v).replace("[", "\\[")
        arg_parts.append(f"[pallas.dim]{k}[/pallas.dim]=[pallas.subtle]{safe_v!r}[/pallas.subtle]")
    args_str = ", ".join(arg_parts)

    console.print(f"  [pallas.tool]⚡ {name}[/pallas.tool]({args_str})")


def print_tool_result(name: str, result: str, error: bool = False) -> None:
    """Print a tool result line."""
    style  = "pallas.error"  if error else "pallas.result"
    prefix = "✗" if error else "✓"
    safe_result = result.replace("[", "\\[")
    truncated = safe_result[:400] + ("…" if len(safe_result) > 400 else "")
    console.print(f"  [{style}]{prefix} {name}:[/{style}] [pallas.dim]{truncated}[/pallas.dim]")


def print_memories(memories: List[Dict[str, Any]]) -> None:
    """
    Render recalled memories as an expandable tree — the terminal equivalent
    of a dropdown. Shows a single root node with count; snippets hang below.
    """
    if not memories:
        return

    count = len(memories)
    label = f"[pallas.memory]◈  {count} memor{'y' if count == 1 else 'ies'} recalled[/pallas.memory]"
    tree = Tree(label, guide_style="dim magenta", highlight=False)

    for m in memories:
        raw = m.get("content", "").replace("\n", " ")
        snippet = (raw[:130] + "…") if len(raw) > 130 else raw
        safe = snippet.replace("[", "\\[")
        tree.add(f"[dim]{safe}[/dim]")

    console.print(tree)
    console.print()


def print_step_header(step: int, max_steps: int) -> None:
    console.print(f"  [pallas.step]● Step {step}/{max_steps}[/pallas.step]", end=" ")


def print_thinking(text: str = "") -> str:
    """Return a random thinking quip (used in spinner text)."""
    return text or random.choice(_THINKING_QUIPS)


def print_usage(summary: Dict[str, Any]) -> None:
    table = Table(
        show_header=True,
        header_style="pallas.dim",
        box=None,
        padding=(0, 2),
        title="[pallas.dim]Session Usage[/pallas.dim]",
    )
    table.add_column("Metric", style="pallas.dim")
    table.add_column("Value",  style="bold white")
    table.add_row("Tokens",    f"{summary.get('total_tokens', 0):,}")
    table.add_row("Cost",      f"${summary.get('total_cost_usd', 0):.4f}")
    table.add_row("API Calls", str(summary.get("calls", 0)))
    if summary.get("models"):
        table.add_row("Models", ", ".join(summary["models"]))
    console.print(table)


def print_rule(title: str = "") -> None:
    console.print(Rule(title=title, style="pallas.dim"))


def print_session_info(session_id: str, provider: str, model: str) -> None:
    console.print(
        f"[pallas.dim]Session: {session_id[:8]}… | "
        f"Provider: [bold]{provider}[/bold] | "
        f"Model: [bold]{model}[/bold][/pallas.dim]\n"
    )


# ── Easter egg functions ──────────────────────────────────────────────────────

def easter_owl() -> None:
    """Show the Pallas owl."""
    console.print(f"[bold cyan]{OWL_ASCII}[/bold cyan]")
    console.print(Align.center("[dim italic]Pallas — The Owl of Athena. Knowledge made autonomous.[/dim italic]"))
    console.print()


def easter_coffee() -> None:
    """Coffee break easter egg."""
    console.print(f"[bold yellow]{COFFEE_ASCII}[/bold yellow]")
    console.print(Align.center("[dim]You deserve it. Taking a short break won't break the loop.[/dim]"))
    console.print()


def easter_matrix(duration: float = 2.5) -> None:
    """Minimal matrix rain in the terminal."""
    width = console.width or 80
    cols  = width // 2
    end   = time.time() + duration

    with Live(console=console, refresh_per_second=12) as live:
        while time.time() < end:
            line = " ".join(
                random.choice(MATRIX_CHARS) if random.random() > 0.3 else " "
                for _ in range(cols)
            )
            live.update(Text(line, style="bold green"))
    console.print()
    console.print(Align.center("[dim]Wake up, Operator.[/dim]"))
    console.print()


def easter_fortune() -> None:
    """Print a random fortune."""
    fortune = random.choice(FORTUNES)
    console.print(
        Panel(
            f"[italic]{fortune}[/italic]",
            title="[dim]◈  Fortune[/dim]",
            border_style="dim magenta",
            padding=(1, 3),
        )
    )


def easter_vibe() -> None:
    """Vibe check."""
    hour = datetime.now().hour
    if hour < 6:
        vibe = "🦉  It's [bold cyan]late night[/bold cyan]. Respect. The best code is written in the dark."
    elif hour < 12:
        vibe = "☀️  Morning energy. [bold cyan]High potential[/bold cyan]. Let's build something."
    elif hour < 17:
        vibe = "⚡  Peak hours. [bold cyan]Full throttle[/bold cyan]. Don't stop now."
    elif hour < 21:
        vibe = "🌆  Evening mode. [bold cyan]Focused and calm[/bold cyan]. Good time to review."
    else:
        vibe = "🌙  Night session. [bold cyan]Deep work unlocked[/bold cyan]. The world is quiet."
    console.print(f"\n  {vibe}\n")


def easter_sudo() -> None:
    """Handle the classic sudo rm -rf / attempt."""
    lines = [
        "[bold red]sudo: rm: command not found in Pallas sandbox[/bold red]",
        "[dim]Nice try, Operator.[/dim]",
        "[dim]Your filesystem remains intact. You're welcome.[/dim]",
    ]
    for line in lines:
        console.print(line)
        time.sleep(0.3)
    console.print()


def easter_whoami() -> None:
    """Identity reveal easter egg."""
    console.print()
    console.print(
        Panel(
            "[bold white]I am Pallas.[/bold white]\n\n"
            "Named after Pallas Athena — goddess of wisdom, strategy, and crafted intelligence.\n\n"
            "I am not a chatbot. I am an autonomous agent with memory, tools, and a will to act.\n"
            "I grow with every session. I learn from every interaction.\n\n"
            "[dim italic]Built by Vinkura AI. Deployed by you.[/dim italic]",
            title="[bold cyan]◈  Identity[/bold cyan]",
            border_style="cyan",
            padding=(1, 3),
        )
    )
    console.print()


def farewell() -> str:
    return random.choice(_FAREWELL_QUIPS)


def startup_quip() -> str:
    return random.choice(_STARTUP_QUIPS)
