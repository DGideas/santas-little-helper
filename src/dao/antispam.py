from dataclasses import dataclass

from src.dao.base_dao import BaseDao, on


@dataclass
class KeyWord:
    id: int
    keyword: str
    created_time: str
    modified_time: str


@on(KeyWord, table="antispam_keyword")
class KeyWordDao(BaseDao):
    @classmethod
    def list_keyword(cls):
        ...


if __name__ == "__main__":
    print(KeyWordDao.create(keyword="你好", score=0))
    print(KeyWordDao.get_by_id(1))
