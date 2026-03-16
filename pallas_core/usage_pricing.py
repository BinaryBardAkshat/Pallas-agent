from typing import Any, Dict, List, Optional


class UsagePricing:
    def __init__(self):
        self.records: List[Dict[str, Any]] = []

    def record(self, model: str, input_tokens: int, output_tokens: int):
        from pallas_core.model_metadata import get_model_info
        from .pallas_time import timestamp

        info = get_model_info(model)
        cost = 0.0
        if info:
            cost = (input_tokens / 1_000_000 * info.cost_per_1m_input) + \
                   (output_tokens / 1_000_000 * info.cost_per_1m_output)

        self.records.append({
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": round(cost, 6),
            "timestamp": timestamp(),
        })

    def total_cost(self) -> float:
        return round(sum(r["cost_usd"] for r in self.records), 6)

    def total_tokens(self) -> int:
        return sum(r["input_tokens"] + r["output_tokens"] for r in self.records)

    def summary(self) -> Dict[str, Any]:
        return {
            "calls": len(self.records),
            "total_tokens": self.total_tokens(),
            "total_cost_usd": self.total_cost(),
        }
