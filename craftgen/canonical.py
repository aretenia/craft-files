# Provenance: written by Slopsmith (build agent), 2026-07-23, at the Proprietor's
# direction, per BRIEF-slopsmith-generator.md and the round-1 and round-2 rulings.
# No human pass; verify before trusting.
"""Canonical serialization, so output is deterministic and hashable.

Determinism is the A1 check's precondition and this module is where it is bought:
fixed separators, LF newlines, and key order that follows the structure rather
than a sort. Given the same inputs the generator emits byte-identical output,
because the transform deep-copies the input and mutates in a fixed order.

Key order is preserved, not sorted: the on-disk grid is a human-audited artifact
and reordering its keys away from the spec's natural layout costs readability and
round-trip fidelity for nothing. The one place a sort survives is the content hash,
where it buys key-order-independent identity for the ledger and never faces a
reader.
"""

import hashlib
import json


def canonical_json(obj):
    """Compact and key-order-independent. Used only for the content hash."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def pretty_json(obj):
    """Indented, key order preserved, trailing LF. The on-disk form."""
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def content_hash(obj):
    """SHA-256 over the canonical form. The ledger's idempotency key."""
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()
