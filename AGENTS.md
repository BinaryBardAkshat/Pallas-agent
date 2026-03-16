# AGENTS.md

This file is for AI coding agents (Codex, Claude, Gemini, etc.) working on this repo.

## Project Overview

Pallas Agent is a persistent autonomous AI operating system. It is not a chatbot wrapper.

## Key Architecture Rules

- `pallas_core/` is the brain. Do not add side effects or I/O imports here.
- `environments/agent_loop.py` is the main reasoning loop. Modify with care.
- `tools/` is where new capabilities live. Each tool is a callable class with `name` and `description`.
- `gateway/` is for message platform adapters. Never put business logic here.
- `skills/` contains markdown playbooks. These are data, not code.
- `pallas_state.py` manages config and session persistence via SQLite.
- `pallas_constants.py` is the single source of truth for paths and model names.

## Adding a New Tool

1. Create `tools/your_tool.py` with a class that has `name`, `description`, and `__call__`.
2. Export it from `tools/__init__.py`.
3. Register it in `pallas_cli/commands.py` chat_session and `toolsets.py`.

## Adding a New Gateway Platform

1. Create `gateway/platforms/your_platform.py` extending `BasePlatform`.
2. Implement `start()` and `send()`.
3. Export from `gateway/platforms/__init__.py`.

## Code Style

- No emojis in code or docstrings.
- No excessive comments. Code should be self-explanatory.
- Python 3.11+, type hints everywhere.
- Ruff for linting, mypy for type checking.
- Never commit `.env`, `*.db`, or `__pycache__/`.

## Testing

```bash
pytest tests/
```

## Running Locally

```bash
pallas start
# or
python run_agent.py
```
