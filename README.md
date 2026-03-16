# Pallas Agent

Pallas is a self-evolving autonomous AI agent designed for persistence, scalability, and advanced workflow execution.

## Core Features
- **Reasoning Loop**: Perception-Action-Reflection cycle.
- **Multi-Platform**: Unified gateway for Telegram, Discord, Terminal, and more.
- **Skills Ecosystem**: Autonomous codification of tasks into reusable skills.
- **Dual-Head Intelligence**: Optimized for Claude 3.5 Sonnet and Gemini 1.5 Pro.

## Setup
1. Install dependencies:
   ```bash
   uv sync
   ```
2. Set up environment variables in `.env`:
   ```env
   ANTHROPIC_API_KEY=your_key
   GOOGLE_API_KEY=your_key
   ```
3. Run the CLI:
   ```bash
   pallas start
   ```

## Architecture
See `docs/architecture.md` for a detailed breakdown of the 5-brain system.
