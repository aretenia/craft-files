# Provenance: written by Slopsmith (build agent), 2026-07-23, at the Proprietor's
# direction, per BRIEF-slopsmith-generator.md and the round-1 and round-2 rulings.
# No human pass; verify before trusting.
"""The transform: (grid, template, injected clock) -> new grid.

Pure and deterministic. The clock is injected rather than read inside, which is
what makes the A1 determinism check mean anything: same inputs, byte-identical
output. Nothing here infers; every decision was ratified in the accretion
conversation and recorded in the template.

The write set for one run is only the cells the template names, plus the reel
appends, the undefined-region additions, and the counter. Untouched cells are left
exactly as they were: the fade over run age is a render concern and is never
written back into a cell, which is why a desk left alone for six months shows no
change in its file, only growing age against a rising run_counter.
"""

import copy
import re

from craftgen.config import DEFAULT_CONFIG
from craftgen.errors import Refusal
from craftgen.validate import validate_grid, validate_template

_U_SERIAL = re.compile(r"^U-(\d+)$")


def bootstrap_grid(desk_id, spec_version="1.1", legend_version=1):
    """The first-run container. Empty of cells by design.

    Cells carry definitions, and a definition is canon; seeding the legend's cells
    is a library-side step, not the generator's. This produces the shell the first
    consumption writes into, with the counter at zero so the first run is run 1.
    """
    return {
        "spec_version": spec_version,
        "legend_version": legend_version,
        "desk_id": desk_id,
        "run_counter": 0,
        "profile_lineage": ["default"],
        "cells": {},
        "undefined_region": [],
        "reel": [],
    }


def generate(grid, template, now, config=DEFAULT_CONFIG, ledger=None):
    """Consume one ratified template, return the updated grid and a report.

    Returns (new_grid, report). The report holds warnings, the assigned run, and the
    template content hash. Raises Refusal on any boundary failure, in which case
    nothing was applied and no counter moved.

    now is an injected ISO-8601 timestamp string for the reel tuples' t field. It is
    provenance for the reader and is never an input to anything computed.
    """
    validate_grid(grid)
    warnings = validate_template(template, grid)

    key = None
    if ledger is not None:
        key = ledger.key_for(template)
        if ledger.seen(key):
            prior = ledger.run_for(key)
            raise Refusal(f"template already consumed at run {prior}; refusing double consumption")

    new_grid = copy.deepcopy(grid)
    new_run = new_grid["run_counter"] + 1
    ratified_on = template["ratified_on"]

    changes = sorted(template["changes"], key=lambda c: c["seq"])
    next_seq = _next_reel_seq(new_grid["reel"], config.reel_seq_base)

    # Pass one: mint one reel tuple per change, in seq order, so every change gets a
    # provenance tuple and a stable reel seq. cluster_id is filled in pass three.
    appended = []
    for change in changes:
        tup = _reel_tuple(template, change, next_seq, now, new_run)
        appended.append((next_seq, tup, change))
        next_seq += 1

    # Pass two: apply the named-rule changes to their cells.
    for reel_seq, tup, change in appended:
        rule_id = change.get("rule_id")
        if rule_id is None:
            continue
        _apply_named(new_grid["cells"][rule_id], change, reel_seq, new_run, ratified_on, config)
        tup["rule_id"] = rule_id
        tup["cluster_id"] = None

    # Pass three: sort the residue into the undefined region as cluster members.
    _apply_residue(new_grid, appended, new_run)

    for reel_seq, tup, change in appended:
        new_grid["reel"].append(tup)

    new_grid["run_counter"] = new_run

    if ledger is not None:
        ledger.record(key, new_run, ratified_on)

    report = {
        "run": new_run,
        "template_hash": key,
        "warnings": warnings,
        "reel_appended": [tup["seq"] for _, tup, _ in appended],
    }
    return new_grid, report


def _next_reel_seq(reel, base):
    if not reel:
        return base
    return max(t["seq"] for t in reel) + 1


def _reel_tuple(template, change, seq, now, run):
    tup = {
        "seq": seq,
        # run is the pipeline run this tuple was appended on, per the run-based time
        # model. t is the date, reader provenance only, and is the injected clock.
        "run": run,
        "t": now,
        "author": template["author"],
        "artifact": template["artifact"],
        "artifact_label": template["artifact_label"],
        "rule_id": None,
        "cluster_id": None,
        "direction": change["direction"],
        "model": template["model"],
        "evidence": change.get("evidence"),
    }
    # The note is carried whenever present, per the ruled policy. It rides the reel
    # tuple, which is the append-only per-change record, rather than overwriting the
    # cell's drift_note. Its structured aggregation into the population layer is open
    # (template spec section 7).
    note = change.get("note")
    if isinstance(note, str) and note.strip():
        tup["note"] = note
    return tup


