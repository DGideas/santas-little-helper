import peewee
from peewee import Model


def on(modelClass: object):
    def wraps(originDao):
        setattr(originDao, "__MODEL_CLASS__", modelClass)
        return originDao

    return wraps


class BaseDao(object):
    __MODEL_CLASS__: Model = None

    @classmethod
    def create(cls, **kwargs):
        return cls.__MODEL_CLASS__.create(**kwargs)

    @classmethod
    def getByIdOrNull(cls, id: int):
        try:
            cls.__MODEL_CLASS__.select().where(cls.__MODEL_CLASS__.id == id).get()
        except peewee.DoesNotExist:
            return None

    @classmethod
    def getByIdOrRaise(cls, id: int):
        return cls.__MODEL_CLASS__.select().where(cls.__MODEL_CLASS__.id == id).get()

    @classmethod
    def updateById(cls, id: int, **updater):
        return (
            cls.__MODEL_CLASS__.select()
            .where(cls.__MODEL_CLASS__.id == id)
            .update(**updater)
        )
