# Brinkman's craft files

*Version 3.3, July 2026. See `CHANGELOG.md` for what changed.*

Thirteen short files that distill writing craft, and the machine artifacts
that betray its absence, into operational guidance for an AI
assistant, plus an eight-stage pipeline that sequences them and a
register layer that tunes the whole system to each kind of writing.
Each file turns "here is the idea" into "here is when to reach for
it, how it fails, and what to watch out for," written as instructions
an AI can act on and a person can learn from.

I use these to refine my own first drafts. I start with an undisciplined
stream-of-consciousness dump and ask the agent to apply the rules. The
agent revises and tells me which moves it used and why, every time. The
craft was never the scarce part. Turning it into something a machine can
act on, and a person can learn from, was.

Version two adds four files and an explicit pipeline. The four: a
generation stage at the front (Goldberg), the controlling-idea layer
above structure (McDonald), a second family of figures that work by
repetition (Forsyth), and a continuity pass that reads for anything
breaking immersion (Gardner). The pipeline, and a small model for
building a calibrated writing system of your own, live in
`scaffold-and-calibration.md`.

Version three adds the machine-artifact layer and parameterizes the
system by register. A tiered catalog of AI-text hallmarks and a
deterministic scrub gate at the end of the pipeline
(`hallmarks-and-the-scrub.md`); a registry of register profiles with
stage manifests and frequency budgets (`register-profiles.md`); and a
small data file of marked terms (`machinelexicon.csv`).
`scrub-gate.py` is the gate's reference implementation: gate mode
scores a draft against a register's budgets, `--calibrate` emits bare
rates for corpus work; budgets ship provisional until the calibration
protocol completes. The scaffold
gains three process disciplines: pushback, a calibration protocol
that replaces judgment numbers with measured ones, and versioning
against model drift. The cut list, experimental in version two, is
promoted to canon and unified with the hallmarks vocabulary. A
fairy-tale register ships in full, backed by three craft files
written for the form: Propp displaces Truby on the surface tale,
Truby survives on the meaning side of a doubled armature, and five
budget rows change, two of them inverting outright, because the
form requires the repetition the default register caps. An llm-script
register ships in full: it flips the audience from a human reader to a
model, and its rules were
tested by compiling this library through them and measuring the
result against the library's own behavioral evaluation.

## Repository layout

The craft files live in `pipeline/`: drop that folder into a project and
the pipeline is what an assistant reads. The gate and its tools sit at the
repository root, `scrub-gate.py` with `machinelexicon.csv` beside it and
`ship-check.py` for canon edits, so the invocation examples below run from
root. Two agent skills are in `skills/`, one folder each. The accretion
organism, an experimental layer that records which of these rules a real
editing pass keeps, has its specifications and frozen fixtures in `grid/`
and its generator in `craftgen/`; none of it runs unless you turn it on,
and it stays out of `pipeline/` so a clean drop carries only the craft.

File names below are bare because they name what the pipeline contains,
which is flat once `pipeline/` is in place.

## The files

| File | What it covers | Source |
| ---- | -------------- | ------ |
| `goldberg-first-thoughts.md` | The generation pass: raw, specific, unhedged first-draft material before the inner editor intervenes | Goldberg, *Writing Down the Bones* (with Allen, *Fast Fiction*) |
| `mcdonald-armature.md` | The controlling idea: the single point a piece is built to prove, and the test of *because* over *and* | McDonald, *Invisible Ink* |
| `truby-story-structure.md` | Seven structural steps adapted from fiction to argumentative non-fiction | Truby, *The Anatomy of Story* |
| `williams-flow-and-cohesion.md` | Five passes for clean paragraph-level prose: character-action, old-to-new, cohesion, end-stress, concision | Williams, *Style: Lessons in Clarity and Grace* |
| `forsyth-figures-of-speech.md` | Five figures for moments that need to land harder than their content alone (the surprise family) | Forsyth, *The Elements of Eloquence* |
| `forsyth-repetition-family.md` | Figures that work by deliberate repetition, for weight, rhythm, and memorability | Forsyth, *The Elements of Eloquence* |
| `orwell-editing-rules.md` | Six rules for the final editing pass | Orwell, "Politics and the English Language" |
| `gardner-continuous-dream.md` | The continuity pass: immersion, psychic distance, and a catalog of dream-breakers | Gardner, *The Art of Fiction* |
| `storytelling-and-attention.md` | The four-beat attention loop and why some writing holds a reader | Loewenstein, Zak, Heath, Green and Brock, Freytag |
| `luthi-folktale-style.md` | The folktale's style layer: one-dimensionality, depthlessness, the abstract style, and the formula machinery that carries them | Lüthi, *The European Folktale* |
| `propp-morphology.md` | The folktale's fixed grammar: thirty-one functions in a uniform order, performed by seven spheres of action | Propp, *Morphology of the Folktale* |
| `tolkien-secondary-belief.md` | Sub-creation, secondary belief, the doorway formula, and the consolation of the turn | Tolkien, "On Fairy-Stories" |
| `hallmarks-and-the-scrub.md` | The machine-artifact layer: a tiered catalog of AI-text hallmarks, the scrub gate, and the shared annotation vocabulary | WikiProject AI Cleanup; Kobak et al.; Liang et al. |

