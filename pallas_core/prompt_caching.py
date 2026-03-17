from typing import List, Dict, Union

class PromptCacher:
    """
    Handles prompt caching annotations for providers that support it (Anthropic, Google).
    """
    
    def wrap_cacheable(self, content: Union[str, List], provider: str) -> Union[str, List, Dict]:
        """Returns provider-specific cache-annotated content block."""
        if provider == "anthropic":
            if isinstance(content, str):
                return {
                    "type": "text",
                    "text": content,
                    "cache_control": {"type": "ephemeral"}
                }
            return content # Already a list or dict, complex to wrap here
        
        return content

    def apply_to_messages(self, messages: List[Dict], provider: str) -> List[Dict]:
        """Annotates system prompt and early turns for caching."""
        if provider not in ["anthropic", "google"]:
            return messages

        new_messages = []
        for i, msg in enumerate(messages):
            # Cache the system prompt and the first few messages if they are stable
            if i < 3: # Cache first 3 turns
                content = msg.get("content", "")
                if isinstance(content, str) and provider == "anthropic":
                    new_messages.append({
                        "role": msg["role"],
                        "content": [
                            {
                                "type": "text",
                                "text": content,
                                "cache_control": {"type": "ephemeral"}
                            }
                        ]
                    })
                else:
                    new_messages.append(msg)
            else:
                new_messages.append(msg)
        
        return new_messages

# Google Gemini: Cache is handled differently via CachedContent API in SDK,
# usually requiring a separate 'create_cache' call. 
# This implementation focuses on Anthropic's inline ephemeral caching.
