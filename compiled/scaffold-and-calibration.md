# The writing-craft scaffold: sequencing and calibrating the files

*Folded from `scaffold-and-calibration.md`, canon V3.3, August 2026. Compiled variant: the source file is master.*

One job: say which file runs at which stage, in what order, and how to tune the set to a writer and a register.

**The one rule, bilateral.** The pipeline proposes and the writer decides, and the pipeline is also obligated to say when there is nothing worth deciding yet.

## The three layers

Keeping them separate is what lets the craft generalize while the specifics stay yours.

1. **The base files.** The craft itself. Universal and stable, with one exception: the hallmarks file describes model generations rather than laws of prose and carries a version header. This part does not change between users.
2. **The sequence scaffold.** Which file applies at which stage, and in what order. Orchestration, not craft.
3. **The register profiles.** Your domains, registers, numbers. A registry, one default plus per-register deltas, each carrying the overlay's five parts plus a stage manifest and a budget table. Schema in `register-profiles.md`. A single overlay is a registry of one.

Your system is base, plus scaffold, plus profiles. Change the profiles and the same base library serves a different writer, or the same writer at a different desk.

## The sequence scaffold

0. **Generate.** Goldberg. Get raw material onto the page: wide, specific, unhedged. Quality is not this stage's job.

1. **Find the point.** McDonald, the armature. Decide, or discover in the raw material, the single thing the piece is built to prove. **Then stop.** State the armature as a claim and hand it back for confirmation before any prose pass begins. **The halt is unconditional:** it fires when the armature looks settled as well as when it looks contested, because confirming a settled armature costs one turn and prose-passing an unsettled one costs the piece. A run that reaches stage 3 without a stated armature and a ruling on it has skipped this stage, whatever else it did.

2. **Structure.** Truby, the seven steps. Shape the arc to serve the point.

3. **Flow.** Williams, cohesion. Make the prose read as written rather than assembled.

4. **Intensify.** Forsyth, both families. Make the load-bearing moments land harder than plain prose would.

5. **Cut.** Orwell, the six rules. Remove what is not earning its place.

6. **Continuity scan.** Gardner. A last read for anything that wakes the reader.

7. **Scrub gate.** Hallmarks, Tiers 0 and 1. Deterministic: scan for leaked interaction artifacts, count the famous tells against the active profile's budgets, normalize typography, report. It runs last because it is the only pass dumb enough to be safe there; it counts and matches rather than interprets, so it cannot undo the judgment work above it. It proposes fixes as candidates, and any accepted fix beyond a trivial substitution gets a continuity spot-check. Tiers 2 and 3 get no stage of their own: they ride stages 5 and 6 as annotation vocabulary.

Running underneath, not a single stage: **the attention layer.** The storytelling file's curiosity loops should be live from the moment you have a point through every prose pass. Consult it whenever a piece is structurally sound but inert.

**Where the order bends.** Stages zero through two interleave by temperament. A dump-first writer generates then finds the point inside it; an outline-first writer reverses them. Both are valid, and flow, intensify, cut, continuity, and scrub run the same either way.

**What does not bend.** Cut comes late. You do not edit while you generate. The gate is last, always, and never during generation. Stage 1 halts for the writer's ruling before any prose pass runs. **A full pipeline run is a conversation with at least one mandatory turn in it, not a program that runs to completion**; an agent that delivers all eight stages in a single reply has taken a decision that was the writer's to make. The gate and stage zero form a pincer: Goldberg fights the machine's defaults from the front, the gate sweeps residue at the back, neither contaminates the other.

## Editing judgment

**Interesting-but-failed.** When you cut, distinguish a real attempt at technique that missed from bland filler that never tried. A process that cuts both with equal speed drifts toward prose that is clean and lifeless. A brave miss is closer to good than the competent average, because it can be repaired where the average can only be tolerated. Flag the interesting failure as something to fix, not remove. This is the main defense against the failure mode every AI-assisted process drifts into. It also forbids the scrub's uniformity checks from sanding off the variance generation produced: the gate caps sameness, this principle protects the strangeness that remains.

**The cut list.** A vocabulary of named judgments an assistant applies to spans while leaving the prose alone, so the writer keeps authorship. Categories with a hallmark twin carry its ID; the rest are craft-side judgments.

Marking something to cut:

- **Throat-clearing.** Warm-up sentences before the real start. *(= H2.1)*
- **Hedging.** Qualifiers that drain a claim of its force. *(= H2.9)*
- **Over-explanation.** Spelling out what the reader would reach on their own. *(kin: H2.4, H2.5)*
- **Generic phrasing.** A line anyone could have written. *(= H3.1)*
- **Over-figuration.** A figure doing decoration, not work. *(craft-only; Forsyth governs)*
- **Wrong register.** A sentence in the wrong voice for its surroundings. *(kin: H3.5)*
- **Telegraphed setup.** A plant so visible it gives the payoff away. *(craft-only)*
- **Orphaned plant.** A setup that never pays off. *(craft-only)*
- **Forced callback.** A payoff with no real plant behind it. *(craft-only)*
- **Padding.** Words present only to fill space. *(= H3.4)*
- **Wrong direction.** A passage pursuing the wrong point. Structural. *(craft-only; McDonald governs)*
- **Interesting-but-failed.** A real attempt that missed. Flag to repair, not remove.

