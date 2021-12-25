from enum import Enum, auto

_DATA_FILE = "2021/data/test/25_sea_cucumber.txt"

class Cucumber(Enum):
  NONE = auto()
  EAST = auto(),
  SOUTH = auto(),

_STR_TO_CUCUMBER = {
  '.': Cucumber.NONE,
  '>': Cucumber.EAST,
  'v': Cucumber.SOUTH,
  }

_CUCUMBER_TO_STR = {d: c for c, d in _STR_TO_CUCUMBER.items()}

# Positive-x is east, positive-y is south.
_MOTION_VECTOR = {
  Cucumber.NONE: (0, 0),
  Cucumber.EAST: (1, 0),
  Cucumber.SOUTH: (0, 1),
  }

class Grid:
  def __init__(self, grid: list[list[Cucumber]]) -> None:
    self.height = len(grid)
    self.width = len(grid[0])
    self.grid = grid
  
  def _next_position(coord: tuple[int, int]) -> tuple[int, int]:
    pass


if __name__ == '__main__':
  with open(_DATA_FILE, "r") as input:
    lines = input.readlines()