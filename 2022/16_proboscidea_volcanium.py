import re

_PART = 1
_DEBUG = False
_DATA_FOLDER = "2022/data/test/" if _DEBUG else "2022/data/"
_DATA_FILE = _DATA_FOLDER + "16_proboscidea_volcanium.txt"

# Parsing constants.
_VALVE_PATTERN = re.compile(
  r"^Valve (?P<name>\w+) has flow rate=(?P<rate>\d+); " +
  r"tunnel(s)? lead(s)? to valve(s)? (?P<neighbors>.+)$")
_NEIGHBOR_DELIMITER = ', '

# Puzzle state
_TOTAL_MINUTES = 30
_FIRST_VALVE = 'AA'

class Valve:
  def __init__(self, name: str, rate: int, neighbors: list[str]) -> None:
    self.name = name
    self.rate = rate
    self.neighbors = neighbors

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
print()

# Memoize the amount of released pressure given a minute, current valve, and set of open valves.
pressure_cache: dict[tuple[int, str, frozenset[str]], int] = {}

def max_released_pressure(minute: int, current_valve: str, open_valves: frozenset[str]):
  key = (minute, current_valve, open_valves)
  if key in pressure_cache:
    return pressure_cache[key]
  
  # Pressure released this minute regardless of action.
  pressure_released = sum([valves[v].rate for v in open_valves])

  # Explore the space of possible actions.
  max_benefit = 0

  # No actions possible if this is the last minute.
  if minute < _TOTAL_MINUTES:
    # Action: Open current closed valve and stay put.
    if current_valve not in open_valves:
      max_benefit = max_released_pressure(minute + 1, current_valve, open_valves | set([current_valve]))

    # Action: Move to another valve.
    for neighbor in valves[current_valve].neighbors:
      max_benefit = max(max_benefit, max_released_pressure(minute + 1, neighbor, open_valves))

  pressure_cache[key] = max_benefit + pressure_released
  return max_benefit + pressure_released

print("Best result: ", max_released_pressure(1, _FIRST_VALVE, frozenset()))
