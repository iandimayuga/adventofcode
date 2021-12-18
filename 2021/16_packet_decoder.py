from enum import Enum
from math import prod

_DATA_FILE = "2021/data/16_packet_decoder.txt"
_BITS_PER_HEX_CHAR = 4
_VERSION_BITS = 3
_TYPE_BITS = 3
_LITERAL_DONE_BITS = 1
_LITERAL_GROUP_BITS = 4
_SUB_PACKET_LENGTH_TYPE_BITS = 1
_SUB_PACKET_LENGTH_BITS = 15
_SUB_PACKET_COUNT_BITS = 11

class PacketType(Enum):
  UNKNOWN = -1
  SUM = 0
  PRODUCT = 1
  MINIMUM = 2
  MAXIMUM = 3
  LITERAL = 4
  GREATER_THAN = 5
  LESS_THAN = 6
  EQUAL_TO = 7

  @classmethod
  def has_value(cls, value):
    return value in cls._value2member_map_

class SubPacketLengthType(Enum):
  LENGTH = 0
  COUNT = 1

# Wraps an integer to allow for leading zeroes.
class BitString:
  def __init__(self, bits: int, bit_length: int) -> None:
    self.int_value = bits
    self.bit_length = bit_length

# Get a window of a bit string starting from an offset.
def bit_window(bits: BitString, offset: int, length: int) -> int:
  end = offset + length
  mask = 2**length - 1
  return (bits.int_value >> (bits.bit_length - end)) & mask

# A packet in a hierarchical expression tree.
class Packet:
  def __init__(self, bits: BitString, offset: int, parent_depth: int) -> None:
    # Offset in the transmission bits.
    self.offset = offset

    # Total bit length of this packet, including sub-packets.
    self.bit_length = 0

    # Hierarchy depth of this packet.
    self.depth = parent_depth + 1

    self.version = self._read_version(bits)
    self.type = self._read_type(bits)

    self.sub_packets = []
    if (self.type == PacketType.LITERAL):
      self.value = self._read_literal_value(bits)
    else:
      self.sub_packets = self._read_sub_packets(bits)
      self.value = self._evaluate()

  # Evaluates the expression of this operator packet.
  def _evaluate(self) -> int:
    values = [p.value for p in self.sub_packets]
    if (self.type == PacketType.SUM):
      return sum(values, 0)
    elif (self.type == PacketType.PRODUCT):
      return prod(values)
    elif (self.type == PacketType.MINIMUM):
      return min(values)
    elif (self.type == PacketType.MAXIMUM):
      return max(values)
    elif (self.type == PacketType.GREATER_THAN):
      return 1 if values[0] > values[1] else 0
    elif (self.type == PacketType.LESS_THAN):
      return 1 if values[0] < values[1] else 0
    elif (self.type == PacketType.EQUAL_TO):
      return 1 if values[0] == values[1] else 0
    else:
      print("ERROR: Unknown packet type!")
      return 0

  def _next_offset(self) -> int:
    return self.offset + self.bit_length

  # Reads out the specified number of bits and increments the bit length of this packet.
  def _read_and_increment(self, bits: BitString, length: int) -> int:
    value = bit_window(bits, self._next_offset(), length)
    self.bit_length += length
    # print(("Read {:d} bits, got {:0" + str(length) + "b} ({:d})").format(length, value, value))
    return value

  # Reads out the next bits as a packet version.
  def _read_version(self, bits: BitString) -> int:
    version = self._read_and_increment(bits, _VERSION_BITS)
    return version

  # Reads out the next bits as a packet type ID.
  def _read_type(self, bits: BitString) -> PacketType:
    type_id = self._read_and_increment(bits, _TYPE_BITS)
    if (PacketType.has_value(type_id)):
      return PacketType(type_id)
    else:
      return PacketType.UNKNOWN

  # Reads out the next bits as a numeric value.
  def _read_literal_value(self, bits: BitString) -> int:
    more = True
    value = 0
    while more:
      more = bool(self._read_and_increment(bits, _LITERAL_DONE_BITS))
      group = int(self._read_and_increment(bits, _LITERAL_GROUP_BITS))
      value = (value << _LITERAL_GROUP_BITS) + group
    return value
  
  # Reads out the next bits as a sub-packet length and set of sub-packets.
  def _read_sub_packets(self, bits: BitString) -> list["Packet"]:
    sub_packet_length_type = SubPacketLengthType(
      self._read_and_increment(bits, _SUB_PACKET_LENGTH_TYPE_BITS)
    )
    if (sub_packet_length_type == SubPacketLengthType.LENGTH):
      length = self._read_and_increment(bits, _SUB_PACKET_LENGTH_BITS)
      return self._read_sub_packets_by_length(bits, length)
    elif (sub_packet_length_type == SubPacketLengthType.COUNT):
      count = self._read_and_increment(bits, _SUB_PACKET_COUNT_BITS)
      return self._read_sub_packets_by_count(bits, count)
  
  # Reads the next specified length of bits as sub-packets.
  def _read_sub_packets_by_length(self, bits: BitString, length: int) -> list["Packet"]:
    length_read = 0
    packets_read = []
    while length_read < length:
      packet = Packet(bits, self._next_offset(), self.depth)
      self.bit_length += packet.bit_length
      packets_read.append(packet)
      length_read += packet.bit_length

    if (length_read > length):
      print("WARNING: last packet was longer than expected!")
      print("Expected length: {:d}, Actual length: {:d}")
      print("Last packet:", packets_read[-1])

    return packets_read

  # Reads the next specified number of sub-packets.
  def _read_sub_packets_by_count(self, bits: BitString, count: int) -> list["Packet"]:
    packets_read = []
    while len(packets_read) < count:
      packet = Packet(bits, self._next_offset(), self.depth)
      self.bit_length += packet.bit_length
      packets_read.append(packet)

    return packets_read
  
  def __format__(self, __format_spec: str) -> str:
    return self.__repr__()

  def __repr__(self) -> str:
    header = "Length={:d} Version={:d} Type={:s}".format(
      self.bit_length,
      self.version,
      self.type.name)
    data = "Value={:d}".format(self.value)
    if (self.type != PacketType.LITERAL):
      for packet in self.sub_packets:
        data += "\n{:s}{:s}".format('\t' * self.depth, packet)

    return "{:s} {:s}".format(header, data)


with open(_DATA_FILE, "r") as input:
  transmissions = input.readlines()

for hex_string in transmissions:
  stripped_hex_string = hex_string.strip()
  print("Transmission received:", stripped_hex_string)
  bits = BitString(int(hex_string, 16), len(stripped_hex_string) * _BITS_PER_HEX_CHAR)
  packet = Packet(bits, offset=0, parent_depth=0)
  print(packet)
  print("Final value:", packet.value)
  print()