from telegram import ChatMemberUpdated, Message

from src.data.enums import SantasOperationEngine

from .base_engine import BaseEngine


class AntispamEngine(BaseEngine):
    __ENGINE__ = SantasOperationEngine.ENGINE_ANTISPAM

    @classmethod
    def doMessage(cls, message: Message):
        ...

    @classmethod
    def doChatMemberUpdated(cls, cmu: ChatMemberUpdated):
        ...
