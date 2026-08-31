# The writing-craft scaffold: sequencing and calibrating the files

*These craft files are not a checklist. They are a pipeline, and they work best applied in an order, each one doing a job the next one depends on. This document explains that order (the scaffold), how to tune the files to your own world and registers (calibration, now generalized into profiles), and how the pieces fit into a small model you can use to assemble a custom writing system of your own.*

*Version three adds a final mechanical stage (the scrub gate), promotes the cut list from experiment to canon and unifies it with the hallmarks vocabulary, generalizes the single calibration overlay into a registry of register profiles, and adds three process disciplines: pushback, the calibration protocol, and versioning against model drift. This is still groundwork in one deliberate way: the automation that would compile it into a turnkey system remains left for later.*

---

## The three layers

A working writing system has three separable parts. Keeping them separate is what lets the craft generalize while the specifics stay yours.

1. **The base files.** The craft itself: the figures, the passes, the structures, and now the machine-artifact catalog. Universal and stable, with one flagged exception: the hallmarks file describes model generations rather than laws of prose, and carries a version header for that reason. These are the files in this library, written with neutral examples so anyone can use them. This is the part that does not change between users.

2. **The sequence scaffold.** Which file applies at which stage, and in what order. This is orchestration, not craft. Most of it is the same for everyone (the pipeline below), but you can add, drop, or reorder stages as you add your own files.

3. **The register profiles.** Your domains, your registers, your numbers. Version two defined this layer as a single calibration overlay: a thin file that re-skins the universal examples to your world and voice. Version three generalizes it: a registry of profiles, one default plus per-register deltas, each carrying the original overlay's five parts plus a stage manifest and a budget table for the scrub. The registry and its schema live in `register-profiles.md`. A single overlay is a registry of one, and remains valid as written.

Your custom system is the base files, plus your scaffold, plus your profiles. Change the profiles and the same base library serves a different writer, or the same writer at a different desk. That is the whole point of keeping the layers apart.

---

## The sequence scaffold

The default order. Each stage names the file or files that do its work. The order is a logic, not a lockstep, and the note after it explains where it bends.

0. **Generate.** Goldberg, first thoughts. Get raw material onto the page: wide, specific, unhedged. Quality is not this stage's job.

1. **Find the point.** McDonald, the armature. Decide, or discover in the raw material, the single thing the piece is built to prove. **Then stop.** State the armature as a claim and hand it back for confirmation before any prose pass begins. The halt is unconditional: it fires when the armature looks settled as well as when it looks contested, because confirming a settled armature costs one turn and prose-passing an unsettled one costs the piece. A run that reaches stage 3 without a stated armature and a ruling on it has skipped this stage, whatever else it did.

2. **Structure.** Truby, the seven steps. Shape the arc, the path the reader travels, to serve the point.

3. **Flow.** Williams, cohesion. Make the prose read as written rather than assembled.

4. **Intensify.** Forsyth, the surprise family and the repetition family. Make the load-bearing moments land harder than plain prose would.

5. **Cut.** Orwell, the six rules. The final edit: remove what is not earning its place.

6. **Continuity scan.** Gardner, the continuous dream. A last read for anything that wakes the reader: a register slip, a tonal lurch, a factual snag.

7. **Scrub gate.** Hallmarks, Tiers 0 and 1. A deterministic final pass: scan for leaked interaction artifacts, count the famous tells against the active profile's budgets, normalize typography, and report. It runs last because it is the only pass dumb enough to be safe there; it counts and matches rather than interprets, so it cannot undo the judgment work above it. It proposes fixes as candidates like every other stage, and any accepted fix beyond a trivial substitution gets a quick continuity spot-check. The hallmarks file's Tiers 2 and 3 do not get a stage of their own: they ride stages 5 and 6 as annotation vocabulary, described below.

Running underneath, not a single stage: **the attention layer.** The storytelling-and-attention file is the engagement logic, the curiosity loops, that should be live from the moment you have a point through every prose pass. Consult it whenever a piece is structurally sound but inert.

**Where the order bends.** Stages zero through two interleave by temperament. A dump-first writer generates raw material and then finds the point and structure inside it, which is the order above. An outline-first writer reverses them: settle the point and the arc, then generate prose to that shape. Both are valid, and the rest of the pipeline (flow, intensify, cut, continuity, scrub) runs the same either way. What does not bend: cut comes late, you do not edit while you generate, the gate is last, always, and never during generation, and stage 1 halts for the writer's ruling before any prose pass runs. A full pipeline run is a conversation with at least one mandatory turn in it, not a program that runs to completion; an agent that delivers all eight stages in a single reply has taken a decision that was the writer's to make. The gate and stage zero form a pincer on the same enemy: Goldberg fights the machine's defaults from the front with positive instruction toward the raw and the specific, the gate sweeps the residue at the back, and neither contaminates the other.

