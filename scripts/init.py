from src.model.antispam import KeyWord
from src.model.db import db


def doInit():
    db.connect()
    db.create_tables([KeyWord])
