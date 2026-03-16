#!/bin/bash

# ==============================================================================
# Pallas Agent - Global Installer
# ==============================================================================

set -e

echo "Initializing Pallas Setup..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: 'uv' package manager is not installed."
    echo "Please install it by running: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "Installing Pallas Agent globally via uv..."

# Uninstall if exists to ensure clean state
uv tool uninstall pallas 2>/dev/null || true

# Install directly from the GitHub repository for global access
uv tool install git+https://github.com/BinaryBardAkshat/Pallas-agent.git --force

echo ""
echo "=============================================================================="
echo "✔ Pallas Agent has been successfully installed globally!"
echo "You can now run it from anywhere in your terminal by typing:"
echo "  pallas start"
echo "=============================================================================="
