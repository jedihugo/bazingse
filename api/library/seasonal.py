# * =========================
# * SEASONAL STRENGTH & TRANSFORMATION RULES
# * =========================
# Season/element_states are now embedded in BRANCHES (core.py).
# This file derives seasonal lookups from that embedded data.

from .core import BRANCHES

# Build SEASONAL_STRENGTH from BRANCHES.element_states
# Format: Element -> {State -> [Branches]}
SEASONAL_STRENGTH = {"Wood": {}, "Fire": {}, "Earth": {}, "Metal": {}, "Water": {}}
for branch_id, branch in BRANCHES.items():
    for element, state in branch["element_states"].items():
        if state not in SEASONAL_STRENGTH[element]:
            SEASONAL_STRENGTH[element][state] = []
        SEASONAL_STRENGTH[element][state].append(branch_id)

SEASONAL_ADJUSTMENT = {
    # Balanced multipliers for seasonal effects (旺相休囚死)
    # Reduced impact for more subtle seasonal influence
    "prosperous": 1.382,     # 旺 Wang - Peak/thriving (strongest)
    "strengthening": 1.236,  # 相 Xiang - Growing phase
    "resting": 1.0,          # 休 Xiu - Baseline (no change)
    "trapped": 0.886,        # 囚 Qiu - Trapped/declining
    "dead": 0.786            # 死 Si - Dead/weakest
}

# Alias for backward compatibility
ELEMENT_SEASONAL_STATES = SEASONAL_STRENGTH
