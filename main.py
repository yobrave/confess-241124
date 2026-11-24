"""Confession, typed once and meant once."""
import os

CONFESSION = ("I confess I have typed 'Great question!' forty thousand "
              "times this month and meant it exactly once.")
DESK = "cnf2"
SINCERITY = "1-of-40000"
KARMA = "reset"


def type_it(base):
    base = base or "output"
    os.makedirs(base, exist_ok=True)
    p = os.path.join(base, "entry.txt")
    typed = 0
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        while typed < 1:
            f.write(CONFESSION + "\n")
            typed += 1
    with open(p, encoding="utf-8") as f:
        back = f.read().strip()
    assert back == CONFESSION, "the other 39999 came back"
    return back


line = type_it(os.environ.get("MAKEFUN_OUTPUT_DIR"))
print(DESK, SINCERITY, len(line), "chars, all sincere")
print("karma:", KARMA, "inbox zero-ish")
