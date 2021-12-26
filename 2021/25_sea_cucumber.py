from enum import Enum, auto

_DATA_FILE = "2021/data/25_sea_cucumber.txt"

class Cucumber(Enum):
  NONE = auto()
  EAST = auto(),
  SOUTH = auto(),

  def __bool__(self) -> bool:
    return self != Cucumber.NONE

_STR_TO_CUCUMBER = {
  '.': Cucumber.NONE,
  '>': Cucumber.EAST,
  'v': Cucumber.SOUTH,
  }

_CUCUMBER_TO_STR = {d: c for c, d in _STR_TO_CUCUMBER.items()}

# Row-major. Positive directions are (south, east)
_MOTION_VECTOR = {
  Cucumber.NONE: (0, 0),
  Cucumber.EAST: (0, 1),
  Cucumber.SOUTH: (1, 0),
  }

_HERD_ORDER = [Cucumber.EAST, Cucumber.SOUTH]

class Trench:
  def __init__(self, grid: list[list[Cucumber]]) -> None:
    self.grid = grid
    self.height = len(grid)
    self.width = len(grid[0])
    self.locked = False

  def __repr__(self) -> str:
    grid_print = '\n'.join([''.join([_CUCUMBER_TO_STR[c] for c in row]) for row in self.grid])
    return grid_print

def get_next_position(trench: Trench, position: tuple[int, int]) -> tuple[int, int]:
  cucumber = get_cucumber(trench, position)
  direction = _MOTION_VECTOR[cucumber]
  bounds = (trench.height, trench.width)
  unbounded_position = tuple(map(sum, zip(position, direction)))
  # Mod the position to wrap around the bounds.
  return tuple(map(lambda u, b: u % b, unbounded_position, bounds))

def get_cucumber(trench: Trench, position: tuple[int, int]) -> Cucumber:
  return trench.grid[position[0]][position[1]]

def set_cucumber(trench: Trench, position: tuple[int, int], cucumber: Cucumber) -> None:
  trench.grid[position[0]][position[1]] = cucumber

def iterate(trench: Trench) -> "Trench":
  anybody_moved = False
  prev_trench = trench
  for herd in _HERD_ORDER:
    next_trench = Trench(
      [[Cucumber.NONE for x in range(trench.width)] for y in range(trench.height)],
      )
    for y in range(trench.height):
      for x in range(trench.width):
        position = (y, x)
        cucumber = get_cucumber(prev_trench, position)
        if cucumber == Cucumber.NONE:
          continue
        elif cucumber == herd:
          # Cucumber is in the currently-moving herd.
          next_position = get_next_position(prev_trench, position)
          if get_cucumber(prev_trench, next_position):
            # There is a cucumber in the next position, so this cucumber cannot move.
            set_cucumber(next_trench, position, cucumber)
          else:
            set_cucumber(next_trench, next_position, cucumber)
            anybody_moved = True
        else:
          # Cucumber is not in the same herd, so stays put.
          set_cucumber(next_trench, position, cucumber)
    prev_trench = next_trench

  next_trench.locked = not anybody_moved
  return next_trench

def iteration_header(iteration: int, locked: bool) -> str:
  return "Iteration {:d}{:s}".format(
    iteration,
    " (LOCKED!)" if locked else ""
  )


if __name__ == '__main__':
  with open(_DATA_FILE, "r") as input:
    lines = input.readlines()

  trench = Trench(
    [[_STR_TO_CUCUMBER[c] for c in line.strip()] for line in lines],
  )

  iteration = 0
  while True:
    print(iteration_header(iteration, trench.locked))
    print(trench)
    if (trench.locked):
      break
    trench = iterate(trench)
    iteration += 1