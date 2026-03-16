import os
import uuid
from typing import Any, Callable, Dict, Optional
from environments.agent_loop import AgentLoop
from tools import FileTool, TerminalTool, WebTool, MemoryTool, CodeExecutionTool, SkillManagerTool
from pallas_core.pallas_constants import PROVIDER_ANTHROPIC


class GatewaySession:
    def __init__(self, user_id: str, platform: str, provider: str = PROVIDER_ANTHROPIC):
        self.user_id = user_id
        self.platform = platform
        self.session_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{platform}:{user_id}"))
        self.agent = AgentLoop(provider=provider, human_in_loop=False, session_id=self.session_id)
        self.agent.register_tool("file", FileTool())
        self.agent.register_tool("terminal", TerminalTool())
        self.agent.register_tool("web", WebTool())
        self.agent.register_tool("memory", MemoryTool(self.agent.memory))
        self.agent.register_tool("code_exec", CodeExecutionTool())
        self.agent.register_tool("skill_manager", SkillManagerTool())

    def handle(self, text: str) -> str:
        return self.agent.run(text)


class GatewayRouter:
    def __init__(self, provider: str = PROVIDER_ANTHROPIC):
        self.provider = provider
        self._sessions: Dict[str, GatewaySession] = {}

    def get_or_create_session(self, user_id: str, platform: str) -> GatewaySession:
        key = f"{platform}:{user_id}"
        if key not in self._sessions:
            self._sessions[key] = GatewaySession(user_id, platform, self.provider)
        return self._sessions[key]

    def route(self, user_id: str, platform: str, text: str) -> str:
        session = self.get_or_create_session(user_id, platform)
        return session.handle(text)


_router: Optional[GatewayRouter] = None


def get_router() -> GatewayRouter:
    global _router
    if _router is None:
        _router = GatewayRouter()
    return _router
