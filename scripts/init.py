from src.model.antispam import AntispamKeyWord, AntispamNewUser, AntispamWatchGroup
from src.model.db import db
from src.model.santas import SantasOperationRecord, TgChatWatchList, TgUpdate


def doInit():
    db.connect()
    db.create_tables(
        [
            AntispamKeyWord,
            AntispamNewUser,
            AntispamWatchGroup,
            TgChatWatchList,
            SantasOperationRecord,
            TgUpdate,
        ]
    )


if __name__ == "__main__":
    doInit()
