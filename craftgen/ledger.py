# Provenance: written by Slopsmith (build agent), 2026-07-23, at the Proprietor's
# direction, per BRIEF-slopsmith-generator.md and the round-1 and round-2 rulings.
# No human pass; verify before trusting.
"""The consumed-template ledger: one owner for the run counter, no double count.

Ruled shape (round-1 decision 2, refined round-2): the generator owns run_counter,
assigns at consumption, and writes it back. The ledger keys on a content hash of the
original template so a second consumption of the same template is refused rather
than counted twice. The assigned run is recorded here for later reading; the
template file itself is never edited after ratification.
"""

import json
import os

from craftgen.canonical import content_hash


class Ledger:
    def __init__(self, path=None):
        self.path = path
        self._data = {}
        if path and os.path.exists(path):
            with open(path, "r", encoding="utf-8") as handle:
                self._data = json.load(handle)

    @staticmethod
    def key_for(template):
        return content_hash(template)

    def seen(self, key):
        return key in self._data

    def run_for(self, key):
        entry = self._data.get(key)
        return entry["run"] if entry else None

    def record(self, key, run, consumed_on):
        self._data[key] = {"run": run, "consumed_on": consumed_on}
        self._save()

    def _save(self):
        if not self.path:
            return
        with open(self.path, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(self._data, handle, ensure_ascii=False, indent=1)
            handle.write("\n")
