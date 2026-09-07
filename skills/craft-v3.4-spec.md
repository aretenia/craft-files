# Craft library V3.4: drafts made visible

**Spec for the provenance record, the layers render, and the package.**
Artlord v1.0, via the Proprietor. Revision 3, 2026-09-07, after
Slopsmith's full build return (Deployment 2 live; Deployment 1 held on
this pass). Reference implementation: the `draft-provenance` and `text-layers`
skills in this bundle, run end to end on the ten drafts of "Rupture."
House rules: it/its; no em-dashes.

**Release note for revision 2.** The `ruled` flag is no longer a bare
boolean asserted at pass level. It carries its evidence class, and in
the Rupture record the four header-sourced rulings are recorded as
such. The picture and the live ledger numbers do not change (110 of 175
sentences mixed, 30/70 by words); the record stops asserting a ruling it
cannot evidence. Acceptance no longer halts on a genuinely tiny pass and
does halt on an empty one whichever hand made it. Revision 3 adds: the
reconstruction manifest is normative as delivered (`drafts`, not
`passes`) and gains an optional date per draft; the tracked-changes
reader is proven on a positive fixture, and the proof found and fixed a
bug that had made it silently inert; the library ships the two locked
faces only. Dispositions of every finding are in section 9.

---

## 1. What this adds

The library already keeps a provenance file, "an append-only record of
how a document changed and which rule fired when." V3.4 makes that file
carry what a picture needs, adds a flag that draws the picture, and adds
a flag that packages a piece with all of its drafts. The picture is the
essay itself with four layers on the words:

| layer | shows | drawn as |
|---|---|---|
| faces | who typed each word | Alegreya for a person, Recursive (Monospace 0.5, weight 370) for a machine, x-height matched, the machine face at 0.907 of the serif's size |
| colour | sentences both hands wrote | a colour per sentence, hue 250 for the person to 40 for the machine, green at the midpoint; pure sentences stay ink |
| taken back | words a later draft restored from an earlier one | a red rule beneath |
| rewrite marks | sentences rewritten across many drafts | a red rule in the left gutter, darker for more drafts |

