from math import prod
import re
from typing import Callable

_DATA_FILE = "2022/data/11_monkey_in_the_middle.txt"
_MONKEY_LINES = 7

_NUM_ROUNDS = 10000
_NUM_MOST_ACTIVE = 2

class Item:
  def __init__(self, worry: int) -> None:
    self.worry = worry

class Modulus:
  def __init__(self) -> None:
    self.modulus = 1

class Monkey:
  def __init__(
    self,
    monkeys: list["Monkey"],
    global_modulus: Modulus,
    index: int,
    items: list[Item],
    operation: Callable[[int], int],
    test: Callable[[int], bool],
    true_monkey_index: int,
    false_monkey_index: int
  ) -> None:
    self.monkeys = monkeys
    self.global_modulus = global_modulus
    self.index = index
    self.items = items
    self.operation = operation
    self.test = test
    self.true_monkey_index = true_monkey_index
    self.false_monkey_index = false_monkey_index
    self.total_inspections = 0
  
  def turn(self):
    # print("Monkey {i:d}:".format(i = self.index))
    for item in self.items:
      monkey = self.inspect_item(item)
      self.throw(item, monkey)
    self.items.clear()

  # Inspects an item, updates worry, and returns which monkey to throw to.
  def inspect_item(self, item: Item) -> "Monkey":
    # print("  Monkey inspects item with worry {w:d}".format(w = item.worry))
    self.total_inspections += 1

    # Update item worry.
    item.worry = int(self.operation(item.worry))
    # print("    Worry updated to {w:d}".format(w = item.worry))

    # Apply modulus.
    item.worry = int(item.worry % self.global_modulus.modulus)
    # print("    Worry decays to {w:d}".format(w = item.worry))

    # Test worry to determine throw.
    if self.test(item.worry):
      return self.monkeys[self.true_monkey_index]
    return self.monkeys[self.false_monkey_index]

  def throw(self, item: Item, monkey: "Monkey"):
    # print("    Item with worry {w:d} thrown to monkey {i:d}".format(
    #  w = item.worry,
    #  i = monkey.index
    #  ))
    monkey.items.append(item)

monkeys: list[Monkey]
monkeys = []
global_modulus = Modulus()

def parse_monkey(lines: list[str]) -> Monkey:
  index = int(re.compile(r"Monkey (\d+)").match(lines[0]).group(1))
  items = [Item(int(w)) for w in
    re.compile(r"Starting items: (.+)").match(lines[1]).group(1).split(', ')
  ]
  operation = lambda old: eval(
    re.compile(r"Operation: new = (.+)").match(lines[2]).group(1)
  )
  local_modulus = int(
    re.compile(r"Test: divisible by (\d+)").match(lines[3]).group(1)
  )
  test = lambda worry: worry % local_modulus == 0
  true_monkey_index = int(
    re.compile(r"If true: throw to monkey (\d+)").match(lines[4]).group(1)
  )
  false_monkey_index = int(
    re.compile(r"If false: throw to monkey (\d+)").match(lines[5]).group(1)
  )

  # Need a global modulus to keep all operations equivalent.
  global_modulus.modulus *= local_modulus

  return Monkey(monkeys, global_modulus, index, items, operation, test, true_monkey_index, false_monkey_index)

lines = []
with open(_DATA_FILE, "r") as inputfile:
  lines = [line.strip() for line in inputfile]

for i in range(0, len(lines), _MONKEY_LINES):
  monkeys.append(parse_monkey(lines[i:i+_MONKEY_LINES]))

for i in range(_NUM_ROUNDS):
  for monkey in monkeys:
    monkey.turn()

most_active = [0] * _NUM_MOST_ACTIVE

for monkey in monkeys:
  if monkey.total_inspections > most_active[0]:
    most_active[0] = monkey.total_inspections
    most_active.sort()
  
  print("Monkey {i:d} inspected {t:d} times.".format(
    i = monkey.index,
    t = monkey.total_inspections
  ))

print("Most active multiplied: " + str(prod(most_active)))