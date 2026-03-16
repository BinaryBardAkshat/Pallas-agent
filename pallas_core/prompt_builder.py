from typing import List, Dict, Any

class PromptBuilder:
    def __init__(self, soul: str = "Default", memory: Any = None):
        self.soul = soul
        self.memory = memory

    def build_system_prompt(self, context: str = "") -> str:
        base_prompt = (
            "You are Pallas, a self-evolving autonomous AI agent. "
            "Your goal is to execute tasks with precision, safety, and strategic wisdom. "
            "You operate in a Perception-Action-Reflection cycle."
        )
        if context:
            base_prompt += f"\n\nCurrent Context: {context}"
        return base_prompt

    def format_messages(self, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        # Logic to format history for specific providers
        return history
