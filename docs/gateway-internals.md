# Gateway Internals

The Gateway layer allows Pallas to receive messages from external platforms (Telegram, Discord, Slack, WhatsApp, Signal, Email, Home Assistant) and respond through the same channel. All platforms share a single session router.

---

## BasePlatform Interface

Every platform adapter inherits from `gateway/platforms/base.py`:

```python
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

class BasePlatform(ABC):
    platform_name: str = "base"

    def __init__(self, token: str = "", on_message: Optional[Callable] = None):
        self.token = token
        self.on_message = on_message

    @abstractmethod
    def start(self):
        """Start the platform listener (blocking)."""
        pass

    @abstractmethod
    def send(self, chat_id: Any, text: str):
        """Send a text response back to a chat."""
        pass

    def handle(self, chat_id: Any, text: str) -> str:
        """Default message handler — delegates to on_message callback."""
        if self.on_message:
            return self.on_message(chat_id=chat_id, text=text, platform=self.platform_name)
        return "(no handler)"
```

The `on_message` callback is the bridge to the agent. It is injected at startup by the CLI's `gateway` command.

---

## Session Routing

`gateway/session.py` manages a pool of `AgentLoop` instances, one per `(chat_id, platform)` pair. This ensures each user gets a persistent, isolated conversation context.

```python
from gateway.session import get_router

router = get_router()

def on_message(chat_id, text, platform_name):
    return router.route(str(chat_id), platform_name, text)
```

`router.route()` looks up or creates an `AgentLoop` for the given session key, then calls `loop.run(text)` and returns the response string. The platform adapter sends this string back to the user.

---

## Supported Platforms

| Platform | Class | Status | Notes |
|---|---|---|---|
| Telegram | `TelegramPlatform` | Active | Uses `python-telegram-bot` |
| Discord | `DiscordPlatform` | Active | Uses `discord.py` |
| Slack | `SlackPlatform` | Active | Uses Slack Bolt SDK |
| WhatsApp | `WhatsAppPlatform` | Scaffold | Business API integration pending |
| Signal | `SignalPlatform` | Scaffold | Requires `signal-cli` bridge |
| Email | `EmailPlatform` | Scaffold | SMTP/IMAP loop pending |
| Home Assistant | `HomeAssistantPlatform` | Scaffold | HA webhook integration pending |

---

## Starting a Gateway

```bash
# Telegram
TELEGRAM_BOT_TOKEN=... pallas gateway telegram

# Discord
DISCORD_BOT_TOKEN=... pallas gateway discord

# Slack
SLACK_BOT_TOKEN=... SLACK_APP_TOKEN=... pallas gateway slack
```

The `gateway` CLI command starts the platform listener in the foreground. For production use, run it under a process manager (systemd, Docker, PM2).

---

## How to Add a New Platform

**Step 1 — Create the platform file**

Create `gateway/platforms/myplatform.py`:

```python
from gateway.platforms.base import BasePlatform
import os

class MyPlatform(BasePlatform):
    platform_name = "myplatform"

    def __init__(self, on_message=None):
        token = os.getenv("MYPLATFORM_TOKEN", "")
        super().__init__(token=token, on_message=on_message)
        # Initialize your SDK client here

    def start(self):
        """Start listening for incoming messages (blocking)."""
        # Set up your SDK's event loop / webhook / polling
        # On each incoming message, call: self.handle(chat_id, text)
        # Then send the response: self.send(chat_id, response)
        pass

    def send(self, chat_id, text: str):
        """Send text back to the user."""
        # Use your SDK to send `text` to `chat_id`
        pass
```

**Step 2 — Register in `__init__.py`**

Add to `gateway/platforms/__init__.py`:

```python
from gateway.platforms.myplatform import MyPlatform
__all__ = [..., "MyPlatform"]
```

**Step 3 — Add to the CLI gateway command**

In `pallas_cli/main.py`, add a branch in the `gateway` command:

```python
elif platform == "myplatform":
    from gateway.platforms.myplatform import MyPlatform
    bot = MyPlatform(on_message=on_message)
    console.print("[bold blue]Starting MyPlatform Gateway...[/bold blue]")
    bot.start()
```

**Step 4 — Test**

```bash
MYPLATFORM_TOKEN=your_token pallas gateway myplatform
```

---

## Session Isolation

Each `(chat_id, platform_name)` pair gets its own `AgentLoop` with its own `MemoryStore` and `Trajectory`. This means:
- A Telegram user and a Discord user never share context
- The same user in two different Telegram chats gets two independent sessions
- Sessions persist across gateway restarts (history stored in SQLite)

---

## Deployment Example

Running Telegram and Discord gateways simultaneously via Docker Compose:

```yaml
services:
  telegram:
    image: pallas-agent:latest
    command: pallas gateway telegram
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - pallas_data:/root/.pallas

  discord:
    image: pallas-agent:latest
    command: pallas gateway discord
    environment:
      - DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - pallas_data:/root/.pallas

volumes:
  pallas_data:
```

Both containers share the same `pallas_data` volume so memories are shared across platforms.
