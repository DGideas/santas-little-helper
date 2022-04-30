from local_settings import TELEGRAM_BOT_KEY
from src.interface.base_client import BaseClient


class TelegramBotClient(BaseClient):
    BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_KEY}"

    @classmethod
    def getUpdates(cls):
        """
        https://core.telegram.org/bots/api#getupdates
        """
        resp = cls.get("/getUpdates")
        return resp

    @classmethod
    def getMe(cls):
        """
        https://core.telegram.org/bots/api#getme
        """
        resp = cls.get("/getMe")
        return resp

    @classmethod
    def sendMessage(
        cls,
        chat_id: str,
        text: str,
        disable_web_page_preview: bool = False,
        disable_notification: bool = False,
        reply_to_message_id: str = None,
    ):
        """
        https://core.telegram.org/bots/api#sendmessage
        """
        args = {
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": disable_web_page_preview,
            "disable_notification": disable_notification,
        }
        if reply_to_message_id:
            args["reply_to_message_id"] = reply_to_message_id

        return cls.post("/sendMessage", args)

    @classmethod
    def getChat(cls, chat_id: str):
        """
        https://core.telegram.org/bots/api#getchat
        """
        resp = cls.get("/getChat", param={"chat_id": chat_id})
        return resp
