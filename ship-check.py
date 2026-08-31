#!/usr/bin/env python3
"""ship-check.py: the canon-shipping tool for Brinkman's craft files.

Provenance: machine-drafted July 9, 2026, at the writer's direction;
no human pass yet.

Three subcommands:
  apply SPEC.json   exact-string edits with uniqueness assertions. The
                    whole spec is validated in memory before any file is
                    written, so a refusal leaves every file untouched.
                    Prints a unified diff per edited file.
  prose FILE        typography and marked-lexicon check on a whole file.
  added ORIG NEW    the same checks, only on lines added between two
                    versions of a file.
  drift             compare scrub-gate.py's DEFAULT_PROFILE against
                    register-profiles.md's default budget table; exits
                    nonzero on any divergence in membership or numbers.

Typography is checked by code point: em dash, en dash, curly double and
single quotes. Lexicon terms come from machinelexicon.csv; single words
match on word boundaries with pragmatic inflections left to the gate,
phrases match as case-insensitive substrings. The tool reports; hits are
for judgment, since quoting a marked word to discuss it is mention, not
use. prose and added exit nonzero on hits so the checks compose.
"""

import argparse
import csv
import difflib
import json
import os
import re
import sys

BAD_CHARS = {
    "\u2014": "em dash",
    "\u2013": "en dash",
    "\u201c": "curly double quote",
    "\u201d": "curly double quote",
    "\u2018": "curly single quote",
    "\u2019": "curly single quote",
}


def find_lexicon(path):
    here = os.path.dirname(os.path.abspath(__file__))
    tries = [path] if path else [
        "machinelexicon.csv",
        os.path.join(here, "machinelexicon.csv"),
        os.path.join(here, os.pardir, "machinelexicon.csv"),
        os.path.join(here, os.pardir, os.pardir, "machinelexicon.csv"),
    ]
    for p in tries:
        if p and os.path.exists(p):
            with open(p, newline="", encoding="utf-8") as f:
                return p, [r["term"] for r in csv.DictReader(f)]
    sys.exit("lexicon CSV not found; tried: " + ", ".join(t for t in tries if t))


def check_lines(lines, terms):
    hits = []
    singles = [t for t in terms if re.fullmatch(r"[A-Za-z-]+", t)]
    phrases = [t for t in terms if not re.fullmatch(r"[A-Za-z-]+", t)]
    single_re = None
    if singles:
        single_re = re.compile(
            r"\b(" + "|".join(re.escape(t.lower()) for t in singles) + r")\b"
        )
    for n, line in enumerate(lines, 1):
        for ch, name in BAD_CHARS.items():
            if ch in line:
                hits.append((n, name, line.strip()[:70]))
        low = line.lower()
        if single_re:
            for m in single_re.finditer(low):
                hits.append((n, "lexicon: " + m.group(1), line.strip()[:70]))
        for ph in phrases:
            if ph.lower() in low:
                hits.append((n, "lexicon: " + ph, line.strip()[:70]))
    return hits


def report(hits):
    if not hits:
        print("CLEAN")
        return 0
    for n, what, ctx in hits:
        print(f"line {n}: {what}: {ctx}")
    print(f"{len(hits)} hit(s)")
    return 1


def cmd_apply(args):
    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)
    texts = {}
    # Phase one: validate every edit against the in-memory texts.
    for e in spec["edits"]:
        f_, old = e["file"], e["old"]
        if f_ not in texts:
            with open(f_, encoding="utf-8") as fh:
                texts[f_] = fh.read()
        if old not in texts[f_]:
            sys.exit(f"refused, nothing written. Target not found in {f_}: {old[:60]!r}")
        n = texts[f_].count(old)
        if n != 1:
            sys.exit(f"refused, nothing written. Target not unique in {f_} ({n} occurrences): {old[:60]!r}")
        texts[f_] = texts[f_].replace(old, e["new"])
    # Phase two: write and show diffs.
    for f_, new_text in texts.items():
        with open(f_, encoding="utf-8") as fh:
            before = fh.read()
        diff = difflib.unified_diff(
            before.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile=f_ + " (before)",
            tofile=f_ + " (after)",
        )
        sys.stdout.writelines(diff)
        with open(f_, "w", encoding="utf-8") as fh:
            fh.write(new_text)
        print(f"applied: {f_}")
    return 0


def cmd_prose(args):
    _, terms = find_lexicon(args.lexicon)
    with open(args.file, encoding="utf-8") as f:
        lines = f.read().splitlines()
    return report(check_lines(lines, terms))


def cmd_added(args):
    _, terms = find_lexicon(args.lexicon)
    with open(args.orig, encoding="utf-8") as f:
        a = f.read().splitlines()
    with open(args.new, encoding="utf-8") as f:
        b = f.read().splitlines()
    added = [l[2:] for l in difflib.ndiff(a, b) if l.startswith("+ ")]
    return report(check_lines(added, terms))


