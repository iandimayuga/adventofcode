_DATA_FILE = "2021/data/03_binary_diagnostic.txt"
_BIT_LENGTH = 12

numlist = []
with open(_DATA_FILE, "r") as input:
  numlist = list(map(lambda s : int(s, base=2), input.readlines()))

# Maintain a count for each bit.
bit_counts = [0] * _BIT_LENGTH

# +1 for 1-bits, and -1 for 0-bits.
for num in numlist:
  for bit in range(0, _BIT_LENGTH):
    if (num & 2**bit):
      bit_counts[bit] += 1
    else:
      bit_counts[bit] -= 1

gamma = 0
epsilon = 0

bit = 0
for bit_count in bit_counts:
  if bit_count > 0:
    gamma += 1 << bit
  elif bit_count < 0:
    epsilon += 1 << bit
  bit += 1

print("gamma:   {:d}".format(gamma))
print("epsilon: {:d}".format(epsilon))
print("product: {:d}".format(gamma * epsilon))