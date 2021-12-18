import math
import heapq

_DATA_FILE = "2021/data/15_chiton.txt"
_REPEATS = 5
_MAX_RISK = 9

class Location:
  def __init__(self) -> None:
    self.x = -1
    self.y = -1
    self.risk = 0
    self.visited = False
    self.distance = math.inf

  def __eq__(self, __o: "Location") -> bool:
    return (self.x, self.y) == (__o.x, __o.y)

  def __lt__(self, __o: "Location") -> bool:
    return self.distance < __o.distance
  
  def __hash__(self) -> int:
    return hash((self.x, self.y))
  

# Risk wraps back to 1, not 0 so we can't just use mod.
def wrap_risk(risk: int) -> int:
  return ((risk - 1) % _MAX_RISK) + 1

def get_neighbors(grid: list[list[Location]], grid_width: int, grid_height: int, location: Location) -> list[Location]:
  neighbors = []
  x = location.x
  y = location.y
  if (x > 0):
    neighbors.append(grid[x - 1][y])
  if (x < grid_width - 1):
    neighbors.append(grid[x + 1][y])
  if (y > 0):
    neighbors.append(grid[x][y - 1])
  if (y < grid_width - 1):
    neighbors.append(grid[x][y + 1])

  return neighbors

lines = []
with open(_DATA_FILE, "r") as input:
  lines = input.readlines()

cell_height = len(lines)
cell_width = len(lines[0].strip())
grid_height = cell_height * _REPEATS
grid_width = cell_width * _REPEATS
grid = [[Location() for y in range(grid_height)] for x in range(grid_width)]

# Dijkstra's with a minheap.
distance_heap = []

y = 0
for row in lines:
  x = 0
  for char in row:
    if (not char.isdigit()):
      continue

    risk = int(char)

    for cell_x in range(_REPEATS):
      for cell_y in range(_REPEATS):
        grid_x = x + (cell_width * cell_x)
        grid_y = y + (cell_height * cell_y)
        location = grid[grid_x][grid_y]
        location.x = grid_x
        location.y = grid_y
        location.risk = wrap_risk(risk + cell_x + cell_y)

    x += 1
  y += 1

current = grid[0][0]
current.distance = 0
destination = grid[grid_width - 1][grid_height - 1]
shortest_set = set()
in_heap = set()

# Do the Dijkstra's.
while destination.distance == math.inf:
  shortest_set.add(current)
  for neighbor in get_neighbors(grid, grid_width, grid_height, current):
    if (neighbor not in shortest_set):
      distance = current.distance + neighbor.risk
      neighbor.distance = min(neighbor.distance, distance)

      if (neighbor not in in_heap):
        heapq.heappush(distance_heap, (neighbor.distance, neighbor))
        in_heap.add(neighbor)


  heapq.heapify(distance_heap)
  current = heapq.heappop(distance_heap)[1]
  if (current == destination):
    break
  print("Heap size:", len(distance_heap), end='\r')

print()
print("Shortest distance:", destination.distance)