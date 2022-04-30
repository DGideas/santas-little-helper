from src.model.antispam import KeyWord

from .base_dao import BaseDao, on


@on(KeyWord)
class KeyWordDao(BaseDao):
    ...
