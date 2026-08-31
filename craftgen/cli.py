# Provenance: written by Slopsmith (build agent), 2026-07-23, at the Proprietor's
# direction, per BRIEF-slopsmith-generator.md and the round-1 and round-2 rulings.
# No human pass; verify before trusting.
"""Thin command line over the transform.

Reads a grid and a template, writes the updated grid, records the ledger. The
render subcommand and the schema-validate front half land next; the parser here
leaves room for them. The clock is supplied at the edge, so the transform stays
pure.
"""

import argparse
import json
import sys
from datetime import datetime, timezone

from craftgen.canonical import pretty_json
from craftgen.errors import Refusal
from craftgen.generate import generate
from craftgen.ledger import Ledger


def _load(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def cmd_generate(args):
    grid = _load(args.grid)
    template = _load(args.template)
    ledger = Ledger(args.ledger) if args.ledger else None
    now = args.now or _now_iso()
    try:
        new_grid, report = generate(grid, template, now, ledger=ledger)
    except Refusal as refusal:
        print(f"refused: {refusal}", file=sys.stderr)
        return 2
    out = pretty_json(new_grid)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(out)
    else:
        sys.stdout.write(out)
    for warning in report["warnings"]:
        print(f"warning: {warning}", file=sys.stderr)
    print(f"run {report['run']}; appended reel seqs {report['reel_appended']}", file=sys.stderr)
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="craftgen", description="Accretion template to grid generator")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Consume a ratified template into the grid")
    gen.add_argument("--grid", required=True, help="Path to the existing grid file")
    gen.add_argument("--template", required=True, help="Path to the ratified accretion template")
    gen.add_argument("--out", help="Where to write the updated grid; stdout if omitted")
    gen.add_argument("--ledger", help="Path to the consumed-template ledger")
    gen.add_argument("--now", help="Injected ISO-8601 timestamp for reel tuples; wall clock if omitted")
    gen.set_defaults(func=cmd_generate)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
