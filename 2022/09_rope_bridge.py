_DATA_FILE = "2022/data/09_rope_bridge.txt"
_DEBUG = False

_MAX_DISTANCE = 1
_NUM_KNOTS = 10

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

    # If the other knot is too far away, we need to move.
    if vector[0] > _MAX_DISTANCE or vector[0] < -_MAX_DISTANCE or vector[1] > _MAX_DISTANCE or vector[1] < -_MAX_DISTANCE:
      if (vector[0] == 0):
        # Same column, only need to move up or down (normalize the y component).
        self.move_to((self.position[0], self.position[1] + (vector[1] / abs(vector[1]))))
      elif (vector[1] == 0):
        # Same row, only need to move left or right (normalize the x component).
        self.move_to((self.position[0] + (vector[0] / abs(vector[0])), self.position[1]))
      else:
        # Different row and column, always move diagonally (normalize the whole vector).
        self.move_to((self.position[0] + (vector[0] / abs(vector[0])), self.position[1] + (vector[1] / abs(vector[1]))))


lines = []
with open(_DATA_FILE, "r") as inputfile:
  lines = [line.strip() for line in inputfile]

knots = [Knot() for i in range(_NUM_KNOTS)]
head = knots[0]
tail = knots[9]

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
    for i in range(1, _NUM_KNOTS):
      knots[i].follow(knots[i - 1])
    lower_bound = (min(head.position[0], lower_bound[0]), min(head.position[1], lower_bound[1]) )
    upper_bound = (max(head.position[0], upper_bound[0]), max(head.position[1], upper_bound[1]) )
  if _DEBUG:
    for y in reversed(range(lower_bound[1], upper_bound[1] + 1)):
      for x in range(lower_bound[0], upper_bound[0] + 1):
        if (head.position == (x, y)):
          print('H', end = '')
          continue
        knot_printed = False
        for i in range(1, _NUM_KNOTS):
          if knots[i].position == (x, y):
            print(i, end = '')
            knot_printed = True
            break
        if (knot_printed):
          continue
        if ((x, y) == (0, 0)):
          print('s', end = '')
          continue
        if ((x, y) in tail.visited):
          print('#', end = '')
          continue
        print('.', end = '')
      print()
    print()

print(len(tail.visited))