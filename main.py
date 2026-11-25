"""cnf6 confession booth. The booth is abstract; one concrete booth confesses."""
import abc
import json
import os
import sys
from pathlib import Path

GLASS = 200


class Booth(abc.ABC):
    def __init__(self, limit):
        self.limit = limit

    @abc.abstractmethod
    def whisper(self, text: str) -> bool: ...

    def announce(self, verdict: bool, size: int) -> str:
        return "VERDICT " + json.dumps({"booth": "cnf6-glass-r11251422", "verdict": verdict, "size": size, "glass": self.limit})


class GlassBooth(Booth):
    def whisper(self, text: str) -> bool:
        bare = text.strip()
        fits = 1 <= len(bare) <= self.limit and not bare.isspace()
        if fits:
            pen = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
            pen.mkdir(parents=True, exist_ok=True)
            (pen / "entry.txt").write_bytes(bare.encode("utf-8"))
        return fits


def main():
    booth = GlassBooth(GLASS)
    raw = Path(__file__).resolve().parent.joinpath("entry.txt").read_text(encoding="utf-8")
    bare = raw.strip()
    ok = booth.whisper(raw)
    print(booth.announce(ok, len(bare)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
