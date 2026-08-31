# skills

Two agent skills, each a folder with a `SKILL.md`:

- `scrub-gate/` — invokes the gate against a register profile.
- `canon-shipping/` — the shipping discipline for canon edits, with
  `ship-check.py` beside its `SKILL.md` so the folder installs whole.

The `ship-check.py` in `canon-shipping/` is a copy of the repository-root
`ship-check.py`, which is the governing version. If the root tool changes,
refresh this copy. Both SKILL.md files were reconciled against the shipped
tools at v3: the gate exposes six register profiles, and `drift` checks all
six registers rather than the default table alone.
