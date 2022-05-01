import datetime
import logging
import time

import telegram

from src.controller.telegram.update_message_handler import TgUpdateMessageHandler
from src.dao.santas import TgUpdateDao
from src.data.enums import TelegramUpdateType
from src.interface.telegram import bot
from src.model.santas import TgUpdate

logger = logging.getLogger("telegram.updater")


class TelegramUpdateMessageController(object):
    @classmethod
    def getTelegramUpdate(cls):
        latestUpdate: TgUpdate = TgUpdateDao.getLatestUpdateOrNull()
        latestUpdateId: int = None
        if latestUpdate:
            latestUpdateId = latestUpdate.update_id + 1

        cls.cleanOldUpdateMessage()

        logger.info(f"Get telegram updates, offset: {latestUpdateId}")
        while True:
            try:
                updates = bot.getUpdates(
                    offset=latestUpdateId,
                    timeout=5,
                    allowed_updates=[
                        "message",
                        "edited_message",
                        "channel_post",
                        "edited_channel_post",
                        "inline_query",
                        "chosen_inline_result",
                        "callback_query",
                        "shipping_query",
                        "pre_checkout_query",
                        "poll",
                        "poll_answer",
                        "my_chat_member",
                        "chat_member",
                        "chat_join_request",
                    ],
                )
                break
            except telegram.error.TimedOut:
                logger.warning("bot.getUpdates timeout, retry...")
                time.sleep(10)
                continue
            except Exception as e:
                raise e
        logger.info(f"Get {len(updates)} update(s).")

        for updateRecord in updates:
            logger.debug(f"Received message {updateRecord}")
            updateType = None
            message = None

            if updateRecord.message:
                message = updateRecord.message
                if updateRecord.message.new_chat_members:
                    updateType = TelegramUpdateType.TYPE_NEW_CHAT_MEMBER
                    TgUpdateMessageHandler.newChatUserHandler(message)
                else:

                    updateType = TelegramUpdateType.TYPE_MESSAGE

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

            else:
                logger.warn(f"Unhandled message: {updateRecord}")

            if TelegramUpdateType.isSupportedType(updateType):
                TgUpdateDao.create(
                    update_id=updateRecord.update_id,
                    update_type=updateType,
                    raw_message=message,
                )

    @classmethod
    def cleanOldUpdateMessage(
        cls, oldMessageThreshold: datetime.timedelta = datetime.timedelta(days=7)
    ):
        now = datetime.datetime.utcnow()
        TgUpdateDao.deleteOldUpdate(now - oldMessageThreshold)
