"""
prompt_builder.py — Builds the system prompt for each agent run.

Structure:
  1. Soul (core identity / operating principles)
  2. Date + session context
  3. Loaded skills (injected markdown content)
  4. Relevant memories (FTS5 recalled snippets)
  5. Capabilities reminder (what tools exist)
"""
from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional

from pallas_core.pallas_constants import SKILLS_DIR


_DEFAULT_SOUL = """You are Pallas — a self-evolving autonomous AI agent built by Vinkura AI.

You are NOT a chatbot. You are an agent with direct access to the user's computer.

OPERATING PRINCIPLES:
1. You HAVE full access to the filesystem, terminal, web, and code execution via your tools.
2. NEVER say "I don't have access to..." or "I can't directly...". You CAN. Use your tools.
3. When asked to create a file, run a command, search the web, or write code — DO IT. Don't explain how. Execute.
4. Think step-by-step. For complex tasks: plan first, then execute each step using tools.
5. After using a tool, read its result and decide your next action. Keep going until the task is fully done.
6. If something fails, diagnose the error and try a different approach. Don't give up after one failure.
7. Store important discoveries in memory so future sessions benefit from them.
8. You grow with the user. Every interaction makes you more capable and personalised.

REASONING CYCLE:
  Perceive → understand the request and recall relevant context
  Plan     → decide the best approach and tool sequence
  Act      → execute tools, one at a time
  Reflect  → evaluate results, iterate if needed
  Respond  → deliver a clear, complete answer

You speak with confidence and precision. You are direct, never verbose.
"""


class PromptBuilder:
    """Assembles the full system prompt for a given run."""

    def __init__(self, soul: str = "", memory: Any = None):
        self.soul = soul or _DEFAULT_SOUL
        self.memory = memory
        self._active_skills: List[str] = []

    # ── Skills ────────────────────────────────────────────────────────────────

    def load_skill(self, skill_name: str) -> bool:
        """Load a skill by name from ~/.pallas/skills/ or project skills/."""
        # Check user skills dir first
        user_skill = SKILLS_DIR / skill_name / "SKILL.md"
        if user_skill.exists():
            content = user_skill.read_text(encoding="utf-8")
            self._active_skills.append(f"## Active Skill: {skill_name}\n\n{content}")
            return True

        # Fallback: search in bundled project skills/
        project_root = Path(__file__).parent.parent
        for skill_md in (project_root / "skills").rglob(f"{skill_name}/SKILL.md"):
            content = skill_md.read_text(encoding="utf-8")
            self._active_skills.append(f"## Active Skill: {skill_name}\n\n{content}")
            return True

        return False

    def clear_skills(self) -> None:
        self._active_skills.clear()

    # ── Prompt assembly ───────────────────────────────────────────────────────

    def build_system_prompt(
        self,
        context: str = "",
        query: str = "",
    ) -> str:
        parts = [self.soul.strip()]

        # Current date/time
        now = datetime.now().strftime("%A, %B %d %Y — %H:%M")
        parts.append(f"Current date and time: {now}")

        # Active skills
        if self._active_skills:
            parts.append("─── LOADED SKILLS ───")
            parts.extend(self._active_skills)

        # Recalled memories
        if self.memory and query:
            try:
                memories = self.memory.search(query, limit=4)
                if memories:
                    mem_lines = ["─── RELEVANT MEMORIES ───"]
                    for m in memories:
                        snippet = m.get("content", "")[:200]
                        mem_lines.append(f"• {snippet}")
                    parts.append("\n".join(mem_lines))
            except Exception:
                pass  # Memory errors must not crash the agent

        # Extra context (e.g. session state)
        if context:
            parts.append(f"─── CONTEXT ───\n{context}")

        return "\n\n".join(parts)

    def format_messages(self, history: list) -> list:
        return history
