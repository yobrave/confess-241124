import codecs
import json
import os

STAMP = "cnf3-absolved"
LIMIT = 200


def pull(base):
    handle = codecs.open(os.path.join(base, "entry.txt"), "r", encoding="utf-8")
    try:
        return handle.read()
    finally:
        handle.close()


def first_with_ink(block):
    rows = (row.rstrip("\r") for row in block.replace("\r\n", "\n").split("\n"))
    chosen = next((r for r in rows if r.strip()), "")
    return chosen


def inspect(line):
    problems = []
    if not line.strip():
        problems.append("confession empty")
    if len(line) > LIMIT:
        problems.append("confession over limit")
    return problems


def stow(line, base):
    cave = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    if not os.path.isdir(cave):
        os.makedirs(cave)
    path = os.path.join(cave, "entry.txt")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        os.write(fd, line.encode("utf-8"))
    finally:
        os.close(fd)
    if codecs.open(path, "r", encoding="utf-8").read() != line:
        raise RuntimeError("stow echo differs")
    return path


where = os.path.dirname(os.path.abspath(__file__))
line = first_with_ink(pull(where))
bad = inspect(line)
if bad:
    print('{"verdict": "held", "why": %s}' % json.dumps(bad[0]))
    raise SystemExit(1)
hole = stow(line, where)
print('{"verdict": "released", "size": %d, "stamp": "%s", "hole": %s}' % (len(line), STAMP, json.dumps(os.path.basename(hole))))
