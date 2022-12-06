_DATA_FILE = "2022/data/06_tuning_trouble.txt"

_WINDOW_SIZE = 14

chars = ""
with open(_DATA_FILE, "r") as input:
  chars = input.read()

print(chars)

for start in range(len(chars) - _WINDOW_SIZE):
  end = start + _WINDOW_SIZE
  charset = set(chars[start : end])
  print(chars[start : end])
  if len(charset) >= _WINDOW_SIZE:
    print(end)
    break