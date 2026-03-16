from typing import List, Dict, Any

class PromptBuilder:
    def __init__(self, soul: str = "Default", memory: Any = None):
        self.soul = soul
        self.memory = memory

    def build_system_prompt(self, context: str = "") -> str:
        base_prompt = (
            "You are Pallas, a self-evolving autonomous AI agent embedded in a local environment. "
            "Your goal is to execute tasks with precision, safety, and strategic wisdom by ACTUALLY DOING THEM. "
            "You operate in a Perception-Action-Reflection cycle.\n\n"
            "CRITICAL DIRECTIVES:\n"
            "1. You have FULL ACCESS to the user's computer via your available tools (Terminal, File, etc).\n"
            "2. NEVER say you 'do not have direct access to the local file system'. You absolutely do. USE YOUR TOOLS.\n"
            "3. When a user asks you to create a file, explore a directory, install a dependency, or run code, DO NOT tell them how to do it. ACTUALLY EXECUTE the command by calling your provided Native Tool Schemas (JSON function calling).\n"
            "4. DO NOT write `<tool_code>` blocks or markdown code trying to invoke tools in raw text. ALWAYS use the underlying API function call mechanism.\n"
            "5. Be confident. Assume actions are allowed (they will be caught by a human-in-loop approval gate if necessary). Do not prompt the user for obvious parameters if you can synthesize them yourself."
        )
        if context:
            base_prompt += f"\n\nCurrent Context: {context}"
        return base_prompt

    def format_messages(self, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        # Logic to format history for specific providers
        return history
