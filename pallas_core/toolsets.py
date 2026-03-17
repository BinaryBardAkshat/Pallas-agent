from typing import Callable, Dict, Optional, List

from tools.file_tools import FileTool, TerminalTool
from tools.web_tools import WebTool
from tools.memory_tool import MemoryTool
from tools.code_execution_tool import CodeExecutionTool
from tools.skill_manager_tool import SkillManagerTool
from tools.session_search_tool import SessionSearchTool
from tools.todo_tool import TodoTool
from tools.delegate_tool import DelegateTool
from tools.vision_tool import VisionTool
from tools.clarify_tool import ClarifyTool


def build_default_toolset() -> Dict[str, Callable]:
    return {
        "file": FileTool(),
        "terminal": TerminalTool(),
        "web": WebTool(),
        "code_exec": CodeExecutionTool(),
        "skill_manager": SkillManagerTool(),
        "session_search": SessionSearchTool(),
        "todo": TodoTool(),
        "delegate": DelegateTool(),
        "vision": VisionTool(),
        "clarify": ClarifyTool(),
    }


def build_memory_toolset(memory_store=None) -> Dict[str, Callable]:
    return {
        "memory": MemoryTool(memory_store),
    }


def get_toolset(tool_names: Optional[List[str]] = None) -> Dict[str, Callable]:
    """Return a dict of tools, optionally filtered to the given names.

    If *tool_names* is None or empty the full default toolset is returned.
    Unknown names are silently ignored so callers don't need to guard against
    tools that may not exist in the current build.
    """
    full = build_default_toolset()
    if not tool_names:
        return full
    return {name: fn for name, fn in full.items() if name in tool_names}


def register_all(agent, memory_store=None):
    for name, tool in build_default_toolset().items():
        agent.register_tool(name, tool)
    for name, tool in build_memory_toolset(memory_store).items():
        agent.register_tool(name, tool)