def _profile_key(heading):
    """`## Profile: default (analytical long-form)` -> `default`.
    `## Profile: satire (slop mode)` -> `satire`. The parenthetical is prose."""
    s = heading.split(":", 1)[1]
    s = re.sub(r"\([^)]*\)", "", s).strip()
    return s.split()[0] if s else ""


def parse_canon(path):
    """Parse every register's budget table from register-profiles.md.

    Keyed on the table's own header row rather than on a subheading, because
    the subheadings are not uniform: three registers head their table with
    `### Budget table` or `### Budget deltas` and three head it with nothing
    at all. The header row is identical in all six.

    Returns {profile: {id: (mode, dir, target, sd, class)}} with the non-default
    profiles holding canon's deltas, not resolved tables. `class` is the declared
    enforcement class the seeder reads; two rows can match on every other field
    and still differ in class, so it is declared rather than derived.
    """
    out, prof, in_table = {}, None, False
    with open(path, encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s.startswith("## Profile:"):
                prof = _profile_key(s)
                out.setdefault(prof, {})
                in_table = False
                continue
            if prof and s.startswith("| id | artifact |"):
                in_table = True
                continue
            if in_table:
                if not s.startswith("|"):
                    in_table = False
                    continue
                if not s.startswith("| H"):
                    continue
                c = [x.strip() for x in s.strip("|").split("|")]
                if len(c) >= 7:
                    # mode, dir, target, sd, class. `note` is prose and is not read.
                    out[prof][c[0]] = (c[2], c[3], c[4], c[5], c[6])
    return out


def _norm(v):
    """Canon writes cells as prose. `n/a` and an empty cell are both absent."""
    if v is None:
        return None
    v = str(v).strip()
    if v in ("n/a", "", "-"):
        return None
    return int(v) if re.fullmatch(r"-?\d+", v) else v


def _load_gate(path):
    """Compile from source every time, never through the bytecode cache.

    importlib will reuse a .pyc whenever the source's recorded mtime and size
    still match, and mtime has one-second granularity. An edit that changes a
    single digit keeps the size identical, so a gate edited and re-checked
    inside the same second was read from stale bytecode: the check reported a
    divergence the file no longer had. A verification tool must read the
    artifact, not a cached compilation of an older one.
    """
    import types, sys as _sys
    src = open(path, encoding="utf-8").read()
    mod = types.ModuleType("_gate")
    mod.__file__ = path
    argv, _sys.argv = _sys.argv, [path]
    try:
        exec(compile(src, path, "exec"), mod.__dict__)
    finally:
        _sys.argv = argv
    return mod


def cmd_drift(args):
    """Compare the gate's resolved table against canon's, for every register.

    Rewritten for the V3.3 gate. The old version scraped `DEFAULT_PROFILE` and
    `COUNT_IDS` out of the source text and checked the default register only,
    which left five of six registers unchecked and broke outright when the
    table it scraped was refactored away. This imports the gate and calls
    `resolve()`, so it compares the structure the gate actually uses.

    Canon's non-default tables are deltas, so canon is resolved the same way
    the gate resolves: default table first, then the register's deltas.
    """
    canon = parse_canon(args.profiles)
    if "default" not in canon or not canon["default"]:
        sys.exit(f"no default budget table found in {args.profiles}")
    try:
        gate = _load_gate(args.script)
        gate.resolve, gate.PROFILES
    except Exception as e:
        sys.exit(f"cannot read {args.script}: {e}")

    problems, owed = [], []
    unknown = sorted(set(canon) - set(gate.PROFILES))
    for p in unknown:
        problems.append(f"canon publishes register '{p}'; the gate does not implement it")

    for p in sorted(gate.PROFILES):
        if p not in canon:
            problems.append(f"the gate implements '{p}'; canon does not publish it")
            continue
        want = dict(canon["default"])
        want.update(canon[p])                      # canon resolved the same way
        got = gate.resolve(p)
        for rid in sorted(set(want) - set(got)):
            problems.append(f"[{p}] canon declares {rid}; the gate's table omits it")
        for rid in sorted(set(got) - set(want)):
            problems.append(f"[{p}] the gate's table declares {rid}; canon does not")
        for rid in sorted(set(want) & set(got)):
            cm, cd, ct, cs = (_norm(x) for x in want[rid][:4])
            g = got[rid]
            # Both sides through _norm: the gate stores 'n/a' as a literal
            # string because budget_str slices it, while canon writes the same
            # absence as a cell. Comparing them raw reports every rule row.
            for field, cval, gval in (("mode", cm, _norm(g.get("mode"))),
                                      ("dir", cd, _norm(g.get("dir"))),
                                      ("target", ct, _norm(g.get("target"))),
                                      ("sd", cs, _norm(g.get("sd")))):
                if cval != gval:
                    problems.append(f"[{p}] {rid} {field}: canon {cval!r}, gate {gval!r}")
            if _norm(g.get("target")) is not None and rid not in gate.COUNTERS:
                owed.append(f"[{p}] {rid} carries a budget and the gate has no counter for it")

    if owed:
        for o in sorted(set(owed)):
            print("owed:", o)
        print(f"{len(set(owed))} declared row(s) the gate cannot score; judged by hand, not drift")
    if problems:
        for p in problems:
            print("drift:", p)
        print(f"{len(problems)} divergence(s)")
        return 1
    print(f"CLEAN across {len(gate.PROFILES)} register(s)")
    return 0



# Seed weights by enforcement class, per grid-spec-v1.md section 3. The class is
# canon's declared column, never inferred here: two rows can share mode, dir,
# target and sd and still differ in class, so a tool that guessed would be a
# second source of truth about canon and would drift the first time a row moved.
SEED_WEIGHT = {"absolute": 1.0, "budgeted": 0.5, "informational": 0.4}


def cmd_seed(args):
    """Emit a populated grid from canon's declared budget table.

    The generator refuses to mint cells, correctly: a cell carries a definition
    and a definition is canon, so seeding belongs to the canon-side tool. This
    is that step. Without it a bootstrapped grid is an empty shell that refuses
    every template, which is the state the accretion organism shipped in before
    this subcommand existed.
    """
    canon = parse_canon(args.profiles)
    if args.profile not in canon:
        sys.exit(f"canon publishes no register {args.profile!r}; "
                 f"available: {', '.join(sorted(canon))}")
    rows = dict(canon["default"])
    rows.update(canon[args.profile])

    def num(v):
        v = (v or "").strip()
        return None if v in ("n/a", "", "-") else (int(v) if re.fullmatch(r"-?\d+", v) else v)

    cells = {}
    for rid in rows:
        mode, direction, target, sd, klass = rows[rid]
        if klass not in SEED_WEIGHT:
            sys.exit(f"{rid}: canon declares class {klass!r}, which is not one of "
                     f"{', '.join(sorted(SEED_WEIGHT))}")
        anchor = "dict#" + rid.lower().replace(".", "").replace("*", "").replace("-", "")
        cells[rid] = {
            "kind": "informal" if rid.startswith("INF-") else "formal",
            "mode": mode,
            "dir": num(direction),
            "target": num(target),
            "sd": num(sd),
            "state": None,
            "weight": SEED_WEIGHT[klass],
            "last_fired_run": None,
            "last_fired": None,
            "definition_ref": anchor,
            "drift_note": None,
            "provenance_refs": [],
        }

    grid = {
        "spec_version": args.spec_version,
        "legend_version": 1,
        "desk_id": args.desk,
        "run_counter": 0,
        "profile_lineage": ["default"] if args.profile == "default"
                           else ["default", args.profile],
        "cells": cells,
        "undefined_region": [],
        "reel": [],
    }
    text = json.dumps(grid, ensure_ascii=False, indent=1) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print(f"seeded {len(cells)} cells from {args.profile} into {args.out}")
    else:
        sys.stdout.write(text)
    return 0

def main():
    ap = argparse.ArgumentParser(description="canon-shipping checks and edits")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("apply", help="exact-string edits from a JSON spec")
    p.add_argument("spec")
    p.set_defaults(func=cmd_apply)

    p = sub.add_parser("prose", help="typography + lexicon check on a file")
    p.add_argument("file")
    p.add_argument("--lexicon", default=None)
    p.set_defaults(func=cmd_prose)

    p = sub.add_parser("added", help="check only lines added between two versions")
    p.add_argument("orig")
    p.add_argument("new")
    p.add_argument("--lexicon", default=None)
    p.set_defaults(func=cmd_added)

    p = sub.add_parser("seed", help="emit a populated grid from canon's budget table")
    p.add_argument("--desk", required=True, help="desk_id for the new grid")
    p.add_argument("--profile", default="default", help="register to seed from")
    p.add_argument("--profiles", default="register-profiles.md")
    p.add_argument("--spec-version", dest="spec_version", default="1.1")
    p.add_argument("--out", help="write here; stdout if omitted")
    p.set_defaults(func=cmd_seed)

    p = sub.add_parser("drift", help="compare the gate's budget table against canon")
    p.add_argument("--profiles", default="register-profiles.md")
    p.add_argument("--script", default="scrub-gate.py")
    p.set_defaults(func=cmd_drift)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()