_DATA_FILE = "2022/data/10_cathode-ray_tube.txt"
_ADDX_CMD = "addx"
_NOOP_CMD = "noop"
_ADDX_CYCLES = 2
_NOOP_CYCLES = 1
_CYCLE_MOD = 40
_CYCLE_MOD_OFFSET = 20

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
strength_sum = 0
line_num = 1

for line in lines:
  command = line.split(' ')
  if command[0] == _NOOP_CMD:
    operation = Operation(0, _NOOP_CYCLES)
  elif command[0] == _ADDX_CMD:
    operation = Operation(int(command[1]), _ADDX_CYCLES)
  while operation.pending():
    cycle += 1
    register_x += operation.add_cycle()
    if (cycle % _CYCLE_MOD == _CYCLE_MOD_OFFSET - 1):
      strength = (cycle + 1) * register_x
      strength_sum += strength
      print("Line:{l:d} Cycle:{c:d} * X:{x:d} = Strength:{s:d}".format(
        l = line_num, c = cycle + 1, x = register_x, s = strength))
  line_num += 1

print("Total: {s:d}".format(s = strength_sum))
