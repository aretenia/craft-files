# craftgen

The generator that turns a ratified accretion template into a grid file.

*Provenance: written by the library orchestrator, July 23, 2026, at the Proprietor's direction, from the package's verified behavior rather than from its build reports. The package itself was written by the build agent; this README was produced after running its transform against the frozen sample fixtures and confirming every ruled invariant. No human pass; verify before trusting.*

## What it is

One transform: `(existing grid, ratified template, injected clock) -> (new grid, report)`. It consumes ratified intent and never infers it. There is no document parsing, no format detection, and no guessing at what an edit meant, because that judgment happened in the accretion conversation and is already recorded in the template.

The generator is the fourth stage of the accretion organism. The pipeline produces prose; the writer edits it; the accretion conversation reads that seam and produces a ratified template (see `accretion-conversation.md` and `accretion-template-spec-v1.md`); this generator turns the template into a grid file (see `grid-spec-v1.md`). It is build-role code, not pipeline canon, which is why it lives here rather than in `pipeline/`.

## Layout

Eight files, standard library only, Python 3:

- `generate.py`: the transform. Validates, deep-copies the grid, mutates in a fixed order, appends one reel tuple per change, sorts residue into the undefined region, stamps retention, increments the run counter. Also `bootstrap_grid`, an empty shell for tests. A real desk is seeded from canon by `ship-check.py seed`, not bootstrapped: the generator refuses to mint cells, because a cell carries a definition and a definition is canon.
- `validate.py`: the boundary. Refuses rather than repairs, and names the offending change by seq. Enforces the template-spec section 5 invariants, the round-2 invariants, and the structural checks every downstream step then gets to assume.
- `config.py`: every tunable magnitude, so a recalibration is a value edit and never a code-path edit. The state machine's structure is fixed in code; its numbers live here, provisional pending design-side calibration.
- `ledger.py`: the consumed-template ledger. One owner for the run counter, keyed on a content hash, so a second consumption of the same template is refused rather than counted twice.
- `canonical.py`: deterministic serialization. This is where the A1 determinism property is bought.
- `errors.py`: the single `Refusal` exception.
- `cli.py`: a thin command line over the transform.
- `__init__.py`: the public surface: `generate`, `bootstrap_grid`, `Config`, `DEFAULT_CONFIG`, `Ledger`, `Refusal`.

## If you have these as loose files

The eight modules import each other as a package, so they must sit inside a
folder named `craftgen/`. A project upload or a chat attachment delivers files
flat, in which case nothing runs until the folder is rebuilt. That is one step:

    mkdir craftgen
    mv __init__.py canonical.py cli.py config.py errors.py generate.py \
       ledger.py validate.py craftgen/

Three other files sit *beside* that folder rather than inside it:
`ship-check.py`, which seeds a desk; `machinelexicon.csv`, which it looks for
next to itself; and `register-profiles.md`, the canon the seeder reads. An agent
with a sandbox can do all of this and then run the commands below, which is the
expected path: the rest of this system already runs in a conversation, and
nothing here needs a local install.

## Running it

From the directory that contains the `craftgen/` package folder:

    python3 -m craftgen.cli generate \
        --grid path/to/grid.json \
        --template path/to/template.json \
        --now 2026-08-05T10:00:00Z \
        --out path/to/new-grid.json \
        --ledger path/to/ledger.json

`--out` writes the updated grid; without it the grid goes to stdout. `--now` injects the timestamp for the reel tuples' `t` field; without it the wall clock is used. `--ledger` enables double-consumption refusal and is where the run a template consumed on is recorded. A refusal prints to stderr and exits 2; a clean run prints the assigned run and the appended reel seqs to stderr.

The clock is injected at the edge rather than read inside the transform, which is the whole reason the output is deterministic: the same grid, template, and `--now` produce byte-identical output every time.

## What it guarantees, and what was checked

Each of these was confirmed by running the transform against the frozen `grid-sample-t*.json` fixtures:

- **Determinism.** Same inputs, byte-identical output.
- **The born-faded guardrail.** `last_fired_run` is stamped from the consumed run, never derived from a cell's provenance array. A run that touches other cells leaves a promoted cell's fired run exactly where it was, so INF-002 stays at 1 against a rising counter.
- **The weight endpoints.** 1.0 and 0.4 are the writer's, unreachable by accretion. A fire on a cell already at either value records state and retention but leaves the weight pinned; interior cells move, and no configured magnitude lands on an endpoint from either side.
- **Refusal, not repair.** A `human_strike` with no machine move, a `cluster_key` beside a named rule, a `rule_id` naming no cell, a bandless row with an empty note, a duplicate seq, an invalid direction, a grid with no run counter, and a desk mismatch are each refused with the offending seq named. Nothing partial is ever written.
- **One owner for the counter.** Consuming the same template twice through a shared ledger is refused on the second attempt.
- **Serial minting across history.** A new cluster takes the high-water mark across both the live undefined region and the reel's history, so a serial retired by promotion is never reused.
- **Field preservation.** The transform deep-copies and mutates, so any field it does not model, whether `named_on_run`, a future `spec_version`, or anything else, survives a round-trip.

## Starting a desk

The generator updates a grid; it does not create one. `bootstrap_grid` returns an
empty shell useful for tests, and a real desk is seeded from canon:

    python3 ship-check.py seed --desk my-desk --out grid.json

That reads the enforcement class canon declares for each budget row and applies
the ruled seed weights. The generator refuses to mint cells itself, because a
cell carries a definition and a definition is canon, so a grid seeded any other
way will refuse the first template that names a rule it does not hold.

## What it deliberately does not do

It does not mint cells: a new cell needs a definition, which is a canon or legend edit rather than a pipeline run. It does not read author from document metadata: the author is a configured desk value. It does not move a cell's target or sd in v1: quantization is the design team's, and the mechanism sits behind a zeroed config step until those numbers land. It does not decay anything: the fade over run age is a render concern and is never written back into a cell.

## Owed

The render subcommand and the standalone schema-validate command are next, then the A1 and A2 acceptance checks and CRLF normalization. The config magnitudes are provisional until the design side calibrates them. The generator's own test suite ships with it; this README's guarantees were verified independently against the fixtures rather than from that suite.