## The pipeline

The files are not a checklist. They are a pipeline, each pass doing a
job the next depends on. The default order:

0. **Generate** (Goldberg): raw material on the page, wide and unhedged.
1. **Find the point** (McDonald): the single thing the piece is built to prove.
2. **Structure** (Truby): the arc that serves the point.
3. **Flow** (Williams): prose that reads as written, not assembled.
4. **Intensify** (Forsyth, both families): the load-bearing moments landing harder.
5. **Cut** (Orwell): remove what is not earning its place.
6. **Continuity** (Gardner): a last read for anything that wakes the reader.
7. **Scrub** (Hallmarks): the machine-artifact gate, deterministic and last.

Underneath all of it, the attention layer (`storytelling-and-attention.md`)
is the engagement logic, live from the moment you have a point.

Stages zero through two interleave by temperament: dump-first writers
generate then find the point; outline-first writers reverse them. What
does not bend: cut comes late, the scrub runs last, and you do not
edit while you generate.

`scaffold-and-calibration.md` has the full account, including the
register profiles that tune budgets and stage manifests per kind of
writing, the calibration protocol that turns judgment numbers into
measured ones, and the pushback discipline.

## How to use them

Drop one or more files into the system prompt or instructions of your
AI assistant, then give it a draft and ask it to apply the rules. The
files are written as agent instructions; the assistant should return a
revision plus a short note naming the two or three moves that did the
most work, and name the register profile in play, since the scrub
gate's budgets come from it.

A full pipeline run is a conversation, not a single reply. Stage one
states the point the piece is built to prove and stops there for your
ruling; the prose passes begin once you have confirmed it. An
assistant that hands back all eight stages at once has decided the
armature on your behalf, which is the one decision the pipeline does
not get to make.

One rule governs the whole thing: the pipeline proposes, the writer
decides. An assistant's output is a proposal, and a change to passed
work ships as a candidate with the case argued, not as a fait accompli.
Version three makes the rule bilateral: the pipeline is also obligated
to say when there is nothing worth deciding yet, plainly and without
nagging. The pushback discipline in the scaffold has the details. The
craft files sharpen judgment. They do not replace it.

## Experimental: the Lamplighter Protocol

`lamplighter-protocol.md` is an experimental overlay for the case where
the constraint is not decoration but the meaning made structural, and
the piece has to enact what it says. It re-sequences the pipeline to
plant the constraint first, and treats the deliverable as the visible
progression from seed to machine pass to human pass. Live for use, and
still being tried.

## Tooling

`scrub-gate.py` runs the stage-seven gate from the command line, with
`machinelexicon.csv` beside it:

    python3 scrub-gate.py draft.md --profile default

`--evidence` also writes a per-match audit file, `--calibrate` emits
bare rates as TSV for corpus work, and `--lexicon` points at a
different term list. The gate counts and matches; it does not
interpret, and it cannot tell a marked word used from one quoted for
discussion. Every verdict is a proposal.

Two agent skills live in `skills/`: one invokes the gate against a
register profile, the other holds the shipping discipline for edits to
these files, with a companion `ship-check.py` that verifies
exact-string replacements and checks the gate's row table against the
budget table in `register-profiles.md`.

### Installing the skills

Each skill is a folder under `skills/` holding a `SKILL.md` and, where
it needs one, a companion script. The folder is the unit of
installation, which is why the shipping skill can carry `ship-check.py`
beside its instructions.

To install for an agent that reads Agent Skills, copy the skill folder
into that agent's skills directory. The name comes from the folder and
its `SKILL.md`, so the folder travels as-is; do not rename `SKILL.md`.

To use a skill in a chat interface that reads uploaded files as project
knowledge instead, upload the `SKILL.md` and rename it on upload to the
skill's name, since that interface takes the filename as the name. A
skill with a companion script wants the Agent Skills path rather than
the upload path, because an uploaded file cannot carry its script.

## Compiled variants