def _apply_named(cell, change, reel_seq, new_run, ratified_on, config):
    direction = change["direction"]
    state = config.state_for_direction[direction]
    cell["state"] = state
    # Weight is evidential bindingness (grid-spec section 3, Weight). The endpoints
    # are 1.0 and 0.4, both the writer's: exactly 1.0 is a writer-locked absolute,
    # exactly 0.4 is informational. Accretion reaches neither, because a category is a
    # ruling and not an accumulation. So a fire on a pinned cell still records state,
    # last_fired and provenance, and leaves the weight where the ruling put it.
    # Interior cells move per the config surface, whose magnitudes are the design
    # team's (section 9) and whose values stay strictly inside the open (0.4, 1.0).
    if cell.get("weight") not in (0.4, 1.0):
        cell["weight"] = _clamp(config.weight_on_fire[state])
    # last_fired is the date, written for the reader and the audit, never read by the
    # fade. last_fired_run is the integer the fade uses.
    cell["last_fired"] = ratified_on
    cell["last_fired_run"] = new_run
    cell.setdefault("provenance_refs", []).append(reel_seq)
    _move_target(cell, direction, config)


def _move_target(cell, direction, config):
    # v1 default leaves target untouched (both steps are zero). The mechanism is here
    # so a design-side step later is a config edit. Hardening tightens, softening
    # loosens, and the sign resolves against dir.
    target = cell.get("target")
    if target is None:
        return
    if direction == "human_strike":
        step = config.harden_target_step
        tighten = True
    elif direction == "human_add":
        step = config.soften_target_step
        tighten = False
    else:
        return
    if step == 0:
        return
    ceiling = cell.get("dir") == "ceiling"
    # Tightening a ceiling lowers it; tightening a floor raises it. Loosening flips.
    down = tighten == ceiling
    cell["target"] = max(0, target - step if down else target + step)


def _apply_residue(new_grid, appended, new_run):
    residue = [(reel_seq, tup, change) for reel_seq, tup, change in appended
               if change.get("rule_id") is None]
    if not residue:
        return

    # Group by cluster_key. Entries sharing a key are one cluster. A null rule_id with
    # no key is a cluster of one. Grouping is the conversation's judgment, carried in
    # cluster_key; the generator never groups by reading the content.
    groups = {}
    order = []
    for reel_seq, tup, change in residue:
        cluster_key = change.get("cluster_key")
        if cluster_key is None:
            token = ("_singleton", reel_seq)
        else:
            token = ("_key", cluster_key)
        if token not in groups:
            groups[token] = []
            order.append(token)
        groups[token].append((reel_seq, tup, change))

    # Assign U- serials deterministically, by the least reel seq in each group, always
    # minting fresh. Merging a new cluster with one from an earlier pass is a separate
    # ratified step, so the generator never reaches back across passes.
    order.sort(key=lambda token: min(rs for rs, _, _ in groups[token]))
    next_serial = _next_u_serial(new_grid)

    for token in order:
        cluster_id = f"U-{next_serial:03d}"
        next_serial += 1
        members = []
        for reel_seq, tup, change in groups[token]:
            tup["rule_id"] = None
            tup["cluster_id"] = cluster_id
            evidence = change.get("evidence")
            # Members point at evidence when it exists, else at the reel tuple, so
            # every member is addressable.
            members.append(evidence if evidence is not None else f"reel:{reel_seq}")
        new_grid["undefined_region"].append({
            "cluster_id": cluster_id,
            # members preserve the order the conversation gave them, never a sort. A
            # numeric sort of rev pointers would visibly reorder the frozen fixture.
            "members": members,
            "admission": "mechanical",
            # first_seen_run is the integer the run-based model uses; the frozen 1.1
            # fixtures carry this rather than a first_seen date.
            "first_seen_run": new_run,
            "name": None,
        })


def _next_u_serial(grid):
    # High-water mark across both the live region and the reel's history. A cluster
    # promoted out of the region leaves the region empty but is still named on its
    # reel tuples, so minting off the region alone would reuse a retired serial and
    # make the reel ambiguous about which cluster U-001 meant.
    highest = 0
    seen = [c.get("cluster_id") for c in grid["undefined_region"]]
    seen += [t.get("cluster_id") for t in grid["reel"]]
    for cluster_id in seen:
        match = _U_SERIAL.match(str(cluster_id or ""))
        if match:
            highest = max(highest, int(match.group(1)))
    return highest + 1


def _clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))
