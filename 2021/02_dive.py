from enum import Enum, auto

_DATA_FILE = "2021/data/02_dive.txt"

class Direction(Enum):
  NONE = auto()
  FORWARD = auto()
  DOWN = auto()
  UP = auto()

_DIRECTION_PARSE = {"forward" : Direction.FORWARD, "down" : Direction.DOWN, "up" : Direction.UP}

# A command for the submarine.
class Command:
  def __init__(self, string) -> None:
    self.direction = Direction.NONE
    self.magnitude = 0
  
    # Parse the command from a string such as "forward 3".
    command_strings = string.strip().split(' ')
    if (command_strings[0] in _DIRECTION_PARSE):
      self.direction = _DIRECTION_PARSE[command_strings[0]]
    if (command_strings[1].isdigit()):
      self.magnitude = int(command_strings[1])
  
  def __repr__(self) -> str:
    return "{:s} {:d}".format(self.direction, self.magnitude)

class Submarine:
  def __init__(self) -> None:
    self.aim = 0
    self.horizontal = 0
    self.depth = 0
  
  def issue_command(self, command: Command) -> None:
    if (command.direction == Direction.FORWARD):
      self.horizontal += command.magnitude
      self.depth += self.aim * command.magnitude
    elif (command.direction == Direction.DOWN):
      self.aim += command.magnitude
    elif (command.direction == Direction.UP):
      self.aim -= command.magnitude

# Read the input data into a list of commands.
commands = []
with open(_DATA_FILE, "r") as input:
  commands = list(map(lambda s: Command(s), input.readlines()))

sub = Submarine()
for command in commands:
  sub.issue_command(command)

print("Horizontal:\t{:d}\nDepth:    \t{:d}\nMultiplied:\t{:d}".format(sub.horizontal, sub.depth, sub.horizontal * sub.depth))