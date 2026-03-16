<div align="center">
  <img src="https://via.placeholder.com/150/000000/FFFFFF/?text=PALLAS" alt="Pallas Logo" width="150" height="150">
  <h1>Pallas Agent System</h1>
  <p><strong>An Elite Autonomous AI Coding & Research Environment</strong></p>
  <p><em>Built to evolve with you. By Vinkura AI.</em></p>
</div>

---

## Why Pallas?

Mainstream chatbots sit behind restrictive firewalls, throttling your engineering potential. You repeatedly paste code, lose context, hit rigid token limits, and start over. 

**Pallas is different.** 
Pallas acts as your highly localized, autonomous co-pilot built entirely on a **Perception-Action-Reflection** loop. It doesn't just answer questions—it drops into a sandbox, spins up a terminal, analyzes your codebase, parses APIs, and executes complex chains of tasks automatically until the job is done. 

It completely persists your identity and project history via a hyper-fast embedded SQL engine with Full-Text Search, recalling design decisions and past architectures across coding sessions. It's your personal Jarvis for elite engineering.

## 1-Click Global Installation

You can install Pallas globally onto your system using our install script. Simply run this command in your terminal from the root of the project:

```bash
bash install.sh
```

Once installed globally, you can initialize the agent from any directory by typing:
```bash
pallas start
```

## The 5-Brain Architecture

Our state-of-the-art multi-agent framework guarantees modular robustness:

1. **Conversation Layer**: The robust interface. Elegant CLI routers and cross-platform message gateways (Telegram, Discord) mapping states together.
2. **Agent Loop**: The actual "Brain". A deeply nested while-loop enforcing step-by-step Reflections, Context Compression, and Trajectory Planning.
3. **Tool Sandbox**: Unfettered local power. Secure execution of bash commands, Python scripts, full modular file manipulation, and dynamic web extraction.
4. **Learning Memory**: `memories_fts`. An SQLite-backed hybrid store archiving every conversational turn to ensure massive context pruning logic.
5. **Execution Scheduler**: Deep background routines allowing self-hosted cron events to trim logs and compress summaries.

## Manual Setup

Pallas incorporates a stunning terminal-based interactive UI to make onboarding beautiful and entirely seamless.

### 1. Install Dependencies
Ensure you are using Python 3.11+ and `uv` to pull all core and optional logic dependencies:
```bash
uv sync --all-extras
```

### 2. Enter the Portal
Execute the main entry point to drop into the interactive environment:
```bash
uv run pallas start
```

### 3. The Interactive Startup Flow
1. **Boot Sequence:** Pallas smoothly initializes internal modules, verified by an elegant terminal spinner.
2. **Matrix Selection:** By utilizing an immersive TUI (text-user-interface), use your **arrow keys** to dynamically select your preferred LLM engine (Anthropic Claude 3.7+, Google Gemini 2.5 Pro, GPT-5.4, OpenRouter, or fully offline via Ollama).
3. **Automated Key Injection:** If it's your absolute first time opening the agent, Pallas detects the missing secrets and securely prompts you for your API key. It quietly auto-generates your `.env` file behind the scenes.
4. **Terminal Interface:** The iconic Vinkura banner drops, system diagnostics go online, and Pallas awaits your directive!

## CLI Usage

Pallas utilizes the massive `click` engine. You can discover its capabilities rapidly:

- `pallas start` - Enter the interactive agent loop.
- `pallas ask "..."` - Push a rapid one-shot task/question to the agent without entering the CLI.
- `pallas doctor` - Run system diagnostics (API checks, dependencies, binary setups).
- `pallas info` - Print the intricate architecture matrix and system design structure.
- `pallas --help` - Explore all granular CLI routing commands.

### Pro-Tip Flag
Power users only: Pass the `--no-approval` flag to run the agent completely autonomously. This bypasses the default `[Y/n]` human-in-the-loop firewalls for bash commands and unspools its true speed:
```bash
pallas start --provider anthropic --no-approval
```
