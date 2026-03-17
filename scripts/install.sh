#!/usr/bin/env bash
set -euo pipefail

# Pallas Agent — Linux/Mac Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/vinkura-ai/pallas/main/scripts/install.sh | bash

PALLAS_VERSION="0.1.4"
MIN_PYTHON="3.11"
MIN_PYTHON_MAJOR=3
MIN_PYTHON_MINOR=11

# ─── ANSI Colors ──────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
RESET='\033[0m'

ok()   { echo -e "${GREEN}  ✔${RESET}  $*"; }
info() { echo -e "${CYAN}  →${RESET}  $*"; }
warn() { echo -e "${YELLOW}  ⚠${RESET}  $*"; }
fail() { echo -e "${RED}  ✖${RESET}  $*" >&2; exit 1; }
step() { echo -e "\n${BOLD}${CYAN}$*${RESET}"; }

# ─── Banner ───────────────────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}╔══════════════════════════════════╗${RESET}"
echo -e "${CYAN}║      Pallas Agent Installer      ║${RESET}"
echo -e "${CYAN}║         v${PALLAS_VERSION}              ║${RESET}"
echo -e "${CYAN}╚══════════════════════════════════╝${RESET}"
echo ""

# ─── Detect if running from curl pipe (no local repo) ─────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-/dev/null}")" 2>/dev/null && pwd || echo "")"
IN_REPO=false
if [[ -n "$SCRIPT_DIR" && -f "$SCRIPT_DIR/../pyproject.toml" ]]; then
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
    IN_REPO=true
fi

# ─── Step 1: Check Python ≥ 3.11 ──────────────────────────────────────────────
step "Checking Python version..."

PYTHON_BIN=""
for candidate in python3 python python3.13 python3.12 python3.11; do
    if command -v "$candidate" &>/dev/null; then
        ver=$("$candidate" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
        major="${ver%%.*}"
        minor="${ver##*.}"
        if [[ "$major" -gt "$MIN_PYTHON_MAJOR" ]] || \
           [[ "$major" -eq "$MIN_PYTHON_MAJOR" && "$minor" -ge "$MIN_PYTHON_MINOR" ]]; then
            PYTHON_BIN="$candidate"
            ok "Found $PYTHON_BIN ($ver)"
            break
        fi
    fi
done

if [[ -z "$PYTHON_BIN" ]]; then
    fail "Python >= ${MIN_PYTHON} is required but was not found.

  Please install Python ${MIN_PYTHON}+:
    • macOS:   brew install python@3.13
    • Ubuntu:  sudo apt install python3.13
    • Fedora:  sudo dnf install python3.13
    • Other:   https://www.python.org/downloads/

  Then re-run this installer."
fi

# ─── Step 2: Check / Install uv ───────────────────────────────────────────────
step "Checking for uv package manager..."

if command -v uv &>/dev/null; then
    UV_VERSION=$(uv --version 2>&1 | awk '{print $2}')
    ok "uv ${UV_VERSION} already installed"
else
    warn "uv not found — installing via curl..."
    if ! command -v curl &>/dev/null; then
        fail "curl is required to install uv. Please install curl and try again."
    fi
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Reload PATH so the freshly installed uv is found
    export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"

    if command -v uv &>/dev/null; then
        ok "uv installed successfully"
    else
        warn "uv binary not on PATH after install. Falling back to pip install."
        UV_UNAVAILABLE=true
    fi
fi

# ─── Step 3: Install Pallas ───────────────────────────────────────────────────
step "Installing Pallas Agent v${PALLAS_VERSION}..."

UV_UNAVAILABLE="${UV_UNAVAILABLE:-false}"

if [[ "$UV_UNAVAILABLE" == "true" ]]; then
    # Fallback: plain pip global install
    info "Installing via pip (pallas-agent)..."
    "$PYTHON_BIN" -m pip install --upgrade pallas-agent
    ok "Installed pallas-agent via pip"
elif [[ "$IN_REPO" == "true" ]]; then
    # Running from a local checkout — use uv tool install .
    info "Installing from local source: $PROJECT_ROOT"
    # Idempotent: uninstall first if already present, ignore errors
    uv tool uninstall pallas-agent 2>/dev/null || true
    (cd "$PROJECT_ROOT" && uv tool install . --force)
    ok "Installed from local source"
else
    # Running from curl pipe — install from PyPI
    info "Installing pallas-agent from PyPI..."
    # Idempotent: uninstall first if already present, ignore errors
    uv tool uninstall pallas-agent 2>/dev/null || true
    uv tool install pallas-agent --force
    ok "Installed pallas-agent from PyPI"
fi

# Ensure uv tool bin directory is on PATH for the rest of this script
UV_TOOL_BIN="$(uv tool dir 2>/dev/null)/bin" || true
if [[ -d "$UV_TOOL_BIN" ]]; then
    export PATH="$UV_TOOL_BIN:$PATH"
fi
# Also add common local bin locations
export PATH="$HOME/.local/bin:$PATH"

# ─── Step 4: pallas doctor ────────────────────────────────────────────────────
step "Running pallas doctor..."

if command -v pallas &>/dev/null; then
    pallas doctor || warn "pallas doctor reported issues (see above). You may need to set API keys."
else
    warn "'pallas' command not found on PATH after install."
    warn "You may need to add the following to your shell profile:"
    warn "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    warn "Then open a new terminal and run: pallas doctor"
fi

# ─── Done ─────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════╗${RESET}"
echo -e "${GREEN}${BOLD}║  ✅ Pallas installed! Run: pallas start      ║${RESET}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════╝${RESET}"
echo ""
echo -e "${DIM}  Docs:    https://github.com/vinkura-ai/pallas${RESET}"
echo -e "${DIM}  Config:  ~/.pallas/config.json${RESET}"
echo ""
