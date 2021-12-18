from enum import Enum

_DATA_FILE = "2021/data/test/16_packet_decoder.txt"
_VERSION_LENGTH = 3

class PacketType(Enum):
  UNKNOWN = -1
  LITERAL = 4
  def has_value(cls, value):
    return value in cls._value2member_map_

def read_bit_window(bits: int, offset: int, length: int) -> int:
  end = offset + length
  mask = 2**length - 1
  return (bits >> (bits.bit_length() - end)) & mask

class Packet:
  def __init__(self, bits: int, offset: int) -> None:
    self.version = 0
    self.type = PacketType.UNKNOWN
    self.value = 0
    self.sub_packets = []
    self.bit_length = 0

    # First three bits are version.
    self.version = read_bit_window(bits, offset, _VERSION_LENGTH)
    self.bit_length += _VERSION_LENGTH
    offset += _VERSION_LENGTH



with open(_DATA_FILE, "r") as input:
  transmissions = input.readlines()

for hex_string in transmissions:
  print("Transmission received:", hex_string)
  bits = int(hex_string, 16)
  packet = Packet(bits, 0)
  print("Packet version:", packet.version)