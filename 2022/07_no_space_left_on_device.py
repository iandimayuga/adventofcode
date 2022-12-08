import re

_DATA_FILE = "2022/data/test/07_no_space_left_on_device.txt"

_CHANGE_DIR_REGEX = re.compile("^\$ cd (?P<directory>.*)$")
_LIST_REGEX = re.compile("^\$ ls$")
_DIRECTORY_REGEX = re.compile("^dir (?P<directory>.*)$")
_FILE_REGEX = re.compile("^(?P<size>\d+) (?P<filename>.*)$")

class Directory:
  def __init__(self, parent: "Directory", name: str, depth: int) -> None:
    self.name = name
    self.parent = parent
    self.depth = depth
    self.children = []

  def add(self, child) -> None:
    self.children.append(child)

  def __str__(self) -> str:
    return "{pad:s}- {name:s} (dir)\n{children:s}".format(
      pad = "  "*self.depth,
      name = self.name,
      children = '\n'.join([str(child) for child in self.children])
    )

class File:
  def __init__(self, name: str, size: int, depth: int) -> None:
    self.name = name
    self.size = size
    self.depth = depth

  def __str__(self) -> str:
    return "{pad:s}- {name:s} (file, size={size:d})".format(
      pad = "  "*self.depth,
      name = self.name,
      size = self.size
    )

lines = []
with open(_DATA_FILE, "r") as input:
  lines = [line for line in input]


root = Directory(None, "/", 0)
root.add(Directory(root, "child", 1))
root.add(File("root.file", 42, 1))
root.children[0].add(File("child.file", 4, 2))

print(root)