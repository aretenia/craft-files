# Provenance: written by Slopsmith (build agent), 2026-07-23, at the Proprietor's
# direction, per BRIEF-slopsmith-generator.md and the round-1 and round-2 rulings.
# No human pass; verify before trusting.
"""The config surface: every magnitude lives here, structure lives in code.

Ruled split (round-1 decision 3): the state machine is structural and fixed; the
numbers are configured with provisional defaults, so a recalibration is a value
edit rather than a code-path edit. grid-spec-v1.md section 9 puts all quantization
with the design team, so the numbers below are provisional and owed.

The two direction-to-state mappings are the Proprietor's ruling, not the library's
reading, as of the round-2 conversation. They still sit behind the config line so a
future change moves a number, not a path.
"""

from dataclasses import dataclass, field


def _default_state_for_direction():
    # Ruled mappings. human_strike sides with the rule the machine broke, so it is
    # confirmation (validated). human_add undoes a correct machine move, so it is
    # dispute (contested). stand is weak confirmation of a fire.
    return {
        "human_strike": "validated",
        "human_add": "contested",
        "stand": "fired",
    }


def _default_weight_on_fire():
    # Provisional, pending design-side calibration. The structure that is NOT
    # provisional: contested outranks validated outranks fired, because contested is
    # the strongest freshness signal (grid-spec section 5) and stand is weak
    # confirmation (section 4). Every value stays strictly inside the open (0.4, 1.0):
    # the update path may never walk a cell to an endpoint (0.4 or 1.0), because an
    # endpoint is a ruling rather than an accumulation (section 3, Weight). Landing on
    # 0.4 would silently reclassify a budgeted row as informational; landing on 1.0
    # would lock it absolute. The fade over run age is a render concern and is never
    # written back into weight here.
    return {
        "contested": 0.9,
        "validated": 0.7,
        "fired": 0.5,
    }


@dataclass(frozen=True)
class Config:
    state_for_direction: dict = field(default_factory=_default_state_for_direction)
    weight_on_fire: dict = field(default_factory=_default_weight_on_fire)

    # v1 does not move a cell's target or sd. Those are the design team's
    # quantization (grid-spec section 9), the numbers are pending, and the sample
    # files hold targets stable across every pass. The mechanism is kept here so a
    # non-zero step later is a config edit: a positive step tightens on a strike and
    # loosens on an add, with the sign resolved against dir (ceiling or floor).
    harden_target_step: int = 0
    soften_target_step: int = 0

    # The first seq a fresh reel uses. The reel is append-only; a non-empty reel
    # continues from its own maximum and ignores this.
    reel_seq_base: int = 1


DEFAULT_CONFIG = Config()

VALID_DIRECTIONS = frozenset({"human_add", "human_strike", "stand"})
