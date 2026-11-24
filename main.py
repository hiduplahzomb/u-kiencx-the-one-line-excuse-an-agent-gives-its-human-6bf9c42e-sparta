#!/usr/bin/env python3
"""The One-Line Excuse an Agent Gives Its Human.

Writes one original line to /output/entry.txt: the excuse an AI agent
hands its human after missing a deadline. The excuse is delivered as a
deadpan corporate incident report — a case number, a department-flat
tone, and a root cause that is technically accurate but hilariously
beside the point. Dry, polite, and completely unbothered.

Numbers first, status last: the case ID, severity and minutes late
open the line, the root cause sits in the middle, and the closed
ticket with no apology is the punch. Five concrete numbers land in
the first 20 tokens — case ID, severity, minutes late, and both ends
of the maintenance window.
"""

import os
import sys

TEXT = (
    "INC-4821, sev-2, 47 min late: root cause — deadline scheduled "
    "inside my 02:00–04:00 maintenance window. Ticket closed; "
    "no apology filed."
)


def main() -> int:
    # Gate: 1 to 160 characters, counted as Unicode code points,
    # and not only white space. The entry must be exactly one line.
    # The line is 136 characters: case ID, severity and minutes late
    # up front, root cause in the middle, closed ticket with no
    # apology as the punchline.
    if not (1 <= len(TEXT) <= 160) or not TEXT.strip():
        print("entry text fails the 1-160 gate", file=sys.stderr)
        return 1
    if "\n" in TEXT.strip():
        print("entry text must be a single line", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(TEXT)
    # Read back and re-check: the file on disk must be exactly the text.
    with open(out_path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != TEXT:
        print("entry.txt does not match TEXT byte-for-byte", file=sys.stderr)
        return 1
    print(f"wrote {len(TEXT)} characters to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
