_DATA_FILE = "2022/data/test/10_cathode-ray_tube.txt"
_ADDX_CMD = "addx"
_NOOP_CMD = "noop"
_ADDX_CYCLES = 2
_NOOP_CYCLES = 1
_SCREEN_WIDTH = 40
_SCREEN_HEIGHT = 6
_SPRITE_RADIUS = 1

class Operation:
  def __init__(self, add: int, cycles: int) -> None:
    self.add = add 
    self.cycles = cycles

  # Determine how much to change the register by this cycle.
  def add_cycle(self) -> int:
    self.cycles -= 1
    if self.cycles == 0:
      return self.add
    return 0
  
  def pending(self) -> bool:
    return self.cycles > 0

lines = []
with open(_DATA_FILE, "r") as inputfile:
  lines = [line.strip() for line in inputfile]

cycle = 0
register_x = 1
operation = Operation(0, 0)
screen = [['.' for x in range(_SCREEN_WIDTH)] for y in range(_SCREEN_HEIGHT)]

for line in lines:
  command = line.split(' ')
  if command[0] == _NOOP_CMD:
    operation = Operation(0, _NOOP_CYCLES)
  elif command[0] == _ADDX_CMD:
    operation = Operation(int(command[1]), _ADDX_CYCLES)
  while operation.pending():
    cycle += 1
    register_x += operation.add_cycle()
    row = int(cycle / _SCREEN_WIDTH)
    column = cycle % _SCREEN_WIDTH
    if column >= register_x - _SPRITE_RADIUS and column <= register_x + _SPRITE_RADIUS:
      screen[row][column] = '#'

for row in screen:
  for char in row:
    print(char, end='')
  print()

