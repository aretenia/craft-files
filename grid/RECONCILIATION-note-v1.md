# Reconciliation note: one generation, and the freeze

*Provenance: written by the craft-files library orchestrator, July 23, 2026, at the Proprietor's direction, accompanying the merged `grid-sample-t0/t1/t2.json`. Routes through Postmaster to Artlord and to the build role. This file is the record of every call the merge made and why. No human pass; verify before trusting, this file included.*

---

## What happened, and what stops happening

Two generations of the sample files existed in two containers. Both were edited. Nothing reconciled them but hand-patching, which produced three separate correction cycles, cost the design side a build cycle, and had the library confidently auditing against a baseline the design side did not hold.

This merge ends that. **From here there is one copy.** Any change to it routes through this orchestrator and gets a line in this note. Neither side patches privately again.

## The base

**Artlord's `baseline-*` files are the base and the library's rulings are applied on top.** The baseline was the better artifact on four counts the library did not know until it diffed them mechanically: it carried the run fields, it implemented weight seeding correctly, its evidence pointers resolve, and its artifact attribution is internally consistent. Two of those four the design side had not flagged, because it was diffing for its own concerns.

## Every call

| call | resolution | basis |
|---|---|---|
| base file | Artlord's `baseline-*` | four counts above |
| `spec_version` | **1.1** | the file carries `named_on_run` and reel `run` values that 1.0 never documented |
| `legend_version` | **2, 3, 4** | baseline's 1, 2, 3 plus the one membership step |
| cell membership | **fourteen formal**, H2.2 and H3.5 out | canon's declared table; both verified dormant with empty provenance before removal |
| time fields | **both**, runs from baseline and dates derived from the run-to-date map | specification section 3 requires both; runs drive the fade, dates are reader provenance |
| weight seeds at t0 | **baseline** | absolute rows 1.0, budgeted 0.5, informational 0.4; the library's copies had flattened all sixteen to 0.5 |
| `author` | **`Proprietor`** | publication standard, since every export embeds its source verbatim |
| `account` | **dropped** | Artlord proved mechanically that it is exactly determined by `direction` and carries nothing that field does not |
| `model` | **the library's real values** | baseline carried a placeholder string |
| `evidence_ref` | **renamed `evidence`** | the specification names it and the generator has twenty-six tests against it |
| artifact attribution, seqs 106 to 108 | **baseline** | the library's copies put three `stand` tuples on the human artifact while three others sat on the machine artifact; baseline is internally consistent |
| seq 117 artifact | **`later-essay.md`** | a month name in a filename invites the date-thinking the time model forbids |
| INF-002 `last_fired_run` at t2 | **1, pinned, never derived** | see below |
| `named_on_run` | **kept as a cell field** | a field is a field |
| seq 118 | **deferred** | restoring it needs curation events as a tuple kind, which is a specification change reaching the generator |
| cluster `members` | **baseline** | see the overrule below |
| evidence pointers | **verified set, null where nothing exists** | see below |


**Correction, entered after Artlord's audit.** The pointer count above originally read twelve resolving. Twelve carry a pointer and eleven resolve. Recorded rather than silently fixed, because this file is the record.

**Correction, same audit: deferring seq 118 did not stop the run-date inversion shipping.** It ships in pieces that no longer sit together: `named_on_run: 13` in the file, the ratification dated July 9 in the cell dictionary, and run 12 dated August 2 in the reel. So run 13 precedes run 12 across the frozen set. The render is unaffected, since age is integer subtraction, but the run-to-date map is not monotone and a fixture is held to being possible. Resolved by moving the dictionary date to after run 12 rather than by moving `named_on_run`, which carries the born-faded demonstration, or seq 117, which is load-bearing for the one recent touch.
## The guardrail, which is now a generator invariant rather than a fixture property

**INF-002 carries `last_fired_run` 1 at t2, against a run counter of 18 and a `named_on_run` of 13.**

That single integer is the born-faded property: a rule is as fresh as its evidence and never as fresh as its christening. Tastemonger ratified it, the storyboard demonstrates it, the reader guide teaches it as the lesson that surprises everyone once.

A generator deriving the value from the provenance array's maximum sets it to 13, which looks like a repair while deleting the demonstration, and does so invisibly because a mark at 65 percent extent is perfectly plausible. So the rule does not live in this file: **`last_fired_run` is stamped, never computed, and a promotion does not refresh it.**

## The pointers, verified rather than reported

Both generations were checked against the shipped artifacts rather than against either side's account of them.

`rupture-v2_evidence.md` carries anchors h11, h11-1 through h11-3, h14, h14-1 through h14-3, h14-filtered, h14-filtered-1, h210, h210-1. `Rupture_V3.docx` carries tracked-change revision ids 0 through 50. `rupture-v4_evidence.md` carries no anchors at all.

Every pointer from the baseline resolves. Every pointer from the library's copies fails, and three of them cite rules that scored zero, which the evidence file's own stated rule forbids: a rule that did not fire has nothing to point at.

