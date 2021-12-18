
_DATA_FILE = "2021/data/test/16_packet_decoder.txt"

with open(_DATA_FILE, "r") as input:
  hex_string = input.readline()

bits = int(hex_string, 16)

for bit in reversed(range(bits.bit_length())):
  print((bits >> bit) & 1, end='')