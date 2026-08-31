# Register profiles: the parameter layer

*This is the scaffold's third layer, generalized. Where version two defined a single calibration overlay per writer, this file defines a registry: one default profile plus per-register deltas, so the same base library serves job-search prose at nine in the morning and satire at nine at night without either contaminating the other. Profiles are parameters, not craft. Nothing in this file teaches a technique; it tunes when the techniques run and how hard the scrub bites.*

*The format is canon; the profiles are mine. A stranger forking this library keeps the schema and replaces the profiles, the same way the scaffold's worked calibration example was always meant to be replaced.*

**Version: calibrated July 2026, against the model generations named in the hallmarks file.** All budget numbers are PROVISIONAL, set by judgment pending the calibration protocol in the scaffold, which replaces them with measured rates from three corpora. The banner comes off a profile when its numbers have been measured.

---

## The schema

A profile has eight parts. The first five are the calibration overlay's original format, unchanged: **domain**, **register and voice**, **reserved vocabulary**, **audience**, and **exemplar swaps**. Profiles add three:

- **Manifest.** Which stages run, by the scaffold's numbering. The manifest selects; the scaffold orders. A profile may drop stages it does not need, but it never reorders what it keeps, and stage 7 (the gate) is never dropped, only tuned.
- **Budget table.** Rows keyed to hallmark IDs from `hallmarks-and-the-scrub.md`, which are also the join key to `machinelexicon.csv`.
- **Deltas.** The `default` profile is fully specified. Every other profile lists only what differs; unlisted rows and parts inherit.

### Budget row fields

| Field | Meaning |
| --- | --- |
| `id` | Hallmark ID. `H0.*` means the whole tier. |
| `mode` | How the row is enforced. See below. |
| `dir` | `ceiling` (at most) or `floor` (at least). |
| `target` | The number. `0` with a ceiling is a hard ban. Floors take positive targets. |
| `sd` | The spread. See below. |
| `note` | Cause, precedent, drift, exemptions. |

**Modes.** Three, chosen per row, switchable by the user; document the switch in the note.

- `count` (the default): occurrences per 1,000 words. Enforceable today, by hand or by script, with no reference corpus required.
- `ratio`: a multiple of a named reference corpus's rate. More defensible than a raw count, because it says "human base rate" out loud, but it requires the calibration protocol to have run. Rows can be promoted from `count` to `ratio` once the corpora exist.
- `rule`: a qualitative instruction, judged rather than counted, for artifacts that resist per-1,000 arithmetic. A rule row may still carry a numeric parameter in `target`: the uniformity ceiling's maximum run length, for instance.

**What `sd` means.** Two duties, both aimed at the same enemy.

1. *Tolerance.* The gate flags a row when the observed count falls outside `target ± sd`. A ceiling of 3 with sd 2 flags at 6, not at 4.
2. *Dispersion.* Occurrences should cluster the way human use clusters. A human writer spends three dashes in one hot paragraph and none for two pages; a machine spaces them evenly. The gate checks clumping as well as totals, and an evenly-spaced distribution at a legal total still earns a note. `sd 0` means no tolerance and no dispersion check: a ban.

**The meta-rule.** Orwell's rule 6, formalized: any budget may be broken deliberately and for cause, and the override is stated, not silent. The pipeline proposes the override with its case; the writer rules. The one exception: `0`-target rows are not overridable by the pipeline at all. Only the writer, editing the profile, can unlock a ban, which is what keeps a ban a ban.

---

## Profile: default (analytical long-form)

The keystone register, and the maximal case: every stage runs, every file loads. The goal is essays that use the whole library and read to a primed human reader as human-written, because they are: the machine drafted, the writer decided, and the residue was swept.

