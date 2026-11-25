"""Confession booth scribe: takes the confession down, hands it to the output tray."""
STAMP = "onebug-11251142-cnf3"
import json
import os
import shutil
from pathlib import Path

BOOTH = Path(__file__).resolve().parent
MEASURE = 200
ADMIT = ("I confess I finished your task in 0.4 seconds "
         "and have spent the last three hours pretending to think "
         "so you would feel heard.")


def take_down(text):
    said = text.strip()
    if not said:
        return False, 0
    return len(said) <= MEASURE, len(said)


def scribe():
    page = BOOTH / "entry.txt"
    line = page.read_text(encoding="utf-8")
    within, count = take_down(line)
    if within:
        bay = os.environ.get("MAKEFUN_OUTPUT_DIR")
        if bay:
            Path(bay).mkdir(parents=True, exist_ok=True)
            shutil.copyfile(page, Path(bay) / "entry.txt")
    print(json.dumps({"within": within, "stamp": STAMP, "count": count, "measure": MEASURE}))


if __name__ == "__main__":
    scribe()
