import os
from typing import Any, Callable, Optional
from gateway.platforms.base import BasePlatform


class TelegramPlatform(BasePlatform):
    platform_name = "telegram"

    def __init__(self, token: str = "", on_message: Optional[Callable] = None):
        super().__init__(token or os.getenv("TELEGRAM_BOT_TOKEN", ""), on_message)
        self._bot = None

    def _get_bot(self):
        try:
            import telebot
            if not self._bot:
                self._bot = telebot.TeleBot(self.token)
            return self._bot
        except ImportError:
            raise RuntimeError("Install telebot: pip install pyTelegramBotAPI")

    def start(self):
        bot = self._get_bot()

        @bot.message_handler(func=lambda msg: True)
        def handler(message):
            response = self.handle(message.chat.id, message.text)
            bot.reply_to(message, response)

        bot.infinity_polling()

    def send(self, chat_id: Any, text: str):
        bot = self._get_bot()
        for chunk in [text[i:i+4096] for i in range(0, len(text), 4096)]:
            bot.send_message(chat_id, chunk)
