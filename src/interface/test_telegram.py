from unittest import TestCase

from src.interface.telegram import TelegramBotClient


class TelegramBotClientTest(TestCase):
    def test_get_me(self):
        print(TelegramBotClient.getMe())
