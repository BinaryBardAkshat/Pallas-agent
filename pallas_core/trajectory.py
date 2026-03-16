from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pallas_time import timestamp


@dataclass
class ToolCall:
    name: str
    input: Dict[str, Any]
    output: Optional[str] = None
    error: Optional[str] = None
    duration_ms: Optional[float] = None


@dataclass
class TrajectoryStep:
    step: int
    role: str
    content: str
    tool_calls: List[ToolCall] = field(default_factory=list)
    tokens: int = 0
    timestamp: str = field(default_factory=timestamp)


class Trajectory:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.steps: List[TrajectoryStep] = []
        self._step_counter = 0

    def add(self, role: str, content: str, tool_calls: List[ToolCall] = None, tokens: int = 0) -> TrajectoryStep:
        self._step_counter += 1
        step = TrajectoryStep(
            step=self._step_counter,
            role=role,
            content=content,
            tool_calls=tool_calls or [],
            tokens=tokens,
        )
        self.steps.append(step)
        return step

    def to_messages(self) -> List[Dict[str, str]]:
        return [
            {"role": s.role, "content": s.content}
            for s in self.steps
            if s.role in ("user", "assistant")
        ]

    def total_tokens(self) -> int:
        return sum(s.tokens for s in self.steps)

    def summary(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "steps": len(self.steps),
            "total_tokens": self.total_tokens(),
            "tool_calls": sum(len(s.tool_calls) for s in self.steps),
        }
