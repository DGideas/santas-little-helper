from src.model.antispam import KeyWord
from src.model.db import db
from src.model.santas import SantasOperationRecord, TgChatWatchList, TgUpdate


def doInit():
    db.connect()
    db.create_tables([KeyWord, TgChatWatchList, SantasOperationRecord, TgUpdate])


if __name__ == "__main__":
    doInit()
