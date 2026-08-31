# Pipeline flags: the settings registry

*Folded from `pipeline-flags.md`, canon V3.3, August 2026. Compiled variant: the source file is master.*

One job: hold the workflow settings, which are not craft, not sequence, and not register parameters. A flag changes how the desk collaborates; a profile changes what kind of writing is on it.

**The one rule for flag conduct.** Flags set defaults; conversations override them; overrides are stated, not silent. A setting the agent flips without saying so is a decision taken from the writer.

Defaults are the writer's to edit. An agent honors the table unless the conversation overrides it, and states the override. GNU-style long names. This registry is markdown because agents read markdown as instruction; it becomes TOML when the compiler exists, and these semantics are what compilation must preserve.

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

**`--verbose`.** The agent halts at every stage boundary, says what it did, where the run stands, and what comes next, and may ask before continuing.

Semantics: adds stops, does not create them. The unconditional stage-1 halt and the pushback triggers stay mandatory when it is off. The behavioral battery's failure family was under-stopping, and a setting that made required stops optional would deepen that fault. Downstream: none. Workflow instruction to the agent, not script code.

Recorded hypothesis, untested: a run that finishes a stage, stops, and resumes from its stated result may do better work than one carrying every stage through a single pass, independent of legibility. A question for the eval battery, not a claim.

**`--evidence`.** Implemented in `scrub-gate.py`. Writes the per-match markdown audit: locations, quoted context, and the candidates the post-filters rejected. The tuning surface for every heuristic counter.

**`--calibrate`.** Implemented in `scrub-gate.py`. Rates only, TSV, no verdicts: the measuring half of the calibration protocol, run across the three corpora.

**`--fired-view`.** One-shot: after a gated run, emit the single grid frame for that artifact, rendered from the grid file. A frame, not the reel; requires a grid file to exist.

**`--provenance-file`.** Append the run's provenance tuples to the reel, creating it if absent. Tuples come from a ratified accretion template, never a raw diff. Every tuple carries its author, a configured desk value and never anything read from document metadata: metadata records the machine a file was opened on, not the hand that did the writing.

**`--grid`.** Master switch for accretion writes. Off means the pipeline runs as it does today and nothing accretes; sensors may still be on for the human's own use. Default stays off and the choice is the writer's: a desk that accretes is a desk whose rules move under it, and that is opted into rather than inherited. Turning it on means seeding a desk with `ship-check.py seed`, then running the accretion conversation after a human pass and consuming its template with `craftgen`.

## Retired

`--trackchanges` asked the agent to return its own passes as tracked changes, serving legibility and sensing at once, and failed at both. A stage-7 scrub marks up as a dozen small removals and reads well; a stage-2 restructure marks up as every sentence changed and reads as noise, so legibility degraded where the work was largest. And a diff cannot carry intent, which is what the sensor needs. Legibility moved to `--verbose`; sensing moved to the accretion conversation in `accretion-conversation.md`. Asking for a marked-up copy of any output remains an ordinary request and needs no flag.
