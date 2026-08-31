# Provenance: written by Slopsmith (build agent), 2026-07-23, at the Proprietor's
# direction, per BRIEF-slopsmith-generator.md and the round-1 and round-2 rulings.
# No human pass; verify before trusting.
"""The boundary. Enforce rather than trust; refuse rather than repair.

Two invariants come from the template spec's section 5, two more were added in the
round-2 rulings, and the rest are the structural checks a mechanical consumer needs
so that everything downstream of this file can assume a clean input.

A returned list holds non-fatal warnings. A Refusal is fatal and stops the run.
"""

from craftgen.config import VALID_DIRECTIONS
from craftgen.errors import Refusal

_TEMPLATE_REQUIRED = (
    "template_version",
    "desk_id",
    "ratified_on",
    "author",
    "artifact",
    "artifact_label",
    "model",
    "changes",
)


def validate_grid(grid):
    """Check the grid the template will update against.

    run_counter is mandatory. The sample files still lack it because the design
    side owes the integers; per the rulings the schema is binding and the samples
    are shape only, so a grid without run_counter is refused rather than defaulted.
    """
    if not isinstance(grid, dict):
        raise Refusal("grid is not an object")
    for key in ("desk_id", "run_counter", "cells", "undefined_region", "reel"):
        if key not in grid:
            raise Refusal(f"grid is missing required field {key!r}")
    if not isinstance(grid["run_counter"], int) or isinstance(grid["run_counter"], bool):
        raise Refusal("grid run_counter must be an integer; the design-side integers are owed")
    if not isinstance(grid["cells"], dict):
        raise Refusal("grid cells must be an object")
    if not isinstance(grid["undefined_region"], list):
        raise Refusal("grid undefined_region must be a list")
    if not isinstance(grid["reel"], list):
        raise Refusal("grid reel must be a list")


def validate_template(template, grid):
    """Refuse a malformed template; return a list of warnings for the rest.

    Assumes validate_grid has already passed for grid.
    """
    warnings = []

    if not isinstance(template, dict):
        raise Refusal("template is not an object")

    for key in _TEMPLATE_REQUIRED:
        if key not in template:
            raise Refusal(f"template is missing required field {key!r}")

    # author is configured, never detected, and never null. A run that cannot name
    # the human pass's author appends nothing (grid-spec section 3).
    author = template["author"]
    if not isinstance(author, str) or not author.strip():
        raise Refusal("template author is missing or empty; the run cannot append")

    if template["desk_id"] != grid["desk_id"]:
        raise Refusal(
            f"template desk_id {template['desk_id']!r} does not match grid "
            f"{grid['desk_id']!r}; there is one grid per desk"
        )

    # run was dropped from the template by ruling: the generator owns the counter.
    # The published template spec still lists it, so tolerate its presence and warn
    # rather than refuse, and ignore the value.
    if "run" in template:
        warnings.append(
            "template carries a 'run' field; ruling dropped it and the generator "
            "owns the counter, so the value is ignored"
        )

    changes = template["changes"]
    if not isinstance(changes, list):
        raise Refusal("template changes must be a list")

    seen_seq = set()
    for change in changes:
        _validate_change(change, grid, seen_seq)

    return warnings


def _validate_change(change, grid, seen_seq):
    if not isinstance(change, dict):
        raise Refusal("change is not an object")

    seq = change.get("seq")
    if not isinstance(seq, int) or isinstance(seq, bool):
        raise Refusal("change is missing an integer seq")
    if seq in seen_seq:
        raise Refusal("duplicate seq within the template", seq=seq)
    seen_seq.add(seq)

    direction = change.get("direction")
    if direction not in VALID_DIRECTIONS:
        raise Refusal(f"direction {direction!r} is not one of {sorted(VALID_DIRECTIONS)}", seq=seq)

    rule_id = change.get("rule_id")
    machine_move = change.get("machine_move")
    cluster_key = change.get("cluster_key")
    note = change.get("note")

    # Section 5: a human_strike requires a non-null machine_move. You cannot strike a
    # move nobody made. This template was built from the prose, not the seam. Refuse.
    if direction == "human_strike" and machine_move is None:
        raise Refusal("human_strike with a null machine_move; built from prose, not the seam", seq=seq)

    # Round-2 invariant: a cluster_key appears only where rule_id is null. A key beside
    # a named rule means the conversation could not classify the change, so it is not
    # ratified.
    if cluster_key is not None and rule_id is not None:
        raise Refusal("cluster_key present on a change with a non-null rule_id", seq=seq)

    if rule_id is not None:
        if rule_id not in grid["cells"]:
            # The generator cannot mint a cell; a new cell needs a definition, which is
            # a canon or legend edit, not a pipeline run.
            raise Refusal(f"rule_id {rule_id!r} names no cell in the grid", seq=seq)
        cell = grid["cells"][rule_id]
        # Ruled note policy: require the note whenever the row carries no band. A
        # bandless row is one whose target is null; the judgment is the only signal
        # there, so it cannot be empty.
        if cell.get("target") is None:
            if not isinstance(note, str) or not note.strip():
                raise Refusal(
                    f"rule_id {rule_id!r} is a bandless row and requires a non-empty note",
                    seq=seq,
                )
