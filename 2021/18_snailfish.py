from ast import literal_eval

_DATA_FILE = "2021/data/test/18_snailfish.txt"
_MAX_DEPTH = 4
_MAX_VALUE = 10

# A nested list of lists of numbers.
class SnailNode:
  def __init__(self, lists: list, parent: "SnailNode") -> None:
    (left, right) = (lists[0], lists[1])
    if (type(left) is list):
      self.left = SnailNode(left, self)
    else:
      self.left = int(left)

    if (type(right) is list):
      self.right = SnailNode(right, self)
    else:
      self.right = int(right)

    self.parent = parent

  # Propagates this SnailNode's values to the left and right,
  # and replaces itself with a 0.
  def explode(self) -> None:
    pass

  # Splits the left value into a SnailNode of two halves.
  def split_left(self) -> None:
    self.left = self._split_value(self.left)

  # Splits the right value into a SnailNode of two halves.
  def split_right(self) -> None:
    self.right = self._split_value(self.right)

  # Splits a value into a SnailNode, assigns its parent, and returns it.
  def _split_value(self, value: int) -> "SnailNode":
    return SnailNode([value / 2, value / 2 + 1], self)

  # Traverses through SnailTree and returns the first SnailNode at max depth.
  def _find_max_depth(self, max_depth: int) -> "SnailNode":
    pass

  # Reduces the SnailTree by exploding and splitting as necessary.
  def reduce(self) -> None:
    nest_level = 0
    while True:
      break
  
  def __repr__(self) -> str:
    return "[{:s},{:s}]".format(str(self.left), str(self.right))

lines = []
with open(_DATA_FILE, "r") as input:
  lines = input.readlines()

# I <3 Python
snail_numbers = [literal_eval(line) for line in lines]

for snail_number in snail_numbers:
  print(SnailNode(snail_number, None))