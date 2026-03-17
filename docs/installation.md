# Installation Guide

Pallas is designed to be running in under 60 seconds. This guide covers three paths: the one-command bootstrap, manual `uv` install, and `pip` install.

---

## Prerequisites

- **Python 3.11 or later** — Check with `python3 --version`
- **uv** (recommended) — Fast Python package manager

Install `uv` if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or via pip:

```bash
pip install uv
```

---

## Method 1: One-Command Bootstrap (Recommended)

The `install.sh` script installs `uv` if missing, then installs Pallas as a global tool and runs the first-time setup.

```bash
curl -fsSL https://raw.githubusercontent.com/BinaryBardAkshat/Pallas-agent/main/install.sh | bash
```

After this completes, `pallas` is available system-wide.

---

## Method 2: uv tool install (From Source)

This method gives you the latest development version and makes `pallas` available globally via `uv tool`.

```bash
# Clone the repository
git clone https://github.com/BinaryBardAkshat/Pallas-agent.git
cd Pallas-agent

# Install all dependencies
uv sync --all-extras

# Install as a global CLI tool
uv tool install .
```

Verify the install:

```bash
pallas --version
# Pallas, version 0.1.4
```

To update later:

```bash
git pull
uv tool install . --force
```

---

## Method 3: pip install

For environments where `uv` is not available:

```bash
pip install pallas-agent
```

Or from source:

```bash
git clone https://github.com/BinaryBardAkshat/Pallas-agent.git
cd Pallas-agent
pip install -e ".[all]"
```

---

## First Run

```bash
pallas start
```

On first launch, Pallas will:

1. Ask you to select an LLM provider (Anthropic, Google, OpenAI, OpenRouter, or Ollama)
2. Prompt for the corresponding API key, which is saved to `~/.pallas/.env`
3. Initialize the local SQLite databases in `~/.pallas/data/`
4. Drop you into an interactive session

---

## Setting API Keys

### During first run

The `start` command handles key collection interactively. You can also use the `keys` subcommand at any time:

```bash
pallas keys anthropic sk-ant-...
pallas keys google AIza...
pallas keys openai sk-...
pallas keys openrouter sk-or-...
```

Keys are stored in `~/.pallas/.env` and never logged.

### Via environment variables

You can also set keys in your shell profile or a local `.env` file. Pallas loads `.env` from the current working directory first, then falls back to `~/.pallas/.env`:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="AIza..."
export OPENAI_API_KEY="sk-..."
export OPENROUTER_API_KEY="sk-or-..."
```

### For Ollama (local models)

No API key needed. Just ensure Ollama is running:

```bash
ollama serve
ollama pull qwen3.5:27b
pallas start --provider ollama
```

---

## File Locations

After installation, Pallas creates these paths:

| Path | Contents |
|---|---|
| `~/.pallas/.env` | API keys |
| `~/.pallas/data/pallas.db` | Session and state storage |
| `~/.pallas/data/memory.db` | FTS5 memory index |
| `~/.pallas/data/sessions.db` | Session history |
| `~/.pallas/skills/` | Installed skills (SKILL.md files) |
| `~/.pallas/logs/` | Agent logs |

---

## Health Check

Run the doctor command after install to verify all dependencies are present and keys are configured:

```bash
pallas doctor
```

This checks:
- Python version
- Required packages
- API key presence
- Database integrity
- Sandbox backend availability

---

## Uninstalling

```bash
pallas uninstall
```

This removes `~/.pallas/` and unregisters the CLI tool. Or manually:

```bash
rm -rf ~/.pallas/
uv tool uninstall pallas-agent
# or: pip uninstall pallas-agent
```
