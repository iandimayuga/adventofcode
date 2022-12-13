from functools import cmp_to_key

_DEBUG = False
_DATA_FOLDER = "2022/data/test/" if _DEBUG else "2022/data/"
_DATA_FILE = _DATA_FOLDER + "13_distress_signal.txt"
_FIRST_MARKER = [[2]]
_SECOND_MARKER = [[6]]

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

packets = []

for line in lines:
  if line:
    packets.append(eval(line))

packets.append(_FIRST_MARKER)
packets.append(_SECOND_MARKER)

sorted_packets = reversed(sorted(packets, key=cmp_to_key(compare)))

print("Sorted: ")

first_marker_index = 0
second_marker_index = 0
i = 1

for packet in sorted_packets:
  print(packet, end='')
  if packet == _FIRST_MARKER:
    print(" First marker!")
    first_marker_index = i
  elif packet == _SECOND_MARKER:
    print(" Second marker!")
    second_marker_index = i
  else:
    print()
  i += 1

print("Total: ", first_marker_index * second_marker_index)