from enum import Enum, auto

_DATA_FILE = "2021/data/test/02_dive.txt"

class Direction(Enum):
  NONE = auto()
  FORWARD = auto()
  DOWN = auto()
  UP = auto()

_DIRECTION_PARSE = {"forward" : Direction.FORWARD, "down" : Direction.DOWN, "up" : Direction.UP}

# A command for the submarine.
class Command:
  direction = Direction.NONE
  distance = 0
  
  def __init__(self, string) -> None:
      # Parse the command from a string such as "forward 3".
      command_strings = string.strip().split(' ')
      if (command_strings[0] in _DIRECTION_PARSE):
        self.direction = _DIRECTION_PARSE[command_strings[0]]
      if (command_strings[1].isdigit()):
        self.distance = int(command_strings[1])
  
  def __repr__(self) -> str:
      return "{:s} {:d}".format(self.direction, self.distance)

# Read the input data into a list of commands.
commands = []
with open(_DATA_FILE, "r") as input:
  commands = list(map(lambda s: Command(s), input.readlines()))

print(commands)