# Grid specification, version 1 draft

*Provenance: drafted by the machine from the ratified rulings of July 8, 2026; no human pass. Amended July 23, 2026 by the library orchestrator at the writer's direction, to close the gap between this document and the render specification: the schema sketch gains `run_counter` and `last_fired_run`, section 6 names the fade's inputs, and the reel note pins the author value to a publication standard. Amended again the same day, after the two sample generations were merged and frozen: the sketch moves to spec_version 1.1 and gains reel `run`, cluster `first_seen_run` and the `named_on_run` cell field; weight seeding and its endpoints are documented from the frozen fixture rather than from anyone's memory; age is stated to move extent and never tone; and the evidence-pointer conventions are written down. Working document for the implementation agents, not repo canon. The design brief's demolition survivors are the requirements here; where this spec and the brief's illustrative mechanics disagree, the rulings recorded in the expansion notes govern.*

---

## 0. Status at v3.3: the file ships, the render does not

The grid file, its schema, the accretion conversation that fills it, and the
generator that writes it are all shipped and working. The render is not. No code
turns a grid into a picture; the visual specification is frozen and three
reference renderings exist, cut by hand, but the runtime renderer was scoped and
never built.

So everything below describing how the grid looks is a specification awaiting an
implementation rather than a description of behavior you can invoke. The tone
ramp, the fade table, and the geometry are all published and sufficient to build
against. Anyone wanting a picture writes the renderer.

This section exists because a reader who met section 2's claim that the grid
generates its own render, without meeting this first, would reasonably expect a
tool that is not here.

## 1. Scope, version one

One grid per project-desk. Cells cover the parameter layer only: hallmark-ID rows, profile budget rows, and informal rules carrying INF-serial IDs. Craft-file moves are excluded until they have stable IDs. Multiple register profiles share the one grid; a cell's values are the active profile's after deltas, and the legend records profile lineage.

## 2. The file is the format

The grid is a structured file that generates its own render. The raster is a derived, human-facing projection; nothing machine-facing ever reads pixels. Round-trip losslessness is a property of the file. The render must be deterministic from the file, and every exported image embeds its source file (PNG text chunk, SVG metadata), so sending someone the picture is sending them the grid.

## 3. Schema sketch

```json
{
  "spec_version": "1.1",
  "legend_version": 3,
  "desk_id": "craft-files",
  "run_counter": 18,
  "profile_lineage": ["default", "creative"],
  "cells": {
    "H1.1": {
      "kind": "formal",
      "mode": "count", "dir": "ceiling", "target": 3, "sd": 2,
      "state": "revised",
      "weight": 0.85,
      "last_fired": "2026-07-07",
      "last_fired_run": 12,
      "definition_ref": "hallmarks-and-the-scrub.md#h11",
      "drift_note": "spacing prior inverted for this hand",
      "provenance_refs": [412, 415]
    },
    "INF-001": {
      "kind": "informal",
      "mode": "rule", "dir": "ceiling", "target": 0, "sd": 0,
      "state": "validated",
      "weight": 0.6,
      "last_fired": "2026-07-07",
      "last_fired_run": 17,
      "named_on_run": 16,
      "definition_ref": "companion#inf-001-sincerity-preamble",
      "provenance_refs": [401, 402]
    }
  },
  "undefined_region": [
    {
      "cluster_id": "U-003",
      "members": ["Rupture_V3.docx#rev-12", "Rupture_V3.docx#rev-17"],
      "admission": "mechanical",
      "first_seen_run": 14,
      "name": null
    }
  ],
  "reel": [
    {
      "seq": 415,
      "run": 12,
      "t": "2026-07-07T14:12:00Z",
      "author": "REQUIRED, never null",
      "artifact": "Rupture_V3.docx",
      "artifact_label": "human edits after the V2 pass",
      "rule_id": "H1.1",
      "cluster_id": null,
      "direction": "human_strike",
      "model": "the generation-side model and version for this run",
      "evidence": "rupture-v2.evidence.md#h11-2"
    }
  ]
}
```

`run` is mandatory on every tuple and is the run counter at which the event was recorded. `t` is reader provenance, never parsed and never computed from; an ISO 8601 date or date-time both satisfy it, and the sample fixtures use the date form while a live run has no reason not to record the time.

**The run-to-date map must be monotone.** Dates never drive anything, but a run counter that advances while wall time runs backward is not a state this system can produce, and a fixture is held to being possible rather than to being real.

`named_on_run` is an optional cell field, an integer, present on an informal cell promoted from a cluster. It records the run at which the writer named the rule. It sits beside `last_fired_run` rather than replacing it because the two answer different questions, and keeping them apart is what stops ceremony from impersonating exercise: **a rule is as fresh as its evidence and never as fresh as its christening.** `last_fired_run` is stamped, never computed from the provenance array's maximum, and a promotion does not refresh it.

`first_seen_run` on a cluster is the run at which it was admitted, an integer for the same reason every other time field is.

A tuple carries exactly one of `rule_id` and `cluster_id`: a change that matched a named rule names it, and residue names the undefined-region cluster it joined. The sample files use `cluster_id` this way and earlier drafts of this sketch omitted the field, which would have led an implementer building from the sketch alone to drop it.

The reel is append-only. The `author` field is mandatory in every tuple; a run that cannot identify the human pass's author appends nothing and reports why. Desk scope plus mandatory author means a per-hand split later is a query over the reel, never a migration.

The author value ships, so it is held to a publication standard rather than a rendering one. Every export embeds the file's JSON verbatim and the extraction is byte-diffed against the input, which means redaction at embed time is not available: it would fail the check by construction. The field therefore carries a role or a stable pseudonym rather than a personal handle on any desk whose renders may leave the writer's own machine. This desk's value is `Proprietor`. No rendered surface prints the field in any case.

