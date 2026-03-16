from typing import Callable, Dict, List, Optional


class GatewayHooks:
    def __init__(self):
        self._pre_hooks: List[Callable] = []
        self._post_hooks: List[Callable] = []

    def add_pre_hook(self, fn: Callable):
        self._pre_hooks.append(fn)

    def add_post_hook(self, fn: Callable):
        self._post_hooks.append(fn)

    def run_pre(self, platform: str, user_id: str, text: str) -> str:
        for hook in self._pre_hooks:
            text = hook(platform, user_id, text) or text
        return text

    def run_post(self, platform: str, user_id: str, response: str) -> str:
        for hook in self._post_hooks:
            response = hook(platform, user_id, response) or response
        return response
