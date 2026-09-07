# Changelog

What changed in each version of this library. Versions before 3.1 are reconstructed
from the README's own version narrative, since no changelog was kept at the
time; entries for 3.1 and 3.2 are written from the record.

## 3.4, September 2026

Drafts made visible. The provenance record grew to carry what a picture needs,
and the library gained the code that draws it.

### Added

- The draft-chain record, specified in `skills/craft-v3.4-spec.md` section 2.
  One entry per pass written at the handoff, with a full text snapshot rather
  than a diff, because a snapshot is what makes a chain auditable years later.
  Each entry carries the pass label, the agent, the ruling with its evidence
  class, a timestamp, the model where there was one, and any moves.
- `skills/draft-provenance`, which reads a chain of drafts and derives the
  per-word record: for every word of the final text, who typed it, which
  hands touched it, whether a later human pass kept it, whether it came back
  from an earlier draft, and how many passes rewrote its sentence.
- `skills/text-layers`, which reads that record and draws the piece: PNG
  sheets at the column measure for review, and one self-contained HTML for
  reading that embeds both faces, makes no external request, and opens on a
  phone with no network.
- Six flags in `pipeline/pipeline-flags.md`: `--provenance` (always on),
  `--layers`, `--layers-out`, `--package`, `--heat-floor`, `--min-minority`.
- The two locked faces, Alegreya for the person and Recursive for the
  machine, with their OFL licences, in `skills/text-layers/assets/`.
- A positive tracked-changes fixture and `scripts/selftest.py`, both part of
  release acceptance.
- V3.4 checks in `accept.py`, covering the audit halts, the self-test, the
  self-containedness of the HTML, and the locked face set.

### Changed

- **A ruling is a per-edit fact, not a pass-level boolean.** The record
  carries `ruled` per edit where a ruling actually happened, and derives a
  pass-level summary that is tri-state (`ruled`, `unruled`, `unrecorded`) and
  always carries its source (`event`, `header`, `attestation`,
  `unrecorded`). A boolean cannot tell "the writer did not rule" from
  "nobody wrote it down," and the library will say `unrecorded` rather than
  infer. No existing pipeline event establishes that a writer ruled every
  change in a pass, so the library never claims one.
- The audit table prints before any render, with shares to four places and
  per-pass flags, and two of its conditions stop the run with a question: a
  pass identical to the draft before it, whichever hand made it, and a pass
  labelled human that changed more than half the words. A genuinely small
  pass passes with a note. Shares are never rounded into a decision.
  `--accept-audit` records that a question was read and proceeds.

### Fixed

- The tracked-changes reader was silently inert. It parsed the document
  twice and marked insertions on the tree it did not walk, so no insertion
  could ever have been flagged, and no chain in hand had surviving tracked
  changes to expose it. Found by asking for a positive fixture, fixed, and
  now proven by one.
- The record and render scripts read and wrote JSON with no encoding
  specified, so on Windows they used the ANSI code page and raised on the
  record's own characters. The library's writer works on Windows; the
  release would not have run for him.
- The review-sheet renderer required a Pillow built with libraqm and raised
  rather than degrading when the OpenType features it asked for were
  unavailable, which is the stock Windows wheel. It now drops the ligature
  settings, says so, and draws the sheet.
- The review sheet drew the two faces at the x-height match, 0.955, while
  the HTML used the locked 0.907, so the two renders disagreed on relative
  face size, which acceptance compares. The locked instance is now the
  default on both sides.
- `accept.py`'s "no committed bytecode" check walked the working tree for
  `.pyc` files, which are gitignored and untracked, so it failed on any
  checkout where anything had been run. It now asks git what is tracked.

## 3.3, July 2026

Two threads landed together: the accretion organism gained its first code and
specification layer, and the scrub gate gained the three register profiles it
was missing along with the hedging row.

### Added

