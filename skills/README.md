# skills

Four agent skills, each a folder with a `SKILL.md`:

- `scrub-gate/` — invokes the gate against a register profile.
- `canon-shipping/` — the shipping discipline for canon edits, with
  `ship-check.py` beside its `SKILL.md` so the folder installs whole.
- `draft-provenance/` — reads a chain of drafts and derives the per-word
  record: who typed each word, which hand kept it, what came back from an
  earlier draft. Carries a positive tracked-changes fixture and
  `scripts/selftest.py`, which is part of release acceptance.
- `text-layers/` — reads that record and draws the piece with its drafts
  showing through: PNG sheets for review and one self-contained HTML for
  reading.

`craft-v3.4-spec.md` is the specification the last two implement, and the
document V3.4 tags against. Its section 7 is the acceptance list; `accept.py`
at the repository root runs the mechanical half.

The two locked faces, Alegreya and Recursive, ship in
`text-layers/assets/` with their OFL licences. The pairing exploration used
four other faces and a `font_pairings.py` that compares them; those stay in
the reference skill outside this repository, per the spec, so nothing here
carries a face the library does not use.

The `ship-check.py` in `canon-shipping/` is a copy of the repository-root
`ship-check.py`, which is the governing version. If the root tool changes,
refresh this copy. Both SKILL.md files were reconciled against the shipped
tools at v3: the gate exposes six register profiles, and `drift` checks all
six registers rather than the default table alone.
