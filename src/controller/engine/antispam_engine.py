import logging

from telegram import ChatMemberUpdated, Message

from src.dao.antispam import AntispamNewUserDao, AntispamWatchGroupDao
from src.data.enums import AntispamWatchGroupStatus, SantasOperationEngine
from src.interface.telegram import whoami
from src.model.antispam import AntispamNewUser
from src.model.db import db

from .base_engine import BaseEngine

logger = logging.getLogger("telegram.engine.antispam")


class AntispamEngine(BaseEngine):
    __ENGINE__ = SantasOperationEngine.ENGINE_ANTISPAM

    @classmethod
    def doNewChatUser(cls, message: Message):
        for user in message.new_chat_members:
            with db.atomic():
                if AntiSpamController.isNewUser(user.id):
                    continue
                logger.info(
                    f"Created newly joined user {user.id} on group chat {message.chat_id}."
                )
                AntiSpamController.createUser(user.id, message.chat_id)

    @classmethod
    def doMessage(cls, message: Message):
        # 处理 /active 和 /inactive 事件
        if message.text == f"/active@{whoami}":
            AntiSpamController.activeGroupInWatchList(message.chat_id)
            cls.sendMessage(message.chat_id, f"已经成功在该群组装载 {whoami}")
        if message.text == f"/inactive@{whoami}":
            AntiSpamController.inactiveGroupInWatchList(message.chat_id)
            cls.sendMessage(message.chat_id, f"已经成功在该群组卸载 {whoami}")

        if not AntiSpamController.isGroupInWatchList(message.chat_id):
            return

        logger.debug(f"Message from {message.from_user.id}")

        if not AntiSpamController.isNewUser(message.from_user.id):
            return

        user = AntiSpamController.getUser(message.from_user.id)
        print(user.created_time)

    @classmethod
    def doChatMemberUpdated(cls, cmu: ChatMemberUpdated):
        ...


class AntiSpamController(object):
    @classmethod
    def isGroupInWatchList(cls, chat_id: str):
        return bool(AntispamWatchGroupDao.getByChatIdOrNull(chat_id))

    @classmethod
    def activeGroupInWatchList(cls, chat_id: str):
        with db.atomic():
            if AntispamWatchGroupDao.getByChatIdOrNull(chat_id) is None:
                AntispamWatchGroupDao.create(
                    chat_id=chat_id,
                )

            AntispamWatchGroupDao.updateStatusByChatId(
                chat_id, AntispamWatchGroupStatus.ST_VALID
            )

    @classmethod
    def inactiveGroupInWatchList(cls, chat_id: str):
        with db.atomic():
            if AntispamWatchGroupDao.getByChatIdOrNull(chat_id) is None:
                AntispamWatchGroupDao.create(
                    chat_id=chat_id,
                )

            AntispamWatchGroupDao.updateStatusByChatId(
                chat_id, AntispamWatchGroupStatus.ST_INVALID
            )

    @classmethod
    def isNewUser(cls, user_id: int):
        return bool(AntispamNewUserDao.getByUserIdOrNull(user_id))

    @classmethod
    def getUser(cls, user_id: int) -> AntispamNewUser:
        return AntispamNewUserDao.getByUserIdOrNull(user_id)

    @classmethod
    def createUser(cls, user_id: int, chat_id: int):
        return AntispamNewUserDao.create(user_id=user_id, chat_id=chat_id)
