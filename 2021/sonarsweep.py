import math

# Test by outputting the input data.
numlist = []
with open("2021/data/sonarsweep.txt", "r") as input:
  numlist = list(map(int, input.readlines()))
previous = math.inf
increase_count = 0
for num in numlist:
  if num > previous:
    increase_count += 1
  previous = num

print("Increased {:d} times".format(increase_count))