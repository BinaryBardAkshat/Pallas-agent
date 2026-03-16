from tools.file_tools import FileTool, TerminalTool
from tools.web_tools import WebTool
from tools.memory_tool import MemoryTool
from tools.code_execution_tool import CodeExecutionTool
from tools.skill_manager_tool import SkillManagerTool
from tools.session_search_tool import SessionSearchTool
from tools.todo_tool import TodoTool
from typing import Callable, Dict


def build_default_toolset() -> Dict[str, Callable]:
    return {
        "file": FileTool(),
        "terminal": TerminalTool(),
        "web": WebTool(),
        "code_exec": CodeExecutionTool(),
        "skill_manager": SkillManagerTool(),
        "session_search": SessionSearchTool(),
        "todo": TodoTool(),
    }


def build_memory_toolset(memory_store=None) -> Dict[str, Callable]:
    return {
        "memory": MemoryTool(memory_store),
    }


def register_all(agent, memory_store=None):
    for name, tool in build_default_toolset().items():
        agent.register_tool(name, tool)
    for name, tool in build_memory_toolset(memory_store).items():
        agent.register_tool(name, tool)
