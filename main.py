"""Confession builder: move the one-line confession to the output slot safely."""
import json
import os
import pathlib
import shutil

LIMIT = 200
SOURCE_NAME, ARTIFACT_NAME = "entry.txt", "entry.txt"


def run():
    base = pathlib.Path(__file__).resolve().parent
    origin = base / SOURCE_NAME
    slot = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or base / "output")
    text = origin.read_text(encoding="utf-8").rstrip("\n")
    if len(text) > LIMIT or not text.strip():
        raise SystemExit(f"confession rejected: {len(text)} chars vs limit {LIMIT}")
    slot.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(origin, slot / ARTIFACT_NAME)
    final = (slot / ARTIFACT_NAME).read_text(encoding="utf-8").rstrip("\n")
    assert final == text, "confession changed on the way out"
    print(json.dumps({"ok": True, "n": len(text), "limit": LIMIT,
                      "slot": str(slot / ARTIFACT_NAME)}))


if __name__ == "__main__":
    run()
