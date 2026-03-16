# Pallas: The Self-Evolving AI Agent 🦉

Welcome to **Pallas**, the next generation of autonomous AI assistants. Renamed from Hermes to embody the wisdom and strategic prowess of Pallas Athena, this system represents a fundamental shift in how humans interact with LLMs. Pallas is not just a chatbot; it is a self-improving agentic system designed to live where you do, learn from every interaction, and execute complex workflows with professional-grade precision.

---

## 🏗️ System Design & Architecture

Pallas is built on a modular, event-driven architecture designed for persistence, scalability, and extreme flexibility.

### 1. The Core Agent Loop
The heart of Pallas is the **Reasoning Loop**. Unlike standard RAG or simple chat interfaces, Pallas operates on a continuous Perception-Action-Reflection cycle:
- **Perception:** Ingests context from standard chat, file attachments, system state, and past memories.
- **Decision:** Analyzes the objective and selects the most efficient tool or skill.
- **Action:** Executes the tool (e.g., searching the web, editing code, running shell commands).
- **Reflection:** Observes the result, updates the internal state, and decides whether to continue or deliver the final response.

### 2. Multi-Platform Gateway
Pallas doesn't stay trapped in a browser tab. Its unified gateway allows a single Pallas process to communicate across:
- **Messaging:** Telegram, Discord, Slack, WhatsApp, Signal.
- **Terminal:** A rich, interactive TUI (Terminal User Interface).
- **Automation:** Home Assistant, Email (IMAP/SMTP), and Cron jobs.

### 3. The Skills Ecosystem
Pallas features a unique **closed-loop learning system**. When the agent performs a complex or repetitive task, it can autonomously codify that logic into a "Skill." These skills are:
- **Portable:** Standardized Python scripts that wrap complex tool calls.
- **Self-Improving:** The agent updates its own skills as it finds better ways to accomplish tasks.
- **Searchable:** Cross-session memory using SQLite FTS5 allows Pallas to recall past workflows and apply them to new challenges.

---

## 🛠️ Tech Stack

Pallas leverages a cutting-edge stack to ensure performance and reliability:

- **Logic Layer:** Python 3.11+ with `uv` for lightning-fast dependency management.
- **LLM Adapters:** First-class support for **Claude 3.5 Sonnet** (via Anthropic) and **Gemini 1.5 Pro** (via Google AI Studio/Vertex), alongside OpenRouter, OpenAI, and Nous Portal.
- **Sandboxing:** Isolated tool execution environments using **Docker**, **SSH**, **Daytona**, **Modal**, and **Singularity**.
- **Persistence:** SQLite for conversation history, vector-like search, and state management.
- **Intelligence Modeling:** Integration with **Honcho** for dialectic user modeling—Pallas builds a deepening model of *who you are* over time.

---

## 🛡️ Security & Trust

Pallas is designed with a "Security First" mindset:
- **Human-in-the-Loop:** Optional command approval prompts (bypassable with `--fuck-it-ship-it`).
- **Secret Redaction:** Automatic stripping of API keys and sensitive tokens from logs and agent context.
- **Execution Isolation:** All destructive or complex side effects happen within sandboxed environments, protecting your host system.

---

## 🚀 Use Cases & Flow

### Professional Software Engineering
Pallas integrates with `mini-swe-agent`, allowing it to solve real-world GitHub issues, perform codebase-wide refactors, and run unit tests autonomously.

### Knowledge Management
Pallas acts as a dynamic second brain. It searches your past conversations, builds a "SOUL.md" personality file, and manages your personal wiki of memories and preferences.

### Automated Life Ops
From nightly backups and daily news summaries to managing your smart home via Home Assistant, Pallas handles the "boring stuff" while you focus on high-level strategy.

---

*Pallas is the wisdom of the machine, refined by your experience.*
