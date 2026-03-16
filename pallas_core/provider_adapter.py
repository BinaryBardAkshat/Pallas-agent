import os
from typing import Any, Dict, List, Optional

from pallas_constants import (
    DEFAULT_MODELS,
    PROVIDER_ANTHROPIC,
    PROVIDER_GOOGLE,
    PROVIDER_OLLAMA,
    PROVIDER_OPENAI,
    PROVIDER_OPENROUTER,
)


class ProviderResponse:
    def __init__(
        self,
        content: str = "",
        tool_calls: Optional[List[Dict[str, Any]]] = None,
        tokens: int = 0,
        stop_reason: str = "end_turn",
        error: Optional[str] = None,
    ):
        self.content = content
        self.tool_calls = tool_calls or []
        self.tokens = tokens
        self.stop_reason = stop_reason
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "tool_calls": self.tool_calls,
            "tokens": self.tokens,
            "stop_reason": self.stop_reason,
            "error": self.error,
        }


class ProviderAdapter:
    def __init__(self, provider: str = PROVIDER_ANTHROPIC):
        self.provider = provider
        self._clients: Dict[str, Any] = {}
        self._init_client()

    def _init_client(self):
        if self.provider == PROVIDER_ANTHROPIC:
            self._init_anthropic()
        elif self.provider == PROVIDER_GOOGLE:
            self._init_google()
        elif self.provider == PROVIDER_OPENAI:
            self._init_openai()
        elif self.provider == PROVIDER_OPENROUTER:
            self._init_openrouter()
        elif self.provider == PROVIDER_OLLAMA:
            self._init_ollama()

    def _init_anthropic(self):
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if not api_key:
            return
        try:
            import anthropic
            self._clients[PROVIDER_ANTHROPIC] = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            pass

    def _init_google(self):
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if not api_key:
            return
        try:
            from google import genai
            self._clients[PROVIDER_GOOGLE] = genai.Client(api_key=api_key)
        except ImportError:
            pass

    def _init_openai(self):
        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            return
        try:
            from openai import OpenAI
            self._clients[PROVIDER_OPENAI] = OpenAI(api_key=api_key)
        except ImportError:
            pass

    def _init_openrouter(self):
        api_key = os.getenv("OPENROUTER_API_KEY", "")
        if not api_key:
            return
        try:
            from openai import OpenAI
            self._clients[PROVIDER_OPENROUTER] = OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1",
            )
        except ImportError:
            pass

    def _init_ollama(self):
        try:
            from openai import OpenAI
            host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
            self._clients[PROVIDER_OLLAMA] = OpenAI(
                api_key="ollama",
                base_url=f"{host}/v1",
            )
        except ImportError:
            pass

    def get_api_key_status(self) -> Dict[str, bool]:
        return {
            PROVIDER_ANTHROPIC: bool(os.getenv("ANTHROPIC_API_KEY")),
            PROVIDER_GOOGLE: bool(os.getenv("GOOGLE_API_KEY")),
            PROVIDER_OPENAI: bool(os.getenv("OPENAI_API_KEY")),
            PROVIDER_OPENROUTER: bool(os.getenv("OPENROUTER_API_KEY")),
        }

    def completion(
        self,
        messages: List[Dict[str, str]],
        system: str = "",
        model: Optional[str] = None,
        max_tokens: int = 4096,
        tools: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        resolved_model = model or DEFAULT_MODELS.get(self.provider, "")

        if self.provider == PROVIDER_ANTHROPIC:
            return self._anthropic_completion(messages, system, resolved_model, max_tokens, tools)
        elif self.provider == PROVIDER_GOOGLE:
            return self._google_completion(messages, system, resolved_model, max_tokens)
        elif self.provider == PROVIDER_OPENAI:
            return self._openai_completion(messages, system, resolved_model, max_tokens)
        elif self.provider == PROVIDER_OPENROUTER:
            return self._openrouter_completion(messages, system, resolved_model, max_tokens)
        elif self.provider == PROVIDER_OLLAMA:
            return self._ollama_completion(messages, system, resolved_model, max_tokens)

        return ProviderResponse(error=f"Unknown provider: {self.provider}").to_dict()

    def _anthropic_completion(
        self, messages, system, model, max_tokens, tools
    ) -> Dict[str, Any]:
        client = self._clients.get(PROVIDER_ANTHROPIC)
        if not client:
            return ProviderResponse(
                content="Anthropic API key not configured. Set ANTHROPIC_API_KEY.",
                error="no_key",
            ).to_dict()

        kwargs: Dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools

        try:
            resp = client.messages.create(**kwargs)
        except Exception as e:
            return ProviderResponse(content="", error=str(e)).to_dict()

        content = ""
        tool_calls = []
        for block in resp.content:
            if block.type == "text":
                content = block.text
            elif block.type == "tool_use":
                tool_calls.append({
                    "name": block.name,
                    "input": block.input,
                    "id": block.id,
                })

        return ProviderResponse(
            content=content,
            tool_calls=tool_calls,
            tokens=resp.usage.input_tokens + resp.usage.output_tokens,
            stop_reason=resp.stop_reason,
        ).to_dict()

    def _google_completion(
        self, messages, system, model, max_tokens, tools=None
    ) -> Dict[str, Any]:
        client = self._clients.get(PROVIDER_GOOGLE)
        if not client:
            return ProviderResponse(
                content="Google API key not configured. Set GOOGLE_API_KEY.",
                error="no_key",
            ).to_dict()

        from google import genai
        from google.genai import types
        
        gemini_tools = []
        if tools:
            for t in tools:
                props = {}
                required = t.get("input_schema", {}).get("required", [])
                for prop_name, prop_data in t.get("input_schema", {}).get("properties", {}).items():
                    props[prop_name] = types.Schema(
                        type=types.Type.STRING,
                        description=prop_data.get("description", ""),
                    )
                
                gemini_tools.append(
                    types.Tool(
                        function_declarations=[
                            types.FunctionDeclaration(
                                name=t["name"],
                                description=t["description"],
                                parameters=types.Schema(
                                    type=types.Type.OBJECT,
                                    properties=props,
                                    required=required,
                                )
                            )
                        ]
                    )
                )

        gemini_messages = []
        for m in messages:
            role = "user" if m["role"] == "user" else "model"
            text_content = m.get("content", "")
            if not text_content:
                text_content = " "
            gemini_messages.append(
                types.Content(role=role, parts=[types.Part.from_text(text=text_content)])
            )
                
        try:
            config_kwargs = {}
            if gemini_tools:
                config_kwargs["tools"] = gemini_tools
            if system:
                config_kwargs["system_instruction"] = system
                
            resp = client.models.generate_content(
                model=model,
                contents=gemini_messages,
                config=types.GenerateContentConfig(**config_kwargs) if config_kwargs else None
            )

            tool_calls = []
            content = ""
            
            if resp.candidates and resp.candidates[0].content and resp.candidates[0].content.parts:
                for part in resp.candidates[0].content.parts:
                    if part.function_call:
                        args_dict = {k: v for k, v in part.function_call.args.items()} if part.function_call.args else {}
                        tool_calls.append({
                            "name": part.function_call.name,
                            "input": args_dict,
                            "id": "gemini_call"
                        })
                    elif part.text:
                        content += part.text

            return ProviderResponse(
                content=content,
                tool_calls=tool_calls,
                tokens=0,
                stop_reason="end_turn",
            ).to_dict()
        except Exception as e:
            return ProviderResponse(content="", error=f"Gemini API Error: {str(e)}").to_dict()

    def _openai_completion(
        self, messages, system, model, max_tokens
    ) -> Dict[str, Any]:
        client = self._clients.get(PROVIDER_OPENAI)
        if not client:
            return ProviderResponse(
                content="OpenAI API key not configured. Set OPENAI_API_KEY.",
                error="no_key",
            ).to_dict()

        combined_input = ""
        if system:
            combined_input += f"[System]\n{system}\n\n"
        for m in messages:
            combined_input += f"[{m['role']}]\n{m['content']}\n\n"

        try:
            resp = client.responses.create(
                model=model,
                input=combined_input.strip(),
            )
            content = ""
            for item in resp.output:
                if hasattr(item, "content"):
                    for part in item.content:
                        if hasattr(part, "text"):
                            content += part.text
            return ProviderResponse(
                content=content,
                tokens=resp.usage.total_tokens if resp.usage else 0,
                stop_reason="end_turn",
            ).to_dict()
        except Exception as e:
            return ProviderResponse(content="", error=str(e)).to_dict()

    def _openrouter_completion(
        self, messages, system, model, max_tokens
    ) -> Dict[str, Any]:
        client = self._clients.get(PROVIDER_OPENROUTER)
        if not client:
            return ProviderResponse(
                content="OpenRouter API key not configured. Set OPENROUTER_API_KEY.",
                error="no_key",
            ).to_dict()

        all_messages = []
        if system:
            all_messages.append({"role": "system", "content": system})
        all_messages.extend(messages)

        try:
            resp = client.chat.completions.create(
                model=model,
                messages=all_messages,
                max_tokens=max_tokens,
            )
            return ProviderResponse(
                content=resp.choices[0].message.content or "",
                tokens=resp.usage.total_tokens if resp.usage else 0,
                stop_reason=resp.choices[0].finish_reason or "end_turn",
            ).to_dict()
        except Exception as e:
            return ProviderResponse(content="", error=str(e)).to_dict()

    def _ollama_completion(
        self, messages, system, model, max_tokens
    ) -> Dict[str, Any]:
        client = self._clients.get(PROVIDER_OLLAMA)
        if not client:
            return ProviderResponse(
                content="Ollama not available. Ensure Ollama is running locally.",
                error="no_client",
            ).to_dict()

        all_messages = []
        if system:
            all_messages.append({"role": "system", "content": system})
        all_messages.extend(messages)

        try:
            resp = client.chat.completions.create(
                model=model,
                messages=all_messages,
                max_tokens=max_tokens,
            )
            return ProviderResponse(
                content=resp.choices[0].message.content or "",
                tokens=resp.usage.total_tokens if resp.usage else 0,
                stop_reason=resp.choices[0].finish_reason or "end_turn",
            ).to_dict()
        except Exception as e:
            return ProviderResponse(content="", error=str(e)).to_dict()

    def switch_provider(self, provider: str):
        self.provider = provider
        self._init_client()
