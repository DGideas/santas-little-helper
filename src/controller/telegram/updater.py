import logging

from src.dao.santas import TgUpdateDao
from src.data.enums import TelegramUpdateType
from src.interface.telegram import bot
from src.model.santas import TgUpdate

from .update_message_handler import TgUpdateMessageHandler

logger = logging.getLogger("telegram.updater")


class TelegramUpdateMessageController(object):
    @classmethod
    def getTelegramUpdate(cls):
        latestUpdate: TgUpdate = TgUpdateDao.getLatestUpdateOrNull()
        latestUpdateId: int = None
        if latestUpdate:
            latestUpdateId = latestUpdate.update_id

        updates = bot.getUpdates(offset=latestUpdateId)

        for updateRecord in updates:
            logger.debug(f"Received message {updateRecord}")
            updateType = None
            message = None

            if updateRecord.message:
                updateType = TelegramUpdateType.TYPE_MESSAGE
                message = updateRecord.message

                TgUpdateMessageHandler.messageHandler(message)
                # TODO handle message by newly created message / edited message
                if message.edit_date:
                    ...
                else:
                    ...

            elif updateRecord.my_chat_member:
                updateType = TelegramUpdateType.TYPE_MY_CHAT_MEMBER
                message = updateRecord.my_chat_member

                TgUpdateMessageHandler.myChatMemberHandler(message)
                # TODO handle different type of message
                ...

            if TelegramUpdateType.isSupportedType(updateType):
                TgUpdateDao.create(
                    update_id=updateRecord.update_id,
                    update_type=updateType,
                    raw_message=message,
                )
