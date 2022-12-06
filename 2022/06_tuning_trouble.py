from collections import Counter

_DATA_FILE = "2022/data/06.txt"

_WINDOW_SIZE = 14

chars = ""
with open(_DATA_FILE, "r") as input:
  chars = input.read()

print(chars)

for start in range(len(chars) - _WINDOW_SIZE):
  end = start + _WINDOW_SIZE
  keys = Counter(chars[start : end]).keys()
  print(chars[start : end])
  if len(keys) >= _WINDOW_SIZE:
    print(end)
    break