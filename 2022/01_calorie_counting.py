_DATA_FILE = "2022/data/01_calorie_counting.txt"
_NUM_TOP_ELVES = 3

class Bag:
  def __init__(self) -> None:
    self.food_items = []
  
  def add_item(self, item: int) -> None:
    self.food_items.append(item)
  
  def total_calories(self) -> int:
    return sum(self.food_items)

lines = []
with open(_DATA_FILE, "r") as input:
  lines = [line.strip() for line in input.readlines()]

# Start with one empty elf bag.
elf_bags = [Bag()]

top_calorie_counts = [0] * _NUM_TOP_ELVES

for line in lines:
  # Fill the latest bag. At blank lines start a new bag.
  latest_bag = elf_bags[-1]
  if line and line.isnumeric():
    latest_bag.add_item(int(line))
    print("Adding food: " + line)
  else:
    total = latest_bag.total_calories()
    print("Finished bag: {bag:s} = {sum:d}".format(
      bag = '+'.join([str(item) for item in latest_bag.food_items]),
      sum = total))
    if (total > top_calorie_counts[0]):
      print("Top elf!")
      top_calorie_counts[0] = total
      top_calorie_counts.sort()
    elf_bags.append(Bag())

print(sum(top_calorie_counts))