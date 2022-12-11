from math import prod
from typing import Callable

_DEBUG = True

_WORRY_DECAY_RATE = 3
_NUM_ROUNDS = 10000
_NUM_MOST_ACTIVE = 2

class Item:
  def __init__(self, worry: int) -> None:
    self.worry = worry

class Monkey:
  def __init__(
    self,
    monkeys: list["Monkey"],
    index: int,
    items: list[Item],
    operation: Callable[[int], int],
    test: Callable[[int], bool],
    modulus: int,
    true_monkey: int,
    false_monkey: int
  ) -> None:
    self.monkeys = monkeys
    self.index = index
    self.items = items
    self.operation = operation
    self.test = test
    self.modulus = modulus
    self.true_monkey = true_monkey
    self.false_monkey = false_monkey
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
    item.worry = int(item.worry % self.modulus)
    # print("    Worry decays to {w:d}".format(w = item.worry))

    # Test worry to determine throw.
    if self.test(item.worry):
      return self.monkeys[self.true_monkey]
    return self.monkeys[self.false_monkey]

  def throw(self, item: Item, monkey: "Monkey"):
    # print("    Item with worry {w:d} thrown to monkey {i:d}".format(
    #  w = item.worry,
    #  i = monkey.index
    #  ))
    monkey.items.append(item)

monkeys: list[Monkey]
monkeys = []

if (_DEBUG):
  monkeys.append(Monkey(monkeys, 0,
    [Item(i) for i in [ 79, 98]],
    lambda old: old * 19,
    lambda worry: worry % 23 == 0,
      23,
      2,
      3))

  monkeys.append(Monkey(monkeys, 1,
    [Item(i) for i in [ 54, 65, 75, 74]],
    lambda old: old + 6,
    lambda worry: worry % 19 == 0,
      19,
      2,
      0))

  monkeys.append(Monkey(monkeys, 2,
    [Item(i) for i in [ 79, 60, 97]],
    lambda old: old * old,
    lambda worry: worry % 13 == 0,
      13,
      1,
      3))

  monkeys.append(Monkey(monkeys, 3,
    [Item(i) for i in [ 74]],
    lambda old: old + 3,
    lambda worry: worry % 17 == 0,
      17,
      0,
      1))
else: 
  monkeys.append(Monkey(monkeys, 0,
    [Item(i) for i in [ 89, 74]],
    lambda old: old * 5,
    lambda worry: worry % 17 == 0,
      17,
      4,
      7))

  monkeys.append(Monkey(monkeys, 1,
    [Item(i) for i in [ 75, 69, 87, 57, 84, 90, 66, 50]],
    lambda old: old + 3,
    lambda worry: worry % 7 == 0,
      7,
      3,
      2))

  monkeys.append(Monkey(monkeys, 2,
    [Item(i) for i in [ 55]],
    lambda old: old + 7,
    lambda worry: worry % 13 == 0,
      13,
      0,
      7))

  monkeys.append(Monkey(monkeys, 3,
    [Item(i) for i in [ 69, 82, 69, 56, 68]],
    lambda old: old + 5,
    lambda worry: worry % 2 == 0,
      2,
      0,
      2))

  monkeys.append(Monkey(monkeys, 4,
    [Item(i) for i in [ 72, 97, 50]],
    lambda old: old + 2,
    lambda worry: worry % 19 == 0,
      19,
      6,
      5))

  monkeys.append(Monkey(monkeys, 5,
    [Item(i) for i in [ 90, 84, 56, 92, 91, 91]],
    lambda old: old * 19,
    lambda worry: worry % 3 == 0,
      3,
      6,
      1))

  monkeys.append(Monkey(monkeys, 6,
    [Item(i) for i in [ 63, 93, 55, 53]],
    lambda old: old * old,
    lambda worry: worry % 5 == 0,
      5,
      3,
      1))

  monkeys.append(Monkey(monkeys, 7,
    [Item(i) for i in [ 50, 61, 52, 58, 86, 68, 97]],
    lambda old: old + 4,
    lambda worry: worry % 11 == 0,
      11,
      5,
      4))


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