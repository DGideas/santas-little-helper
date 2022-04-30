import datetime

from peewee import DateTimeField, IntegerField, Model, TextField

from .db import db


class KeyWord(Model):
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
