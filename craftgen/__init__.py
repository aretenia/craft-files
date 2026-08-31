# Provenance: written by Slopsmith (build agent), 2026-07-23, at the Proprietor's
# direction, per BRIEF-slopsmith-generator.md and the round-1 and round-2 rulings.
# No human pass; verify before trusting.
"""craftgen: the accretion-template-to-grid generator.

Input is one ratified accretion template. Output is a spec-conformant grid file.
The generator consumes ratified intent and never infers it: no document parsing,
no format detection, no guessing.
"""

from craftgen.errors import Refusal
from craftgen.config import Config, DEFAULT_CONFIG
from craftgen.generate import generate, bootstrap_grid
from craftgen.ledger import Ledger

__all__ = [
    "Refusal",
    "Config",
    "DEFAULT_CONFIG",
    "generate",
    "bootstrap_grid",
    "Ledger",
]
