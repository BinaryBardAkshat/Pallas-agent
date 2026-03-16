from typing import Any, Dict, List
from pallas_core.usage_pricing import UsagePricing
from pallas_core.trajectory import Trajectory


class SessionInsights:
    def __init__(self, trajectory: Trajectory, pricing: UsagePricing):
        self.trajectory = trajectory
        self.pricing = pricing

    def summary(self) -> Dict[str, Any]:
        traj = self.trajectory.summary()
        cost = self.pricing.summary()
        return {
            "session_id": traj["session_id"],
            "steps": traj["steps"],
            "total_tokens": traj["total_tokens"],
            "tool_calls": traj["tool_calls"],
            "total_cost_usd": cost["total_cost_usd"],
            "api_calls": cost["calls"],
        }

    def report(self) -> str:
        s = self.summary()
        lines = [
            f"Session: {s['session_id']}",
            f"  Steps: {s['steps']}",
            f"  Tokens: {s['total_tokens']}",
            f"  Tool calls: {s['tool_calls']}",
            f"  API calls: {s['api_calls']}",
            f"  Cost: ${s['total_cost_usd']:.4f}",
        ]
        return "\n".join(lines)