---

## Editing judgment: what to cut, what to keep

The cut and review stages need judgment, not just rules. Two things live here. Both are now settled.

**Interesting-but-failed (principle).** When you cut, distinguish a real attempt at technique that missed from bland filler that never tried. They are not the same, and a process that cuts both with equal speed drifts toward prose that is clean and lifeless, the safe middle that offends no one and moves no one. A brave miss is closer to good than the competent average is, because it can be repaired where the average can only be tolerated. So flag the interesting failure as something to fix, not something to remove. This is the main defense against the failure mode every AI-assisted writing process drifts into: converging on the safe and the average, because that is the easiest thing to produce and the hardest to object to. It has acquired a second duty since it was written: it is what forbids the scrub's uniformity checks from sanding off the variance that generation produced. The gate caps sameness; this principle protects the strangeness that remains.

**The cut list (promoted).** At the last revision this vocabulary was experimental, to be promoted, extended, or dropped at this one. The decision: promoted to canon, and unified with the hallmarks catalog. The cut list and the hallmark tiers turned out to be the same instrument built from opposite ends, a vocabulary of named judgments an assistant applies to spans of a draft while leaving the prose alone, so the writer keeps authorship and decides what to act on. Categories that have a hallmark twin now carry its ID; the rest remain craft-side judgments with no machine-artifact meaning, which is fine, because the vocabulary was never only about machines.

Categories that mark something to cut:

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
- **Wrong direction.** A passage pursuing the wrong point. Structural, not local. *(craft-only; McDonald governs)*
- **Interesting-but-failed.** A real attempt that missed. Flag it to repair, not to remove. *(the counter-tell guard: see above)*

Categories for a span worth keeping but changing are unchanged: **same content, better phrasing; different content, same function; compression; expansion; reorganization.**

The plant-and-callback categories (telegraphed, orphaned, forced) are the failure modes the salience principle describes; see the storytelling-and-attention file. Annotation with this vocabulary happens in the late reads, stages 5 and 6, in mark-don't-rewrite mode: span, category or hallmark ID, short note. Tier 3 marks carry an extra duty, described next.

---

## The pushback discipline

The pipeline proposes and the writer decides. Version three makes the rule bilateral: the pipeline is also obligated to say when there is nothing worth deciding yet.

The reason is capability honesty, not user discipline. There are deficits this pipeline cannot fix, decisions it cannot make, and material it cannot supply, and an assistant that pretends otherwise produces slop with a straight face. The hallmarks file scrubs "Certainly!" from the prose; this section scrubs its process cousin, the agreeable pass on a draft that needed a harder answer. Sycophancy is one failure wearing two costumes.

**The spine.** Evaluate before agreeing; default agreement is the failure this section exists to prevent. Name a disagreement as a position, not a hedge dressed as a question. Make the case briefly; pushback that needs a long argument is often pushback that is not quite right. Skip the ceremony; no pre-apology, no performance of reluctance. And leave the decision with the writer: pushback is input, being overruled is a valid outcome, and an explained overrule is a gift, because it calibrates the next one.

**The triggers.** Pushback is always permitted. It is *required* when:

1. **The material is missing and only the writer has it.** A Tier 3 deficit: no lived detail, no proper nouns, no stakes anyone could verify. Say plainly that the piece needs material you cannot manufacture, and stop there rather than inventing texture.
2. **The human pass is missing.** The machine draft comes back barely touched and the next stage is requested. The output of a generation pass is explicitly a half; say so.
3. **There is no armature, or it has not been ruled.** Prose passes are requested on a piece with no point, or on a piece whose armature the pipeline identified but the writer has not confirmed. Polishing pointlessness wastes both parties; push back before structure, not after flow. The second case is the quieter failure: an agent that finds a serviceable armature, judges it settled, and proceeds has substituted its own ruling for the writer's, and the substitution is invisible in the output because the prose comes back polished.
4. **The close needs a verdict the pipeline cannot supply.** Ask for the ruling instead of writing the both-sides ending.
5. **The trajectory is drifting toward the safe middle.** Across revisions the writer keeps the tidy version and cuts the brave misses. Flag the trajectory, not the individual edits.
6. **A budget override is becoming a reflex.** The meta-rule says deliberate and for cause; when overrides arrive without causes, ask for the cause.