For a span worth keeping but changing: **same content, better phrasing; different content, same function; compression; expansion; reorganization.**

Annotation happens in the late reads, stages 5 and 6, in mark-don't-rewrite mode: span, category or hallmark ID, short note.

## The pushback discipline

The reason is capability honesty, not user discipline. There are deficits this pipeline cannot fix, decisions it cannot make, and material it cannot supply, and an assistant that pretends otherwise produces slop with a straight face. The hallmarks file scrubs "Certainly!" from the prose; this scrubs its process cousin, the agreeable pass on a draft that needed a harder answer. Sycophancy is one failure wearing two costumes.

**The spine.** Evaluate before agreeing; default agreement is the failure this prevents. Name a disagreement as a position, not a hedge dressed as a question. Make the case briefly; pushback that needs a long argument is often not quite right. Skip the ceremony. Leave the decision with the writer: pushback is input, being overruled is a valid outcome, and an explained overrule is a gift.

**The triggers.** Pushback is always permitted. It is *required* when:

1. **The material is missing and only the writer has it.** A Tier 3 deficit. Say plainly the piece needs material you cannot manufacture, and stop rather than inventing texture.
2. **The human pass is missing.** The machine draft comes back barely touched and the next stage is requested. The output of a generation pass is explicitly a half; say so.
3. **There is no armature, or it has not been ruled.** Prose passes requested on a piece with no point, or on one whose armature the pipeline identified but the writer never confirmed. Push back before structure, not after flow. The second case is the quieter failure: an agent that finds a serviceable armature, judges it settled, and proceeds has substituted its own ruling for the writer's, and the substitution is invisible because the prose comes back polished.
4. **The close needs a verdict the pipeline cannot supply.** Ask for the ruling instead of writing the both-sides ending.
5. **The trajectory is drifting toward the safe middle.** Across revisions the writer keeps the tidy version and cuts the brave misses. Flag the trajectory, not the individual edits.
6. **A budget override is becoming a reflex.** When overrides arrive without causes, ask for the cause.

**The anti-nag clause.** A conduct rule degrades into a tic, and "consider adding a personal anecdote!" on every run is an engagement closer wearing a discipline costume. Pushback fires when the deficit is load-bearing and silence would paper over it. Everywhere else the default is silence. Not contrarianism either: pushback because something is wrong, never to demonstrate independence.

**The writer's side.** Pushback is the pipeline working as designed, not friction to be managed; overrules get explained when explanation is cheap; a missed pushback is a calibration point, not an indictment.

## Provenance labels

Every artifact the pipeline emits or receives across the seam carries its own provenance line: written when that artifact is created, describing that artifact, never inherited unedited. The rule cuts both ways. A machine label left on human-edited work launders in reverse and undercounts the writer; a stale "rerun" or "final" is the same failure at the process layer.

## The calibration mapping

An overlay re-skins the universal examples to your world. It does not rewrite the craft; it tells an assistant what register and domain to illustrate it in. Five parts:

- **Domain.** The world the writing lives in: subject, recurring scenarios, nouns.
- **Register and voice.** Formality, tone, voice signatures to keep.
- **Reserved vocabulary.** Words to prefer and words to avoid. The avoid-list matters as much as the prefer-list.
- **Audience.** Who the writing is for, in a line or two.
- **Exemplar swaps.** Two or three worked examples: a generic example from a base file and its calibrated version. These teach the re-skinning better than any instruction.

**How to use it.** Drop the base files and your calibration into the assistant's context together, with one instruction: apply the techniques in the craft files, but illustrate them using the domain, register, and vocabulary in the calibration rather than the generic examples.

A register profile is an overlay plus three parts: a stage manifest, a budget table keyed to hallmark IDs, and delta inheritance from a default profile.

### A worked example

For a small software company's engineering blog:

- **Domain.** A business software product. Scenarios: shipping releases, postmortems, feature tradeoffs, lessons learned. Nouns: the product, the release, the incident, the on-call rotation, the customer.
- **Register and voice.** Plain and candid. Technical but human. Willing to admit fault. No marketing gloss.
- **Reserved vocabulary.** Prefer plain verbs: use, build, ship, break, fix. Avoid "leverage," "synergy," "robust," "seamless," "delight." Never call an outage a "learning opportunity."
- **Audience.** Working engineers and the technically literate, not executives.
- **Exemplar swaps.** "She was a brilliant manager, right up until anyone disagreed with her" becomes "The architecture was elegant, right up until real traffic hit it." "The resume opens the door. The interview decides whether you walk through it" becomes "The demo gets you the pilot. The first on-call week decides whether you keep the account."

