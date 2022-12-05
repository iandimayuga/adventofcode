_DATA_FILE = "2022/data/05_supply_stacks.txt"

_STACK_INDICES = [1, 5, 9, 13, 17, 21, 25, 29, 33]

class Stack:
  def __init__(self) -> None:
    self.crates = []

  # Remove and return the crates in the order removed.
  def pop(self, num: int) -> list[str]:
    removed = []
    for i in range(num):
      removed.append(self.crates.pop())
    return removed

  def push(self, crates: list[str]) -> None:
    self.crates.extend(crates)

  def __str__(self) -> str:
    return str(self.crates)

def read_crate(line: str, index: int) -> str:
  if len(line) > index:
    return line[index].strip()

lines = []
with open(_DATA_FILE, "r") as input:
  lines = [line.rstrip() for line in input]


line_break = 0
# Find the line break.
for line in lines:
  if not line:
    break
  line_break += 1

# Back up to the stacks.
stacks_bottom = line_break - 1

print("Line " + str(stacks_bottom))

stacks = [Stack() for i in range(len(_STACK_INDICES))]

for i in reversed(range(stacks_bottom)):
  line = lines[i]
  print(line)
  for j in range(len(_STACK_INDICES)):
    crate = read_crate(line, _STACK_INDICES[j])
    if crate:
      stacks[j].push([crate])

for stack in stacks:
  print(str(stack))

print("*** MOVING ***")

# Interpret moves.
moves_top = line_break + 1
for i in range(moves_top, len(lines)):
  move_words = lines[i].split(' ')
  num = int(move_words[1])
  src = int(move_words[3]) - 1
  dst = int(move_words[5]) - 1
  moved = stacks[src].pop(num)
  stacks[dst].push(moved)

for stack in stacks:
  print(str(stack))

for stack in stacks:
  if stack.crates:
    print(stack.crates.pop(), end='')