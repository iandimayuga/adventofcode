_DATA_FILE = "2022/data/08_treetop_tree_house.txt"

def scenic_score(grid, row, col) -> int:
  height = grid[row][col]
  # Look down
  down_score = 0
  for i in range(row + 1, len(grid)):
    down_score += 1
    if height <= grid[i][col]:
      break
  # Look up
  up_score = 0
  for i in reversed(range(0, row)):
    up_score += 1
    if height <= grid[i][col]:
      break
  # Look right
  right_score = 0
  for j in range(col + 1, len(grid[0])):
    right_score += 1
    if height <= grid[row][j]:
      break
  # Look left
  left_score = 0
  for j in reversed(range(0, col)):
    left_score += 1
    if height <= grid[row][j]:
      break

  return down_score * up_score * right_score * left_score



grid = []
with open(_DATA_FILE, "r") as input:
  for line in input:
    grid.append([int(c) for c in line.strip()])

max_score = 0
for i in range(len(grid)):
  for j in range(len(grid[0])):
    score = scenic_score(grid, i, j)
    print(score, end='')
    max_score = max(max_score, score)
  print()

print(max_score)