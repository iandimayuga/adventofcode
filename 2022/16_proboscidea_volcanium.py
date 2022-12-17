import re

_PART = 1
_DEBUG = True
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

# Dynamic Programming solution

# Table for if a valve is reachable by a certain minute.
reach_set = set()
# Table for the open valves and max pressure signed up for
# while at a certain final valve by a certain minute.
state_table = {}

def key(valve: str, minute: int):
  return (valve, minute)

def max_released_pressure():
  # Only the first valve is reachable in the zeroth minute.
  first_key = key(_FIRST_VALVE, 0)
  reach_set.add(first_key)
  state_table[first_key] = (0, frozenset())
  
  # Build the table out from the next minute onward.
  for minute in range(1, _TOTAL_MINUTES):
    for current_valve in valves.values():
      current_key = key(current_valve.name, minute)
      if current_key not in state_table:
        state_table[current_key] = (0, frozenset())

      for previous_valve in valves.values():
        previous_key = key(previous_valve.name, minute - 1)

        if previous_key in reach_set:
          previous_pressure = state_table[previous_key][0]
          open_valves = state_table[previous_key][1]

          if (current_valve.name == previous_valve.name or 
            current_valve.name in previous_valve.neighbors):
            reach_set.add(key(current_valve.name, minute))

            pressure_bought_here = 0
            # In the event we stayed here this minute, we can open the valve.
            if (previous_valve.name == current_valve.name and
              not current_valve.name in set([valve[0] for valve in open_valves]) and
              current_valve.rate > 0):
              # The pressure we sign up for by opening this valve.
              pressure_bought_here = current_valve.rate * (_TOTAL_MINUTES - minute)

              # Open the current valve.
              open_valves |= set([current_key])

            # If this results in a better state, replace the best state we have so far.
            best_running_pressure = state_table[current_key][0]
            if previous_pressure + pressure_bought_here > best_running_pressure:
              state_table[current_key] = (
                previous_pressure + pressure_bought_here,
                open_valves
              )
  
  # Determine the best pressure we can get at each valve in the last minute.
  return max([state_table[key(v.name, _TOTAL_MINUTES - 1)] for v in valves.values()])

print("Best result: ", max_released_pressure())