- The accretion organism's first working code and the canon that specifies it.
  The pipeline can now read a human editing pass and turn which of its rules
  earned their place into a live, glanceable record. The sensor is a
  conversation, specified in `accretion-conversation.md`; its output is a
  ratified template, specified in `accretion-template-spec-v1.md`; a generator
  turns that template into a grid file, specified in `grid-spec-v1.md`. The
  grid itself remains unshipped and its pipeline flags stay off; what lands
  here is the specification layer and the generator that reads it.
- `--verbose`, a workflow flag that stops the pipeline at every stage boundary
  to narrate and optionally ask. It adds stops rather than creating them: the
  mandatory stage-one halt and the pushback triggers stay mandatory when it is
  off, since the behavioral battery's one failure family was under-stopping.

- - `H2.9`, symmetric hedging, is now counted. Job-search has declared it since
  the register existed and the gate never enforced it. It ships as two lexicon
  subsets: dissolution, the verdict that refuses to land, which is canon's own
  example; and qualifier, the force-draining hedges the cut list names. Both
  are scoped to job-search, because the corpus evidence says hedge frequency
  does not indicate machine authorship and surfacing it elsewhere would report
  a signal against the evidence.
- A `subset` column on `machinelexicon.csv` and an optional subset selector on
  profile rows, so a register can govern part of a tier rather than all of it.

- The three register profiles the gate did not implement: satire, fairy-tale,
  and llm-script. Canon published six; `scrub-gate.py` scored three, and the
  other three were rejected at the command line rather than merely missing.
- Two rows canon declares that the gate had no entry for at all. Satire and
  the fairy-tale register declare H2.1, the throat-clearing opener and the
  opening formula respectively; job-search declares H2.9, symmetric hedging.
  H2.9 has no counter and now reports as owed rather than vanishing.

### Changed

- The accretion organism ships usable rather than as a specification. It was
  not: `bootstrap_grid` produced an empty shell, the generator correctly refused
  to mint cells, and nothing else created them, so a new desk refused every
  template it was given. `ship-check.py seed` closes that gap, reading canon's
  budget table and emitting a populated grid at the ruled seed weights. Found by
  running the documented workflow rather than by testing components, each of
  which passed.
- `register-profiles.md` budget tables gain a `class` column declaring each row's
  enforcement class: absolute, budgeted, or informational. The seed weight
  follows from it. The column exists because the class is not derivable from the
  other fields: citations and typography share mode, direction, target and sd,
  and seed at 1.0 and 0.4 respectively. A tool that inferred the difference from
  the prose note would have been a second source of truth about canon.
- `accretion-conversation.md` gains three rules the first real run exposed:
  residue carries a direction, and a cluster of strikes is a habit the machine
  keeps producing while a cluster of adds is one the writer keeps reaching for,
  which become different rules at promotion; every entry cites what recorded the
  change, because a cluster whose members point only at reel positions can be
  counted but not reread; and `accretion-template-spec-v1.md` now says what a
  null `model` costs, which is that the pattern can accumulate evidence and
  never promote, since version survival is the classifier and it answers from
  that field.
- `accretion-conversation.md` also gains the role-assignment rule, found by
  running the sensor against a deliberately ambiguous artifact. Which file is
  the draft, which the machine pass, and which the writer's markup is told to
  the conversation out of band and never read from the document, because the
  library holds a file whose own header note says one thing before its tracked
  changes are applied and the opposite after. The residue fallback narrowed in
  the same pass: it holds where the roles are known and the draft is absent, and
  fails where the roles themselves are undetermined, since logging residue would
  first require assuming whose hand made the edits.
- `--trackchanges` is retired. It tried to serve legibility and accretion
  sensing with one mechanism and failed at both: it drowned dense passes in
  markup, and a diff cannot carry the intent the sensor needs. Legibility moved
  to `--verbose`; sensing moved to the accretion conversation, which recovers
  the seam from document versions and asks the writer what each change meant.

