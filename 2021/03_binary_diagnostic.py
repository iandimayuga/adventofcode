_DATA_FILE = "2021/data/03_binary_diagnostic.txt"
_BIT_LENGTH = 12 

numlist = []
with open(_DATA_FILE, "r") as input:
  numlist = list(map(lambda s : int(s, base=2), input.readlines()))

# Treat it like a binary search.
# Keep a running number starting with the largest power of 2.
o2_pivot = 0
co2_pivot = 0

o2_list = numlist.copy()
co2_list = numlist.copy()
for bit in reversed(range(0, _BIT_LENGTH)):
  if (len(o2_list) > 1):
    # Set the bit to 1 in the value for comparison.
    o2_pivot += 2**bit

    o2_1s = []
    o2_0s = []
    for num in o2_list:
      if (num >= o2_pivot):
        o2_1s.append(num)
      else:
        o2_0s.append(num)
    
    if (len(o2_1s) >= len(o2_0s)):
      # 1s are more common, leave the 1 in the pivot.
      o2_list = o2_1s
    else:
      # 0s are more common, set the bit to 0 in the pivot.
      o2_pivot -= 2**bit
      o2_list = o2_0s
    
  if (len(co2_list) > 1):
    # Set the bit to 1 in the pivot for comparison.
    co2_pivot += 2**bit

    co2_1s = []
    co2_0s = []
    for num in co2_list:
      if (num >= co2_pivot):
        co2_1s.append(num)
      else:
        co2_0s.append(num)

    if (len(co2_1s) >= len(co2_0s)):
      # 0s are less common, set the bit to 0 in the pivot.
      co2_pivot -= 2**bit
      co2_list = co2_0s
    else:
      # 1s are less common, leave the 1 in the pivot.
      co2_list = co2_1s

o2_value = o2_list[0]
co2_value = co2_list[0]

print("o2_value:  {0:b} ({0:d})".format(o2_value))
print("co2_value: {0:b} ({0:d})".format(co2_value))
print("product:   {:d}".format(o2_value * co2_value))