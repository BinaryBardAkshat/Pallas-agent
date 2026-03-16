# 📖 Pallas Operations & Future Intelligence Guide

This document serves as the primary manual for interacting with Pallas and outlines the advanced features currently in development.

---

## FILE STRUTRE MUST BE THIS

1pallas-agent/
├── pallas_adapter/
│   ├── auth.py
│   ├── entry.py
│   ├── events.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── permissions.py
│   ├── server.py
│   ├── session.py
│   └── tools.py
│
├── pallas_registry/
│   ├── agent.json
│   └── icon.svg
│
├── pallas_core/
│   ├── provider_adapter.py
│   ├── auxiliary_client.py
│   ├── context_compressor.py
│   ├── display.py
│   ├── __init__.py
│   ├── insights.py
│   ├── model_metadata.py
│   ├── prompt_builder.py
│   ├── prompt_caching.py
│   ├── redact.py
│   ├── skill_commands.py
│   ├── trajectory.py
│   └── usage_pricing.py
│
├── pallas_cli/
│   ├── auth.py
│   ├── banner.py
│   ├── callbacks.py
│   ├── checklist.py
│   ├── workspace.py
│   ├── clipboard.py
│   ├── models.py
│   ├── colors.py
│   ├── commands.py
│   ├── config.py
│   ├── cron.py
│   ├── curses_ui.py
│   ├── default_soul.py
│   ├── doctor.py
│   ├── env_loader.py
│   ├── gateway.py
│   ├── __init__.py
│   ├── main.py
│   ├── pairing.py
│   ├── plugins.py
│   ├── runtime_provider.py
│   ├── setup.py
│   ├── skills_config.py
│   ├── skills_hub.py
│   ├── skin_engine.py
│   ├── status.py
│   ├── tools_config.py
│   └── uninstall.py
│
├── gateway/
│   ├── channel_directory.py
│   ├── config.py
│   ├── delivery.py
│   ├── hooks.py
│   ├── __init__.py
│   ├── mirror.py
│   ├── pairing.py
│   ├── platforms/
│   │   ├── ADDING_A_PLATFORM.md
│   │   ├── base.py
│   │   ├── discord.py
│   │   ├── email.py
│   │   ├── homeassistant.py
│   │   ├── __init__.py
│   │   ├── signal.py
│   │   ├── slack.py
│   │   ├── telegram.py
│   │   └── whatsapp.py
│   ├── run.py
│   ├── session.py
│   ├── status.py
│   └── sticker_cache.py
│
├── cron/
│   ├── __init__.py
│   ├── jobs.py
│   └── scheduler.py
│
├── environments/
│   ├── pallas_base_env.py
│   ├── agent_loop.py
│   ├── patches.py
│   ├── tool_context.py
│   ├── web_research_env.py
│   ├── terminal_test_env/
│   ├── pallas_swe_env/
│   ├── benchmarks/
│   └── tool_call_parsers/
│
├── tools/
│   ├── approval.py
│   ├── browser_tool.py
│   ├── checkpoint_manager.py
│   ├── clarify_tool.py
│   ├── code_execution_tool.py
│   ├── cronjob_tools.py
│   ├── debug_helpers.py
│   ├── delegate_tool.py
│   ├── environments/
│   ├── file_operations.py
│   ├── file_tools.py
│   ├── fuzzy_match.py
│   ├── homeassistant_tool.py
│   ├── integration_tools.py
│   ├── image_generation_tool.py
│   ├── __init__.py
│   ├── interrupt.py
│   ├── mcp_tool.py
│   ├── memory_tool.py
│   ├── mixture_of_agents_tool.py
│   ├── model_router.py
│   ├── patch_parser.py
│   ├── process_registry.py
│   ├── registry.py
│   ├── rl_training_tool.py
│   ├── send_message_tool.py
│   ├── session_search_tool.py
│   ├── skill_manager_tool.py
│   ├── skills_guard.py
│   ├── skills_hub.py
│   ├── skills_sync.py
│   ├── skills_tool.py
│   ├── terminal_tool.py
│   ├── safety.py
│   ├── todo_tool.py
│   ├── transcription_tools.py
│   ├── tts_tool.py
│   ├── vision_tools.py
│   ├── voice_mode.py
│   └── web_tools.py
│
├── skills/
│   ├── autonomous-ai-agents/
│   ├── github/
│   ├── productivity/
│   ├── research/
│   ├── software-development/
│   ├── creative/
│   ├── mlops/
│   ├── note-taking/
│   ├── media/
│   ├── domain/
│   ├── index-cache/
│   └── ...
│
├── optional-skills/
│   ├── autonomous-ai-agents/
│   ├── research/
│   ├── productivity/
│   └── ...
│
├── docs/
│   ├── architecture.md
│   ├── installation.md
│   ├── prompt-assembly.md
│   ├── tools-runtime.md
│   ├── creating-skills.md
│   ├── environments.md
│   ├── gateway-internals.md
│   └── ...
│
├── website/
│   ├── docs/
│   ├── static/
│   ├── src/
│   ├── docusaurus.config.ts
│   └── ...
│
├── assets/
│   └── banner.png
│
├── tests/
│   ├── pallas_adapter/
│   ├── pallas_core/
│   ├── pallas_cli/
│   ├── gateway/
│   ├── cron/
│   ├── tools/
│   ├── integration/
│   └── ...
│
├── scripts/
│   ├── install.sh
│   ├── install.ps1
│   ├── install.cmd
│   ├── release.py
│   ├── pallas-gateway
│   └── ...
│
├── batch_runner.py
├── cli.py
├── run_agent.py
├── model_tools.py
├── toolsets.py
├── toolset_distributions.py
├── trajectory_compressor.py
├── utils.py
├── pallas_constants.py
├── pallas_state.py
├── pallas_time.py
├── AGENTS.md
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── package.json
├── package-lock.json
└── uv.lock
---

