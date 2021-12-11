_DATA_FILE = "2021/data/09_smoke_basin.txt"

class Location:
  def __init__(self) -> None:
    self.x = -1
    self.y = -1
    self.height = 0
    self.neighbors = []
  
  def is_low(self) -> bool:
    for neighbor in self.neighbors:
      if (neighbor.height <= self.height):
        return False
    return True

  def risk_level(self) -> int:
    return self.height + 1

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
    # Add the two neighbors that come after this octopus.
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

total_risk = 0
for y in range(height):
  for x in range(width):
    if (grid[x][y].is_low()):
      total_risk += grid[x][y].risk_level()

print("Total risk:", total_risk)