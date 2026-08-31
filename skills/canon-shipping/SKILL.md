---
name: canon-shipping
description: The discipline for editing craft-files canon. Use whenever applying ratified edits to canon files, delivering candidate edits for ratification, or checking prose and diffs against house typography and the marked lexicon. Trigger on "ship this edit", "apply the ruling", "canon edit", "deliver a candidate", or any change to files in the craft-files project or repository, even a one-line edit. Do NOT hand-edit canon without it; drift between copies is how the V3.1 batch nearly forked.
---

# Shipping canon edits

*Provenance: machine-drafted July 9, 2026, at the writer's direction; the tool reproduced that day's ratified README and LICENSE edits byte for byte before delivery; no human pass yet.*

## The discipline

1. State the authoritative copies. Name the exact set being edited (project files of a given date, or a delivered batch) before touching anything. When copies disagree, halt and resolve first; editing a stale copy forks canon.
2. Edit by exact string. Every change is an old-string to new-string replacement, and the old string must exist exactly once in the file. `ship-check.py apply` enforces both and refuses otherwise, validating the whole spec before writing anything.
3. Verify the diff. The diff against the authoritative copy must show the intended lines and nothing else. Carried-over text stays verbatim; minimal touch.
4. Check the added lines. Run `ship-check.py added` (or `prose`, for a whole file) for typography (em and en dashes, curly quotes) and marked-lexicon terms from `machinelexicon.csv`. The tool reports; hits are for judgment, since quoting a marked word to discuss it is mention, not use.
5. Know the regression trigger. Edits to `scrub-gate.py` behavior or to `machinelexicon.csv` require the gate regression: run the gate on the specimen set and compare with the expected flag patterns in the current batch notes. Text-only canon edits do not trigger it. Any edit touching a budget number or a profile's row set also requires `ship-check.py drift`, which resolves each of the six registers from the gate and compares it against canon's table for that register, failing on any disagreement in membership or numbers.
6. Label new artifacts. Every new artifact carries its own provenance label, written at creation, never inherited.
7. Deliver as candidates. The pipeline proposes, the writer decides: ship edits for ratification and say which one-string revert undoes each.

## The tool

```
python3 ship-check.py apply SPEC.json   # exact-string edits; unified diff per file
python3 ship-check.py prose FILE        # typography + lexicon check, whole file
python3 ship-check.py added ORIG NEW    # same checks, only on lines added between versions
python3 ship-check.py drift                     # each register's resolved table vs canon's, all six
python3 ship-check.py seed --desk NAME          # populated grid from canon's budget table
```

`seed` reads the enforcement class canon declares per row and applies the ruled
seed weights, absolute at 1.0, budgeted at 0.5, informational at 0.4. The class
is read, never inferred: two rows can match on mode, direction, target and sd
and still differ in class, so a tool that guessed would be a second source of
truth about canon.

`SPEC.json` holds `{"edits": [{"file": ..., "old": ..., "new": ...}]}`. All modes take `--lexicon PATH`; by default the tool looks for `machinelexicon.csv` in the working directory, then beside and above the script. `prose` and `added` exit nonzero on hits so the checks compose in scripts.
