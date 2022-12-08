_DATA_FILE = "2022/data/08_treetop_tree_house.txt"

grid = []
with open(_DATA_FILE, "r") as input:
  for line in input:
    grid.append([int(c) for c in line.strip()])

print(grid)

visible = [[False] * len(grid[0]) for i in range(len(grid))]

for i in range(len(grid)):
  running_max = -1
  for j in range(len(grid[0])):
    height = grid[i][j]
    if height > running_max:
      visible[i][j] = True
      print("{height:d} at {i:d},{j:d} is visible from left".format(
        height = height, i = i, j = j
      ))
    running_max = max(running_max, height)

  running_max = -1
  for j in reversed(range(len(grid[0]))):
    height = grid[i][j]
    if height > running_max:
      visible[i][j] = True
      print("{height:d} at {i:d},{j:d} is visible from right".format(
        height = height, i = i, j = j
      ))
    running_max = max(running_max, height)

for j in range(len(grid[0])):
  running_max = -1
  for i in range(len(grid)):
    height = grid[i][j]
    if height > running_max:
      visible[i][j] = True
      print("{height:d} at {i:d},{j:d} is visible from above".format(
        height = height, i = i, j = j
      ))
    running_max = max(running_max, height)

  running_max = -1
  for i in reversed(range(len(grid))):
    height = grid[i][j]
    if height > running_max:
      visible[i][j] = True
      print("{height:d} at {i:d},{j:d} is visible from below".format(
        height = height, i = i, j = j
      ))
    running_max = max(running_max, height)

num_visible = 0
for i in range(len(grid)):
  for j in range(len(grid[0])):
    if visible[i][j]:
      num_visible += 1

print(num_visible)