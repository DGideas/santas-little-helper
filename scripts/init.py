from src.model.antispam import AntispamKeyWord, AntispamNewUser, AntispamWatchGroup
from src.model.db import db
from src.model.santas import SantasOperationRecord, TgChatWatchList, TgUpdate

KEYWORDS = {
    "赚": 2,
    "棋牌": 5,
    "作弊": 1,
    "活动": 2,
    "惊喜": 1,
    "楼凤": 5,
    "本地": 1,
    "学生": 1,
    "在校": 1,
    "兼职": 4,
    "Q": 1,
    "q": 1,
}


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

    if AntispamKeyWord.select().count() == 0:
        # initialize keyword list
        for keyword, score in KEYWORDS.items():
            AntispamKeyWord.create(
                keyword=keyword,
                score=score,
            )


if __name__ == "__main__":
    doInit()
