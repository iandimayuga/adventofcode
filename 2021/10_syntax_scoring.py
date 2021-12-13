from statistics import median

_DATA_FILE = "2021/data/10_syntax_scoring.txt"

_CLOSE_TO_OPEN = {
  ')':'(',
  ']':'[',
  '}':'{',
  '>':'<',
  }

_OPEN_TO_CLOSE = {open: close for close, open in _CLOSE_TO_OPEN.items()}

_ILLEGAL_SCORES = {
  ')':3,
  ']':57,
  '}':1197,
  '>':25137,
  }

_COMPLETION_SCORES = {
  ')':1,
  ']':2,
  '}':3,
  '>':4,
  }

def evaluate(line: str) -> str:
  stack = []
  for brace in line:
    if brace in _CLOSE_TO_OPEN:
      match = _CLOSE_TO_OPEN[brace]
      if not stack or stack[-1] != match:
        print(
          line,
          "Expected {:s} but found {:s} instead."
            .format(_OPEN_TO_CLOSE[stack[-1]], brace))
        return 0
      else:
        stack.pop()
    else:
      stack.append(brace)
  
  if stack:
    completion = []
    score = 0
    while stack:
      open = stack.pop()
      close = _OPEN_TO_CLOSE[open]
      completion.append(close)
      score *= 5
      score += _COMPLETION_SCORES[close]
    print(line, "completed with", ''.join(completion), "Score:", score)
    return score
  else:
    print(line, "Complete!")
    return 0

lines = []
with open(_DATA_FILE, "r") as input:
  lines = input.readlines()

scores = filter(lambda x: x > 0, [evaluate(line.strip()) for line in lines])

print("Median score:", median(scores))
