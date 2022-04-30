import datetime

from src.dao.db import getConn


def on(dataclass, table: str):
    def wrapper(daoclass: BaseDao):
        daoclass.__DATACLASS__ = dataclass
        daoclass.__TABLE__ = table
        return daoclass

    return wrapper


class BaseDao(object):
    __DATACLASS__ = None
    __TABLE__ = None

    @classmethod
    def get_by_id(cls, id: int):
        cur = getConn().cursor()
        return cur.execute(
            f"select * from {cls.__TABLE__} where id=? limit 1", (id,)
        ).fetchone()

    @classmethod
    def update_by_id(cls, id: int, **kwargs):
        cur = getConn().cursor()
        updater = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
        cur.execute(f"update {cls.__TABLE__} set {updater} where id=?", (id,))
        getConn().commit()

    @classmethod
    def create(cls, **kwargs):
        cur = getConn().cursor()

        if "created_time" not in kwargs:
            kwargs["created_time"] = datetime.datetime.now().isoformat()
        if "modified_time" not in kwargs:
            kwargs["modified_time"] = datetime.datetime.now().isoformat()

        # column orders metter
        keys = ", ".join([k for k in kwargs.keys()])
        valuesPlaceholder = ", ".join(["?" for _ in kwargs.values()])
        values = tuple(kwargs.values())
        cur.execute(
            f"insert into {cls.__TABLE__} ({keys}) values ({valuesPlaceholder})",
            values,
        )
        getConn().commit()
