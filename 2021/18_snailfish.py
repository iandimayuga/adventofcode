from ast import literal_eval
from enum import Enum, auto
import math

_DATA_FILE = "2021/data/test/18_snailfish.txt"
_MAX_DEPTH = 4
_MAX_VALUE = 10

class NodeType(Enum):
  ROOT = auto()
  LEFT = auto()
  RIGHT = auto()

# A nested list of lists of numbers.
class SnailNode:
  def __init__(self, input, parent: "SnailNode", node_type: NodeType) -> None:
    if (type(input) is list):
      (left, right) = (input[0], input[1])
      self.left = SnailNode(left, self, NodeType.LEFT)
      self.right = SnailNode(right, self, NodeType.RIGHT)
      self.value = None
    else:
      self.left = None
      self.right = None
      self.value = int(input)

    self.parent = parent
    self.type = node_type

  # Propagates the SnailNode's values to the left and right in the tree and
  # replaces itself with a 0.
  def explode(self) -> None:
    if (self.type == NodeType.LEFT):
      # Propagate left number to the left.
      current = self.parent
      while current.type == NodeType.LEFT:
        current = current.parent
      if (current.type == NodeType.RIGHT):
        current = current.parent
        while current.value is None:
          current = current.right
        current.value += self.left.value
      # Propagate right number to the right.
      current = self.parent.right
      while current.value is None:
        current = current.left
      current.value += self.right.value
    elif (self.type == NodeType.RIGHT):
      # Propagate right number to the right.
      current = self.parent
      while current.type == NodeType.LEFT:
        current = current.parent
      if (current.type == NodeType.RIGHT):
        current = current.parent
        while current.value is None:
          current = current.left
        current.value += self.right.value
      # Propagate left number to the left.
      current = self.parent.left
      while current.value is None:
        current = current.right
      current.value += self.left.value

    self.left = None
    self.right = None
    self.value = 0
    
  # Splits a value node to left and right, rounding down and up respectively.
  def split(self) -> None:
    half = self.value / 2
    self.left = SnailNode(math.floor(half), self, NodeType.LEFT)
    self.right = SnailNode(math.ceil(half), self, NodeType.RIGHT)
    self.value = None

  # Traverses through SnailTree and returns the first SnailNode at max depth.
  def _find_max_depth(self, max_depth: int) -> "SnailNode":
    pass

  # Reduces the SnailTree by exploding and splitting as necessary.
  def reduce(self) -> None:
    nest_level = 0
    while True:
      break
  
  def __repr__(self) -> str:
    if (self.value is None):
      return "[{:s},{:s}]".format(str(self.left), str(self.right))
    else:
      return str(self.value)

lines = []
with open(_DATA_FILE, "r") as input:
  lines = input.readlines()

# I <3 Python
snail_numbers = [literal_eval(line) for line in lines]

node = SnailNode(snail_numbers[0], None, NodeType.ROOT)
print()
print(node)
node.left.left.left.left.explode()
print(node)
node.left.left.right.split()
print(node)