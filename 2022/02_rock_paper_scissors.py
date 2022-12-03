_DATA_FILE = "2022/data/02_rock_paper_scissors.txt"

_ROCK_LETTER_THEM = 'A'
_ROCK_LETTER_ME = 'X'
_ROCK_SCORE = 1
_LOSE_SCORE = 0
_DRAW_SCORE = 3
_WIN_SCORE = 6

def me_throw_score(letter: str) -> int:
  return ord(letter) - ord(_ROCK_LETTER_ME) + _ROCK_SCORE

def them_throw_score(letter: str) -> int:
  return ord(letter) - ord(_ROCK_LETTER_THEM) + _ROCK_SCORE

def rps_score(them: str, me: str) -> int:
  # Rock-paper-scissors:
  # You win if you're 1 greater than your opponent mod 3 (1 mod 3).
  # You lose if you're 1 less than your opponent mod 3 (2 mod 3).
  # You draw if you're equal (0 mod 3).
  mod_diff = (me_throw_score(me) - them_throw_score(them)) % 3
  if mod_diff == 2:
    return _LOSE_SCORE
  elif mod_diff == 1:
    return _WIN_SCORE
  elif mod_diff == 0:
    return _DRAW_SCORE

games = []

with open(_DATA_FILE, "r") as input:
  games = [tuple(c.strip() for c in line.split(' ')) for line in input]

total_score = 0

for game in games:
  them = game[0]
  me = game[1]
  score = rps_score(them, me) + me_throw_score(me)
  print(str(score))
  total_score += score

print("Total: {t:d}".format(t = total_score))