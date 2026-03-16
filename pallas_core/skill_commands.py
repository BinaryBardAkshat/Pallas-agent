from pathlib import Path
from typing import List, Optional
from .pallas_constants import SKILLS_DIR


class SkillCommands:
    def __init__(self, skills_dir: Path = SKILLS_DIR):
        self.skills_dir = skills_dir

    def list_skills(self) -> List[str]:
        if not self.skills_dir.exists():
            return []
        return sorted(d.name for d in self.skills_dir.iterdir() if d.is_dir())

    def get_skill(self, name: str) -> Optional[str]:
        skill_file = self.skills_dir / name / "SKILL.md"
        if skill_file.exists():
            return skill_file.read_text(encoding="utf-8")
        return None

    def skill_exists(self, name: str) -> bool:
        return (self.skills_dir / name / "SKILL.md").exists()

    def invoke_skill_prompt(self, name: str, user_query: str) -> Optional[str]:
        content = self.get_skill(name)
        if not content:
            return None
        return (
            f"You have a skill called '{name}'. Follow these instructions precisely:\n\n"
            f"{content}\n\n"
            f"User request: {user_query}"
        )