- `scrub-gate.py`: the registry of what the gate can measure is separated from
  the transcription of canon's budget tables. Holding both in one structure is
  what let the earlier divergence hide. Classification is now derived rather
  than listed: declared with a band and backed by a counter is gated, declared
  without a band is a rule row judged by hand, declared with a band and no
  counter reports as owed, and a counter the active profile does not declare
  reports as annotation vocabulary. The previous hardcoded annotation list
  could not express the fairy-tale register, which declares H2.2 as a required
  closing formula rather than an artifact to suppress.
- `scrub-gate.py`: verdict arithmetic is null-safe. Canon writes `n/a` for an
  absent band, and two registers use shapes that previously raised an error, a
  floor with no band and a row stood down entirely.
- `scrub-gate.py`: where a register renames a row, canon's name now prints,
  because the rename usually carries the inversion.
- `scrub-gate.py`: H1.1 evidence no longer reports marks on footnote-definition
  lines, which the counting pass strips. The evidence file is the deliverable
  of record and must not name a match the gate did not count.
- `scrub-gate.py`: the lexicon search no longer carries absolute container
  paths, which meant nothing to anyone who cloned the repository.
- Report row order follows canon's tables, and the rule rows print inline
  rather than in a trailing line. Counts, verdicts and flag totals are
  unchanged for the three registers that already worked.

- `compiled/`, folded variants of all seventeen pipeline files, compressed
  through the llm-script register for a model audience. Aggregate 79 percent of
  source words, ranging from 60 to 97 by how much a file had to remove. Every
  hallmark ID, budget number, and citation survives; the six budget tables are
  reproduced verbatim. Not eval-certified: the July fold was measured against
  the behavioral kit at six of six, and these were not measured. The source
  files are master, the fold is lossy and one-directional, and where the two
  disagree the source governs.

### Fixed

- Job-search banned all seventy-seven marked-lexicon terms when canon declares
  only the flowery subset, because the gate had no way to express a subset. A
  resume was flagged for domain verbs that canon explicitly exempts. Flowery is
  now the noun and phrase clusters, twenty-nine terms, covering every term
  canon names by example.
- `ship-check.py drift` checked one register of six and broke outright against
  the restructured gate, since it read the budget table by scraping source
  text. It now imports the gate, resolves canon the same way the gate resolves,
  and compares every register field by field. Its canon parser also keyed on a
  `### Budget` heading that only three registers have; it keys on the table
  header row, which all six share.
- `ship-check.py drift` read stale bytecode. Python reuses a cached compilation
  while the source's recorded size and modification time still match, and that
  time has one-second resolution, so a one-digit edit rechecked within the same
  second was verified against the file as it had been before the edit. It now
  compiles from source and writes no cache.
- `scrub-gate.py` recorded no evidence for H3.2, a counted and gated floor row:
  its matches were counted but never located, so the evidence file's own claim
  to list every pattern location was false for that one row, and the row was
  missing from the evidence section order entirely. Both passes now record each
  match at its position and the row has a section. Counts and verdicts are
  unchanged.

## 3.2, July 2026

### Added

- `luthi-folktale-style.md`, `propp-morphology.md`, and
  `tolkien-secondary-belief.md`: three craft files for the fairy-tale form,
  covering the flat surface and its formula machinery, the fixed grammar of
  functions and spheres of action, and the sub-creation contract the other
  two exist to serve.
- The fairy-tale register in `register-profiles.md`, replacing the stub it
  shipped as in 3.0. Propp displaces Truby on the surface tale; Truby
  survives on the meaning side of a doubled armature, where the reader
  arrives with a frame and leaves changed. Five budget rows change: the
  opening and closing formulas invert from ceiling to floor on the frame
  argument, the rule of three is re-moded from count to rule because the
  counter matches syntactic lists and the form's threes are structural, the
  uniformity ceiling loosens to six because verbatim repetition is the
  form's machinery, and the specificity floor is re-scoped to concrete
  images since the abstract style forbids the documentary detail.
- The llm-script register in `register-profiles.md`, replacing its stub.
  It flips the audience from a human reader to a model and supplies the
  fold rules as operational canon, so refolding the library needs only
  these files.

