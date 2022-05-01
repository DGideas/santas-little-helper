from src.controller.telegram.updater import TelegramUpdateMessageController


def main():
    while True:
        TelegramUpdateMessageController.getTelegramUpdate()