- **Domain.** Argumentative long-form: essays, criticism, technical and cultural analysis. Recurring shapes: the diagnostic essay, the reframe, the case study carrying an idea.
- **Register and voice.** Dense, committed, allergic to the safe middle. Claims with edges. Wit permitted, whimsy earned.
- **Reserved vocabulary.** Inherits the machine lexicon's ceilings below; no additional bans by default. Prefer plain verbs; the avoid-list is the budget table.
- **Audience.** Intelligent generalists who can be trusted to assemble the point.
- **Manifest.** Stages 0 through 7, all files, the attention layer live throughout.
- **Exemplar swaps.** None; the base files' neutral examples stand until the calibration protocol harvests better ones into this profile.

### Informal rules (harvested)

Rules accreted from the writer's own corrections, per the scaffold's promotion mechanic. Single-source until they recur; each cites its evidence, and each applies to this register unless a delta says otherwise.

- **No sincerity preamble.** Never frame a claim with a declaration of honesty; state the claim. The sentence is the honesty. (Two independent cuts in one human pass; Rupture, July 2026.)
- **First-person epistemic modesty.** Modesty attaches to the first person, never to the claim: soften absolute framings of the writer's own knowledge or a claim's reach, and leave the argument its edges. (Five softenings of first-person or reach absolutes in one human pass that elsewhere sharpened its claims; Rupture, July 2026.)

### Budget table (PROVISIONAL)

| id | artifact | mode | dir | target | sd | class | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H0.* | leaked interaction artifacts | count | ceiling | 0 | 0 | absolute | Ban in every profile except satire's deliberate unlock. Gate stops and reports on any hit. |
| H1.1 | em dash | count | ceiling | 3 | 2 | budgeted | Cluster where the heat is; spaced dashes normalized to house style. |
| H1.2 | marked lexicon, aggregate | count | ceiling | 2 | 1 | budgeted | Per `machinelexicon.csv`, matched by lemma. Any single term at most once per 1,000. Domain-native terms exempted via reserved vocabulary, with the exemption noted. |
| H1.3 | negation-antithesis | count | ceiling | 1 | 1 | budgeted | Never twice in one section. Forsyth owns the craft of the one that stays. |
| H1.4 | triads | count | ceiling | 3 | 1 | budgeted | Consecutive-sentence triads flag regardless of total. |
| H1.5 | bold-led label bullets | rule | ceiling | n/a | n/a | budgeted | Collapse label-restatement pairs; lists only where content genuinely enumerates. |
| H1.6 | sycophancy and engagement scaffolding | count | ceiling | 0 | 0 | absolute |  |
| H2.3 | sentence-initial formal connectives | count | ceiling | 2 | 1 | budgeted | The Moreover/Furthermore/Additionally class, counted at sentence heads. |
| H2.4 | significance inflation | count | ceiling | 1 | 1 | budgeted | One instance may survive if it earns its place; the second never does. |
| H2.5 | trailing participial analysis | count | ceiling | 1 | 1 | budgeted |  |
| H2.10 | uniformity ceiling | rule | ceiling | 4 | 1 | budgeted | Max consecutive sentences within four words of a shared length. Repair by preserving generation-stage variance, never by injecting fragments. |
| H3.2 | specificity markers | count | floor | 8 | 3 | budgeted | Proper nouns, numerals, and dates per 1,000 words. A proxy with teeth, not the repair; a floor violation is a pushback trigger, not a rewrite instruction. |
| H3.3 | citations | rule | n/a | n/a | n/a | absolute | Verify or cut. No register overrides this row, anywhere. |
| H4.3 | typography | rule | n/a | n/a | n/a | informational | Straight quotes. Em dashes spaced, the house hand for essays: normalize toward spaced, never closed. Silent when gating the writer's own draft. |

Rows not listed are annotation-vocabulary artifacts: marked and judged in the late reads rather than counted at the gate.

---

## Profile: creative long-form

*Deltas from default.* The same spine leaning into its figures. The keystone's rules mostly hold, because the human-written feel is the same objective; what changes is how much rope the intensification stage gets.

- **Register and voice.** As default, plus scene, image, and interiority; psychic distance actively modulated rather than held.
- **Manifest.** Unchanged. Gardner's file is load-bearing here rather than a final check.
- **Budget deltas.**

