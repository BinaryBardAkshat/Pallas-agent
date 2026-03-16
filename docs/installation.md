# 🚀 Installation Guide

Pallas is designed to be up and running in under 60 seconds.

## 1-Click Global Install

The easiest way to install Pallas is via our global bootstrap script. This will set up `uv`, install Pallas as a system-wide tool, and initialize your configuration.

```bash
curl -fsSL https://raw.githubusercontent.com/BinaryBardAkshat/Pallas-agent/main/install.sh | bash
```

## Manual Installation

If you prefer to manage the environment yourself:

### 1. Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (Recommended for dependency management)

### 2. Clone and Setup
```bash
git clone https://github.com/BinaryBardAkshat/Pallas-agent.git
cd Pallas-agent
uv sync --all-extras
```

### 3. Global Linking (Optional)
```bash
uv tool install .
```

## First Run

Start the agent using the `pallas` command:

```bash
pallas start
```

Pallas will guide you through:
1. Selecting your preferred **LLM Provider**.
2. Securely storing your **API Keys** in `~/.pallas/.env`.
3. Running a system check via `pallas doctor`.
