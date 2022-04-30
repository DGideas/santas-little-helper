from src.dao.santas import TgUpdateDao
from src.interface.telegram import bot
from src.model.santas import TgUpdate


class TelegramUpdateMessageController(object):
    @classmethod
    def getTelegramUpdate(cls):
        latestUpdate: TgUpdate = TgUpdateDao.getLatestUpdateOrNull()
        latestUpdateId: int = None
        if latestUpdate:
            latestUpdateId = latestUpdate.update_id

        updates = bot.getUpdates(offset=latestUpdateId)

        for updateRecord in updates:
            print(updateRecord)
            if updateRecord.message:
                message = updateRecord.message
                if message.edit_date:
                    ...
                else:
                    ...
            elif updateRecord.my_chat_member:
                ...


if __name__ == "__main__":
    TelegramUpdateMessageController.getTelegramUpdate()
