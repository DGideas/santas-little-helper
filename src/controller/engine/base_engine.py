from src.dao.santas import SantasOperationRecordDao
from src.data.enums import DURATION_INF, SantasOperationEngine, SantasOperationType
from src.interface.telegram import bot
from src.model.db import db


class BaseEngine(object):
    __ENGINE__: SantasOperationEngine = None

    @classmethod
    def sendMessage(cls, chat_id: str, message: str):
        with db.atomic():
            SantasOperationRecordDao.create(
                engine=cls.__ENGINE__,
                operation_type=SantasOperationType.OP_SEND_MESSAGE.value,
                target=chat_id,
                message=message,
                extra_info={},
            )
            bot.sendMessage(chat_id=chat_id, text=message)

    @classmethod
    def banUserFromChat(cls, chat_id: str, user_id: str, duration: int = DURATION_INF):
        with db.atomic():
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
