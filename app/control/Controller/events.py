from enum import Enum, auto


# Define the events
class Event(Enum):
    ON_CLOSE = auto()

    CONNECT_HARDWARE = auto()
    DISCONNECT_HARDWARE = auto()

    PLAY_AUDIO = auto()
    STOP_AUDIO = auto()