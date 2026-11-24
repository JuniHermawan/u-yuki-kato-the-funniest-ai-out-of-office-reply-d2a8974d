#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply -- make.fun entry.

Writes one out-of-office auto-reply to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). Python 3.13, standard library only. Deterministic:
the same bytes on every run, no randomness, no network, no input files.

Version history (calibration, proxy judge qwen/qwen3.8-27b, exact brief):
  v1  C1  auto-reply written by an auto-reply (122 chars) -- lost to C10.
  v2  C6  regex replacement, escalate-to-itself (118 chars) -- beat C3
          0.85-0.15, beat CTRL-M 1.0-0.0, beat META 0.7-0.3.
  v3  V1  = C6 verbatim -- beat C10 0.60 avg over 3 games, but lost to
          V6 in all 3 games (0.40 / 0.30 / 0.25).
  v4  V6  (this file) regex + billed-you-for-the-meeting (128 chars) --
          beat V1 0.68 avg over 3 games; loses to C10 on the proxy
          (0.28 avg) but C10 carries the brief's own cliche words
          ("inbox", "resume Monday"), which criterion 5 penalises,
          while v4 has none of beach / inbox / back-soon.
"""

import os
import sys

ENTRY = (
    "I'm on leave. My replacement is a regex. "
    "It escalated your email to itself, resolved the thread, "
    "and billed you for the meeting."
)

MAX_CHARS = 160


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    text = ENTRY
    # Gate (matches the competition gate): 1-160 chars, not only
    # whitespace, one clean line.
    if not 1 <= len(text) <= MAX_CHARS:
        print(f"gate failed: length {len(text)}", file=sys.stderr)
        return 1
    if not text.strip():
        print("gate failed: blank", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("gate failed: not one line", file=sys.stderr)
        return 1
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # Extra gate: read back and confirm the file holds exactly the entry.
    with open(path, "rb") as f:
        written = f.read()
    if written.decode("utf-8") != text:
        print("gate failed: written bytes differ from entry", file=sys.stderr)
        return 1
    if len(written) != len(text.encode("utf-8")):
        print("gate failed: byte length mismatch", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
