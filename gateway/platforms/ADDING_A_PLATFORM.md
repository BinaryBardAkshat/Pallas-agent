# Adding a New Gateway Platform

To add a new platform adapter to Pallas Gateway, follow these steps:

1. **Create the adapter file**
   Create a new file in `gateway/platforms/your_platform.py`.

2. **Extend `BasePlatform`**
   Your class must inherit from `gateway.platforms.base.BasePlatform`.
   ```python
   from .base import BasePlatform
   from typing import Any, Callable, Optional

   class YourPlatform(BasePlatform):
       platform_name: str = "your_platform"

       def __init__(self, token: str = "", on_message: Optional[Callable] = None):
           super().__init__(token=token, on_message=on_message)

       def start(self):
           # Initialize connection
           pass

       def send(self, chat_id: Any, text: str):
           # Send message to platform
           pass
   ```

3. **Implement 4 core methods**
   - `__init__`: Set up configuration and token.
   - `start`: Establish the connection or start polling/listening.
   - `send`: Deliver messages to the user.
   - `handle`: (Optional override) Map incoming data to `on_message` callback.

4. **Register the platform**
   - Export it in `gateway/platforms/__init__.py`.
   - Register it in your session manager or mapping logic (check `gateway/session.py`).

5. **Environment Variables**
   Add any required variables to `.env.example`.

6. **Usage**
   Pallas will automatically use registered platforms if configured in the environment.
