import base64
import os
from typing import Optional

import httpx


def _detect_media_type_from_extension(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    mapping = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return mapping.get(ext, "image/jpeg")


def _detect_media_type_from_content_type(content_type: str) -> str:
    """Extract a clean media_type from a Content-Type header value."""
    ct = content_type.split(";")[0].strip().lower()
    allowed = {"image/jpeg", "image/png", "image/gif", "image/webp"}
    return ct if ct in allowed else "image/jpeg"


class VisionTool:
    """Analyze an image file or URL using Claude Vision or Gemini Vision."""

    schema = {
        "name": "vision",
        "description": "Analyze an image file or URL — describe content, read text, answer questions about it",
        "input_schema": {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Local file path or URL"},
                "question": {
                    "type": "string",
                    "description": "Specific question about the image (default: describe it)",
                },
            },
            "required": ["source"],
        },
    }

    def __call__(self, source: str, question: str = "Describe this image in detail.") -> str:
        try:
            image_bytes: bytes
            media_type: str

            if source.startswith(("http://", "https://")):
                response = httpx.get(source, follow_redirects=True, timeout=30)
                response.raise_for_status()
                image_bytes = response.content
                content_type = response.headers.get("content-type", "")
                media_type = _detect_media_type_from_content_type(content_type) if content_type else "image/jpeg"
            else:
                if not os.path.exists(source):
                    return f"Error: File not found at {source}"
                with open(source, "rb") as fh:
                    image_bytes = fh.read()
                media_type = _detect_media_type_from_extension(source)

            b64_data = base64.standard_b64encode(image_bytes).decode("utf-8")

            anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
            google_key = os.environ.get("GOOGLE_API_KEY", "")

            if anthropic_key:
                return self._call_anthropic(b64_data, media_type, question, anthropic_key)
            elif google_key:
                return self._call_google(image_bytes, media_type, question, google_key)
            else:
                return "Error: No API key found. Set ANTHROPIC_API_KEY or GOOGLE_API_KEY."

        except Exception as e:
            return f"Error in vision tool: {str(e)}"

    def _call_anthropic(self, b64_data: str, media_type: str, question: str, api_key: str) -> str:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-5-haiku-latest",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": b64_data,
                            },
                        },
                        {"type": "text", "text": question},
                    ],
                }
            ],
        )
        text_blocks = [
            getattr(block, "text", None)
            for block in message.content
            if hasattr(block, "text")
        ]
        return "\n".join(t for t in text_blocks if t is not None)

    def _call_google(self, image_bytes: bytes, media_type: str, question: str, api_key: str) -> str:
        import google.generativeai as genai
        from google.generativeai.types import Part

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        image_part = Part.from_bytes(data=image_bytes, mime_type=media_type)
        response = model.generate_content([image_part, question])
        return response.text
