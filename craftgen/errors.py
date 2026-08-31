# Provenance: written by Slopsmith (build agent), 2026-07-23, at the Proprietor's
# direction, per BRIEF-slopsmith-generator.md and the round-1 and round-2 rulings.
# No human pass; verify before trusting.
"""The one failure mode the boundary has: refuse, and say why.

A malformed template is refused rather than repaired. Repair would be the
generator deciding, and the one rule says it proposes. Every refusal names the
offending change by seq where a change is at fault.
"""


class Refusal(Exception):
    """Raised when a template or grid fails a boundary check.

    The transform is all-or-nothing: a refusal means nothing was applied and no
    counter moved.
    """

    def __init__(self, message, seq=None):
        self.seq = seq
        if seq is not None:
            message = f"change seq {seq}: {message}"
        super().__init__(message)
