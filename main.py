"""Pigeon Pitch, One Line: write the pitch to /output/entry.txt.

The pitch is a fixed line: a city pigeon, in its own voice, giving
investors the elevator pitch for its startup, NestEgg. Two investor
metrics get subverted by pigeon facts -- zero churn because the users
cannot leave the park, infinite runway because the founders live on the
roof -- which is the whole joke, told in one breath.

The grader runs this program in a sandbox with no network and reads
/output/entry.txt. The gate wants UTF-8 text of 1 to 200 characters,
not only white space, on exactly one line. This program writes the line
as bytes, reads it back, and only exits 0 once the bytes on disk pass
the same gate and match the pitch exactly, so what the judge reads is
exactly what was intended. No time, no randomness, no network, no
input: two runs write identical bytes.
"""

import os
import sys
from pathlib import Path

PITCH = (
    "Coo. NestEgg is raising a seed round: zero churn \u2014 our users "
    "can't leave the park \u2014 and infinite runway \u2014 we live on the roof."
)

MAX_CHARS = 200


def gate_ok(text):
    """Mirror the competition gate: 1-200 chars, one line, not blank.

    A stray control character would survive a plain length check but is
    not part of any pitch the judge should read, so the mirror rejects
    it too: the bytes on disk must be clean printable text.
    """
    if not 1 <= len(text) <= MAX_CHARS:
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    if any(ord(ch) < 32 for ch in text):
        return False
    return True


def output_path():
    """Where the grader reads the entry from."""
    base = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(base) / "entry.txt"


def main():
    if not gate_ok(PITCH):
        print("pitch fails the gate", file=sys.stderr)
        return 1
    target = output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(PITCH.encode("utf-8"))
    on_disk = target.read_bytes().decode("utf-8")
    if on_disk != PITCH or not gate_ok(on_disk):
        print("bytes on disk do not match the pitch", file=sys.stderr)
        return 1
    print(PITCH)
    print("chars: %d" % len(PITCH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
