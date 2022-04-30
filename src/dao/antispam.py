from src.model.antispam import AntispamKeyWord, AntispamNewUser, AntispamWatchGroup

from .base_dao import BaseDao, on


@on(AntispamKeyWord)
class AntispamKeyWordDao(BaseDao):
    ...


@on(AntispamNewUser)
class AntispamNewUserDao(BaseDao):
    @classmethod
    def getByUserIdOrNull(cls, user_id: int):
        try:
            cls.__MODEL_CLASS__.select().where(AntispamNewUser.user_id == user_id).get()
        except AntispamNewUser.DoesNotExist:
            return None


@on(AntispamWatchGroup)
class AntispamWatchGroupDao(BaseDao):
    @classmethod
    def getByChatIdOrNull(cls, chat_id: int):
        try:
            cls.__MODEL_CLASS__.select().where(
                AntispamWatchGroup.chat_id == chat_id
            ).get()
        except AntispamWatchGroup.DoesNotExist:
            return None
