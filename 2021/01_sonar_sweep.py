import math

_WINDOW_SIZE = 3
_DATA_FILE = "2021/data/01_sonarsweep.txt"

# Read the input data into a list of ints.
numlist = []
with open(_DATA_FILE, "r") as input:
  numlist = list(map(int, input.readlines()))

# Create a rotating buffer to hold the window.
window = [math.inf] * _WINDOW_SIZE

increase_count = 0
mod_index = 0
# A value's place in the window is its index mod window size.
# This way, the value will take the place of the value sliding out of the
# window. We can then simply compare the value to the value it is replacing to
# know if the window sum would increase, without needing to actually take the
# sum.
for num in numlist:
  if num > window[mod_index]:
    increase_count += 1
  window[mod_index] = num
  mod_index = (mod_index + 1) % _WINDOW_SIZE

print("Increased {:d} times".format(increase_count))