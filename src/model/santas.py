import datetime

from peewee import CharField, DateTimeField, IntegerField, Model, TextField

from src.data.enums import SantasWatchlistStatus, TelegramUpdateType
from src.model.db import db


class TgUpdate(Model):
    id = IntegerField(primary_key=True)
    update_id = IntegerField(null=False, unique=True, index=True)
    update_type = IntegerField(choices=TelegramUpdateType, null=False, index=True)
    raw_message = TextField(default="")
    created_time = DateTimeField(default=datetime.datetime.utcnow)
    modified_time = DateTimeField(default=datetime.datetime.utcnow)

    def save(self, force_insert=False, only=None):
        self.modified_time = datetime.datetime.utcnow()
        return super().save(force_insert, only)

    class Meta:
        database = db


class SantasOperationRecord(Model):
    id = IntegerField(primary_key=True)
    engine = CharField(max_length=128, default="manual", null=False, index=True)
    operation_type = CharField(max_length=128, null=False)
    target = TextField(default="", null=False)
    message = TextField(default="", null=False)
    extra_info = TextField(default="{}", help_text="JSON 格式", null=False)
    created_time = DateTimeField(default=datetime.datetime.utcnow)
    modified_time = DateTimeField(default=datetime.datetime.utcnow)

    def save(self, force_insert=False, only=None):
        self.modified_time = datetime.datetime.utcnow()
        return super().save(force_insert, only)

    class Meta:
        database = db


class TgChatWatchList(Model):
    id = IntegerField(primary_key=True)
    chat_id = CharField(max_length=128, index=True)
    config = TextField(default="{}", help_text="JSON 格式")
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
