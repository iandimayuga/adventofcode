_DATA_FILE = "2022/data/02_rock_paper_scissors.txt"

_ROCK_LETTER_THEM = 'A'
_ROCK_LETTER_ME = 'X'
_ROCK_SCORE = 1
_LOSE_SCORE = 0
_DRAW_SCORE = 3
_WIN_SCORE = 6

_LOSE_OUTCOME_LETTER = 'X'
_LOSE_OUTCOME_MOD_DIFF = 2

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
    return _LOSE_SCORE + me_throw_score(me)
  elif mod_diff == 1:
    return _WIN_SCORE + me_throw_score(me)
  elif mod_diff == 0:
    return _DRAW_SCORE + me_throw_score(me)

# Determine the desired mod-diff based on the prescribed outcome.
def outcome_mod_diff(letter: str) -> int:
  return (ord(letter) - ord(_LOSE_OUTCOME_LETTER) + _LOSE_OUTCOME_MOD_DIFF) % 3

def needed_throw(them: str, outcome: str) -> str:
  # me - them = outcome, mod 3
  # me = outcome + them, mod 3
  me_throw_score = (outcome_mod_diff(outcome) + them_throw_score(them)) % 3
  return chr((me_throw_score - _ROCK_SCORE) % 3 + ord(_ROCK_LETTER_ME))

games = []

with open(_DATA_FILE, "r") as input:
  games = [tuple(c.strip() for c in line.split(' ')) for line in input]

total_score = 0

for game in games:
  them = game[0]
  outcome = game[1]
  me = needed_throw(them, outcome)
  score = rps_score(them, me)
  print("Them: {them:s} Me: {me:s} Outcome: {outcome_mod_diff:d} Throw Score: {me_throw_score:d} RPS Score: {rps_score:d}".format(
    them = them,
    me = me,
    outcome_mod_diff = outcome_mod_diff(outcome),
    me_throw_score = me_throw_score(me),
    rps_score = rps_score(them, me)
  ))
  total_score += score

print("Total: {t:d}".format(t = total_score))