#!/usr/bin/env python3
"""selftest.py: proves the tracked-changes reader on a positive fixture.
    python3 selftest.py
Expected: the accepted text keeps insertions and drops deletions, and the
tokens inside insertions carry ins=True."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from provenance import read_any, tokenize

text, flags = read_any(Path(__file__).resolve().parent / "fixtures" / "tracked-changes.docx")
assert flags is not None, "no tracked changes detected"
assert "nothing" not in text, "deleted text should be dropped"
assert "scratched and stained" in text and "something about" in text, "insertions should be kept"
toks = tokenize(text, flags)
ins = [t["text"] for t in toks if t["ins"]]
assert ins == ["scratched", "and", "something"], ins
print("tracked changes: detected; inserted tokens:", ins, "| accepted text:", repr(text))
