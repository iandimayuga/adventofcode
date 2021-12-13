from collections import deque

_DATA_FILE = "2021/data/12_passage_pathing.txt"

class Cave:
  def __init__(self, name: str, big: bool) -> None:
    self.name = name
    self.big = big
    self.neighbors = []
  
  def __repr__(self) -> str:
    return "Cave: {:s} ({:s})".format(self.name, "BIG" if self.big else "small")

  def __format__(self, __format_spec: str) -> str:
    return self.__repr__()

class Path:
  def __init__(self, cave: Cave) -> None:
    self.path = deque()
    self.record(cave)
  
  # Records the order of visited caves on the way back up.
  def record(self, cave: Cave):
    # Prepend since we're backtracking.
    self.path.insert(0, cave.name)

  def __repr__(self) -> str:
    return ','.join(self.path)

# Returns the start Cave.
def build_caves(connections: list[str]) -> Cave:
  start = Cave("start", False)
  lookup = {start.name: start}
  for connection in connections:
    name_pair = connection.split('-')
    first_name = name_pair[0].strip()
    second_name = name_pair[1].strip()
    if (first_name not in lookup):
      lookup[first_name] = Cave(first_name, first_name.isupper())
    if (second_name not in lookup):
      lookup[second_name] = Cave(second_name, second_name.isupper())

    first_cave = lookup[first_name]
    second_cave = lookup[second_name]
    first_cave.neighbors.append(second_cave)
    second_cave.neighbors.append(first_cave)
    
  return start

def explore(cave: Cave, visited: set[str]) -> list[Path]:
  if (cave.name == "end"):
    return [Path(cave)]

  visited.add(cave.name)
  paths = []
  for neighbor in cave.neighbors:
    if (neighbor.name in visited and not neighbor.big):
      continue

    paths.extend(explore(neighbor, visited.copy()))
  
  for path in paths:
    path.record(cave)
  
  return paths


with open(_DATA_FILE, "r") as input:
  start = build_caves(input.readlines())

paths = explore(start, set(start.name))

print('\n'.join(str(path) for path in paths))
print("Count:", len(paths))