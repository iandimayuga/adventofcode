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

def common_letters(rucksacks: list[list[str]]) -> list[str]:
  return list(set.intersection(
    *[set(rucksack) for rucksack in rucksacks]))


rucksacks = []
with open(_DATA_FILE, "r") as input:
  rucksacks = [[c for c in line.strip()] for line in input]

sum = 0

for rucksack in rucksacks:
  halves = compartments(rucksack)
  dup = common_letters([halves[0], halves[1]])[0]
  priority = letter_priority(dup)
  print("dup:'{dup:s}' pri:{pri:02d}\t{left:s}|{right:s} ".format(
    left = ','.join(halves[0]),
    right = ','.join(halves[1]),
    dup = dup,
    pri = priority
  ))
  sum += priority

print("Total: {sum:d}".format(sum = sum))