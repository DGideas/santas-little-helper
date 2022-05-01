import datetime
import logging
from typing import Dict

import telegram
from telegram import ChatMemberUpdated, Message

from src.dao.antispam import (
    AntispamKeyWordDao,
    AntispamNewUserDao,
    AntispamWatchGroupDao,
)
from src.data.enums import AntispamWatchGroupStatus, SantasOperationEngine
from src.interface.telegram import whoami
from src.model.antispam import AntispamKeyWord, AntispamNewUser
from src.model.db import db

from .base_engine import BaseEngine

logger = logging.getLogger("telegram.engine.antispam")


class AntispamEngine(BaseEngine):
    __ENGINE__ = SantasOperationEngine.ENGINE_ANTISPAM

    @classmethod
    @db.atomic()
    def doNewChatUser(cls, message: Message):
        for user in message.new_chat_members:
            logger.debug(
                f"Got new user {user.id}({user.username}) from group {message.chat_id}."
            )
            if AntiSpamController.isNewUser(user.id):
                continue
            logger.info(
                f"Created newly joined user {user.id} on group chat {message.chat_id}."
            )
            AntiSpamController.createUser(user.id, message.chat_id)
            cls.sendMessage(message.chat_id, f"欢迎用户 {user.username} 加入群!")

    @classmethod
    @db.atomic()
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
        user_old = datetime.datetime.utcnow() - user.created_time
        if user_old >= datetime.timedelta(days=3):
            logger.info(f"User {user} too old, remove it from NewUser table.")
            AntiSpamController.removeUser(user.user_id)
            return

        # no message forwarding
        if message.forward_date:
            cls.deleteMessage(
                message.chat_id,
                message.message_id,
                message.from_user.id,
                message.from_user.username,
            )

        # no message with link and other entites
        if message.entities:
            deleteIt = False
            for entity in message.entities:
                if entity.type in [
                    telegram.constants.MESSAGEENTITY_EMAIL,
                    telegram.constants.MESSAGEENTITY_PHONE_NUMBER,
                    telegram.constants.MESSAGEENTITY_BOT_COMMAND,
                    telegram.constants.MESSAGEENTITY_TEXT_LINK,
                    telegram.constants.MESSAGEENTITY_URL,
                ]:
                    deleteIt = True
                    break
            if deleteIt:
                cls.deleteMessage(
                    message.chat_id,
                    message.message_id,
                    message.from_user.id,
                    message.from_user.username,
                )

        # message antispam
        keywords = AntiSpamController.loadKeywords()
        textScore = 0
        for keyword, score in keywords.items():
            if message.text.find(keyword) != -1:
                textScore += score
        if textScore >= 5:
            cls.deleteMessage(
                message.chat_id,
                message.message_id,
                message.from_user.id,
                message.from_user.username,
            )

    @classmethod
    @db.atomic()
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

    @classmethod
    def removeUser(cls, user_id: int):
        return AntispamNewUserDao.deleteUserByUserId(user_id)

    @classmethod
    def loadKeywords(cls) -> Dict[str, int]:
        keywords = {}
        for keyword in AntispamKeyWordDao.getAllKeywords():
            keyword: AntispamKeyWord
            keywords[keyword.keyword] = keyword.score
        return keywords

    @classmethod
    def addKeyword(cls, keyword: str, score: int):
        AntispamKeyWordDao.create(
            keyword=keyword,
            score=score,
        )