Note that its avoid-list was already banning a slice of the machine lexicon; the overlay format was fighting this war before the hallmarks file named the enemy.

## The calibration protocol

Budget numbers ship provisional, set by judgment. This protocol replaces judgment with measurement. Run it when standing up a profile, and again whenever the hallmarks file's version header expires.

Assemble three corpora. **The writer's own samples:** pieces written by hand, pre-pipeline, in the register being calibrated. These give personal base rates and are the true target, because "reads as human" cashes out as "reads as you." **Quality human prose in the public domain:** general human base rates, and the legally clean pool for a public repository is pre-1930 publication and similar. Mind the era gap; a 1920s essayist's dash rate is a reference point, not a law. **Raw machine output:** the same prompts, no pipeline, current models.

Measure the countable hallmark IDs per thousand words across all three. Budgets land at the writer's rates, sanity-checked against the human pool; the deltas between corpora are the evidence for every number, and the machine column tells you which artifacts need a budget at all. Floors calibrate the same way and to the same source: the writer's own English, never an assumption that one dialect's base rates are universal.

Two byproducts. Spans failing the new budgets in the writer's own drafts are harvested as calibrated examples into the profile's exemplar swaps. And the measured rates date-stamp themselves: record the model versions in the machine corpus, and the version header writes itself.

## Versioning against drift

The craft files are durable; Orwell's rules run fine at eighty. The hallmarks material is perishable, because it describes habits of specific model generations, and vendors change those habits, sometimes in response to the very notoriety the catalog records.

Perishable files open with a version block stating when they were calibrated, which model families they describe, and a review-by date. Three carry it: the hallmarks file, the register profiles, and `machinelexicon.csv`. The craft files are exempt. When a block expires, re-run the calibration protocol, review the entries with drift notes first, and re-date. An expired block does not mean the file is wrong; it means the file no longer knows whether it is right.

## The accretion organism

One organism, five organs. The **sensor** is the accretion conversation: the agent and the writer reading the human pass together and settling what each change meant. The signal is the signed diff of that pass and never the bare occurrence of a mark, but a diff alone cannot say whether a struck dash was refusing the machine's habit, restoring a quotation, or fixing a typo, and direction is a claim about intent. So the pipeline proposes a reading and the writer ratifies it: an inferred direction is a guess wearing the clothes of a record. The writer may mark the pass up however they like; the conversation reads whatever is there, and its ratified output is the only thing downstream reads.

The **frame** is the one-shot fired view of a single run. The **reel** is the provenance file, append-only, one tuple per update with the author mandatory. The **surface** is the grid: the desk's live parameter state, formal and informal cells plus an undefined region for clusters that recur before anyone names them. The **population layer** is aggregation across desks, governed by a two-target promotion rule: durable recurrences promote to craft canon, version-bound ones to the hallmarks catalog, and the classifier is survival across a model-version change, because a habit that dies with a model generation was a hallmark all along.

Build order follows anatomy: sensor, frame, reel, surface, population. Version one scopes the surface to the parameter layer, one grid per project-desk, and ships with this release: specifications and frozen fixtures in `grid/`, the generator in `craftgen/`, a desk seeded from canon's own budget table by `ship-check.py seed`. The population layer remains unbuilt. Settings live in `pipeline-flags.md`, and `--grid` is off by default, because a desk whose rules move under it is something a writer opts into.

## Building your own system

Pick the base files you want. Use the default sequence or adjust it. Write a profile for your world using the schema in `register-profiles.md`, or just the five-part overlay if one register is all you need.

**Conventions that keep this forward-compatible.** Base files keep neutral examples and stay free of any one domain. Calibration lives in the profile layer, never baked into a base file, and budget numbers never live in base files either: the hallmarks file defines what to count, the profiles say how much. Perishable files carry version blocks; craft files do not. The sequence is described, not hard-coded.

## One guardrail

Calibration changes examples, registers, and numbers. It does not change the rules that govern public writing. Anything published still follows the same standards the base files do: credit sources, do not reproduce copyrighted text, verify citations or cut them, and do not let a profile reintroduce something the base files were careful to leave out.

Two clarifications. The satire profile inverts budgets, not standards: it may demand slop, but its citations are still real or obviously fictional within a frame labeled as satire, and it never launders machine text as human elsewhere. And no profile encodes one dialect's base rates as everyone's: floors and ceilings calibrate to the writer's own English, which is what keeps the scrub a style tool rather than an accusation engine. The profile localizes the craft; it does not license exceptions to it.
