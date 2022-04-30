import datetime

from peewee import DateTimeField, IntegerField, Model, SmallIntegerField, TextField

from src.data.enums import AntispamWatchGroupStatus

from .db import db


class AntispamKeyWord(Model):
    id = IntegerField(primary_key=True)
    keyword = TextField(null=False, unique=True)
    score = IntegerField(null=False, default=0)
    created_time = DateTimeField(default=datetime.datetime.utcnow)
    modified_time = DateTimeField(default=datetime.datetime.utcnow)

    def save(self, force_insert=False, only=None):
        self.modified_time = datetime.datetime.utcnow()
        return super().save(force_insert, only)

    class Meta:
        database = db


class AntispamWatchGroup(Model):
    id = IntegerField(primary_key=True)
    chat_id = IntegerField(null=False, unique=True)
    status = SmallIntegerField(
        choices=AntispamWatchGroupStatus,
        default=AntispamWatchGroupStatus.ST_VALID,
        null=False,
        index=True,
    )
    config = TextField(default="{}", null=False, help_text="JSON 格式")
    created_time = DateTimeField(default=datetime.datetime.utcnow)
    modified_time = DateTimeField(default=datetime.datetime.utcnow)

    def save(self, force_insert=False, only=None):
        self.modified_time = datetime.datetime.utcnow()
        return super().save(force_insert, only)

    class Meta:
        database = db


class AntispamNewUser(Model):
    id = IntegerField(primary_key=True)
    user_id = IntegerField(null=False)
    chat_id = IntegerField(null=False)
    created_time = DateTimeField(default=datetime.datetime.utcnow)
    modified_time = DateTimeField(default=datetime.datetime.utcnow)

    def save(self, force_insert=False, only=None):
        self.modified_time = datetime.datetime.utcnow()
        return super().save(force_insert, only)

    class Meta:
        database = db
