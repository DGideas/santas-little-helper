import requests


class BaseClient(object):
    # TODO Error Handling
    BASE_URL: str = ""

    @classmethod
    def get(cls, endpoint: str, param: dict = {}) -> dict:
        return requests.get(f"{cls.BASE_URL}{endpoint}", params=param).json()

    @classmethod
    def post(cls, endpoint: str, json: dict = {}) -> dict:
        return requests.post(f"{cls.BASE_URL}{endpoint}", json=json).json()
