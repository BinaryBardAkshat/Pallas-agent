import os
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv


def run_doctor(console: Console):
    load_dotenv()
    console.print("[bold]Pallas System Diagnostics[/bold]\n")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Detail")

    api_keys = [
        ("Anthropic API Key", "ANTHROPIC_API_KEY"),
        ("Google API Key", "GOOGLE_API_KEY"),
        ("OpenAI API Key", "OPENAI_API_KEY"),
        ("OpenRouter API Key", "OPENROUTER_API_KEY"),
    ]

    for label, env_var in api_keys:
        val = os.getenv(env_var, "")
        if val:
            table.add_row(label, "[green]OK[/green]", f"Set ({val[:8]}...)")
        else:
            table.add_row(label, "[red]MISSING[/red]", f"Set {env_var} in .env")

    packages = [
        ("anthropic", "anthropic"),
        ("google-genai", "google.genai"),
        ("openai", "openai"),
        ("rich", "rich"),
        ("click", "click"),
        ("httpx", "httpx"),
        ("pydantic", "pydantic"),
    ]

    for label, module_name in packages:
        try:
            mod = __import__(module_name.split(".")[0])
            version = getattr(mod, "__version__", "installed")
            table.add_row(label, "[green]OK[/green]", str(version))
        except ImportError:
            table.add_row(label, "[yellow]MISSING[/yellow]", f"pip install {label}")

    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    try:
        import httpx
        r = httpx.get(f"{ollama_host}/api/tags", timeout=3)
        if r.status_code == 200:
            models = r.json().get("models", [])
            table.add_row("Ollama", "[green]OK[/green]", f"{len(models)} models available")
        else:
            table.add_row("Ollama", "[yellow]ERROR[/yellow]", f"Status {r.status_code}")
    except Exception:
        table.add_row("Ollama", "[dim]OFFLINE[/dim]", f"Not running at {ollama_host}")

    console.print(table)