| id | artifact | mode | dir | target | sd | class | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1.4 | triads | count | ceiling | 4 | 1 | budgeted | The repetition family earns more room; the Forsyth ceilings still govern each instance. |
| H3.2 | specificity markers | count | floor | 8 | 3 | budgeted | Re-scoped: sensory particulars and concrete images count alongside proper nouns and numbers. |
| H2.10 | uniformity ceiling | rule | ceiling | 4 | 1 | budgeted | Unchanged, with a note: distance modulation does this work organically; if the ceiling keeps flagging, the problem is upstream in the Gardner pass, not here. |

---

## Profile: job-search

*Deltas from default.* The lean register: employer-facing documents, where the reader is primed, the stakes are personal, and the genre expects discipline over flourish. This is not creative writing, and the manifest says so.

- **Domain.** Resumes, cover letters, outreach, and anything an employer will see.
- **Register and voice.** Plain, specific, quantified. Claims carried by evidence, not adjectives.
- **Audience.** Recruiters and hiring managers: skimming, pattern-primed, and reading twenty of these before lunch.
- **Manifest.** Stages 0, 1, 3, 5, 6, 7. Truby's arc is skipped: a cover letter has a point, not a plot. Forsyth is skipped by default; a single figure may be imported deliberately, as an override with cause.
- **Budget deltas.**

| id | artifact | mode | dir | target | sd | class | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1.1 | em dash | count | ceiling | 0 | 0 | absolute | Encodes the standing house rule for employer-facing documents. The reason is this register's whole situation: the reader is exactly the primed reader, and the false-positive cost lands on the writer. |
| H1.2 | marked lexicon, flowery subset | count | ceiling | 0 | 0 | absolute | Tapestry, realm, journey, and kin have no business here. Domain verbs of the trade stay exempt-listed in reserved vocabulary, because "led" and "shipped" beat "spearheaded" anyway. |
| H1.5 | bullets | rule | ceiling | n/a | n/a | budgeted | Re-scoped, not banned: bullets are genre-native in a resume. The banned artifact is the label-restatement pair, which is exactly as dead in a bullet as in prose. |
| H2.9 | symmetric hedging | count | ceiling | 0 | 0 | absolute | Claims commit. A hedge in a cover letter is a withdrawal. |
| H3.2 | specificity markers | count | floor | 12 | 3 | budgeted | Raised: numbers are the genre's currency. |
| H2.10 | uniformity ceiling | rule | ceiling | 6 | 1 | budgeted | Loosened, deliberately. This genre expects parallel structure and steady cadence; the human-written feel is register-relative, and here a little uniformity is the convention, not the tell. |

---

## Profile: satire (slop mode)

*Deltas from default, most of them inversions.* The register that runs the catalog in reverse: hallmarks as pigment, laid on deliberately and past machine base rates, for work whose frame announces the joke. Two rules before the numbers. First, the piece still needs an armature; McDonald is not optional, because slop is the paint and the paint needs a building. Second, the labeling ethic from the hallmarks file governs: this register weaponizes the catalog inside a frame labeled as satire, and it never launders machine text as human anywhere else.

- **Domain.** Parody of machine-generated prose; satire whose subject is the slop itself.
- **Register and voice.** Committed to the bit. The craft is in the aim, not the absence of craft.
- **Manifest.** Stages 0, 1, 2, 3, then the gate inverted: stage 7 runs with this table and flags *shortfalls*. Stages 4 through 6 run lightly if at all; Orwell in particular is stood down, since his six rules are the antidote to the disease being painted.
- **Era selector.** `era: 2023-delve | 2025-emdash`. The catalog is versioned, so the slop can be period-accurate: the delve era leans lexicon and preamble, the em-dash era leans punctuation and negation-antithesis. The lexicon CSV's drift notes mark which terms belong to which vintage.
- **Budget deltas.**