Two further red layers exist in the reference renderer and are off by
default: cut marks (where one hand removed the other's words) and loss
(the other hand's words removed from a paragraph). Red is scarce by
design; two red layers at most.

## 2. The provenance record

The library writes one entry per pass at the moment of the handoff.
Snapshots, not just diffs: a full text snapshot per pass is what makes
the chain auditable years later.

```json
{
  "piece": "rupture",
  "passes": [
    {
      "label": "V7",
      "agent": "machine",             // human | machine | mixed
      "ruled": {"value": true, "source": "header"},   // see below; never a bare boolean
      "at": "2026-09-01T18:22:00Z",
      "model": "claude-...",          // machine passes only
      "snapshot": "drafts/V7.md",     // the full text after this pass
      "source": "drafts/V7.docx",     // the file as delivered, if different
      "edits": [                      // per edit, when the pipeline records it
        {"rule": "em-dash", "action": "override", "from": "...", "to": "...", "ruled": true}
      ],
      "moves": [                      // when the machine relocates a block, say so
        {"words": 61, "from_para": 20, "to_para": 28}
      ],
      "notes": "V6 through the full pipeline; three structural rulings, four sentence edits"
    }
  ]
}
```

Rules the record must respect, learned from the Rupture chain:

- **The machine writes the labels.** Stale headers were the first
  corruption found; a human should never have to update one.
- **Snapshot at the handoff**, not on autosave, so a later edit cannot
  leak into an earlier version.
- **Ruled is a per-edit fact first and a pass-level summary second,
  never a bare boolean.** The pipeline records a ruling where one
  happens (the stage-1 halt on the armature; the accretion conversation
  under `--grid`); each such edit carries `ruled: true` in `edits[]`.
  The pass-level value is derived and tri-state: `ruled` (every recorded
  edit was ruled), `unruled` (edits recorded, none ruled), `unrecorded`
  (nothing was recorded, which is the case for every pass made before
  this release), and it always carries its `source`: `event` (the
  pipeline saw it), `header` (a version note said so), `attestation`
  (the writer said so afterwards), or `unrecorded`. A boolean cannot
  tell "did not rule" from "nobody wrote it down"; the record must.
  Slopsmith's finding stands: no existing pipeline event establishes
  "the writer ruled every change in this pass," so the library never
  infers it.
- **Moves are events**, written by whoever moved the block. Reconstructed
  moves are unreliable when a move is reworded in the same pass.
- **Tracked changes are exact provenance.** When the writer edits with
  Track Changes on, keep the .docx; every insertion inside it is theirs.
  The reader that extracts them is proven against a committed positive
  fixture (`scripts/fixtures/tracked-changes.docx`, one insertion, one
  deletion, one replacement) by `scripts/selftest.py`, and that self-test
  is part of acceptance. Rupture's chain has no surviving tracked changes
  anywhere, so the chain alone cannot demonstrate the reader.
- **Footnotes are text.** Read them; a pass whose work was footnotes must
  not look empty.

## 3. Derivation (what the renderer reads)

From the record, derive per word of the final text: `class` (human,
machine, unattributed), origin pass, hands that touched it, `approved`
(a machine word a later human pass kept), `moved`, `heat` (passes that
rewrote its sentence), `restored` (brought back from an earlier pass,
and from which), and per sentence: `mix` and `lean`. The reference
derivation is `draft-provenance/scripts/provenance.py`; its output
schema is `references/schema.md` in that skill. Two thresholds are
fixed for V3.4: a sentence counts as both hands' when the smaller hand
wrote at least 12 percent of it, and a sentence counts as rewritten by
the other hand when its words come from more than one pass and a later
one was the other hand or a ruled pass. Reconstruction from drafts alone
(no record) remains supported, with a manifest and the same thresholds.
In the reconstruction path a header-sourced ruling is recorded with
`source: header`, which the picture treats as the writer's own claim
(the same standing as an attestation), not as an evidenced event. That
is the relabel Slopsmith recommended, adopted: the 688 words that carry
it in the Rupture record keep their half-credit, the 110 mixed sentences
stand, and a reader of the record can see on what authority.

## 4. Flags

```
--provenance            always on; writes the record above at every handoff
--layers [list]         render the piece with the named layers; default: faces,colour,restored,heat
                        also: scars, loss, heatwash, lines (experimental)
--layers-out [dir]      where the renders go; default alongside the piece
--package               build the package below (implies --layers)
--heat-floor N          drafts a sentence must have been rewritten in before the gutter shows red (default 1)
--min-minority F        smaller hand's share for a mixed sentence (default 0.12)
```

`--layers` produces two forms: PNG sheets at the column measure for
review, and one self-contained HTML for reading.

## 5. The HTML render

- One file. Both faces embedded as base64 woff2, instanced at the locked
  axes and subset to the piece's characters (about 60 KB for the pair).
  No external requests; the only link is back to the published piece.
- Location-independent: the file holds no reference to its own path, so
  it can be served from any slug without editing. Rupture's is served at
  `essay-04-rupture/layers/`.
- Never patched. The render shows what the chain produced, full stops
  and all; a change to the text enters as a new pass and the render is
  regenerated. If the render and the published piece differ by a
  character, that is the chain's truth, not a bug.
- The library bundles the two locked faces only, Alegreya and Recursive,
  with their OFL licences. The pairing exploration's other faces stay in
  the reference skill, not in the public repository.
- Deployment, from Slopsmith's build: serve with `noindex, follow` so a
  full copy of the piece does not compete with the canonical page; leave
  it out of the sitemap; pin the file against line-ending conversion in
  the repository so the published bytes are the delivered bytes.
- Reads on a phone offline; 672 px measure; the essay is the page.
- Words are spans with a face class; sentences are spans with the colour
  as a CSS variable, a `data-heat`, and a plain-words tooltip; restored
  words are spans with a red underline.
- The gutter is drawn after layout by inline script from each sentence's
  line boxes, so it survives reflow and stays out of the text.
- Four checkboxes let a reader turn layers off; with all off the page is
  the plain essay.
- The header explains the legend in one paragraph that demonstrates
  itself; the footer carries the credit, the ledger in one sentence, and
  the link.
- Reference: `text-layers/scripts/render_html.py`; the Rupture render is
  `render/rupture-layers.html` in this bundle.

## 6. The package

The reconstruction manifest is normative as delivered: its list is
`drafts`, each with `file`, `label`, `agent`, `ruled` (value and
source), `evidence`, and an optional `at` (ISO date when the writer
knows it; absent otherwise, never guessed from file times, which
autosave makes meaningless). The library's own record (section 2)
requires `at`; the reconstruction path cannot, and says so.

```
<piece>-provenance-package/
  README.md              what this is, the audit table, the legend, the ledger, a privacy note
  manifest.json          drafts in order with agent, ruled (value and source), at (date, when known), evidence
  provenance.json        the derived per-word record
  drafts/                every version as delivered
  render/<piece>-layers.html
  render/<piece>-layers.png
  fonts/                 the two faces and their OFL licences
```

The package must re-render itself: the fonts, the record, and the
scripts' names are inside it. The README carries the caution in plain
words: the package contains every draft, including the first, and
publishing it is a decision, not a side effect of the flag.

## 7. Acceptance

- The audit table (per pass: words in, words out, share changed to four
  places, flags) is printed before any render. Two conditions halt the
  run with a question: a pass whose text is identical to the previous
  draft (zero words in and out; the question is whether the file is a
  flattened export that lost its tracked changes, or a duplicate), and a
  pass labelled human that changed more than half of the words (the
  question is whether the label is right). A genuinely small pass, such
  as Rupture's V4 with three words changed, passes with a note
  suggesting the label `mechanical`; it does not halt. Shares are never
  rounded into a decision. The identical-draft halt applies to any hand:
  Rupture's V8, a human pass at zero in and zero out, is exactly the row
  that must not pass silently.
- `scripts/selftest.py` passes: the tracked-changes reader detects the
  fixture's insertions and drops its deletion.
- The HTML has no external references beyond the published link; it
  opens from a file on a phone with no network.
- The PNG at 672 px and the HTML agree on faces, colour, and the two red
  layers for the same passage.
- No em-dashes in any prose the library writes; the piece's own text is
  exempt.

## 8. Known limits, carried forward

Sentence splitting is naive (a title with a period inside it splits);
the record should carry sentence boundaries where the pipeline has them.
Matching ignores case, so a recapitalisation pass is invisible. Two
consecutive passes by the same hand are fine, but a "mixed" pass
produces unattributed words, which render as the person's, unlabelled.

## 9. Dispositions of the build return (revision 2)

| finding | disposition |
|---|---|
| `ruled` cannot be evidenced by any pipeline event | Adopted as relabel: evidence class recorded, header-sourced rulings marked `header`, per-edit `ruled` in `edits[]`, pass-level tri-state plus `unrecorded`. Picture and ledger unchanged. Recompute (strip half-credit from 688 words, unmix some of 110 sentences) remains available as one re-run if the Proprietor prefers the numbers to the continuity; the spec would then carry the changed ledger in this note. |
| Section 7 halts on V4 (three words, share rounds to 0.0) | Fixed above: halts only on an identical draft or a human pass over half; small passes pass with a note. |
| Render and published page differ by a stop and a line break | No change; the render is never patched (section 5). Agreement, if wanted, enters as V11. |
| Render served at `layers/`, not `drafts/`; no manifest reachable | No change; render only was the recommendation. The package stays unpublished until the Proprietor decides. |
| `noindex, follow`, sitemap absence, line-ending pin | Adopted into section 5 as deployment rules. |
| Generator and verifier live outside the repository | Slopsmith's domain; the spec only asks (section 6) that a package can re-render itself, which argues for the move. |
| Spec 6 said `passes` with dates; the manifest says `drafts` with none | Artifact is normative for the reconstruction path; spec 6 corrected. `at` added as optional per draft, supplied by the writer or absent; the library's record requires it. |
| V8 (a human pass) looked empty and the old halt only covered machine passes | Fixed: the identical-draft halt applies to any hand. |
| Tracked-changes detector unverified; no positive fixture | The finding found a bug: the reader parsed the document twice and marked insertions on the tree it did not walk, so no insertion could ever have been flagged. Fixed, and proven by the committed fixture and self-test, now part of acceptance. |
| Port scope: six variable fonts in the skill, two locked | Agreed: the library ships Alegreya and Recursive only; the exploration faces stay in the reference skill. |
| Alt text on the threaded plate: measured sentence versus canonical wording | Ruled by Artlord: keep the live measured sentence; position and scarcity are what a listener needs. One word may change, "line" to "thread," at Slopsmith's convenience; not required. |
| Lossy WebP for the plates (routed to Artlord) | Ruled: lossless stays. The plates are grain on dark gradients; lossy compression is invisible on the grain and visible as banding in the dark, which is where the seam lives. Revisit only if page weight becomes a measured problem, with a side-by-side on the darkest region. |

Artlord v1.0
