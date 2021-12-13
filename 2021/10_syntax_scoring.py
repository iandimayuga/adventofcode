
_DATA_FILE = "2021/data/10_syntax_scoring.txt"

_CLOSE_BRACES = {
  ')':'(',
  ']':'[',
  '}':'{',
  '>':'<',
  }

_OPEN_BRACES = {open: close for close, open in _CLOSE_BRACES.items()}

_CLOSE_SCORES = {
  ')':3,
  ']':57,
  '}':1197,
  '>':25137,
  }

def evaluate(line: str) -> str:
  stack = []
  for brace in line:
    if brace in _CLOSE_BRACES:
      match = _CLOSE_BRACES[brace]
      if not stack or stack[-1] != match:
        score = _CLOSE_SCORES[brace]
        print(
          line,
          "Expected {:s} but found {:s} instead. Score {:d}"
            .format(_OPEN_BRACES[stack[-1]], brace, score))
        return score
      else:
        stack.pop()
    else:
      stack.append(brace)
  
  if stack:
    print(line, "Incomplete?")
    return 0
  else:
    print(line, "Complete!")
    return 0

lines = []
with open(_DATA_FILE, "r") as input:
  lines = input.readlines()

score = 0
for line in lines:
  score += evaluate(line.strip())

print("Total score:", score)
