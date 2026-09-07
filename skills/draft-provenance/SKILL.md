---
name: draft-provenance
description: Build a word-level provenance map across an ordered chain of drafts (docx, md, txt) that says, for every word of the final text, which draft introduced it, whether a human or a machine pass wrote it, whose hands touched it since, whether a human kept a machine's words, and whether a run of text was moved. Use this whenever the user wants to compare versions of an essay or document, attribute text to human versus machine, visualise collaboration across drafts, apply version theory or "fluid text" ideas to their own writing, or asks how much of a piece survived from an early draft. Run it before any rendering with the text-layers skill, and re-run it every time a new intermediate draft arrives, because attribution changes as the chain fills in.
---

# Draft provenance

One script, one manifest, one JSON out. The picture is drawn elsewhere
(the `text-layers` skill reads this skill's output).

## What it does

Given drafts in order, each labelled with who made the pass, it aligns
every consecutive pair with a longest-common-subsequence diff over
normalised words and carries a provenance record forward token by token.
For the last draft it emits, per word:

| field | meaning |
|---|---|
| `class` | `human`, `machine`, or `unattributed` (introduced in a pass marked `mixed`) |
| `origin`, `origin_agent` | the draft label and agent that introduced the word |
| `hands` | the agents that touched it since, in order |
| `approved` | true when a human pass kept a word a machine wrote |
| `survived` | passes the word has survived unchanged |
| `moved`, `moved_by`, `move_from_para` | it travelled inside a moved run |
| `churn` | how many passes changed something within twelve words of it |
| `mix`, `lean`, `sentence` | back and forth at the sentence level: a sentence both hands wrote parts of is mixed; `mix` is how balanced (1 = even), `lean` is the human share (drives the hue), pure sentences are 0 |
| `proximity_mix` | the older word-level heuristic, kept for comparison |

plus a `summary` (share by class, approved machine words, moves, count of
unattributed words, a per-pass audit), the list of `events` per pass,
`scars` (every cut of `--min-cut` words or more, placed at the surviving
neighbour in the final text, with whose words were cut and by whom) and
`restorations` (inserted runs that existed in an earlier draft but not
the one just before: a hand bringing text back). Tokens also carry
`heat` (passes that rewrote the sentence, plus cuts inside it),
`para_loss` (the other hand's words cut from the paragraph),
`cut_before` / `cut_after`, and `restored`.

## The rules it encodes

- **When in doubt, human.** Words born in a `mixed` pass are
  `unattributed`, not machine. Renderers set them in the human face. The
  summary counts them so the size of the guess is visible.
- **A word is carried, not re-typed, when it sits in an unchanged run of
  at least `--min-run` words (default 2).** Lone common words ("the",
  "and") that happen to reappear are treated as rewritten, so they do
  not inflate the human share.
- **A move is a deleted run that reappears verbatim elsewhere in the
  same pass, at least `--min-move` words long (default 4).** Moved words
  keep their origin; the move is recorded on them.
- **Approval is survival.** A machine word that a later human pass left
  in place is marked `approved`. That is the only intent the script can
  see; it does not know why.
- **Three kinds of pass.** `human`; `machine`; and a machine pass that
  was ruled, meaning the human ruled every change (a pipeline pass that
  hands decisions back). Write it with its evidence:
  `"ruled": {"value": true, "source": "header"}` where source is
  `event` (the pipeline recorded it), `header` (a version note says so),
  or `attestation` (the writer says so). A bare `true` is accepted and
  recorded as `header`. Words born in a ruled pass are machine words that
  carry a human hand, and the record says on what authority. The
  library's own passes will carry rulings per edit; the reconstruction
  path can only carry claims.
- **A sentence is back and forth in two ways.** Both hands wrote words
  that are still in it; or one hand rewrote the other's: the sentence's
  words come from more than one pass, and a later one was the other
  hand or a ruled pass. In a rewrite, ruled words count half for the
  human when the lean is computed, which is why "That is my grievance."
  (machine sentence in V2, reworded in the ruled V7) comes out mixed and
  leaning machine rather than pure. The smaller hand still needs
  `--min-minority` of the sentence (default 0.12), so a one-word fix does
  not colour a paragraph. Colour follows this; fonts follow the word.
- **Tracked changes are exact provenance.** When a `.docx` carries
  tracked changes, every word inside an insertion is new in that pass
  by that pass's agent, whatever the diff would have guessed; deleted
  text is dropped. Ask for the real `.docx` when a draft was edited
  with Track Changes on: a project copy arrives as flattened text and
  loses this (and can glue words together at change boundaries).

## Manifest

```json
{
  "title": "Rupture",
  "drafts": [
    {"file": "Rupture_V1.docx", "label": "V1", "agent": "human"},
    {"file": "Rupture_V2.docx", "label": "V2", "agent": "machine"},
    {"file": "Rupture_V3.docx", "label": "V3", "agent": "human"},
    {"file": "Rupture_V4.docx", "label": "V4", "agent": "machine", "ruled": true},
    {"file": "Rupture_V5.docx", "label": "V5", "agent": "mixed"}
  ]
}
```

`agent` is `human`, `machine`, or `mixed`. Order is the order of the
chain; the last entry is the text that gets attributed. Put the manifest
in the folder with the drafts. Optional per draft: `"skip_paragraphs": 1`
to drop a version note at the top of a file ("This version is V10..."),
`"at": "2026-09-01"` when the writer knows the date (never guessed from
file times), and `"evidence": "..."` for why the label is what it is.
A `.docx` that is really text (project copies) is read as text.

### Attestations: the writer's memory as a source (optional, last resort)

The chain records who made a pass, not who thought of the words. The
`ruled` flag and the rewrite rule cover most of that gap in a
generalisable way; prefer them. Attestations exist for the residue, and
only if the user wants to keep such a list:

```json
"attestations": [
  {"text": "That is my grievance.", "agent": "human", "note": "writer's recollection, 2026-09-07"}
]
```

Attested phrases are matched after the diff and override it: class and
origin become the attested agent, `origin` reads `attested`, and the
summary counts the words. Attestations are the only place the user's
memory enters the record; keep the note so the next reader knows why.

## Run

```bash
python3 scripts/selftest.py                      # proves the tracked-changes reader on the fixture
python3 scripts/provenance.py manifest.json -o provenance.json
python3 scripts/provenance.py manifest.json -o provenance.json --min-run 3 --min-move 6 --min-minority 0.25
```

The summary prints to the console; read it before rendering anything.
It carries a per-pass **audit**: words in, words out, share of the draft
changed (to four places, never rounded into a decision), moves, and
flags. Two flags are stop signs: a draft identical to the one before it
(a flattened export that lost its tracked changes, or a duplicate) and a
human pass that changed more than half the text (check the label). A
very small machine pass is noted, not stopped; three changed words is a
real pass. Report the audit to the user in a short table before showing
any picture.
If `unattributed` is large, the chain is missing passes or the passes
are labelled `mixed`; ask for the intermediate drafts before drawing
conclusions, because a later human draft that is not in the chain will
make human words look like machine words.

## Workflow

1. Collect every draft the user has, in order. Ask who made each pass.
   A draft the human edited after a machine pass is `human`; a machine
   pass over a human draft is `machine`; a machine pass in which the
   human ruled every change is `machine` with `ruled: true`; a draft
   where both worked and the file cannot say who typed what is `mixed`.
   Draft headers often say which; where they are stale, assume the
   passes alternate.
2. Write the manifest. Run the script. Read the summary aloud to the
   user in plain terms (share by class, how many machine words a human
   kept, how many moves).
3. Spot-check three or four sentences against the drafts by eye. The
   diff is word-level and blind to intent; if a spot-check disagrees with
   it, say so and adjust `--min-run` before trusting the picture.
4. Hand `provenance.json` to `text-layers` to render.
5. When a new draft arrives, add it to the manifest in its place and
   re-run. Provenance is only as good as the chain.

## Limits, stated plainly

- Word-level. Punctuation rides with its word. No sentence parsing.
- Moves are detected only when a run reappears verbatim. A paragraph
  that moved and was reworded in the same pass registers as a delete
  and an insert. Fuzzy move detection (sentence similarity) is the next
  improvement if the user's drafts reorder a lot.
- `mix` and `churn` are heuristics for "how much both hands were in
  here", not measurements of anything.
- Two drafts give a coarse picture; ten give a real one.
- Matching ignores case and diacritics, so a recapitalisation pass (a ≠ a
  to A ≠ A) is invisible by design. Footnotes are not read; a pass whose
  work was mostly footnotes will look empty, and a draft whose footnotes
  moved from body text into Word's footnote store will show a large false
  cut at the end (Rupture's V10 did).
- Flattened copies (project uploads) carry markdown emphasis residue;
  it is stripped, and headings lose their marks.

See `references/schema.md` for the full output schema.
