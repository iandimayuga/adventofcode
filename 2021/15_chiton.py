import math
from functools import total_ordering
import heapq

_DATA_FILE = "2021/data/15_chiton.txt"

@total_ordering
class Location:
  def __init__(self) -> None:
    self.x = -1
    self.y = -1
    self.risk = 0
    self.neighbors = []
    self.visited = False
    self.distance = math.inf

  def __eq__(self, __o: "Location") -> bool:
    return self.distance == __o.distance
  
  def __lt__(self, __o: "Location") -> bool:
    return self.distance < __o.distance

lines = []
with open(_DATA_FILE, "r") as input:
  lines = input.readlines()

height = len(lines)
width = len(lines[0].strip())
grid = [[Location() for y in range(height)] for x in range(width)]

# Dijkstra's with a minheap.
shortest_heap = []

y = 0
for row in lines:
  x = 0
  for char in row:
    if (not char.isdigit()):
      continue

    location = grid[x][y]
    location.x = x
    location.y = y
    location.risk = int(char)
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

    if (x > 0 or y > 0):
      heapq.heappush(shortest_heap, location)

    x += 1
  y += 1

current = grid[0][0]
current.distance = 0
destination = grid[width - 1][height - 1]

# Do the Dijkstra's.
while destination.distance == math.inf and shortest_heap:
  for neighbor in current.neighbors:
    distance = current.distance + neighbor.risk
    neighbor.distance = min(neighbor.distance, distance)

  heapq.heapify(shortest_heap)
  current = heapq.heappop(shortest_heap)

print("Shortest distance:", destination.distance)