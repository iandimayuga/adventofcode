from ast import literal_eval
from enum import Enum, auto

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

  # Propagates the left SnailNode's values to the left and right,
  # and replaces it with a 0.
  def explode_left(self) -> None:
    self.left = self._explode_node(self.left)

  # Propagates the right SnailNode's values to the left and right,
  # and replaces it with a 0.
  def explode_right(self) -> None:
    self.right = self._explode_node(self.right)
  
  # Propagates the SnailNode's values to the left and right in the tree.
  def _explode_node(self, node: "SnailNode") -> "SnailNode":
    if (node.type == NodeType.LEFT):
      # Propagate left number to the left.
      current = node.parent
      while current.type == NodeType.LEFT:
        current = current.parent
      if (current.type == NodeType.RIGHT):
        current = current.parent
        while current.value is None:
          current = current.right
        current.value += node.left.value
      # Propagate right number to the right.
      current = node.parent.right
      while current.value is None:
        current = current.left
      current.value += node.right.value
    elif (node.type == NodeType.RIGHT):
      # Propagate right number to the right.
      current = node.parent
      while current.type == NodeType.LEFT:
        current = current.parent
      if (current.type == NodeType.RIGHT):
        current = current.parent
        while current.value is None:
          current = current.left
        current.value += node.right.value
      # Propagate left number to the left.
      current = node.parent.left
      while current.value is None:
        current = current.right
      current.value += node.left.value

    return SnailNode(0, self, node.type)
    

  # Splits the left value into a SnailNode of two halves.
  def split_left(self) -> None:
    self.left = self._split_value(self.left, NodeType.LEFT)

  # Splits the right value into a SnailNode of two halves.
  def split_right(self) -> None:
    self.right = self._split_value(self.right, NodeType.RIGHT)

  # Splits a value into a SnailNode, assigns its parent, and returns it.
  def _split_value(self, node: "SnailNode", type: NodeType) -> "SnailNode":
    return SnailNode([node.value / 2, node.value / 2 + 1], self, type)

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
node.left.left.left.explode_left()
print(node)