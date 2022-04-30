from enum import Enum, IntEnum


class TelegramUpdateType(IntEnum):
    """
    https://core.telegram.org/bots/api#update
    """

    TYPE_MESSAGE = 1
    TYPE_EDITED_MESSAGE = 2
    TYPE_CHANNEL_POST = 3  # TBI
    TYPE_EDITED_CHANNEL_POST = 4  # TBI
    TYPE_INLINE_QUERY = 5  # TBI
    TYPE_CHOSEN_INLINE_RESULT = 6  # TBI
    TYPE_CALLBACK_QUERY = 7  # TBI
    TYPE_SHIPPING_QUERY = 8  # TBI
    TYPE_PRE_CHECKOUT_QUERY = 9  # TBI
    TYPE_POLL = 10  # TBI
    TYPE_POLL_ANSWER = 11  # TBI
    TYPE_MY_CHAT_MEMBER = 12
    TYPE_CHAT_MEMBER = 13
    TYPE_CHAT_JOIN_REQUEST = 14

    @classmethod
    def isSupportedType(cls, val: "TelegramUpdateType") -> bool:
        if val in [
            cls.TYPE_MESSAGE,
            cls.TYPE_EDITED_MESSAGE,
            cls.TYPE_MY_CHAT_MEMBER,
            cls.TYPE_CHAT_MEMBER,
            cls.TYPE_CHAT_JOIN_REQUEST,
        ]:
            return True
        return False


class SantasOperationEngine(Enum):
    ENGINE_MANUAL = "manual"
    ENGINE_ANTISPAM = "antispam"


class SantasWatchlistStatus(IntEnum):
    ST_VALID = 0
    ST_INVALID = 1
