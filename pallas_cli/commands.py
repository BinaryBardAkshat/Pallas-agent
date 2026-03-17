"""
commands.py — Chat session logic and config display for pallas CLI.
"""
import os
from pathlib import Path
from rich.table import Table
from rich.rule import Rule

from environments.agent_loop import AgentLoop
from pallas_core.pallas_constants import PROVIDER_ANTHROPIC, DEFAULT_MODELS
from pallas_core.display import (
    console,
    easter_coffee,
    easter_fortune,
    easter_matrix,
    easter_owl,
    easter_sudo,
    easter_vibe,
    easter_whoami,
    farewell,
    startup_quip,
)


def _register_all_tools(agent: AgentLoop) -> None:
    """Register every available tool on an AgentLoop instance."""
    from tools.file_tools import FileTool, TerminalTool
    from tools.web_tools import WebTool
    from tools.memory_tool import MemoryTool
    from tools.code_execution_tool import CodeExecutionTool
    from tools.skill_manager_tool import SkillManagerTool
    from tools.session_search_tool import SessionSearchTool
    from tools.todo_tool import TodoTool

    agent.register_tool("file",           FileTool())
    agent.register_tool("terminal",       TerminalTool())
    agent.register_tool("web",            WebTool())
    agent.register_tool("memory",         MemoryTool(agent.memory))
    agent.register_tool("code_exec",      CodeExecutionTool())
    agent.register_tool("skill_manager",  SkillManagerTool())
    agent.register_tool("session_search", SessionSearchTool())
    agent.register_tool("todo",           TodoTool())

    # Optional tools — import gracefully
    for tool_name, module_path, class_name in [
        ("delegate", "tools.delegate_tool", "DelegateTool"),
        ("vision",   "tools.vision_tool",   "VisionTool"),
        ("clarify",  "tools.clarify_tool",  "ClarifyTool"),
    ]:
        try:
            import importlib
            mod = importlib.import_module(module_path)
            cls = getattr(mod, class_name)
            agent.register_tool(tool_name, cls())
        except Exception:
            pass


_SLASH_COMMANDS_HELP = """\
[bold cyan]Slash commands:[/bold cyan]
  [dim]/usage[/dim]           Show token usage and cost
  [dim]/memories[/dim]        Show recent memories
  [dim]/session[/dim]         Show session ID and trajectory summary
  [dim]/skills[/dim]          List loaded skills
  [dim]/load <skill>[/dim]    Load a skill into context
  [dim]/provider <name>[/dim] Switch LLM provider (anthropic/google/openai/openrouter/ollama)
  [dim]/model <name>[/dim]    Switch model
  [dim]/doctor[/dim]          Run system diagnostics
  [dim]/fortune[/dim]         Random wisdom
  [dim]/vibe[/dim]            Vibe check
  [dim]/owl[/dim]             ...
  [dim]/coffee[/dim]          Take a break
  [dim]/matrix[/dim]          Wake up, Operator
  [dim]/whoami[/dim]          Who is Pallas?
  [dim]/help[/dim]            Show this help
  [dim]/exit[/dim]            End session\
"""

# ── Easter egg trigger words in normal chat ───────────────────────────────────

_SUDO_TRIGGERS = {"sudo rm -rf /", "sudo rm -rf /*", "rm -rf /", "rm -rf /*"}


def _check_easter_egg(text: str) -> bool:
    """
    Check if raw user input is an easter egg trigger.
    Returns True if consumed (skip agent.run).
    """
    low = text.lower().strip()

    if low in _SUDO_TRIGGERS:
        easter_sudo()
        return True

    if low in ("who are you", "who are you?", "what are you", "what are you?"):
        easter_whoami()
        return True

    if low in ("hello pallas", "hey pallas", "hi pallas"):
        console.print(f"\n  [bold cyan]Hello, Operator.[/bold cyan] {startup_quip()}\n")
        return True

    return False


