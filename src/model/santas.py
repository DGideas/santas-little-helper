import datetime

from peewee import CharField, DateTimeField, IntegerField, Model

from src.data.enums import SantasWatchlistStatus
from src.model.db import db


class WatchList(Model):
    id = IntegerField(primary_key=True)
    chat_id = CharField(max_length=128, index=True)
    status = IntegerField(
        choices=SantasWatchlistStatus,
        default=SantasWatchlistStatus.ST_VALID,
        null=False,
    )
    created_time = DateTimeField(default=datetime.datetime.utcnow)
    modified_time = DateTimeField(default=datetime.datetime.utcnow)

    def save(self, force_insert=False, only=None):
        self.modified_time = datetime.datetime.utcnow()
        return super().save(force_insert, only)

    class Meta:
        database = db
