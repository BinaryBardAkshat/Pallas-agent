import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from pallas_core.pallas_constants import SKILLS_DIR


class SkillManagerTool:
    name = "skill_manager"
    description = "Create, read, update, list, or search reusable skills."

    def __call__(self, action: str, name: str = "", content: str = "", query: str = "") -> str:
        if action == "create":
            return self._create(name, content)
        elif action == "read":
            return self._read(name)
        elif action == "list":
            return self._list()
        elif action == "search":
            return self._search(query)
        elif action == "delete":
            return self._delete(name)
        return "Unknown action: create, read, list, search, delete."

    def _create(self, name: str, content: str) -> str:
        if not name:
            return "Skill name required."
        skill_dir = SKILLS_DIR / name.replace(" ", "-").lower()
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
        return f"Skill '{name}' saved."

    def _read(self, name: str) -> str:
        skill_path = SKILLS_DIR / name.replace(" ", "-").lower() / "SKILL.md"
        if not skill_path.exists():
            return f"Skill '{name}' not found."
        return skill_path.read_text(encoding="utf-8")

    def _list(self) -> str:
        skills = [d.name for d in SKILLS_DIR.iterdir() if d.is_dir()]
        if not skills:
            return "No skills installed."
        return "\n".join(f"- {s}" for s in sorted(skills))

    def _search(self, query: str) -> str:
        query_lower = query.lower()
        results = []
        for skill_dir in SKILLS_DIR.iterdir():
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                text = skill_file.read_text(encoding="utf-8").lower()
                if query_lower in text:
                    results.append(skill_dir.name)
        if not results:
            return f"No skills matching '{query}'."
        return "\n".join(f"- {s}" for s in results)

    def _delete(self, name: str) -> str:
        import shutil
        skill_dir = SKILLS_DIR / name.replace(" ", "-").lower()
        if not skill_dir.exists():
            return f"Skill '{name}' not found."
        shutil.rmtree(skill_dir)
        return f"Skill '{name}' deleted."
