
from enum import Enum, auto


# Define the events
class Event(Enum):

    # TDT Hardware Events
    TDT_CONNECT = auto()
    TDT_DISCONNECT = auto()


    # Initializing Server Events
    START_HARDWARE_SERVER = auto()
    SERVER_DISCONNECT = auto()
    PLAY_AUDIO = auto()
    STOP_AUDIO = auto()
    GAIN_VALUES_UPDATED = auto()


    STOP_LOADING = auto()


    ON_CLOSE = auto()