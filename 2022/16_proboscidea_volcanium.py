import re

_DEBUG = True
_DATA_FOLDER = "2022/data/test/" if _DEBUG else "2022/data/"
_DATA_FILE = _DATA_FOLDER + "16_proboscidea_volcanium.txt"

_VALVE_PATTERN = re.compile(
  r"^Valve (?P<name>\w+) has flow rate=(?P<rate>\d+); " +
  r"tunnel(s)? lead(s)? to valve(s)? (?P<neighbors>.+)$")
_NEIGHBOR_DELIMITER = ', '

class Valve:
  def __init__(self, name: str, rate: int, neighbors: list[str]) -> None:
    self.name = name
    self.rate = rate
    self.neighbors = neighbors
    self.open = False

  def __str__(self) -> str:
    return "Name={n:s}\tRate={r:d}\tNeighbors={ns:s}".format(
      n = self.name,
      r = self.rate,
      ns = ','.join(self.neighbors)
    )
    

lines = []
with open(_DATA_FILE, "r") as inputfile:
  lines = [line.strip() for line in inputfile]

valves: dict[str, Valve] = {}

for line in lines:
  match = _VALVE_PATTERN.match(line)
  name = match.group("name")
  rate = int(match.group("rate"))
  neighbors = match.group("neighbors").split(_NEIGHBOR_DELIMITER)
  valves[name] = Valve(name, rate, neighbors)

print('\n'.join([str(valve) for valve in valves.values()]))