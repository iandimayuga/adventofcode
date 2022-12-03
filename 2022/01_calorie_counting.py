
_DATA_FILE = "2022/data/01_calorie_counting.txt"

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

for line in lines:
  # Fill the latest bag. At blank lines start a new bag.
  latest_bag = elf_bags[-1]
  if line and line.isnumeric():
    latest_bag.add_item(int(line))
    print("Adding food: " + line)
  else:
    print("Finished bag: {bag:s} = {sum:d}".format(
      bag = '+'.join([str(item) for item in latest_bag.food_items]),
      sum = latest_bag.total_calories()))
    elf_bags.append(Bag())

max_calories = max([bag.total_calories() for bag in elf_bags])

print(max_calories)