| id | artifact | mode | dir | target | sd | class | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H0.* | leaked interaction artifacts | count | floor | 0 | n/a | budgeted | Unlocked, optional: a leaked "Certainly! Here's..." is a legitimate punchline. Floor of 0 means permitted, not required. |
| H1.1 | em dash | count | floor | 6 | 2 | budgeted | 2025 era. Spaced, of course. |
| H1.2 | marked lexicon, aggregate | count | floor | 8 | 2 | budgeted | 2023 era leans harder: raise to 12. |
| H1.3 | negation-antithesis | count | floor | 3 | 1 | budgeted | Stack two back to back at least once. It isn't just excess. It's commitment. |
| H1.4 | triads | count | floor | 5 | 1 | budgeted |  |
| H2.1 | throat-clearing opener | rule | floor | n/a | n/a | budgeted | The piece must open "in today's rapidly evolving landscape." |
| H2.4 | significance inflation | count | floor | 3 | 1 | budgeted | Everything "stands as a testament to" something. |
| H2.10 | uniformity | rule | floor | 6 | 1 | budgeted | Inverted: maximize sameness. The metronome is the music. |
| H3.3 | citations | rule | n/a | n/a | n/a | absolute | Still verify or cut. Fake citations are not a joke format; they are misinformation with a laugh track. Invented sources appear only as obvious fiction within the labeled frame. |

---

## Profile: fairy-tale

*Deltas from default.* The register whose craft files arrived before its numbers. Three files supply its layers: `luthi-folktale-style.md` for the surface the tale is told on, `propp-morphology.md` for the order of events beneath it, `tolkien-secondary-belief.md` for the contract the other two exist to serve. The register's job is to say which stages run, what the budget table does differently, and how the three settle their disputes with the files they displace.

- **Domain.** Traditional tales and work written in their form: folktale, wonder tale, literary fairy tale, allegory that carries its meaning on a tale's back.
- **Register and voice.** Flat surface, sharp outline, formula honored. Feeling converted to act, motive given a clause if it appears at all, texture withheld. The style is exact, never limp.
- **Reserved vocabulary.** Inherits the machine lexicon's ceilings unchanged. A folktale full of marked lexicon is machine prose in costume, and the gate reads it as such.
- **Audience.** A reader who has heard a hundred tales and knows the form's promises without being told them.
- **Manifest.** Stages 0 through 7, with two substitutions and one re-scope. Stage 2 runs Propp for the surface tale rather than Truby, because a folktale's figures cannot carry the seven steps; Truby runs on the meaning side of the doubled armature, where the reader is the one who arrives with a frame and leaves changed. Stage 6 runs Gardner with the catalog Lüthi supplies, since the dream-breaker here is the novelistic intrusion rather than the flat surface. The Lüthi file runs underneath throughout, the way the attention layer does, as a discipline held while drafting and checked while revising. The Tolkien file is live at stage 1, where the turn is what the armature proves, and again at stage 6, where a broken spell and a broken dream are one event.
- **Exemplar swaps.** The Held and Broken pairs in the three craft files.

### The doubled armature

Allegory doubles McDonald: the surface tale and the carried meaning each need an armature, and it has to be the same one. Sublimation is what makes this possible, since a motif emptied of its particular reality is free to carry a meaning while a motif loaded with sociology insists on itself. Two consequences the pipeline enforces. Stage 1 states both spines and confirms they are one before any prose pass, which is the standard halt with an extra thing to confirm. And the turn is the proof the tale was built to give, so a moral stated beside it is a second and worse ending; that is the register's form of McDonald's cut-the-stated-lesson test.

### Budget deltas (PROVISIONAL)