### Weight

Weight is evidential bindingness, not freshness, and it is the only channel that carries tone.

Cells seed by enforcement class: **1.0 for an absolute row**, one whose violation is conclusive; **0.5 for a budgeted row**, one carrying a numeric band; **0.4 for an informational row**, one that reports without a verdict. The frozen t0 fixture is the reference: three absolutes at 1.0, ten budgeted at 0.5, one informational at 0.4.

Weight moves only along the update path, and only by events that leave records. A weight that has moved with a null state, a null last-fired and an empty provenance array is a defect rather than a value, because the update path cannot produce it.

**The endpoints are 1.0 and 0.4, and both belong to the writer.** Exactly 1.0 always means a writer-locked absolute. Exactly 0.4 always means informational. Accretion reaches neither: no sequence of update-path events may walk a cell to either value, because a category is a ruling and not an accumulation. The update path therefore moves weight strictly inside the open interval between them, and a fire on a pinned cell still records state, last-fired, last-fired-run and provenance while leaving the weight where the ruling put it. The frozen fixtures carry no cell at any weight below 0.4, and none at 0.0 at all.

## 4. The update path

Input is the ratified accretion template, never bare occurrence: the machine closing a dash and the human re-spacing it must land as human_strike against the machine's habit, not as two occurrences of a dash. That example is also the requirement the template inherits, because reading it correctly needs both sides of the seam. A template built from the finished prose alone has rebuilt bare occurrence with extra steps. The generator consumes ratified intent and never infers it. Direction semantics: **human_add** against a rule softens it; **human_strike** of a machine move hardens the rule the move violated; **stand** is weak confirmation, logged at low weight. The sort is three-way: countable rows update mechanically; annotation-category matches update semi-mechanically with the judgment noted; residue that matches nothing lands in the undefined region as cluster members. One provenance tuple per update, no exceptions.

## 5. States and the legend

Four states: **fired** (the rule acted this run), **validated** (human pass confirmed the action), **contested** (human pass reversed it; the strongest freshness signal), **revised** (the rule's definition changed). A revision bumps `legend_version` and moves no ink; definition history lives in the companion file, keyed by legend version.

## 6. Retention

Freshness fades; the fade function is the retention layer and the McGaugh citation's proper home: the reel records everything like a camera, the grid retains like memory, and significance gates what stays vivid. Render requirement, owed to the design team as R-fixed-geometry: ink fades and shrinks inside a cell that never moves or resizes, because position is identity and growing whitespace is honest data.

**Age moves extent, never tone.** The event mark shrinks as it ages and never lightens; darkness is weight alone. The two are split on purpose and the split is ratified: the material's own drypoint fade compounds richness and wear, this encoding refuses to, and age must never impersonate looseness. A record that attaches age to tone is how the compound creeps back, so the distinction is fixed here rather than left in conversation.

The fade is a function of work done, not of time elapsed. Age is `run_counter` minus `last_fired_run`, integers, pipeline runs only, and wall time never enters the render. The dates in `last_fired` are provenance for the reader and for the audit; they are never the fade's input, because a desk that aged against the calendar would read a month away from work as decay, which inverts what this layer means. A null `last_fired_run` is dormancy, categorically distinct from a mark that has faded. Earlier drafts of this section described the fade without naming its inputs, and the sample files were authored against the schema sketch rather than against this rule; the sketch above now carries both fields.

### Evidence pointers

Two schemes, deliberately. The rule is to cite whatever recorded the event, not to sort by who made it.

Where the gate detected the rule, an evidence file carries an anchor and the pointer names it, `rupture-v2.evidence.md#h11-1`. That holds whether the tuple records the machine pass or the writer's response to it, because the gate's record is what locates the thing either way.

Where no gate evidence exists, which is every informal rule and all undefined residue, the pointer names the document revision that made the edit, `Rupture_V3.docx#rev-12`. Collapsing the two would make those pointers cite an evidence file that has no entry for them.

**A pointer with nothing to cite is null, never fabricated.** A rule that did not fire has no anchor, by the evidence file's own rule, and a pointer naming an anchor that does not exist is worse than an absent one because it cannot be told from a broken one. One deliberately unresolvable pointer belongs in any fixture set as the drill-down degradation case, and it only works if the honest nulls stay honest.

Evidence filenames follow whatever `scrub-gate.py` emits, which is the input stem plus `.evidence.md`. Any consumer resolving pointers normalizes to that form rather than inferring one.

## 7. Promotion, two targets

Recurrent informal dimensions promote out of the desk in one of two directions: durable recurrences to craft canon, version-bound recurrences to the hallmarks catalog with a version block. The classifier is survival across a model-version change, which the reel's `model` field exists to answer. The criterion's form, numbers pending data: independence of lineage, cross-register recurrence, version survival. Informal cells carry drift notes from birth.

## 8. The watch condition

The genuinely authorless event is narrow and precisely defined: an unnamed cluster, admitted by mechanical threshold, that demonstrably functions in generation before anyone labels it. The spec requires only that the system can detect and report this condition, not that it do anything about it. If it fires, something operated before it was named, and the writer decides what that means.

## 9. Open, deliberately

The sd channel and all quantization steps belong to the design team, bounded by the handoff brief's requirements. Consent posture for population-layer sharing (a grid plus reel is a stylistic fingerprint) and gameability of promotion-by-recurrence are open questions seven and eight on the expansion ledger; nothing in version one depends on them.
