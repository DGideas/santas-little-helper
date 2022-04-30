from telegram import Message


class TgUpdateMessageHandler(object):
    @classmethod
    def messageHandler(cls, msg: Message):
        ...
