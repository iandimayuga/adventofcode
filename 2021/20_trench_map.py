
_DATA_FILE = "2021/data/test/20_trench_map.txt"
_IMAGE_FILE_OFFSET = 2
_ITERATIONS = 2
_ON_PIXEL = '#'
_OFF_PIXEL = '.'

class Image:
  # Input image is row-major.
  def __init__(self, input_image: list[list[bool]], enhancement_lookup: list[bool]) -> None:
    self.image = input_image
    self.enhancement_lookup = enhancement_lookup

  def __repr__(self) -> str:
    return '\n'.join(
      [''.join(
        ['#' if pixel else '.' for pixel in line]
      ) for line in input_image])

lines = []
with open(_DATA_FILE, "r") as input:
  lines = input.readlines()

enhancement_string = lines[0].strip()
enhancement_lookup = [(char == _ON_PIXEL) for char in enhancement_string]

image_width_initial = len(lines[_IMAGE_FILE_OFFSET].strip())
image_height_initial = len(lines) - _IMAGE_FILE_OFFSET

input_image = [[] for y in range(image_height_initial)]

y = 0
for line in lines[_IMAGE_FILE_OFFSET:]:
  input_image[y] = [(char == _ON_PIXEL) for char in line.strip()]
  y += 1

image = Image(input_image, enhancement_lookup)
print(image)