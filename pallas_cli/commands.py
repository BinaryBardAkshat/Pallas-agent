import os
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv

from environments.agent_loop import AgentLoop
from tools import FileTool, TerminalTool, WebTool, MemoryTool, CodeExecutionTool, SkillManagerTool
from pallas_constants import PROVIDER_ANTHROPIC, DEFAULT_MODELS


def chat_session(
    provider: str = PROVIDER_ANTHROPIC,
    model: str = None,
    human_in_loop: bool = True,
    session_id: str = None,
):
    console = Console()
    agent = AgentLoop(
        provider=provider,
        model=model,
        human_in_loop=human_in_loop,
        session_id=session_id,
    )

    agent.register_tool("file", FileTool())
    agent.register_tool("terminal", TerminalTool())
    agent.register_tool("web", WebTool())
    agent.register_tool("memory", MemoryTool(agent.memory))
    agent.register_tool("code_exec", CodeExecutionTool())
    agent.register_tool("skill_manager", SkillManagerTool())

    resolved_model = model or DEFAULT_MODELS.get(provider, "default")
    console.print(
        f"[dim]Session: {agent.session_id} | Provider: {provider} | Model: {resolved_model}[/dim]\n"
    )

    while True:
        try:
            user_input = console.input("[bold cyan]> [/bold cyan]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Session ended.[/dim]")
            break

        if not user_input:
            continue

        if user_input.lower() in ("/exit", "/quit", "exit", "quit"):
            console.print("[dim]Goodbye, Operator.[/dim]")
            break

        if user_input.lower() == "/usage":
            from pallas_core.display import print_usage
            print_usage(agent.pricing.summary())
            continue

        if user_input.lower() == "/memories":
            from pallas_core.display import print_memories
            memories = agent.memory.get_recent(10)
            print_memories(memories)
            continue

        if user_input.lower() == "/session":
            console.print(f"[dim]Session ID: {agent.session_id}[/dim]")
            console.print(f"[dim]{agent.trajectory.summary()}[/dim]")
            continue

        if user_input.lower() == "/skills":
            from pallas_core.skill_commands import SkillCommands
            sc = SkillCommands()
            skills = sc.list_skills()
            if skills:
                for s in skills:
                    console.print(f"  [dim]- {s}[/dim]")
            else:
                console.print("[dim]No skills installed.[/dim]")
            continue

        if user_input.lower() == "/doctor":
            from pallas_cli.doctor import run_doctor
            run_doctor(console)
            continue

        if user_input.lower().startswith("/provider "):
            new_provider = user_input.split(" ", 1)[1].strip()
            agent.adapter.switch_provider(new_provider)
            agent.provider = new_provider
            console.print(f"[dim]Switched to provider: {new_provider}[/dim]")
            continue

        agent.run(user_input)


def show_config(console: Console):
    from pallas_state import PallasState
    state = PallasState()

    table = Table(title="Pallas Configuration", show_header=True)
    table.add_column("Key")
    table.add_column("Value")
    for k, v in state.config.items():
        table.add_row(str(k), str(v))

    console.print(table)