`compiled/` holds folded versions of the pipeline canon, compressed for a model
audience through the llm-script register. All seventeen pipeline files are folded;
the rest are complete and uncompressed in `pipeline/`. The source files are
master, the fold is lossy and one-directional, and these folds are not
eval-certified. See `compiled/README.md`.

## The accretion organism

Every budget in this library ships marked provisional, which is an honest way
of saying the numbers were reasoned to rather than measured. The accretion
organism is how they stop being guesses: it watches which of these rules your
own editing actually keeps, and records the answer.

It is off by default. A desk whose rules move under it is something to opt
into, not inherit.

The loop has four steps. Seed a desk from canon:

    python3 ship-check.py seed --desk my-desk --out grid.json

Run the pipeline on a draft as usual, then edit the result yourself. After that
human pass, the accretion conversation reads the seam between what the machine
did and what you did, and asks what each change meant. That procedure is canon,
in `grid/accretion-conversation.md`. Its output is a ratified template, a record
of your rulings rather than the agent's readings.

Feed the template to the generator:

    python3 -m craftgen.cli generate --grid grid.json --template t.json \
        --out grid.json --ledger ledger.json

The grid now knows a little more about your hand. A rule you kept strikes
hardens; a rule you overrode softens; edits answering to no named rule collect
in an undefined region, and a cluster that keeps recurring there is how a rule
you have never articulated becomes visible.

**The render is experimental and unfinished.** The grid is a file, and the file
is complete: it accretes correctly, and everything above works. What does not
exist is the thing that turns it into a picture. The visual specification is
frozen and three reference renderings exist as hand-cut artifacts, but no code
renders a grid, so what you get back from a real pass is JSON. Read it or write
your own renderer; the specification and the fixtures are in `grid/`, and the
tone ramp and fade table are published there. This is the one part of the
library that promises more than it delivers, and it is marked here rather than
discovered later.

Both steps run wherever your agent runs. The accretion conversation is a
conversation, and the generator is eight files an agent with a sandbox can
execute, so nothing here needs a local install; `craftgen/README.md` covers the
case where those files arrive loose rather than as a folder.

The specifications are in `grid/`, the generator in `craftgen/`, and both have
their own documentation. Three things are deliberately absent: nothing renders
the grid to an image yet, the population layer that would aggregate across desks
is unbuilt, and the config magnitudes governing how far a weight moves are still
provisional.

## Credits and further reading

Each file credits its source at the top. The sources are the canonical
treatments and are worth reading directly if you want depth beyond the
operational distillation. The files are adapters, not substitutes.

- Natalie Goldberg, *Writing Down the Bones* (Shambhala, 1986), with a
starting tactic from Roberta Allen, *Fast Fiction*.
- Brian McDonald, *Invisible Ink: A Practical Guide to Building Stories
That Resonate*.
- John Truby, *The Anatomy of Story* (Farrar, Straus and Giroux, 2007).
- Joseph Williams, *Style: Lessons in Clarity and Grace*. Any recent
edition.
- Mark Forsyth, *The Elements of Eloquence* (Icon Books, 2013). For
figures beyond the two families here, see also Silva Rhetoricae
(rhetoric.byu.edu).
- George Orwell, "Politics and the English Language" (1946). Free at
the Orwell Foundation (orwellfoundation.com).
- John Gardner, *The Art of Fiction: Notes on Craft for Young Writers*
(Knopf, 1984).
- The synthesis file cites George Loewenstein on the information gap,
Paul Zak on narrative and attention, Chip and Dan Heath's *Made to
Stick*, Melanie Green and Timothy Brock on narrative transportation,
and Gustav Freytag on dramatic shape.
- The hallmarks file synthesizes the field catalog of Wikipedia's
WikiProject AI Cleanup ("Signs of AI writing"); Dmitry Kobak, Rita
González-Márquez, Emőke-Ágnes Horvát, and Jan Lause, "Delving into
LLM-assisted writing in biomedical publications through excess
vocabulary" (*Science Advances*, 2025); and Weixin Liang, Mert
Yuksekgonul, Yining Mao, Eric Wu, and James Zou, "GPT detectors are
biased against non-native English writers" (*Patterns*, 2023).

## License

Licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).
Use them, adapt them, share them. Attribution appreciated; commercial
use permitted; the license has the details.

## About

I wrote these for my own use and am sharing them because they have been
useful. If they are useful to you, that is the whole point. If they are
not, the source books are excellent and might serve better.

— Donald Brinkman <donald@donaldbrinkman.com> · [@brinkmanship](https://x.com/brinkmanship)
