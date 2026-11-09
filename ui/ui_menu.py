from enum import Enum, auto


class UIMenu(Enum):
    MAIN = auto()
    SENDER = auto()
    SENDER_FILE = auto()
    SENDER_STREAM = auto()
    RECEIVER = auto()
    RECEIVER_FILE = auto()
    RECEIVER_STREAM = auto()
    EXIT = auto()