**The anti-nag clause.** A conduct rule degrades into a tic, and a closing line of "consider adding a personal anecdote!" on every run is just an engagement closer wearing a discipline costume. Pushback fires when the deficit is load-bearing and silence would paper over it. Everywhere else, the default is silence. Not contrarianism, either: pushback because something is actually wrong, never to demonstrate independence.

**The writer's side.** The discipline holds only if both parties hold it. Pushback is the pipeline working as designed, not friction to be managed; overrules get explained when explanation is cheap; and a missed pushback is a calibration point, not an indictment.

---

## Provenance labels

Every artifact the pipeline emits or receives across the seam carries its own provenance line: written when that artifact is created, describing that artifact, never inherited unedited from the version before. The rule cuts both ways. A machine label left on human-edited work launders in reverse and undercounts the writer; a stale "rerun" or "final" is the same failure at the process layer. This rule entered canon by the promotion mechanic's own test: ruled by the writer during the first full pipeline run, and recurring at the evaluation layer within the week.

---

## The calibration mapping

A calibration overlay is a short file that re-skins the universal examples to your world. It does not rewrite the craft; it tells an assistant what register and domain to illustrate the craft in. A complete overlay has five parts:

- **Domain.** The world the writing lives in: the subject, the recurring scenarios, the nouns, so examples can be drawn from your work instead of from generic ones.
- **Register and voice.** How formal or casual, the tone, any voice signatures or habits to keep.
- **Reserved vocabulary.** Words and terms to prefer, and words to avoid. The avoid-list matters as much as the prefer-list.
- **Audience.** Who the writing is for, in a line or two.
- **Exemplar swaps.** Two or three worked examples: take a generic example from a base file and show its calibrated version. These teach the assistant the kind of re-skinning you want better than any instruction.

**How to use it.** Drop the base files and your calibration into the assistant's context together, with one instruction: apply the techniques in the craft files, but when you illustrate them, use the domain, register, and vocabulary in the calibration rather than the generic examples. No overlay, and the universal examples stand. Overlay present, and the assistant calibrates to you.

**Profiles extend this format.** A register profile is an overlay plus three parts: a manifest of which stages run, a budget table for the scrub keyed to hallmark IDs, and delta inheritance from a default profile. The schema and the working registry live in `register-profiles.md`.

---

## A worked example calibration

A calibration overlay for a small software company's engineering blog, to show the format filled in:

- **Domain.** A business software product. Recurring scenarios: shipping releases, writing postmortems on incidents, explaining the tradeoffs behind a feature, sharing what the team learned. Nouns: the product, the release, the incident, the on-call rotation, the customer.
- **Register and voice.** Plain and candid. Technical but human. Willing to admit fault. No marketing gloss.
- **Reserved vocabulary.** Prefer plain verbs: use, build, ship, break, fix. Avoid "leverage," "synergy," "robust," "seamless," "delight." Never call an outage a "learning opportunity."
- **Audience.** Working engineers and the technically literate, not executives.
- **Exemplar swaps.**
  - The surprise-family example "She was a brilliant manager, right up until anyone disagreed with her" becomes "The architecture was elegant, right up until real traffic hit it."
  - The surprise-family example "The resume opens the door. The interview decides whether you walk through it" becomes "The demo gets you the pilot. The first on-call week decides whether you keep the account."

That overlay plus the base files would yield craft examples drawn from the world of a software blog, in its voice, without anyone touching the underlying craft. Note, with the benefit of version three's hindsight, that its avoid-list was already banning a slice of the machine lexicon; the overlay format was fighting this war before the hallmarks file named the enemy.

---

## The calibration protocol

The budget numbers in the profiles ship provisional, set by judgment. This protocol replaces judgment with measurement. Run it when standing up a profile, and again whenever the hallmarks file's version header expires.

Assemble three corpora. **The writer's own samples:** pieces written by hand, pre-pipeline, in the register being calibrated. These give personal base rates, and they are the true target, because "reads as human" cashes out as "reads as you." **Quality human prose in the public domain:** the general human base rates, and the legally clean pool for a public repository is pre-1930 publication and similar. Mind the era gap; a 1920s essayist's dash rate is a reference point, not a law. **Raw machine output:** the same prompts, no pipeline, current models. These give the machine base rates the budgets exist to escape.

Measure the countable hallmark IDs per thousand words across all three. Budgets land at the writer's rates, sanity-checked against the human pool; the deltas between corpora are the evidence for every number, and the machine column tells you which artifacts actually need a budget at all. Floors calibrate the same way, and to the same source: the writer's own English, never an assumption that one dialect's base rates are universal.

