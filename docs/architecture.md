# 🏗️ Architecture

Pallas is built on a modular, event-driven framework designed for persistence and extreme local flexibility.

## The 5-Brain Framework

### 1. Conversation Layer
Unified entry points for user communication.
- **Terminal UI (TUI)**: Rich, interactive CLI experiences using `rich` and `click`.
- **Multi-Platform Gateway**: Platform-specific adapters (Telegram, Slack, Discord) that map user identities into unique session pools.

### 2. Agent Loop
The core reasoning engine based on the **Perception-Action-Reflection (PAR)** loop.
- **Perception**: Scans the environment, reads file attachments, and retrieves prior memories using Full-Text Search.
- **Action**: Uses a deterministic model selector to decide which LLM is best suited for the current tool call (e.g., Claude for Coding, Gemini for Research).
- **Reflection**: Compares the tool output against the original objective. If the goal isn't met, Pallas adjusts its strategy and loops back.

### 3. Tool Sandbox
The execution layer for real-world side effects.
- **Files**: Native I/O with permission guarding.
- **Terminal**: Real bash execution (sanitized via approval gates).
- **Code Execution**: Python REPL for mathematical or algorithmic tasks.
- **Web Research**: Headless extraction and search synthesis.

### 4. Memory Store
Persistence beyond the active context.
- **SQLite FTS5**: Conversation logs are indexed for instant semantic-like retrieval.
- **Trajectory Logs**: Structured JSON traces of every decision tree Pallas followed.

### 5. Infrastructure Layer
The deployment and maintenance substrate.
- **Cron**: Automated task scheduling.
- **Sandboxing**: Support for Docker, SSH, and Modal execution environments to keep the host system secure.
