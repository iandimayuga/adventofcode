import numpy

_DATA_FILE = "2021/data/09_smoke_basin.txt"
_MAX_HEIGHT = 9

class Location:
  def __init__(self) -> None:
    self.x = -1
    self.y = -1
    self.height = 0
    self.neighbors = []
    self.visited = False
  
  def is_low(self) -> bool:
    for neighbor in self.neighbors:
      if (neighbor.height <= self.height):
        return False
    return True

  def risk_level(self) -> int:
    return self.height + 1
  
  def basin_size(self) -> int:
    if (self.visited):
      return 0
    if (self.height >= _MAX_HEIGHT):
      return 0
    self.visited = True
    basin_size = 1
    for neighbor in self.neighbors:
      if (neighbor.height < _MAX_HEIGHT):
        basin_size += neighbor.basin_size()
    return basin_size

lines = []
with open(_DATA_FILE, "r") as input:
  lines = input.readlines()

height = len(lines)
width = len(lines[0].strip())
grid = [[Location() for y in range(height)] for x in range(width)]

y = 0
for row in lines:
  x = 0
  for char in row:
    if (not char.isdigit()):
      continue

    location = grid[x][y]
    location.x = x
    location.y = y
    location.height = int(char)
    # Add the two neighbors that come after this location.
    # The previous two neighbors would have already added this one.
    if (x < width - 1):
      right = grid[x + 1][y]
      location.neighbors.append(right)
      right.neighbors.append(location)
    if (y < height - 1):
      bottom = grid[x][y + 1]
      location.neighbors.append(bottom)
      bottom.neighbors.append(location)

    x += 1
  y += 1

basins = []
for y in range(height):
  for x in range(width):
    basin_size = grid[x][y].basin_size()
    if (basin_size > 0):
      basins.append(basin_size)

basins.sort()
print(basins[-3:])
print(numpy.prod(basins[-3:]))