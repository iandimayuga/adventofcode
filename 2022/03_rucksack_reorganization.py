_DATA_FILE = "2022/data/03_rucksack_reorganization.txt"

_LOWERCASE_LETTER_PRIORITY_A = 1
_UPPERCASE_LETTER_PRIORITY_A = 27

_GROUP_SIZE = 3

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

# Break the rucksacks into groups.
rucksack_groups = [rucksacks[i:i + _GROUP_SIZE]
                    for i in range(0, len(rucksacks), _GROUP_SIZE)]

sum = 0

for rucksack_group in rucksack_groups:
  badge = common_letters(rucksack_group)[0]
  priority = letter_priority(badge)
  print("badge:'{badge:s}' pri:{pri:02d}\t{group:s} ".format(
    group = ' '.join([''.join(rucksack) for rucksack in rucksack_group]),
    badge = badge,
    pri = priority
  ))
  sum += priority

print("Total: {sum:d}".format(sum = sum))