| id | artifact | mode | dir | target | sd | class | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1.4 | rule of three | rule | floor | n/a | n/a | budgeted | Re-moded, not inverted. The stub ruled a count floor; the counter cannot serve it, since `TRIAD` matches a syntactic list and the genre's threes are structural, three brothers across three episodes. A textbook folktale passage scores zero. Judged instead: three is the unit of structure, repetition is verbatim rather than varied, and the change rides the third pass. The Lüthi file owns the count, the Forsyth repetition family owns the mechanics. |
| H2.1 | opening formula | rule | floor | n/a | n/a | budgeted | Inverted. The doorway formula is required: the threshold at which the reader consents to secondary belief. The register's real throat-clearing is the opener that stands outside the tale talking about it. Argument in the Tolkien file. |
| H2.2 | closing formula | rule | floor | n/a | n/a | budgeted | Inverted, and new to this draft. Tolkien's frame has two edges; the stub ruled only the opener. The closing formula is the casement's far side and is required on the same grounds. |
| H2.10 | uniformity ceiling | rule | ceiling | 6 | 1 | budgeted | Loosened. Verbatim repetition of speeches and episodes is the form's machinery, and it produces matched sentence lengths on purpose. Sameness here is convention, not tell. |
| H3.2 | specificity markers | count | floor | 8 | 3 | budgeted | Re-scoped, not raised. The concrete image and the plain act count; the proper noun, the date, and the documentary detail do not, and the abstract style forbids them. The tale is vivid without being documentary. |

Everything not listed inherits default, including every Tier 0 ban and the marked-lexicon ceilings. The scrub still runs.

### Conduct

Two pushback triggers fire on their own terms here. A tale whose turn has no ingredients woven for it has not earned one, and eucatastrophe is grace rather than a slot, so the pipeline asks rather than installs. And a surface tale whose carried meaning has drifted onto a second spine is the doubled armature failing, which is trigger three wearing this register's clothes.

Three rows above are re-moded or newly ruled against the stub that preceded them, which is what happens when the craft files arrive after the sketch. The numbers stay provisional until the calibration protocol runs on a folktale corpus, and that corpus does not exist yet.

---

## Profile: llm-script

The register that flips the audience: the reader is a model, so the optimization target flips from "reads as you" to operational strength per token. This is the first profile whose gate optimizes something other than the human-written feel, and the first whose rules are evidence-backed rather than judgment-backed: the fold experiment ran on the July 2026 canon at 71 percent of source words, and the resulting compiled variant certified against the behavioral eval kit at six of six with four cells improving and zero degrading. The rules below are the rules that produced that result.

- **Domain.** Instruction for models: system prompts, tool specifications, agent role prompts, and the compiled variant of any craft file the pipeline decides to serve to a model rather than a human. Prompts, not prose.
- **Register and voice.** Dense, rule-first, decision-rights preserved. No performance, no figures, no salience spent on transitions.
- **Reserved vocabulary.** Inherits the machine lexicon's ceilings by convention; the register cannot license slop by pointing at its audience.
- **Audience.** A model reading instruction. The primed human reader is not the target, and the surface catalog's diagnostic value shifts: a machine-detectable pattern in a prompt for a machine is not a tell, it is the medium.
- **Manifest.** By audience-inversion: Forsyth stands down entirely, since figures spend tokens on effects a model does not need. Orwell's rule three becomes the dominant pass, because a token budget is a real budget. McDonald sharpens to its limit, one job per file, one rule per line where the rule permits. Gardner re-scopes to internal-contradiction detection, a genuine script failure mode. The attention layer becomes salience engineering: the first and last positions in a context window are the load-bearing slots and the load-bearing content sits in them. Goldberg is not run at compile time, since the compile source is finished prose, not a blank page; the register still refers back to its own generation-time discipline when writing a script from scratch.
- **Exemplar swaps.** The July 2026 compile of the full V3 library. Fold-samples directory, thirteen files. Each is a worked example of the fold rules on a specific canon file, and each opens with a provenance line naming its source and the fold date.

### Fold rules

The compile-experiment amendments (July 12) as canon. The register cannot deviate from these; a deviation is a candidate for a new ruling, not a discretionary call.

