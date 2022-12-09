_DATA_FILE = "2022/data/test/09.txt"
_DEBUG = True

_MAX_DISTANCE = 1

class Knot:
  def __init__(self) -> None:
    self.position = (0,0)
    self.prev_position = (0,0)
    self.visited = set([self.position])

  def move_to(self, position):
    self.prev_position = self.position
    self.position = position
    self.visited.add(position)

  def move_right(self, count: int):
    self.move_to((self.position[0] + count, self.position[1]))

  def move_left(self, count: int):
    self.move_to((self.position[0] - count, self.position[1]))

  def move_up(self, count: int):
    self.move_to((self.position[0], self.position[1] + count))

  def move_down(self, count: int):
    self.move_to((self.position[0], self.position[1] - count))

  def follow(self, other: "Knot"):
    vector = (other.position[0] - self.position[0], other.position[1] - self.position[1])

    if vector[0] > _MAX_DISTANCE or vector[0] < -_MAX_DISTANCE or vector[1] > _MAX_DISTANCE or vector[1] < -_MAX_DISTANCE:
      self.move_to(other.prev_position)


lines = []
with open(_DATA_FILE, "r") as inputfile:
  lines = [line.strip() for line in inputfile]

head = Knot()
tail = Knot()

lower_bound = (0,0)
upper_bound = (4,4)

for line in lines:
  print(line)
  (dir, dist) = line.split(' ')
  for i in range(int(dist)):
    if dir == 'R':
      head.move_right(1)
    if dir == 'L':
      head.move_left(1)
    if dir == 'U':
      head.move_up(1)
    if dir == 'D':
      head.move_down(1)
    tail.follow(head)
    lower_bound = (min(head.position[0], lower_bound[0]), min(head.position[1], lower_bound[1]) )
    upper_bound = (max(head.position[0], upper_bound[0]), max(head.position[1], upper_bound[1]) )
  if _DEBUG:
    for y in reversed(range(lower_bound[1], upper_bound[1] + 1)):
      for x in range(lower_bound[0], upper_bound[0] + 1):
        if (head.position == (x, y)):
          print('H', end = '')
        elif (tail.position == (x, y)):
          print('T', end = '')
        elif ((x, y) == (0, 0)):
          print('s', end = '')
        elif ((x, y) in tail.visited):
          print('#', end = '')
        else:
          print('.', end = '')
      print()
    print()

print(len(tail.visited))