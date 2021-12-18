from enum import Enum

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
  OPERATOR = -1
  LITERAL = 4

  @classmethod
  def has_value(cls, value):
    return value in cls._value2member_map_

class SubPacketLengthType(Enum):
  LENGTH = 0
  COUNT = 1

class BitString:
  def __init__(self, bits: int, bit_length: int) -> None:
    self.int_value = bits
    self.bit_length = bit_length

def bit_window(bits: BitString, offset: int, length: int) -> int:
  end = offset + length
  mask = 2**length - 1
  return (bits.int_value >> (bits.bit_length - end)) & mask

class Packet:
  def __init__(self, bits: BitString, offset: int) -> None:
    # Offset in the transmission bits.
    self.offset = offset

    # Total bit length of this packet, including sub-packets.
    self.bit_length = 0

    self.version = self._read_version(bits)
    self.total_version = self.version
    self.type = self._read_type(bits)

    self.value = 0
    self.sub_packets = []
    if (self.type == PacketType.LITERAL):
      self.value = self._read_literal_value(bits)
    else:
      self.sub_packets = self._read_sub_packets(bits)
      for packet in self.sub_packets:
        self.total_version += packet.total_version

  def next_offset(self) -> int:
    return self.offset + self.bit_length

  def _read_and_increment(self, bits: BitString, length: int) -> int:
    value = bit_window(bits, self.next_offset(), length)
    self.bit_length += length
    # print(("Read {:d} bits, got {:0" + str(length) + "b} ({:d})").format(length, value, value))
    return value

  def _read_version(self, bits: BitString) -> int:
    version = self._read_and_increment(bits, _VERSION_BITS)
    return version

  def _read_type(self, bits: BitString) -> PacketType:
    type_id = self._read_and_increment(bits, _TYPE_BITS)
    if (PacketType.has_value(type_id)):
      return PacketType(type_id)
    else:
      return PacketType.OPERATOR

  def _read_literal_value(self, bits: BitString) -> int:
    more = True
    value = 0
    while more:
      more = bool(self._read_and_increment(bits, _LITERAL_DONE_BITS))
      group = int(self._read_and_increment(bits, _LITERAL_GROUP_BITS))
      value = (value << _LITERAL_GROUP_BITS) + group
    return value
  
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
  
  def _read_sub_packets_by_length(self, bits: BitString, length: int) -> list["Packet"]:
    length_read = 0
    packets_read = []
    while length_read < length:
      packet = Packet(bits, self.next_offset())
      self.bit_length += packet.bit_length
      packets_read.append(packet)
      length_read += packet.bit_length

    if (length_read > length):
      print("WARNING: last packet was longer than expected!")
      print("Expected length: {:d}, Actual length: {:d}")
      print("Last packet:", packets_read[-1])

    return packets_read

  def _read_sub_packets_by_count(self, bits: BitString, count: int) -> list["Packet"]:
    packets_read = []
    while len(packets_read) < count:
      packet = Packet(bits, self.next_offset())
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
    if (self.type == PacketType.LITERAL):
      data = "Value={:d}".format(self.value)
    else:
      data = ""
      for packet in self.sub_packets:
        data += "\n\t{:s}".format(packet)

    return "{:s} {:s}".format(header, data)


with open(_DATA_FILE, "r") as input:
  transmissions = input.readlines()

for hex_string in transmissions:
  stripped_hex_string = hex_string.strip()
  print("Transmission received:", stripped_hex_string)
  bits = BitString(int(hex_string, 16), len(stripped_hex_string) * _BITS_PER_HEX_CHAR)
  packet = Packet(bits, 0)
  print(packet)
  print("Total version: {:d}".format(packet.total_version))
  print()