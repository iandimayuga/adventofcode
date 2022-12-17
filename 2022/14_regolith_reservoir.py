
_DEBUG = False
_DATA_FOLDER = "2022/data/test/" if _DEBUG else "2022/data/"
_DATA_FILE = _DATA_FOLDER + "14_regolith_reservoir.txt"

class Block:
  def __init__(self, x: int, y: int, char: str) -> None:
    self.x = x
    self.y = y
    self.char = char

  def __eq__(self, __o: "Block") -> bool:
    return (self.x, self.y) == (__o.x, __o.y)

  def __lt__(self, __o: "Block") -> bool:
    return self.distance < __o.distance
  
  def __hash__(self) -> int:
    return hash((self.x, self.y))
  
  def __str__(self) -> str:
    return "{x:d},{y:d} '{c:s}'".format(x = self.x, y = self.y, c = self.char)

lines = []
with open(_DATA_FILE, "r") as inputfile:
  lines = [line.strip() for line in inputfile]
