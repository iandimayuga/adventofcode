from enum import Enum

_DATA_FILE = "2021/data/test/16_packet_decoder.txt"
_VERSION_LENGTH = 3
_TYPE_LENGTH = 3
_LITERAL_DONE_LENGTH = 1
_LITERAL_GROUP_LENGTH = 4


class PacketType(Enum):
  OPERATOR = -1
  LITERAL = 4

  @classmethod
  def has_value(cls, value):
    return value in cls._value2member_map_

def bit_window(bits: int, offset: int, length: int) -> int:
  end = offset + length
  mask = 2**length - 1
  return (bits >> (bits.bit_length() - end)) & mask

class Packet:
  def __init__(self, bits: int, offset: int) -> None:
    # Offset in the transmission bits.
    self.offset = offset

    # Total bit length of this packet, including sub-packets.
    self.bit_length = 0

    self.version = self._read_version(bits)
    self.type = self._read_type(bits)

    if (self.type == PacketType.LITERAL):
      self.value = self._read_literal_value(bits)
    else:
      self.sub_packets = []

  def next_offset(self) -> int:
    return self.offset + self.bit_length

  def _read_version(self, bits: int) -> int:
    version = bit_window(bits, self.next_offset(), _VERSION_LENGTH)
    self.bit_length += _VERSION_LENGTH
    return version

  def _read_type(self, bits: int) -> PacketType:
    type_id = bit_window(bits, self.next_offset(), _TYPE_LENGTH)
    self.bit_length += _TYPE_LENGTH
    if (PacketType.has_value(type_id)):
      return PacketType(type_id)
    else:
      return PacketType.OPERATOR

  def _read_literal_value(self, bits: int) -> int:
    more = True
    value = 0
    while more:
      more = bool(bit_window(bits, self.next_offset(), _LITERAL_DONE_LENGTH))
      self.bit_length += _LITERAL_DONE_LENGTH
      group = int(bit_window(bits, self.next_offset(), _LITERAL_GROUP_LENGTH))
      self.bit_length += _LITERAL_GROUP_LENGTH
      value = (value << _LITERAL_GROUP_LENGTH) + group
    return value
  
  def __repr__(self) -> str:
    header = "Version={:d} Type={:s}".format(self.version, self.type.name)
    if (self.type == PacketType.LITERAL):
      data = "Value={:d}".format(self.value)
    else:
      data = "Operator"

    return "{:s} {:s}".format(header, data)


with open(_DATA_FILE, "r") as input:
  transmissions = input.readlines()

for hex_string in transmissions:
  print("Transmission received:", hex_string)
  bits = int(hex_string, 16)
  packet = Packet(bits, 0)
  print(packet)