_DATA_FILE = "2021/data/11_dumbo_octopus.txt"
_WIDTH = 10
_HEIGHT = 10
_ITERATIONS = 500
_FLASH_LEVEL = 10

class Octopus:
  def __init__(self) -> None:
    self.x = -1
    self.y = -1
    self.level = 0
    self.flashed = False
    self.neighbors = []

  # Increments the energy level and returns the total number of resultant flashes.
  def increment(self) -> int:
    self.level += 1
    if (self.level >= _FLASH_LEVEL and not self.flashed):
      return self.flash()
    return 0
    
  # Flashes nearby octopuses, returning the total number of resultant flashes.
  def flash(self) -> int:
    self.flashed = True
    flashes = 1
    for neighbor in self.neighbors:
      flashes += neighbor.increment()
    return flashes
  
  def reset(self) -> None:
    if (self.flashed):
      self.level = 0
    self.flashed = False

grid = [[Octopus() for y in range(_HEIGHT)] for x in range(_WIDTH)]

with open(_DATA_FILE, "r") as input:
  y = 0
  for row in input.readlines():
    x = 0
    for char in row:
      if (not char.isdigit()):
        continue

      octopus = grid[x][y]
      octopus.x = x
      octopus.y = y
      octopus.level = int(char)
      # Add the four neighbors that come after this octopus.
      # The previous four neighbors would have already added this one.
      if (x < _WIDTH - 1):
        right = grid[x + 1][y]
        octopus.neighbors.append(right)
        right.neighbors.append(octopus)
      if (y < _HEIGHT - 1):
        bottom = grid[x][y + 1]
        octopus.neighbors.append(bottom)
        bottom.neighbors.append(octopus)
      if (x < _WIDTH - 1 and y < _HEIGHT - 1):
        bottom_right = grid[x + 1][y + 1]
        octopus.neighbors.append(bottom_right)
        bottom_right.neighbors.append(octopus)
      if (x > 0 and y < _HEIGHT - 1):
        bottom_left = grid[x - 1][y + 1]
        octopus.neighbors.append(bottom_left)
        bottom_left.neighbors.append(octopus)

      x += 1
    y += 1
    
total_flashes = 0
all_flash_iterations = []
for i in range(_ITERATIONS):
  for y in range(_HEIGHT):
    for x in range(_WIDTH):
      print(grid[x][y].level, end="")
    print()
  print()
  print("*** ITERATION {:d} ***".format(i))
  flashes_this_iteration = 0
  for y in range(_HEIGHT):
    for x in range(_WIDTH):
      flashes = grid[x][y].increment()
      flashes_this_iteration += flashes
      total_flashes += flashes
  for y in range(_HEIGHT):
    for x in range(_WIDTH):
      grid[x][y].reset()
  if (flashes_this_iteration == _WIDTH * _HEIGHT):
    all_flash_iterations.append(i)

for y in range(_HEIGHT):
  for x in range(_WIDTH):
    print(grid[x][y].level, end="")
  print()
print()
print("Total flashes in {:d} iterations: {:d}".format(_ITERATIONS, total_flashes))
print("All octopuses flashed in iterations", all_flash_iterations)