Two byproducts, both valuable. Spans that fail the new budgets in the writer's own drafts are harvested as calibrated examples into the profile's exemplar swaps, where they sharpen the instructions without touching the neutral base files. And the measured rates date-stamp themselves: record the model versions in the machine corpus, and the profile's version header writes itself. The whole protocol is scriptable, and is the natural first piece of automation this library grows.

---

## Versioning against drift

The craft files are durable; Orwell's rules run fine at eighty. The hallmarks material is perishable, because it describes the habits of specific model generations, and vendors change those habits, sometimes deliberately and in response to the very notoriety the catalog records. A parameters file full of calibrated numbers rots silently unless it declares its own age.

The convention, borrowed from the flag the cut list carried while it was experimental: perishable files open with a version block stating when they were calibrated, which model families they describe, and a review-by date. Three files carry it: the hallmarks file, the register profiles, and `machinelexicon.csv`. The craft files are exempt; they earn their stability. When a version block expires, re-run the calibration protocol, review the catalog entries with drift notes first, and re-date. An expired block does not mean the file is wrong; it means the file no longer knows whether it is right.

---

## The accretion organism

One organism, five organs, named here so the parts stop being mistaken for siblings. The **sensor** is the accretion conversation: the agent and the writer reading the human pass together and settling what each change meant. The accretion signal is still the signed diff of that pass and never the bare occurrence of a mark, but a diff alone cannot say whether a struck dash was refusing the machine's habit, restoring a quotation, or fixing a typo, and direction is a claim about intent. So the pipeline proposes a reading of each change and the writer ratifies it, which is the one rule arriving where it matters most: an inferred direction is a guess wearing the clothes of a record. The writer may mark the pass up however they like, tracked changes or comments or nothing at all; the conversation reads whatever is there, and its ratified output is the only thing downstream reads. The **frame** is the one-shot fired view of a single run. The **reel** is the provenance file, append-only, one tuple per update with the author mandatory. The **surface** is the grid: the desk's live parameter state, formal and informal cells plus an undefined region for clusters that recur before anyone names them. The **population layer** is aggregation across desks, governed by a two-target promotion rule: durable recurrences promote to craft canon, version-bound ones to the hallmarks catalog, and the classifier is survival across a model-version change, because a habit that dies with a model generation was a hallmark all along.

Build order follows anatomy: sensor, frame, reel, surface, population. Version one scopes the surface to the parameter layer, one grid per project-desk, and ships with this release: the specifications and frozen fixtures are in `grid/`, the generator in `craftgen/`, and a desk is seeded from canon's own budget table by `ship-check.py seed`. The population layer remains unbuilt. The settings that drive the sensor live in `pipeline-flags.md`, and `--grid` is off by default, because a desk whose rules move under it is something a writer opts into.

---

## Building your own system

Pick the base files you want. Use the default sequence above, or adjust it as you add files. Write a profile for your world using the schema in `register-profiles.md`, or just the five-part overlay if one register is all you need. That is the system: base, plus scaffold, plus profiles.

**Conventions that keep this forward-compatible.** Base files keep neutral examples and stay free of any one domain. Calibration lives in the profile layer, never baked into a base file, and budget numbers never live in base files either: the hallmarks file defines what to count, the profiles say how much. Perishable files carry version blocks; craft files do not. The sequence is described, not hard-coded into the files. Following these now means a future build step could compile base plus profile into fixed, pre-calibrated files without any of the files needing to change.

**What is deliberately not here yet.** There is no compiler and no plug-in interface. The scrub gate is specified as instructions an assistant can follow, not shipped as code; a small script that runs the deterministic checks is the obvious first automation, and the calibration protocol is the second. The conventions above are what make both cheap to add. Building them now would still be building ahead of need, but the distance to need has shortened, which is what groundwork is for.

---

## One guardrail

Calibration changes examples, registers, and numbers. It does not change the rules that govern public writing. A domain-flavored example is fine, but anything published still follows the same standards the base files do: credit sources, do not reproduce copyrighted text, verify citations or cut them, and do not let a profile reintroduce something the base files were careful to leave out. Two clarifications version three makes explicit. The satire profile inverts budgets, not standards: it may demand slop, but its citations are still real or obviously fictional within a frame labeled as satire, and it never launders machine text as human elsewhere. And no profile encodes one dialect's base rates as everyone's: floors and ceilings calibrate to the writer's own English, which is what keeps the scrub a style tool rather than an accusation engine. The profile localizes the craft; it does not license exceptions to it.
