# * =========================
# * LIFE ASPECTS ANALYSIS PACKAGE
# * =========================
# Unified system for analyzing life aspects from BaZi charts:
# - Health: TCM organ-element correlations
# - Wealth: Financial opportunities and risks
# - Learning: Education and skill development
#
# Each aspect uses the same three-dimensional analysis:
# 1. TEN GODS (十神) - What type of energy
# 2. PILLAR POSITION (宮位) - Whose life / which period
# 3. ELEMENT STATE (旺相休囚死) - Strength of energy

from .base import (
    # Pillar position mappings
    NODE_RELATIONSHIPS,
    PILLAR_LIFE_PERIODS,
    TEN_GOD_ASPECT_MAPPING,
    # Element cycle constants
    ELEMENT_CONTROLS,
    ELEMENT_GENERATES,
    # Utility functions
    stems_to_element_totals,
    get_node_relationship_context,
    detect_control_imbalances,
    calculate_aspect_severity,
)

from .health import (
    ELEMENT_ORGANS,
    CONFLICT_HEALTH_WEIGHTS,
    SEASONAL_HEALTH_MODIFIER,
    generate_health_analysis,
)

from .wealth import (
    WEALTH_TEN_GODS,
    WEALTH_INDICATORS,
    generate_wealth_analysis,
)

from .learning import (
    LEARNING_TEN_GODS,
    LEARNING_INDICATORS,
    generate_learning_analysis,
)

from .ten_gods_detail import (
    TEN_GOD_PILLAR_MEANINGS,
    get_ten_god_for_stem,
    generate_ten_gods_detail,
)

__all__ = [
    # Base
    "NODE_RELATIONSHIPS",
    "PILLAR_LIFE_PERIODS",
    "TEN_GOD_ASPECT_MAPPING",
    "ELEMENT_CONTROLS",
    "ELEMENT_GENERATES",
    "stems_to_element_totals",
    "get_node_relationship_context",
    "detect_control_imbalances",
    "calculate_aspect_severity",
    # Health
    "ELEMENT_ORGANS",
    "CONFLICT_HEALTH_WEIGHTS",
    "SEASONAL_HEALTH_MODIFIER",
    "generate_health_analysis",
    # Wealth
    "WEALTH_TEN_GODS",
    "WEALTH_INDICATORS",
    "generate_wealth_analysis",
    # Learning
    "LEARNING_TEN_GODS",
    "LEARNING_INDICATORS",
    "generate_learning_analysis",
    # Ten Gods Detail
    "TEN_GOD_PILLAR_MEANINGS",
    "get_ten_god_for_stem",
    "generate_ten_gods_detail",
]
