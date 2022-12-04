from ast import Set


_DATA_FILE = "2022/data/03_rucksack_reorganization.txt"

_LOWERCASE_LETTER_PRIORITY_A = 1
_UPPERCASE_LETTER_PRIORITY_A = 27

def letter_priority(letter: str) -> int:
  if letter.islower():
    return ord(letter) - ord('a') + _LOWERCASE_LETTER_PRIORITY_A
  return ord(letter) - ord('A') + _UPPERCASE_LETTER_PRIORITY_A

def compartments(rucksack: list[str]) -> tuple[list[str], list[str]]:
  middle = int(len(rucksack) / 2)
  return (rucksack[middle:], rucksack[:middle])

def duplicate(left: list[str], right: list[str]) -> str:
  return next(iter(set(left).intersection(set(right))))

rucksacks = []
with open(_DATA_FILE, "r") as input:
  rucksacks = [[c for c in line.strip()] for line in input]

sum = 0

for rucksack in rucksacks:
  halves = compartments(rucksack)
  dup = duplicate(halves[0], halves[1])
  priority = letter_priority(dup)
  print("dup:'{dup:s}' pri:{pri:02d}\t{left:s}|{right:s} ".format(
    left = ','.join(halves[0]),
    right = ','.join(halves[1]),
    dup = dup,
    pri = priority
  ))
  sum += priority

print("Total: {sum:d}".format(sum = sum))