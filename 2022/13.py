
_DEBUG = True
_DATA_FOLDER = "2022/data/test/" if _DEBUG else "2022/data/"
_DATA_FILE = _DATA_FOLDER + "13.txt"

def compare(left, right) -> int:
  if isinstance(left, list) and isinstance(right, list):
    return compare_lists(left, right)
  if isinstance(left, list) and isinstance(right, int):
    return compare_list_int(left, right)
  if isinstance(left, int) and isinstance(right, list):
    return compare_int_list(left, right)
  return compare_ints(left, right)

def compare_lists(left: list, right: list) -> int:
  if _DEBUG: print("Compare {l:s} vs {r:s}".format(l = str(left), r = str(right)))
  for (left_child, right_child) in zip(left, right):
    comparison = compare(left_child, right_child)
    if comparison < 0:
      return -1
    elif comparison > 0:
      return 1
  
  return len(right) - len(left)

def compare_list_int(left: list, right: int) -> int:
  if _DEBUG:
    print("Compare {l:s} vs {r:s}".format(l = str(left), r = str(right)))
    print("Mixed types.")
  return compare(left, [right])

def compare_int_list(left: int, right: list) -> int:
  if _DEBUG:
    print("Compare {l:s} vs {r:s}".format(l = str(left), r = str(right)))
    print("Mixed types.")
  return compare([left], right)

def compare_ints(left: int, right: int) -> int:
  if _DEBUG: print("Compare {l:s} vs {r:s}".format(l = str(left), r = str(right)))
  return right - left

lines = []
with open(_DATA_FILE, "r") as inputfile:
  lines = [line.strip() for line in inputfile]

# Group into pairs, skipping the line break in between.
pairs = [lines[i:i+2] for i in range(0, len(lines), 3)]

pair_index = 1
total_right = 0
for pair in pairs:
  print("== Pair {i:d} ==".format(i = pair_index))
  print(pair)
  comparison = compare(eval(pair[0]), eval(pair[1]))
  if comparison < 0:
    print("Wrong order!")
  elif comparison > 0:
    total_right += pair_index
    print("Right order!")
  print()
  pair_index += 1

print("Total: ", total_right)