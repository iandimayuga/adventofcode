import re
from tkinter import W

_DATA_FILE = "2022/data/07_no_space_left_on_device.txt"

_CHANGE_DIR_REGEX = re.compile(r"^\$ cd (?P<dirname>\w*)$")
_PARENT_DIR_REGEX = re.compile(r"^\$ cd \.\.$")
_LIST_REGEX = re.compile(r"^\$ ls$")
_DIRECTORY_REGEX = re.compile(r"^dir (?P<dirname>.*)$")
_FILE_REGEX = re.compile(r"^(?P<size>\d+) (?P<filename>.*)$")

_MAX_DIR_SIZE_TO_COUNT = 100000
_MAX_TOTAL_SPACE = 40000000

class Directory:
  def __init__(self, parent: "Directory", name: str, depth: int) -> None:
    self.name = name
    self.parent = parent
    self.depth = depth
    self.children = {}
    self.dir_size = 0
    self.is_size_cached = False

  def add(self, child: "Directory") -> None:
    self.is_size_cached = False
    self.children[child.name] = child

  def add(self, child: "File") -> None:
    self.is_size_cached = False
    self.children[child.name] = child

  def size(self) -> int:
    if not self.is_size_cached:
      self.dir_size = sum([child.size() for child in self.children.values()])
      self.is_size_cached = True
    return self.dir_size

  def __str__(self) -> str:
    return "{pad:s}- {name:s} (dir)\n{children:s}".format(
      pad = "  "*self.depth,
      name = self.name,
      children = '\n'.join([str(child) for child in self.children.values()])
    )

class File:
  def __init__(self, name: str, size: int, depth: int) -> None:
    self.name = name
    self.file_size = size
    self.depth = depth
  
  def size(self) -> int:
    return self.file_size

  def __str__(self) -> str:
    return "{pad:s}- {name:s} (file, size={size:d})".format(
      pad = "  "*self.depth,
      name = self.name,
      size = self.file_size
    )

lines = []
with open(_DATA_FILE, "r") as input:
  lines = [line.strip() for line in input]

root = Directory(None, "/", 0)
working_dir = root
all_dirs = []

# skip "$ cd /"
for line in lines[1:]:
  # Parse the command or output.
  change_dir_match = re.match(_CHANGE_DIR_REGEX, line)
  parent_dir_match = re.match(_PARENT_DIR_REGEX, line)
  list_match = re.match(_LIST_REGEX, line)
  directory_match = re.match(_DIRECTORY_REGEX, line)
  file_match = re.match(_FILE_REGEX, line)

  if change_dir_match:
    dirname = change_dir_match.group("dirname")
    print("{line:s}: Change to dir '{dir:s}'".format(line = line, dir = dirname))
    working_dir = working_dir.children[dirname]
  elif parent_dir_match:
    print("{line:s}: Change to parent dir".format(line = line))
    working_dir = working_dir.parent
  elif list_match:
    print("{line:s}: List current directory".format(line = line))
    # Do nothing, the following output will add stuff to the working dir.
  elif directory_match:
    dirname = directory_match.group("dirname")
    print("{line:s}: Child directory '{dir:s}'".format(line = line, dir = dirname))
    dir = Directory(working_dir, dirname, working_dir.depth + 1)
    working_dir.add(dir)
    all_dirs.append(dir)
  elif file_match:
    filename = file_match.group("filename")
    size = int(file_match.group("size"))
    print("{line:s}: File '{file:s}' with size {size:d}".format(line = line, file = filename, size = size))
    working_dir.add(File(filename, size, working_dir.depth + 1))

print(root)

# Iterate through dirs and sum sizes under the limit.
print("Total size of dirs over {max:d}: {total:d}".format(
  max = _MAX_DIR_SIZE_TO_COUNT,
  total = sum([dir.size() for dir in all_dirs if dir.size() <= _MAX_DIR_SIZE_TO_COUNT])
))

# Find the smallest directory to delete to recover the required size.
print("Total size taken up: {size:d}".format(size = root.size()))
min_size_to_delete = root.size() - _MAX_TOTAL_SPACE
size_to_delete = min([dir.size() for dir in all_dirs if dir.size() >= min_size_to_delete])
print("Size of directory to delete: {size: d}".format(size = size_to_delete))
