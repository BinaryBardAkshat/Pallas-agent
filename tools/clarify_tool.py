import threading
from rich.console import Console
from rich.panel import Panel

console = Console()


class ClarifyTool:
    """Ask user a clarifying question when genuinely needed. Pauses agent loop."""

    schema = {
        "name": "clarify",
        "description": (
            "Ask the user a clarifying question when you genuinely cannot proceed without more info. "
            "Do NOT use for minor uncertainties."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "The specific question to ask"},
                "context": {
                    "type": "string",
                    "description": "Brief explanation of why you need this info",
                },
            },
            "required": ["question"],
        },
    }

    def __call__(self, question: str, context: str = "") -> str:
        header = "[bold yellow]Clarification Needed[/bold yellow]"
        body = question
        if context:
            body = f"[dim]{context}[/dim]\n\n{question}"

        console.print(Panel(body, title=header, border_style="yellow", padding=(1, 2)))

        answer_container: dict = {}

        def _prompt():
            try:
                answer_container["answer"] = console.input("[bold yellow]Your answer:[/bold yellow] ")
            except (EOFError, KeyboardInterrupt):
                answer_container["answer"] = ""

        thread = threading.Thread(target=_prompt, daemon=True)
        thread.start()
        thread.join(timeout=600)  # 10-minute timeout

        if thread.is_alive():
            return "TIMEOUT: No response after 10 minutes"

        return answer_container.get("answer") or ""