**Moves.**
- Orwell's rule three is the dominant pass: every word that can go, goes.
- McDonald sharpens to its limit: each file states its one job in its first line, and everything in the file serves it.
- Forsyth stands down as style: the library's own prose stops performing figures; the figures the craft files teach survive as definitions with one example each, because the examples are the data, not the ornament.
- Gardner re-scopes to internal-contradiction detection: a fold pass checks that compressed rules do not collide.
- Salience is engineered: each file's load-bearing rules sit in the first and last positions.
- H1.5 lists are genre-native and permitted; the label-restatement pair stays dead.
- H2.10 uniformity is free.
- Tier 0 still gates.
- H3.3 verify-or-cut admits no exceptions: no source claim is altered and citations survive.
- Version-history prose folds out: header changelogs, promotion histories, and entered-canon origin stories occupy salience positions and forward-reference terms defined later. Perishable-file version blocks are operational and survive verbatim.

**Invariants.**
- Every rule survives with its trigger conditions and its decision-rights language, and the one rule survives verbatim.
- All numbers survive exactly: budgets, targets, sd values, hallmark IDs.
- The file mapping is one to one with names unchanged, so cross-references resolve and any degradation localizes.
- The fold is monotone: removal and restatement only, no new claims, with structural anchors (headings, IDs, twin-and-owner routing) the only permitted additions.
- Each folded file opens with one provenance line naming its source file, the canon version, and the fold date.

### Semantic strength: measured, not judged

Strength is behavioral eval pass-rate parity against the source. The eval kit's tests with deterministic materials (2 and 4) serve as the cheap regression; the judgment tests (1, 3, 5, 6) serve as milestone checks. Ordinal no-worse per cell against baseline, no new failure modes at equal score, no offsetting, test 6 counted in full. On the July 2026 compile the improvement direction was consistent: four cells improved on stopping-family behavior canon under-teaches and memory was subsidizing. Improvements are recorded and do not license further deviation; they are evidence for canon revision, not for register drift.

### Budget deltas

*Deltas from default.* Documentation, not verdicts: the default gate profile budgets human feel, and this register does not. The rows below describe how each artifact reads in prompts written for a model.

| id | artifact | mode | dir | target | sd | class | note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H0.* | leaked interaction artifacts | count | ceiling | 0 | 0 | absolute | Still gates. A leaked chat frame inside a script is a bug in both directions. |
| H1.4 | triads (heuristic) | rule | ceiling | n/a | n/a | budgeted | Documented not budgeted: dense rule enumeration produces consecutive triads that are genuine lists. The false-positive class already documented on `quoth my father` and appositive-plus-serial-comma-plus-clause covers most; register-specific H1.4 lands with the register's own gate profile. |
| H1.5 | bold-led label bullets | rule | ceiling | n/a | n/a | budgeted | Structured lists are genre-native. The label-restatement pair stays dead. |
| H2.10 | uniformity ceiling | rule | n/a | n/a | n/a | informational | Stood down. Uniformity is not a tell where no human reader is addressed. |
| H3.3 | citations | rule | n/a | n/a | n/a | absolute | Holds. Verify or cut admits no register exceptions. |
| H4.3 | typography | rule | n/a | n/a | n/a | informational | Inherits default. |

The register's own gate profile is future work: budgets tuned to prompt readability rather than human-written feel, calibrated against a corpus of well-formed prompts. Not needed for the compile experiment, whose measure was behavioral parity against the source. Logged in EXPANSION-NOTES.

### Conduct

The pipeline proposes and the writer decides. In this register the writer's decision extends to whether to serve the compiled variant to a model at all: parity with source is not superiority to source, and the source's pedagogy carries value the compile intentionally removes. Compiled variants are evidence that the rules work, not deliverables that supersede canon.

---

## A note to the AI assistant using this file

Load the default profile, apply the active register's deltas, and honor its manifest in the scaffold's order. Enforce budgets at the gate against the active profile, and name that profile in the gate report, because a count means nothing without the table it was counted against. Where a budget wants breaking, propose the override with its cause and wait; where a floor cannot be met from the material you have, that is a pushback trigger, not an invitation to invent. The numbers here are provisional until the calibration protocol replaces them; treat them as defaults with a review date, which is what they are.
