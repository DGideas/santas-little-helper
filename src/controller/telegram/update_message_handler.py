from telegram import ChatMemberUpdated, Message

from ..engine.antispam_engine import AntispamEngine


class TgUpdateMessageHandler(object):
    @classmethod
    def newChatUserHandler(cls, msg: Message):
        AntispamEngine.doNewChatUser(msg)

    @classmethod
    def messageHandler(cls, msg: Message):
        AntispamEngine.doMessage(msg)

    @classmethod
    def myChatMemberHandler(cls, cmu: ChatMemberUpdated):
        AntispamEngine.doChatMemberUpdated(cmu)
