_DATA_FILE = "2022/data/04_camp_cleanup.txt"

class Assignment:
  def __init__(self, lower: int, upper: int) -> None:
    self.lower = lower
    self.upper = upper

  def contains(self, other: "Assignment") -> bool:
    return self.lower <= other.lower and self.upper >= other.upper

  def overlaps(self, other: "Assignment") -> bool:
    return self.contains(other) or (self.lower <= other.upper and self.lower >= other.lower) or (self.upper <= other.upper and self.upper >= other.lower)
  
  def __str__(self) -> str:
    return "{lower:d}-{upper:d}".format(lower = self.lower, upper = self.upper)

pairs = []
with open(_DATA_FILE, "r") as input:
  for line in input:
    pair = line.strip().split(',')
    pairs.append(tuple([Assignment(*[int(bound) for bound in assignment.split('-')]) for assignment in pair]))

total = 0
for pair in pairs:
  print("{one:s} {two:s}".format(one = str(pair[0]), two = str(pair[1])))
  if (pair[0].overlaps(pair[1])):
    total += 1

print(total)