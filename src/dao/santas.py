import datetime

from src.data.enums import SantasWatchlistStatus
from src.model.santas import SantasOperationRecord, TgChatWatchList, TgUpdate

from .base_dao import BaseDao, on


@on(TgChatWatchList)
class WatchListDao(BaseDao):
    @classmethod
    def listByStatus(cls, status: SantasWatchlistStatus):
        return cls.__MODEL_CLASS__.select().where(TgChatWatchList.status == status)


@on(SantasOperationRecord)
class SantasOperationRecordDao(BaseDao):
    pass


@on(TgUpdate)
class TgUpdateDao(BaseDao):
    @classmethod
    def getLatestUpdateOrNull(cls) -> TgUpdate:
        try:
            return (
                cls.__MODEL_CLASS__.select().order_by(TgUpdate.update_id.desc()).get()
            )
        except TgUpdate.DoesNotExist:
            return None

    @classmethod
    def deleteOldUpdate(cls, datetimeThreshold: datetime.datetime) -> int:
        return (
            cls.__MODEL_CLASS__.delete()
            .where(TgUpdate.created_time < datetimeThreshold)
            .execute()
        )
