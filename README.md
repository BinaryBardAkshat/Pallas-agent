<div align="center">
  <img src="https://via.placeholder.com/150/000000/FFFFFF/?text=PALLAS" alt="Pallas Logo" width="150" height="150">
  <h1>Pallas Agent System</h1>
  <p><strong>The Final Autonomous AI Operating System</strong></p>
  <p><em>Wisdom in action. By Vinkura AI.</em></p>
</div>

---

## Why Pallas?

Mainstream chatbots sit behind restrictive firewalls, throttling your engineering potential. You repeatedly paste code, lose context, hit rigid token limits, and start over. 


Pallas acts as your highly localized, autonomous co-pilot built entirely on a **Perception-Action-Reflection (PAR)** loop. It doesn't just answer questions—it drops into a sandbox, spins up a terminal, analyzes your codebase, parses APIs, and executes complex chains of tasks automatically until the job is done. 

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

1. **Conversation Layer**: The immersive interface. Elegant CLI routers and cross-platform message gateways (Telegram, Discord, Slack, WhatsApp, Signal) mapping states together.
2. **Agent Loop**: The actual "Brain". A deeply nested cycle enforcing step-by-step Reflections, Context Compression, and Trajectory Planning.
3. **Tool Sandbox**: Unfettered local power. Secure execution of bash commands, Python scripts, full modular file manipulation, and dynamic web extraction.
4. **Learning Memory**: `memories_fts`. An SQLite-backed hybrid store archiving every conversational turn to ensure massive context pruning logic.
5. **Infrastructure Layer**: Deep background routines allowing self-hosted jobs (Local Shell, Docker, SSH, Modal) to manage state persistence and scheduled tasks.

## The Skills Ecosystem

Pallas features a **closed-loop learning system**. When the agent performs complex tasks, it autonomously codifies that logic into reusable "Skills" stored in `~/.pallas/skills/`. These are portable markdown playbooks the agent uses to execute massive, repeatable workflows without manual oversight.

## Future Vector: Multi-Model Synthesis

Pallas is capable of querying both **Claude** (for high-level logic/coding) and **Gemini** (for massive long-context retrieval) in a single turn, synthesizing their specific strengths into a superior final output.

## CLI Usage

Pallas utilizes a massive `click` engine for professional management:

- `pallas start` - Enter the interactive agent loop.
- `pallas ask "..."` - Push a rapid one-shot task to the agent.
- `pallas doctor` - Run system diagnostics (API checks, binary setups).
- `pallas info` - Print the intricate architecture matrix and system design.
- `pallas help` - Explore all granular CLI routing commands.

### Pro-Tip: Autonomous Mode
Pass the `--no-approval` flag to run the agent completely autonomously. This bypasses the default `[Y/n]` firewalls for bash commands and unspools its true speed:
```bash
pallas start --no-approval
```