def chat_session(
    provider: str = PROVIDER_ANTHROPIC,
    model: str = None,
    human_in_loop: bool = True,
    session_id: str = None,
) -> None:
    agent = AgentLoop(
        provider=provider,
        model=model,
        human_in_loop=human_in_loop,
        session_id=session_id,
    )

    _register_all_tools(agent)

    resolved_model = model or DEFAULT_MODELS.get(provider, "default")
    console.print(
        f"[dim]Session: [bold]{agent.session_id[:12]}…[/bold] | "
        f"Provider: [bold]{provider}[/bold] | "
        f"Model: [bold]{resolved_model}[/bold][/dim]"
    )
    console.print("[dim]Type /help for commands. Ctrl+C or /exit to quit.[/dim]\n")

    while True:
        try:
            user_input = console.input("[bold cyan]› [/bold cyan]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print(f"\n[dim]{farewell()}[/dim]")
            break

        if not user_input:
            continue

        low = user_input.lower().strip()

        # ── Hard exits ────────────────────────────────────────────────────────
        if low in ("/exit", "/quit", "exit", "quit"):
            console.print(f"[dim]{farewell()}[/dim]")
            break

        # ── Slash commands ────────────────────────────────────────────────────
        elif low == "/help":
            console.print(_SLASH_COMMANDS_HELP)

        elif low == "/usage":
            from pallas_core.display import print_usage
            print_usage(agent.pricing.summary())

        elif low == "/memories":
            from pallas_core.display import print_memories
            mems = agent.memory.get_recent(10)
            if mems:
                print_memories(mems)
            else:
                console.print("[dim]No memories stored yet.[/dim]")

        elif low == "/session":
            console.print(f"[dim]Session ID: {agent.session_id}[/dim]")
            try:
                console.print(f"[dim]{agent.trajectory.summary()}[/dim]")
            except Exception:
                pass

        elif low == "/skills":
            from pallas_core.skill_commands import SkillCommands
            sc = SkillCommands()
            skills = sc.list_skills()
            if skills:
                console.print("[dim]Installed skills:[/dim]")
                for s in skills:
                    console.print(f"  [dim cyan]· {s}[/dim cyan]")
            else:
                console.print("[dim]No skills installed in ~/.pallas/skills/[/dim]")
                project_root = Path(__file__).parent.parent / "skills"
                if project_root.exists():
                    bundled = [
                        d.name for cat in project_root.iterdir() if cat.is_dir()
                        for d in cat.iterdir() if d.is_dir() and (d / "SKILL.md").exists()
                    ]
                    if bundled:
                        console.print(f"[dim]Bundled skills: {', '.join(bundled[:12])}[/dim]")

        elif low.startswith("/load "):
            skill_name = user_input.split(" ", 1)[1].strip()
            if agent.prompt_builder.load_skill(skill_name):
                console.print(f"[green]✓ Loaded skill: {skill_name}[/green]")
            else:
                console.print(f"[red]Skill '{skill_name}' not found.[/red]")

        elif low == "/doctor":
            from pallas_cli.doctor import run_doctor
            run_doctor(console)

        elif low.startswith("/provider "):
            new_provider = user_input.split(" ", 1)[1].strip()
            agent.adapter.switch_provider(new_provider)
            agent.provider = new_provider
            agent.model = DEFAULT_MODELS.get(new_provider, agent.model)
            console.print(f"[green]✓ Switched to provider: {new_provider} (model: {agent.model})[/green]")

        elif low.startswith("/model "):
            new_model = user_input.split(" ", 1)[1].strip()
            agent.model = new_model
            console.print(f"[green]✓ Switched to model: {new_model}[/green]")

        # ── Easter egg slash commands ─────────────────────────────────────────
        elif low == "/owl":
            easter_owl()

        elif low == "/coffee":
            easter_coffee()

        elif low == "/matrix":
            easter_matrix()

        elif low == "/fortune":
            easter_fortune()

        elif low == "/vibe":
            easter_vibe()

        elif low in ("/whoami", "/whoareyou"):
            easter_whoami()

        # ── Easter egg natural language triggers ──────────────────────────────
        elif _check_easter_egg(user_input):
            pass  # already handled

        # ── Normal agent run ──────────────────────────────────────────────────
        else:
            agent.run(user_input)


def show_config(console) -> None:
    from pallas_core.pallas_state import PallasState
    state = PallasState()

    table = Table(title="Pallas Configuration", show_header=True, header_style="bold cyan")
    table.add_column("Key",   style="cyan")
    table.add_column("Value", style="white")
    for k, v in (state.config or {}).items():
        table.add_row(str(k), str(v))
    console.print(table)
