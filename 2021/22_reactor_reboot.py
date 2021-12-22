from multiprocessing import Pool
from itertools import product
import math

_DATA_FILE = "2021/data/22_reactor_reboot.txt"
_COMMAND_DELIMITER = ' '
_ON_COMMAND = "on"
_COORD_DELIMITER = ','
_COORD_OFFSET = 2
_RANGE_DELIMITER = '..'
_GRID_MIN = -50
_GRID_MAX = 50
_CELL_SIZE = 10000
_POOL_SIZE = 16

class BoundingBox:
  def __init__(self, intervals: list[range]) -> None:
    self.intervals = intervals

  def intersection(self, other: "BoundingBox") -> list[range]:
    if (self and other):
      return BoundingBox([
        range(max(s[0], o[0]), min(s[-1], o[-1])+1)
          for (s, o) in zip(self.intervals, other.intervals)
      ])
    
    return BoundingBox(range(0) for i in range(3))

  def __bool__(self) -> bool:
    return all(self.intervals)

  def contains(self, point: list[int]) -> bool:
    return all([interval.__contains__(coordinate)
      for (interval, coordinate) in zip(self.intervals, point)])

  def __repr__(self) -> str:
    return "x={:s}\ty={:s}\tz={:s}".format(
      str(self.intervals[0]), str(self.intervals[1]), str(self.intervals[2]))
  def __format__(self, __format_spec: str) -> str:
    return self.__repr__()

class Command:
  def __init__(self, line: str) -> None:
    (command_string, coords) = tuple(line.split(_COMMAND_DELIMITER))
    (x_coord, y_coord, z_coord) = tuple(coords.split(_COORD_DELIMITER))
    (x_low, x_high) = tuple(x_coord[_COORD_OFFSET:].split(_RANGE_DELIMITER))
    (y_low, y_high) = tuple(y_coord[_COORD_OFFSET:].split(_RANGE_DELIMITER))
    (z_low, z_high) = tuple(z_coord[_COORD_OFFSET:].split(_RANGE_DELIMITER))

    self.on = (command_string == _ON_COMMAND)
    self.bbox = BoundingBox([
      range(int(x_low), int(x_high) + 1),
      range(int(y_low), int(y_high) + 1),
      range(int(z_low), int(z_high) + 1),
    ])

  def __repr__(self) -> str:
    return "{:s}\t{:s}".format("ON" if self.on else "off", self.bbox)

class CellArgs:
  def __init__(self, commands: list[Command], cell_min: list[int], cell_max: list[int]) -> None:
    self.commands = commands
    self.cell_min = cell_min
    self.cell_max = cell_max

def process_cell(args: CellArgs) -> int:
  commands = args.commands
  cell_min = args.cell_min
  cell_max = args.cell_max

  print("Processing cell", str(cell_min), str(cell_max))

  bounds = [set() for i in range(3)]
  cell = BoundingBox([range(min, max) for (min, max) in zip(cell_min, cell_max)])
  for command in commands:
    # print(command)
    constrained_bbox = command.bbox.intersection(cell)
    if (constrained_bbox):
      for (bound, interval) in zip(bounds, constrained_bbox.intervals):
        bound.add(interval.start)
        bound.add(interval.stop)

  x_bounds = sorted(bounds[0])
  y_bounds = sorted(bounds[1])
  z_bounds = sorted(bounds[2])

  total = 0
  for i in range(len(x_bounds) - 1):
    for j in range(len(y_bounds) - 1):
      for k in range(len(z_bounds) - 1):
        (x, y, z) = (x_bounds[i], y_bounds[j], z_bounds[k])
        volume = (x_bounds[i + 1] - x) * (y_bounds[j + 1] - y) * (z_bounds[k + 1] - z)
        # print("Volume of {:d},{:d},{:d}\tto {:d},{:d},{:d}\tis {:d}".format(
        #   x,y,z,x_bounds[i+1],y_bounds[j+1],z_bounds[k+1],volume
        # ))
        for command in reversed(commands):
          if (command.bbox.contains([x,y,z])):
            if (command.on):
              total += volume
            break

  return total

if __name__ == '__main__':
  with open(_DATA_FILE, "r") as input:
    lines = input.readlines()

  commands = [Command(line.strip()) for line in lines]
  # print(process_cell(CellArgs(commands, _GRID_MIN, _GRID_MAX + 1)))

  grid_min = [math.inf]*3
  grid_max = [-math.inf]*3

  for command in commands:
    for i in range(3):
      grid_min[i] = min(grid_min[i], command.bbox.intervals[i].start)
      grid_max[i] = max(grid_max[i], command.bbox.intervals[i].stop)
  
  print(grid_min)
  print(grid_max)

  cells = []
  for cell_x in range(grid_min[0], grid_max[0], _CELL_SIZE):
    for cell_y in range(grid_min[1], grid_max[1], _CELL_SIZE):
      for cell_z in range(grid_min[2], grid_max[2], _CELL_SIZE):
        cell_min = [cell_x, cell_y, cell_z]
        cell_max = [cell_x + _CELL_SIZE, cell_y + _CELL_SIZE, cell_z + _CELL_SIZE]
        print("Creating cell", cell_min, cell_max)
        cells.append(CellArgs(commands, cell_min, cell_max))

  with Pool(_POOL_SIZE) as p:
      print(sum(p.map(process_cell, cells)))