## 🔮 Future Features in the Flow

Pallas is evolving rapidly. Here are the core "Flow" features being added:

### 1. Hierarchical Sub-Agents
Pallas will soon be able to parallelize complex tasks by spawning sub-agents. You can say *"Pallas, research these 5 technologies and write a comparison paper"* and it will spawn 5 sub-agents to research concurrently.

### 2. Multi-Model Synthesis
The "Synthesis" flow allows Pallas to query both **Claude** (for logic/coding) and **Gemini** (for long-context retrieval) in a single turn, combining their strengths for a superior final answer.

### 3. Visual Web Navigation
Moving beyond text-only browsing, Pallas will use Vision models to "see" and interact with complex web UIs (e.g., clicking buttons on dynamic SPAs that text-browsers miss).

---

## 🔌 Offline Capabilities

Pallas is designed to be resilient. Our offline strategy focuses on **Local Intelligence**:

### Local Execution (Llama.cpp / Ollama)
You can configure Pallas to use a local LLM back-end. This is ideal for:
- Sensitive data processing that must not leave the server.
- Basic automation tasks when internet connectivity is intermittent.
- Cost-saving for simple classification or extraction tasks.

### Local Knowledge Persistence
- **Offline Vector Store:** Your entire conversation history is indexed locally. Even without an LLM, Pallas can search and retrieve past facts using local embeddings.
- **Air-Gapped Toolsets:** A specialized toolset containing only local scripts (file management, system monitoring, data processing) that functions without external API calls.

---

## 🛠️ Developer Instructions

### Adding New Skills
To add a skill to Pallas, create a Python file in `~/.pallas/skills/`:
```python
# example_skill.py
def run(agent, query):
    # Your logic here
    result = agent.execute_tool("terminal", {"command": "ls -la"})
    return f"I found these files: {result}"
```

### Customizing the Flow
You can modify the core agent loop by editing `agent/prompt_builder.py` to change how Pallas reasons about its objectives.

---

## 🏹 Pallas Principles
- **Clarity over Complexity:** Use the most direct path to the goal.
- **Continuous Learning:** Every mistake is a future skill.
- **Privacy First:** The user's data is their own; local processing is the default for sensitive work.
What is Pallas Agent?

Pallas Agent is a persistent personal / team AI operating system.

It is not just a chatbot.

It is an agent runtime that can:

talk through CLI or messaging platforms

use tools (files, terminal, browser, code execution, MCP, web, voice, etc.)

maintain persistent memory across sessions

create and reuse skills (procedural memory in markdown)

spawn sub-agents for parallel work

run scheduled jobs

work in different execution environments (local shell, Docker, SSH, Modal, etc.)

act like a long-lived AI operator, not a single conversation bot

Core mental model
It has 5 brains:

Conversation layer

CLI / Telegram / Slack / WhatsApp / Discord / Email

Agent loop

prompt assembly

tool calling

memory retrieval

sub-agent delegation

response synthesis

Tool runtime

files

terminal

browser

code execution

search

integrations

Learning system

memories

skills

session search

usage insights

self-improving procedural docs

Infrastructure layer

local / docker / ssh / modal / daytona / cloud execution

cron jobs

session persistence

tests / docs / deployment

PART 3 — WHAT EACH TOP-LEVEL FOLDER DOES

This is the part you asked for directly.

1) pallas_adapter/
What it is:

A protocol adapter / runtime bridge for external agent-control protocols (like ACP-style systems).

What it does:

authentication

session handling

permission mediation

event streaming

tool exposure to external clients

Keep if:

you want external orchestration / inter-agent protocol support

Can skip in MVP:

yes

2) pallas_registry/
What it is:

Metadata for discovery / registration.

Contains:

agent.json → machine-readable metadata about the agent

