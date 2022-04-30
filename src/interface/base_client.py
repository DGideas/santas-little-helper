import requests


class BaseClient(object):
    BASE_URL: str = ""

    @classmethod
    def get(cls, endpoint: str, args: dict = {}) -> requests.Response:
        return requests.get(f"{cls.BASE_URL}{endpoint}", params=args)
