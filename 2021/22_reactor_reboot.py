_DATA_FILE = "2021/data/22_reactor_reboot.txt"
_COMMAND_DELIMITER = ' '
_ON_COMMAND = "on"
_COORD_DELIMITER = ','
_COORD_OFFSET = 2
_RANGE_DELIMITER = '..'
_GRID_MIN = -50
_GRID_MAX = 50

class BoundingBox:
  def __init__(self, range: list[range]) -> None:
    self.range = range

  def intersection(self, other: "BoundingBox") -> list[range]:
    return BoundingBox([
      range(max(s[0], o[0]), min(s[-1], o[-1])+1)
        for (s, o) in zip(self.range, other.range)
    ])

  def __repr__(self) -> str:
    return "x={:s} y={:s} z={:s}".format(
      str(self.range[0]), str(self.range[1]), str(self.range[2]))
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
    return "{:s} {:s}".format("ON" if self.on else "off", self.bbox)

with open(_DATA_FILE, "r") as input:
  lines = input.readlines()

commands = [Command(line.strip()) for line in lines]
for command in commands:
  print(command)
