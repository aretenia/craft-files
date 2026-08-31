---
name: scrub-gate
description: Run the deterministic scrub gate (stage 7 of Brinkman's craft files) on a draft. Use whenever a text needs gating against a register profile's hallmark budgets, whenever bare per-thousand rates are needed for calibration or corpus work, whenever an evidence audit of every match and rejected candidate is wanted, and whenever gate or lexicon changes require regression runs. Trigger on "run the gate", "scrub this", "gate this draft", "calibrate rates", "evidence audit", or any request to measure AI-text hallmarks in a file. Do NOT use it to overrule borderline flags by hand; judgment lives in canon (hallmarks-and-the-scrub.md and register-profiles.md), and the gate proposes while the writer decides.
---

# Running the scrub gate

*Provenance: machine-drafted July 9, 2026, at the writer's direction; commands verified against a live run of the July 2026 script; no human pass yet.*

## What this is

`scrub-gate.py` is the reference implementation of the pipeline's stage 7, the deterministic scrub. It counts the countable hallmark rows against a register profile's budgets and reports. The artifact definitions live in `hallmarks-and-the-scrub.md`, the budgets in `register-profiles.md`, the marked terms in `machinelexicon.csv`. The gate holds two structures the maintainer keeps aligned: a registry of what it can measure, and a transcription of canon's budget tables, one per register. Both are marked PROVISIONAL, July 2026. When a profile changes, its table changes with it, and any change touching a budget number or a profile's row set is checked by `ship-check.py drift` and triggers the regression suite (see the maintainer note).

## Invocation

Run it from a directory holding `machinelexicon.csv`, or point `--lexicon` at one.

```
python3 scrub-gate.py DRAFT.md                       # gate mode, default profile
python3 scrub-gate.py DRAFT.md --profile job-search  # six profiles: default, creative, job-search, satire, fairy-tale, llm-script
python3 scrub-gate.py DRAFT.md --calibrate           # rates only, TSV, no verdicts
python3 scrub-gate.py DRAFT.md --evidence            # also writes DRAFT.evidence.md
python3 scrub-gate.py corpus/*.md --calibrate        # globs work; one TSV row per file
```

## Reading the output

Gate mode prints one console report per file: fourteen rows, of which twelve are counted artifacts, one is the H2.10 uniformity run, and one is an H4.3 typography info line. Each counted row shows count, per-thousand rate, budget as a ceiling or floor with target and sd, and a verdict. A footer gives sentence-length stats and the em-dash mark detail: marks, characters, run lengths, and how many are spaced. Short texts get a small-sample warning; per-thousand rates on them are noise, so read counts, not rates.

Calibrate mode prints one TSV row per file with the same measures as rates. This is the measuring half of the calibration protocol; run it across the three corpora and file the rows in the corpus ledger.

Evidence mode writes a markdown audit per input, listing every pattern location and every rejected candidate; counts de-overlap masked spans, so evidence lines can slightly exceed counts. When the input's directory is read-only, the audit falls back to the working directory.

## Where judgment lives

Counters marked (heuristic) have false positives and negatives by design, and no counter can tell use from mention: quoted slop counts as slop, fine for calibration corpora, a caveat for documents about slop. Verdicts are proposals. The override discipline (audit the counter, then rule), the documented false-positive classes, and the specificity-proxy caveat are canon in `hallmarks-and-the-scrub.md`; budgets and their provisional status are canon in `register-profiles.md`. Read those before arguing with a flag. The gate proposes; the writer decides.

## Maintainer note

Any change to gate behavior or to `machinelexicon.csv` triggers the regression suite: run gate mode against the specimen set and compare with the expected flag patterns in the current batch notes, which live outside the repository by contamination discipline.