icon.svg → branding icon

Use for:

platform registration

integrations

future marketplace / registry support

3) pallas_core/
This is the actual agent brain.

This is the most important folder.

Main files:

provider_adapter.py → unified wrapper around LLM providers

auxiliary_client.py → helper clients / side-models / secondary calls

context_compressor.py → compresses long context

display.py → formatting / rendering for outputs

insights.py → usage summaries / session insights

model_metadata.py → provider/model capabilities

prompt_builder.py → constructs final prompt from memory, skills, tool schemas, system prompt

prompt_caching.py → caches repeated prompt fragments

redact.py → secret / PII redaction

skill_commands.py → special logic for skill invocation

trajectory.py → captures structured interaction traces

usage_pricing.py → token usage / pricing estimates

This is where:

the model is selected

the prompt is assembled

tool calls are parsed

the final response is generated

4) pallas_cli/
What it is:

The terminal interface / TUI / CLI app.

It provides:

interactive chat

setup flow

config management

model selection

tools configuration

skill browsing

TUI display

diagnostics

update commands

Important files:

main.py → CLI entrypoint

commands.py → slash commands / CLI commands

curses_ui.py → terminal UI

setup.py → onboarding wizard

doctor.py → environment diagnostics

runtime_provider.py → chooses provider runtime

skills_hub.py → skill browsing/install logic

tools_config.py → tool enable/disable config

default_soul.py → default personality / system identity

5) gateway/
What it is:

The multi-platform messaging layer.

What it does:

Allows the same agent to be reachable via:

Telegram

Discord

Slack

WhatsApp

Signal

Email

Home Assistant

Core responsibilities:

route incoming messages

pair users to sessions

deliver outputs

manage platform-specific behaviors

preserve conversation continuity across channels

Important files:

platforms/*.py → one adapter per platform

delivery.py → sends messages back

pairing.py → maps user/channel → session

session.py → messaging session state

run.py → gateway process entrypoint

6) cron/
What it is:

The scheduled automation engine.

What it does:

natural language scheduling

recurring tasks

reminders

daily/weekly summaries

autonomous jobs

Files:

jobs.py → job definitions / execution

scheduler.py → actual scheduler

7) environments/
What it is:

Execution sandboxes / task environments / evaluation environments

This folder is very important if you want:

reproducible tool execution

benchmarks

safe terminal backends

RL / evaluation

Types:

base environment abstraction

SWE task environment

research environment

test environment

benchmark environments

tool call parsers for different models

Important:

This is where you define:

how shell/code/browser tools actually run

how models format tool calls

how evals are executed

8) tools/
This is the tool runtime. Another critical folder.
What it contains:

All callable capabilities the agent can use.

Examples:

file_tools.py → read/write/list/search files

terminal_tool.py → shell execution

browser_tool.py → web browsing / extraction

code_execution_tool.py → run Python/code

memory_tool.py → store/retrieve memory

skill_manager_tool.py → create/update/search skills

session_search_tool.py → search prior sessions

delegate_tool.py → spawn sub-agents

todo_tool.py → planning/task tracking

approval.py → risky action confirmation

mcp_tool.py → external MCP integrations

vision_tools.py → image/document understanding

voice_mode.py, tts_tool.py, transcription_tools.py

cronjob_tools.py → schedule jobs

web_tools.py → web search / page extraction

This is where you add most new capabilities.
9) skills/
This is the procedural memory system (the real magic).

These are reusable markdown playbooks the agent can invoke.

Examples:

how to review a GitHub PR

how to use Gmail search

how to debug a repo

how to write a research paper

how to do domain intelligence

how to run code review

how to manage worktrees

Why this matters:

This is what makes the agent improve with repeated use.

Each skill typically contains:

purpose

trigger conditions

prerequisites

steps

commands

validation

failure modes

10) optional-skills/
What it is:

Skills not installed/enabled by default.

Use for:

domain-specific packs

heavy integrations

niche workflows

premium/internal packs

For Vinkura, this is where you’d add:

police-tech proposal generation

government tender response pack

SOP drafting

incident workflow pack

public-sector document QA

research submission pack

11) docs/
Internal / developer docs

Use for:

architecture docs

prompt assembly docs

how tools work

how skills work

how to add providers

how environments work

This is for contributors and AI coding agents.

12) website/
Public documentation site

Usually Docusaurus.

Use for:

user docs

API references

tutorials

getting started

CLI docs

messaging docs

13) assets/

Brand assets:

banner

logos

icons

14) tests/
Huge and very important

This repo is big because it tests:

CLI behavior

tool safety

platform adapters

permissions

session handling

cron

skills

model providers

sub-agents

interrupts

security edge cases

This is why the project is serious, not just a demo.

15) scripts/

Installers / release scripts / helper commands.

Examples:

install script

update script

release automation

gateway launchers

platform bridges