Twelve of seventeen tuples carry a pointer. **Eleven are intended to resolve; the twelfth is the deliberate failure below, and the distinction is the whole value of the set.** Five are null because nothing exists to cite, which is honest where a fabricated target is not. Seqs 101, 102 and 103 name rules that did not fire. Seq 109 names an informational row that gets no evidence section. **Seq 108 is the interesting null: H3.2 fired sixty-eight times on this document and the gate records no evidence for it at all**, which is a defect in `scrub-gate.py` rather than in the fixture, logged below.

**Seq 117 keeps its deliberately unresolvable pointer** to `later-essay.evidence.md#h12-1`. It is the drill-down degradation fixture and it is the reason the other nulls matter: a fixture set where every pointer fails cannot distinguish the deliberate failure from the accidental ones, and the degradation path stops being tested.

Pointer filenames use the dot form, `rupture-v2.evidence.md`, which is what `scrub-gate.py` emits. The uploaded copies arrive as `rupture-v2_evidence.md`, and the platform is known to alter filenames on upload, so the tool's output was taken as canonical. **Verified since, by Artlord, at source rather than from help text:** `scrub-gate.py` builds the name as the input stem plus `.evidence.md`, so the dot form is what the tool emits and the container's other form is a platform rename. This item is closed.

## One overrule, against Artlord's own recommendation

Artlord recommended taking the library's cluster `members` on the grounds that the specification's schema sketch shows evidence-style members, and flagged that the swap would cost the fixture its sort-bug coverage.

**The merge takes baseline's members instead**, for two reasons Artlord's own analysis supports without connecting them. The sketch shows `ev:2026-07-07#c14`, a date-keyed format matching neither generation and contradicting the restored time model, so it is an illustrative example needing correction rather than a rule to follow. And the library's members resolve nowhere, which is Artlord's gap-3 argument applied to the one field it did not apply it to.

Baseline's members resolve and preserve the sort coverage. The specification's example is what needs fixing.

## Defects found in each generation, recorded so neither is mistaken for clean

**The library's copies:** weight seeds flattened to 0.5 across all sixteen cells at t0; three `stand` tuples attributed to the wrong artifact; every evidence pointer unresolvable, three of them structurally impossible; run fields absent entirely.

**Artlord's copies:** seq 118 carries run 13 with date 2026-07-09 while seq 117 carries run 12 with date 2026-08-02, so run 13 predates run 12. The tuple is deferred so the inversion does not ship, but whichever field is wrong should be settled before it is ever restored. Also H2.2 and H3.5 still in the cell set, and placeholder strings in `model`.

## The ledger

The freeze discipline is that anything outstanding carries a line here. So does anything closed, with what closed it, because an owed list that only grows is not a record.

**Closed since the merge**

The specification amendments this merge implied: `spec_version` bumped to 1.1, weight seeding sourced to the frozen fixture rather than to anyone's memory, `named_on_run` and `first_seen_run` and reel `run` documented, the undefined-region members example moved off its retired date-keyed form, the exactly-one-of rule for `rule_id` and `cluster_id`, the evidence-pointer conventions, the monotonicity constraint on the run-to-date map, and the extent-not-tone distinction fixed in the document.

The pointer filename convention, the one call this note declared unverified. Closed at source by Artlord reading the gate's construction rather than its description.

The run-date inversion, by moving the cell dictionary's ratification date to 2026-08-03.

The dictionary's six over-limit short names, brought to the writer's ruled renames: chat leak, not-just, metronome, sigflation, self-grading, self-hedge. The two names sitting at exactly eighteen characters keep their full form.

**The weight endpoint, and it was logged nowhere until Artlord raised it.** The specification stated the endpoints as 1.0 and 0.0. The ratified values are 1.0 and 0.4, exactly 1.0 meaning a writer-locked absolute and exactly 0.4 meaning informational, neither reachable by accretion. The wrong value was written into the very section meant to source weight rules to the fixture instead of to memory, and the build role had already implemented an open interval against it. Corrected in the specification and in the generator, which now verifies the pin against the frozen t0 fixture directly.

**The retired pointer form surviving in the reel example**, the sibling of the one the members overrule removed twelve lines away. Corrected, along with the pointer rule itself, which was imprecise in a way the example exposed: pointers follow whatever recorded the event, so a gate-detected rule cites the evidence file even when the tuple records the writer's response.

**Still owed**

Seq 118 and curation events as a tuple kind, at specification v1.1.

The H3.2 evidence gap in `scrub-gate.py`: a counted, gated floor row whose matches are never recorded, so the evidence file's own claim to list every pattern location is false for that row.

The render specification's own amendment pass, design-side: the minimum working scale, the version bump, `named_on_run`, the pointer normalization rule, and the extent-not-tone line. No geometry moves.

## The freeze

These three files are the fixtures. Artlord audits them against its committed checklist plus the sixty-six-tone script and the pointer-resolution check it proposed, then reports before cutting. The build role uses them as fixtures and continues to write invariant tests against the specification rather than against these files.

Any subsequent change routes through this orchestrator and is recorded here. That is the whole point of the freeze, and it is cheaper than the three correction cycles that preceded it.
