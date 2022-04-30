from local_settings import TELEGRAM_BOT_KEY
from src.interface.base_client import BaseClient


class TelegramBotClient(BaseClient):
    BASE_URL = f"https://api.telegram.org/{TELEGRAM_BOT_KEY}"

    @classmethod
    def getMe(cls):
        resp = cls.get("/getMe")
        return resp
