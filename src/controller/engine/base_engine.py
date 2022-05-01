from abc import ABC

from src.dao.santas import SantasOperationRecordDao
from src.data.enums import DURATION_INF, SantasOperationEngine, SantasOperationType
from src.interface.telegram import bot
from src.model.db import db


class BaseEngine(ABC):
    __ENGINE__: SantasOperationEngine = None

    @classmethod
    @db.atomic()
    def sendMessage(cls, chat_id: str, message: str):
        SantasOperationRecordDao.create(
            engine=cls.__ENGINE__,
            operation_type=SantasOperationType.OP_SEND_MESSAGE.value,
            target=chat_id,
            message=message,
            extra_info={},
        )
        bot.sendMessage(chat_id=chat_id, text=message)

    @classmethod
    @db.atomic()
    def banUserFromChat(cls, chat_id: str, user_id: str, duration: int = DURATION_INF):
        SantasOperationRecordDao.create(
            engine=cls.__ENGINE__,
            operation_type=SantasOperationType.OP_SEND_MESSAGE.value,
            target=user_id,
            extra_info={
                "duration": duration,
                "chat_id": chat_id,
                "user_id": user_id,
            },
        )
        bot.banChatMember(chat_id=chat_id, user_id=user_id, until_date=duration)

    @classmethod
    @db.atomic()
    def deleteMessage(cls, chat_id: int, message_id: int, user_id: int, username: str):
        SantasOperationRecordDao.create(
            engine=cls.__ENGINE__,
            operation_type=SantasOperationType.OP_REMOVE_MESSAGE_FROM_CHAT.value,
            target=message_id,
            extra_info={
                "chat_id": chat_id,
                "message_id": message_id,
                "user_id": user_id,
                "username": username,
            },
        )
        bot.deleteMessage(chat_id=chat_id, message_id=message_id)