### Changed

- `scaffold-and-calibration.md`: the stopping discipline. The stage-one
  halt is now unconditional, firing when the armature looks settled as
  well as when it looks contested. A full pipeline run is stated to be a
  conversation with at least one mandatory turn rather than a program that
  runs to completion. Pushback trigger three widens to cover an armature
  the pipeline identified but the writer never ruled on, which is the
  quieter failure, because the prose comes back polished either way.
- `hallmarks-and-the-scrub.md`: H1.6 extends to the pipeline's own replies,
  not just the artifacts it gates. A report that closes on an offer of
  further work is the artifact the row bans, produced by the agent
  enforcing the ban. End on the finding.
- `scrub-gate.py`: sentence segmentation now closes on em-dash-attached
  terminals and on no-space terminals between a lowercase letter and a
  capital, unit-tested so initialisms and decimals stay whole. Evidence
  lines locate the matched text rather than the base lemma's first word,
  which restores audit lines that stem-changing inflections used to drop
  and points phrase hits at the phrase.
- `scrub-gate.py`: drift alignment. The reported table now equals the
  fourteen rows the default budget table declares. H2.2 and H3.5 are still
  counted but report below the table as annotation vocabulary rather than
  as gated rows, because canon does not declare them; H1.5 and H3.3 print
  as the rule rows canon does declare, for the reader to judge, rather
  than being silently omitted.
- `README.md`: thirteen files rather than ten, three table rows for the
  new craft files, the pipeline described as a conversation that halts for
  the writer's ruling, both registers named, and a tooling section.
- `truby-story-structure.md`, `forsyth-repetition-family.md`,
  `scaffold-and-calibration.md`: marked-lexicon terms swapped for
  unmarked equivalents. The library holds its own files to the budgets it
  publishes.

## 3.1, July 2026

### Added

- First-person epistemic modesty as a harvested informal rule in the
  default profile: modesty attaches to the first person, never to the
  claim. Soften absolute framings of the writer's own knowledge or a
  claim's reach; leave the argument its edges.
- `scrub-gate.py` published to the repository, with its description in the
  README.
- A source-frameworks section in `LICENSE`, crediting the machine-artifact
  layer to Wikipedia's WikiProject AI Cleanup and two academic papers
  alongside the craft sources.

## 3.0

### Added

- The machine-artifact layer: `hallmarks-and-the-scrub.md`, a tiered
  catalog of AI-text hallmarks and a deterministic gate at the end of the
  pipeline; `machinelexicon.csv`, the marked-term data file; and
  `scrub-gate.py` as the gate's reference implementation.
- `register-profiles.md`: a registry of register profiles with stage
  manifests and frequency budgets, generalizing version two's single
  calibration overlay. Budgets ship provisional until the calibration
  protocol measures them.
- Three process disciplines in the scaffold: pushback, the calibration
  protocol that replaces judgment numbers with measured ones, and
  versioning against model drift.

### Changed

- The cut list, experimental in version two, promoted to canon and
  unified with the hallmarks vocabulary.

## 2.0

### Added

- Four files: `goldberg-first-thoughts.md` for the generation pass,
  `mcdonald-armature.md` for the controlling idea above structure,
  `forsyth-repetition-family.md` for the figures that work by repetition,
  and `gardner-continuous-dream.md` for the continuity pass.
- An explicit pipeline sequencing the files, and a model for building a
  calibrated writing system, both in `scaffold-and-calibration.md`.

## 1.0

### Added

- The first craft files, turning source frameworks into operational
  guidance an assistant can act on: structure, paragraph-level flow, the
  surprise family of figures, the final editing rules, and the attention
  layer beneath them.

---

*Provenance: assembled by the craft-files library orchestrator, July 23,
2026, at the writer's direction, from the project files and the session
record. Entries for 3.1 and 3.2 were checked against the files they
describe. Entries for 3.0 and earlier are reconstructed from the README's
version narrative and are the weaker claim. No human pass.*
