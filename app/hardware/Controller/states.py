

from enum import Enum, auto



# Define the states using an enumeration
class State(Enum):
    IDLE = auto()

    TDT_INITIALIZING = auto()

    SERVER_INITIALIZING = auto()

    FULLY_RUNNING = auto() # once both tdt and controller are connected

    SHUTTING_DOWN = auto()


