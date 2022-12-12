import heapq
import math

_DATA_FILE = "2022/data/12_hill_climbing_algorithm.txt"
_DEBUG = "/test/" in _DATA_FILE

_LOWEST_HEIGHT_CHAR = 'a'
_HIGHEST_HEIGHT_CHAR = 'z'
_SOURCE_CHAR = 'S'
_DEST_CHAR = 'E'

class Location:
  def __init__(self) -> None:
    self.x = -1
    self.y = -1
    self.height = 0
    self.visited = False
    self.distance = math.inf
    self.char = ''

  def __eq__(self, __o: "Location") -> bool:
    return (self.x, self.y) == (__o.x, __o.y)

  def __lt__(self, __o: "Location") -> bool:
    return self.distance < __o.distance
  
  def __hash__(self) -> int:
    return hash((self.x, self.y))
  
  def __str__(self) -> str:
    return "{x:d},{y:d} '{c:s}'".format(x = self.x, y = self.y, c = self.char)

def can_ascend(from_loc: Location, to_loc: Location) -> bool:
  return to_loc.height <= from_loc.height + 1

def get_neighbors(grid: list[list[Location]], grid_width: int, grid_height: int, location: Location) -> list[Location]:
  neighbors = []
  x = location.x
  y = location.y
  if (x > 0):
    neighbor = grid[x - 1][y]
    if can_ascend(neighbor, location):
      neighbors.append(neighbor)
  if (x < grid_width - 1):
    neighbor = grid[x + 1][y]
    if can_ascend(neighbor, location):
      neighbors.append(neighbor)
  if (y > 0):
    neighbor = grid[x][y - 1]
    if can_ascend(neighbor, location):
      neighbors.append(neighbor)
  if (y < grid_height - 1):
    neighbor = grid[x][y + 1]
    if can_ascend(neighbor, location):
      neighbors.append(neighbor)

  return neighbors

lines = []
with open(_DATA_FILE, "r") as inputfile:
  lines = [line.strip() for line in inputfile]

grid_height = len(lines)
grid_width = len(lines[0])
print("h:{h:d} w:{w:d}".format(h = grid_height, w = grid_width))
grid = [[Location() for y in range(grid_height)] for x in range(grid_width)]

source: Location
destination: Location

# Build the topography.
y = 0
for row in lines:
  x = 0
  for char in row:
    if not char.isalpha():
      continue

    location = grid[x][y]
    location.x = x
    location.y = y
    location.char = char
    if char == _SOURCE_CHAR:
      location.height = 0
      source = location
    elif char == _DEST_CHAR:
      location.height = 25
      destination = location
    else:
      location.height = ord(char) - ord(_LOWEST_HEIGHT_CHAR)
    print("{d:02d} ".format(d = location.height), end='')
    x += 1
  print()
  y += 1

print("Src: {s:s}".format(s = str(source)))
print("Dst: {d:s}".format(d = str(destination)))

# Dijkstra's with a minheap.
distance_heap = []

current = destination
current.distance = 0
shortest_set = set()
in_heap = set()

no_path = False
found_source = False

# Do the Dijkstra's.
while not found_source:
  shortest_set.add(current)
  if _DEBUG: print("Current: {c:s}".format(c = str(current)))
  neighbors = get_neighbors(grid, grid_width, grid_height, current)
  if _DEBUG: print("Neighbors: \n  {n:s}".format(
    n = '\n  '.join([str(n) for n in neighbors])
  ))
  for neighbor in neighbors:
    if (neighbor not in shortest_set):
      distance = current.distance + 1
      neighbor.distance = min(neighbor.distance, distance)

      if (neighbor not in in_heap):
        heapq.heappush(distance_heap, (neighbor.distance, neighbor))
        in_heap.add(neighbor)

  heapq.heapify(distance_heap)
  if not distance_heap:
    no_path = True
    break
  current = heapq.heappop(distance_heap)[1]
  if current.height == 0:
    found_source = True
    break
  print("Heap size:", len(distance_heap), end='\r')

if _DEBUG:
  for y in range(grid_height):
    for x in range(grid_width):
      if grid[x][y].distance == math.inf:
        print("in ", end='')
      else:
        print("{d:02d} ".format(d = grid[x][y].distance), end='')
    print()

print()

if (no_path):
  print("No path!")
else:
  print("Shortest distance:", current.distance)