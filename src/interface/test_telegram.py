from unittest import TestCase

from src.interface.telegram import TelegramBotClient


class TelegramBotClientTest(TestCase):
    def test_get_me(self):
        bot_info: dict = TelegramBotClient.getMe()
        self.assertTrue(bot_info["ok"])

        bot_info = bot_info["result"]
        self.assertTrue(bot_info["is_bot"])
        self.assertIn("username", bot_info)
        self.assertTrue(bot_info["can_join_groups"])

    def test_get_chat(self):
        resp: dict = TelegramBotClient.getChat("@bi_pt")
        self.assertTrue(resp["ok"])

        resp = resp["result"]
        self.assertIn("title", resp)
        self.assertIn("username", resp)
        self.assertIn("description", resp)
        self.assertIn("type", resp)
