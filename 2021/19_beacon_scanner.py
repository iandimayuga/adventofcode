import typing
_DATA_FILE = "2021/data/test/19_beacon_scanner.txt"

class Vector:
  def __init__(self, x, y, z) -> None:
    self.x = x
    self.y = y
    self.z = z

def rot90(vector: tuple[int, int, int]):
  pass

def rotations_in_plane(vectors: array, axes: tuple[int, int]) -> list[array]:
  return [rot90(vectors, i, axes) for i in range(4)]

def rotations_in_space(vectors: array) -> list[array]:
  # Around x and -x axes.
  yield from rotations_in_plane(rot90(vectors,  0, (0,1)), (1,2))
  yield from rotations_in_plane(rot90(vectors,  2, (0,1)), (1,2))

  # Around y and -y axes.
  yield from rotations_in_plane(rot90(vectors,  1, (0,1)), (0,2))
  yield from rotations_in_plane(rot90(vectors, -1, (0,1)), (0,2))

  # Around z and -z axes.
  yield from rotations_in_plane(rot90(vectors,  1, (0,2)), (0,1))
  yield from rotations_in_plane(rot90(vectors, -1, (0,2)), (0,1))

if __name__ == '__main__':
  with open(_DATA_FILE, "r") as input:
    lines = input.readlines()

  test_array = array([
    [
      [1,1,0],[],[],
    ],
    [
      [],[],[],
    ],
    [
      [],[],[],
    ],
  ])