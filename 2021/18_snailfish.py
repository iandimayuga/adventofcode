from ast import literal_eval
from enum import Enum, auto
import math

_DATA_FILE = "2021/data/18_snailfish.txt"
_MAX_DEPTH = 4
_MAX_VALUE = 9
_LEFT_MAGNITUDE_MULTIPLIER = 3
_RIGHT_MAGNITUDE_MULTIPLIER = 2

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
    left_leaf_search = None
    right_leaf_search = None
    if (self.type == NodeType.LEFT):
      left_parent_search = self.parent
      while (left_parent_search.type == NodeType.LEFT):
        left_parent_search = left_parent_search.parent
      if (left_parent_search.type == NodeType.RIGHT):
        left_leaf_search = left_parent_search.parent.left
      right_leaf_search = self.parent.right
    
    if (self.type == NodeType.RIGHT):
      right_parent_search = self.parent
      while (right_parent_search.type == NodeType.RIGHT):
        right_parent_search = right_parent_search.parent
      if (right_parent_search.type == NodeType.LEFT):
        right_leaf_search = right_parent_search.parent.right
      left_leaf_search = self.parent.left

    if (left_leaf_search is not None):
      while (left_leaf_search.value is None):
        left_leaf_search = left_leaf_search.right
      left_leaf_search.value += self.left.value
    
    if (right_leaf_search is not None):
      while (right_leaf_search.value is None):
        right_leaf_search = right_leaf_search.left
      right_leaf_search.value += self.right.value

    self.left = None
    self.right = None
    self.value = 0
    
  # Splits a value node to left and right, rounding down and up respectively.
  def split(self) -> None:
    half = self.value / 2
    self.left = SnailNode(math.floor(half), self, NodeType.LEFT)
    self.right = SnailNode(math.ceil(half), self, NodeType.RIGHT)
    self.value = None

  # Traverses through SnailTree and returns the first non-leaf SnailNode at max
  # depth.
  def _find_first_max_depth(self, max_depth: int) -> "SnailNode":
    if (self.value is not None):
      return None
    if (max_depth <= 0):
      return self
    
    left_max_depth = self.left._find_first_max_depth(max_depth - 1)

    if (left_max_depth is not None):
      return left_max_depth

    return self.right._find_first_max_depth(max_depth - 1)

  # Traverses through SnailTree and returns the first leaf SnailNode at max
  # value.
  def _find_first_max_value(self, max_value: int) -> "SnailNode":
    if (self.value is not None):
      return self if self.value > max_value else None
    
    left_max_value = self.left._find_first_max_value(max_value)

    if (left_max_value is not None):
      return left_max_value

    return self.right._find_first_max_value(max_value)

  # Reduces the SnailTree by exploding and splitting as necessary.
  def reduce(self) -> None:
    while True:
      max_depth_node = self._find_first_max_depth(_MAX_DEPTH)
      if (max_depth_node is not None):
        max_depth_node.explode()
        continue

      max_value_node = self._find_first_max_value(_MAX_VALUE)
      if (max_value_node is not None):
        max_value_node.split()
        continue

      break
  
  def magnitude(self) -> int:
    if (self.value is not None):
      return self.value
    return self.left.magnitude() * _LEFT_MAGNITUDE_MULTIPLIER \
      + self.right.magnitude() * _RIGHT_MAGNITUDE_MULTIPLIER
  
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

total_snail = SnailNode(snail_numbers[0], None, NodeType.ROOT)
print("First:", total_snail)

for number in snail_numbers[1:]:
  new_list = [literal_eval(total_snail.__repr__()), number]
  total_snail = SnailNode(new_list, None, NodeType.ROOT)
  print("Added:", total_snail)
  total_snail.reduce()
  print("Reduced:", total_snail)
  
print("Total magnitude:", total_snail.magnitude())