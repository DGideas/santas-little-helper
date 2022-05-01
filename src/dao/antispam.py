from src.data.enums import AntispamWatchGroupStatus
from src.model.antispam import AntispamKeyWord, AntispamNewUser, AntispamWatchGroup

from .base_dao import BaseDao, on


@on(AntispamKeyWord)
class AntispamKeyWordDao(BaseDao):
    @classmethod
    def getAllKeywords(cls):
        return cls.__MODEL_CLASS__.select()


@on(AntispamNewUser)
class AntispamNewUserDao(BaseDao):
    @classmethod
    def getByUserIdOrNull(cls, user_id: int):
        try:
            return (
                cls.__MODEL_CLASS__.select()
                .where(AntispamNewUser.user_id == user_id)
                .get()
            )
        except AntispamNewUser.DoesNotExist:
            return None

    @classmethod
    def deleteUserByUserId(cls, user_id: int):
        return (
            cls.__MODEL_CLASS__.delete()
            .where(AntispamNewUser.user_id == user_id)
            .execute()
        )


@on(AntispamWatchGroup)
class AntispamWatchGroupDao(BaseDao):
    @classmethod
    def getByChatIdOrNull(cls, chat_id: int):
        try:
            return (
                cls.__MODEL_CLASS__.select()
                .where(AntispamWatchGroup.chat_id == chat_id)
                .get()
            )
        except AntispamWatchGroup.DoesNotExist:
            return None

    @classmethod
    def updateStatusByChatId(cls, chat_id: int, status: AntispamWatchGroupStatus):
        cls.__MODEL_CLASS__.update(status=status).where(
            AntispamWatchGroup.chat_id == chat_id
        )
