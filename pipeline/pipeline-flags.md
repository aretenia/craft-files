# Pipeline flags: the settings registry

*A thin settings layer beside the three the scaffold names: workflow preferences, not craft, not sequence, not register parameters. A flag changes how the desk collaborates; a profile changes what kind of writing is on it. Flags use GNU-style long names. This registry is markdown because agents read markdown as instruction; it becomes TOML when the compiler exists, and the semantics here are the spec that compilation must preserve. Defaults are the writer's to edit in the table below; an agent honors the table unless the conversation overrides it, and states the override.*

---

## Defaults

| flag | default | note |
| --- | --- | --- |
| `--verbose` | off | Stops at every stage boundary. On when you want to watch the run. |
| `--evidence` | off | On for gate runs the writer intends to audit or tune. |
| `--calibrate` | off | Measurement mode; corpus work only. |
| `--fired-view` | off | Grid v1 shipped; on when you want the frame for a run. |
| `--provenance-file` | off | Grid v1 shipped; on to append the run to the reel. |
| `--grid` | off | Master switch for accretion writes. Grid v1 shipped; the writer's call. |

## Registry

**`--verbose`.** The agent halts at every stage boundary, says what it did, where the run stands, and what comes next, and may ask before continuing. Semantics: this flag adds stops; it does not create them. The unconditional stage-1 halt and the pushback triggers stay mandatory when it is off, because the failure family the behavioral battery found was under-stopping, and a setting that made the required stops optional would deepen exactly that fault. Downstream: none. One recorded hypothesis, untested, kept here so it stays findable: a run that finishes a stage, stops, and resumes from its stated result may do better work than one carrying every stage through a single pass, independent of any gain in legibility. That is a question for the eval battery, not a claim this file makes. This flag is a workflow instruction to the agent, not script code.

An earlier flag, `--trackchanges`, asked the agent to return its own passes as tracked changes, serving legibility and sensing at once. It failed at both. A stage-7 scrub marks up as a dozen small removals and reads well; a stage-2 restructure marks up as every sentence changed and reads as noise, so legibility degraded exactly where the work was largest. And a diff cannot carry intent, which is what the sensor actually needs. Legibility moved here; sensing moved into the accretion conversation described in `scaffold-and-calibration.md`. Asking for a marked-up copy of any output remains an ordinary request and needs no flag.

**`--evidence`.** Already implemented in `scrub-gate.py`. Writes the per-match markdown audit: locations, quoted context, and the candidates the post-filters rejected. The tuning surface for every heuristic counter.

**`--calibrate`.** Already implemented in `scrub-gate.py`. Rates only, TSV, no verdicts: the measuring half of the calibration protocol, run across the three corpora.

**`--fired-view`.** One-shot: after a gated run, emit the single grid frame for that artifact, rendered from the grid file. A frame, not the reel; requires a grid file to exist. Grid v1.

**`--provenance-file`.** Append the run's provenance tuples to the reel, creating it if absent. Tuples come from a ratified accretion template, never from a raw diff. Every tuple carries its author, which is a configured desk value rather than anything read out of document metadata, since metadata records the machine a file was opened on and not the hand that did the writing. Grid v1.

**`--grid`.** The master switch for accretion writes. Off means the pipeline runs exactly as it does today and nothing accretes; sensors may still be on for the human's own use. Grid v1 ships with this release, so the default stays off and the choice is the writer's: a desk that accretes is a desk whose rules move under it, and that should be opted into rather than inherited. Turning it on means seeding a desk with `ship-check.py seed`, then running the accretion conversation after a human pass and consuming its template with `craftgen`.

---

## One rule for flag conduct

Flags set defaults; conversations override them; overrides are stated, not silent. The pattern is the budget meta-rule wearing workflow clothes, and it exists for the same reason: a setting the agent flips without saying so is a decision taken from the writer.
