# * =========================
# * BAZI LIBRARY - MODULAR PACKAGE
# * =========================
# THE CORE PRINCIPLE: Everything in BaZi derives from the 10 Stems and 12 Branches.
# core.py contains ONLY STEMS and BRANCHES - the single source of truth.
# derived.py contains all computed data and utility functions.
# All other modules derive from these core definitions.
#
# Usage: from library import Gan, Zhi, HEAVENLY_STEMS, etc.

# =========================
# PRIMARY: The 10 Stems and 12 Branches (from core.py)
# =========================
from .core import STEMS, BRANCHES

# =========================
# DERIVED: All computed data and functions (from derived.py)
# =========================
from .derived import (
    # Elements
    ELEMENTS,
    ELEMENT_CYCLES,
    ELEMENT_CHINESE,
    # Day Officers
    DAY_OFFICERS,
    DAY_OFFICER_ORDER,
    # Ordered lists
    STEM_ORDER,
    STEM_CHINESE,
    BRANCH_ORDER,
    BRANCH_CHINESE,
    # Lookup tables
    STEM_CHINESE_TO_PINYIN,
    BRANCH_CHINESE_TO_PINYIN,
    ELEMENT_POLARITY_TO_STEM,
    STORAGE_BRANCHES,
    BRANCH_TO_MONTH,
    MONTH_TO_BRANCH,
    # Utility functions
    get_stem,
    get_branch,
    get_primary_qi,           # Primary Qi (本氣) - main energy at index 0
    get_hidden_stems,         # Hidden Stems (藏干) - index 1+ only
    get_all_branch_qi,        # All qi values (Primary + Hidden combined)
    get_stem_by_element_polarity,
    get_day_officer,
    get_ten_god,
    # Backward compatibility aliases
    HEAVENLY_STEMS,
    EARTHLY_BRANCHES,
    WUXING,
    Gan,
    Zhi,
    GAN_MAP,
    ZHI_MAP,
)

# =========================
# DERIVED: Additional lookup maps (consolidated from stems.py, branches.py, elements.py)
# =========================
from .derived import (
    # From stems.py
    STEM_COMBINATIONS_MAP,
    STEM_CONFLICTS_MAP,
    # From branches.py
    BRANCH_TO_SEASON,
    SIX_HARMONIES_MAP,
    CLASHES_MAP,
    HARMS_MAP,
    SELF_PUNISHMENT_BRANCHES,
    get_branch_by_month,
    # From elements.py
    ELEMENT_POLARITY_STEMS,
    ELEMENT_COLORS,
    ELEMENT_CHARACTERS,
)

# Distance calculations
from .distance import (
    NODE_COORDINATES,
    get_distance_key,
    get_distance_key_3nodes,
)

# Scoring system
from .scoring import (
    DISTANCE_MULTIPLIERS,
    BASE_SCORES,
    generate_scoring,
    generate_single_scoring,
    generate_asymmetric_scoring,
)

# Ten Gods (computed from STEMS in derived.py)
from .derived import TEN_GODS, TEN_GOD_NOTES

# Seasonal configurations
from .seasonal import (
    SEASONAL_STRENGTH,
    SEASONAL_ADJUSTMENT,
    ELEMENT_SEASONAL_STATES,
)

# Wealth Storage
from .wealth_storage import (
    EARTH_STORAGE_BRANCHES,
    LARGE_WEALTH_STORAGE,
    SMALL_WEALTH_STORAGE,
    DM_WEALTH_ELEMENT,
    WEALTH_ELEMENT_STEMS,
)

# Wu Xing Combat Engine and Qi Interactions
from .unity import (
    WUXING_COMBAT,
    get_distance_multiplier,
    get_qi_type,               # Replaces get_hidden_stem_priority
    get_hidden_stem_priority,  # Backward compatibility alias
    calculate_hidden_penalty,
    format_interaction_math,
    apply_wuxing_interaction,
    calculate_wuxing_control,
    calculate_wuxing_generation,
    HIDDEN_QI_INTERACTIONS,
)

# Positive Combinations
from .combinations import (
    THREE_MEETINGS,
    THREE_COMBINATIONS,
    HALF_MEETINGS,
    SIX_HARMONIES,
    ARCHED_COMBINATIONS,
    STEM_COMBINATIONS,
    TRANSFORMATION_STRENGTH,
    STRENGTH_ORDER,
)

# Negative Conflicts
from .conflicts import (
    PUNISHMENTS,
    PUNISHMENT_SEVERITY,
    HARMS,
    CLASHES,
    DESTRUCTION,
    STEM_CONFLICTS,
    WUXING_ENERGY_FLOW,
)

# Dong Gong Date Selection
from .dong_gong import (
    DONG_GONG_RATINGS,
    DONG_GONG_DAY_OFFICERS,
    DONG_GONG_OFFICER_ORDER,
    DONG_GONG_BRANCH_ORDER,
    DONG_GONG_MONTHS,
    DONG_GONG_BRANCH_TO_MONTH,
    DONG_GONG,
    get_dong_gong_officer,
    get_dong_gong_rating,
    get_dong_gong_day_info,
    check_consult_promotion,
)

# Unit Story Tracker
from .unit_tracker import (
    UnitEvent,
    UnitStory,
    UnitTracker,
)

# Qi Phase (十二長生 / Twelve Life Stages)
from .qi_phase import (
    QI_PHASES,
    QI_PHASE_BY_ID,
    QI_PHASE_TABLE,
    QI_PHASE_STRENGTH_COLORS,
    get_qi_phase,
    get_qi_phase_id,
    get_qi_phase_for_pillar,
)

# Dynamic Scoring System (動態計分系統)
from .dynamic_scoring import (
    COMBINATION_MULTIPLIERS,
    TRANSFORMATION_BONUS,
    get_primary_qi_info,            # Primary Qi (本氣) info retrieval
    get_primary_hidden_stem_info,   # Backward compatibility alias
    get_current_qi_for_stem,
    calculate_dynamic_combination_score,
    calculate_dynamic_conflict_score,
    calculate_symmetric_conflict_score,
    format_combination_narrative,
    format_conflict_narrative,
)

# Life Aspects Analysis (Health, Wealth, Learning)
from .life_aspects import (
    # Base utilities
    NODE_RELATIONSHIPS,
    PILLAR_LIFE_PERIODS,
    TEN_GOD_ASPECT_MAPPING,
    ELEMENT_CONTROLS,
    ELEMENT_GENERATES,
    stems_to_element_totals,
    get_node_relationship_context,
    detect_control_imbalances,
    calculate_aspect_severity,
    # Health Analysis (TCM organ-element correlations)
    ELEMENT_ORGANS,
    CONFLICT_HEALTH_WEIGHTS,
    SEASONAL_HEALTH_MODIFIER,
    generate_health_analysis,
    # Wealth Analysis
    WEALTH_TEN_GODS,
    WEALTH_INDICATORS,
    generate_wealth_analysis,
    # Learning Analysis
    LEARNING_TEN_GODS,
    LEARNING_INDICATORS,
    generate_learning_analysis,
    # Ten Gods Detail Analysis
    TEN_GOD_PILLAR_MEANINGS,
    get_ten_god_for_stem,
    generate_ten_gods_detail,
)

# Narrative Interpretation System
from .narrative import (
    generate_narrative,
    NARRATIVE_TEMPLATES,
    calculate_priority_score,
    prioritize_narratives,
    apply_element_modifiers,
    apply_shen_sha_modifiers,
    get_element_balance_context,
    generate_remedies,
    REMEDY_TEMPLATES,
    ELEMENT_REMEDIES,
    build_narrative_text,
    get_localized_template,
    SUPPORTED_LOCALES,
)

# Export all symbols for "from library import *"
__all__ = [
    # PRIMARY: Core data
    "STEMS",
    "BRANCHES",
    # Elements
    "ELEMENTS",
    "ELEMENT_CYCLES",
    "ELEMENT_CHINESE",
    # Day Officers
    "DAY_OFFICERS",
    "DAY_OFFICER_ORDER",
    # Stem lookups
    "HEAVENLY_STEMS",
    "STEM_ORDER",
    "STEM_CHINESE",
    "STEM_CHINESE_TO_PINYIN",
    "ELEMENT_POLARITY_TO_STEM",
    "STEM_COMBINATIONS_MAP",
    "STEM_CONFLICTS_MAP",
    "get_stem",
    "get_stem_by_element_polarity",
    # Branch lookups
    "EARTHLY_BRANCHES",
    "BRANCH_ORDER",
    "BRANCH_CHINESE",
    "BRANCH_CHINESE_TO_PINYIN",
    "BRANCH_TO_SEASON",
    "BRANCH_TO_MONTH",
    "MONTH_TO_BRANCH",
    "STORAGE_BRANCHES",
    "SIX_HARMONIES_MAP",
    "CLASHES_MAP",
    "HARMS_MAP",
    "SELF_PUNISHMENT_BRANCHES",
    "get_branch",
    "get_primary_qi",
    "get_hidden_stems",
    "get_all_branch_qi",
    "get_branch_by_month",
    # Constants
    "Gan",
    "Zhi",
    "GAN_MAP",
    "ZHI_MAP",
    # Elements
    "WUXING",
    "ELEMENT_POLARITY_STEMS",
    "ELEMENT_COLORS",
    "ELEMENT_CHARACTERS",
    # Distance
    "NODE_COORDINATES",
    "get_distance_key",
    "get_distance_key_3nodes",
    # Scoring
    "DISTANCE_MULTIPLIERS",
    "BASE_SCORES",
    "generate_scoring",
    "generate_single_scoring",
    "generate_asymmetric_scoring",
    # Ten Gods
    "TEN_GODS",
    "TEN_GOD_NOTES",
    "get_ten_god",
    # Day Officers
    "get_day_officer",
    # Seasonal
    "SEASONAL_STRENGTH",
    "SEASONAL_ADJUSTMENT",
    "ELEMENT_SEASONAL_STATES",
    # Wealth Storage
    "EARTH_STORAGE_BRANCHES",
    "LARGE_WEALTH_STORAGE",
    "SMALL_WEALTH_STORAGE",
    "DM_WEALTH_ELEMENT",
    "WEALTH_ELEMENT_STEMS",
    # Wu Xing Combat Engine
    "WUXING_COMBAT",
    "get_distance_multiplier",
    "get_qi_type",
    "get_hidden_stem_priority",  # Backward compatibility
    "calculate_hidden_penalty",
    "format_interaction_math",
    "apply_wuxing_interaction",
    "calculate_wuxing_control",
    "calculate_wuxing_generation",
    "HIDDEN_QI_INTERACTIONS",
    # Combinations
    "THREE_MEETINGS",
    "THREE_COMBINATIONS",
    "HALF_MEETINGS",
    "SIX_HARMONIES",
    "ARCHED_COMBINATIONS",
    "STEM_COMBINATIONS",
    "TRANSFORMATION_STRENGTH",
    "STRENGTH_ORDER",
    # Conflicts
    "PUNISHMENTS",
    "PUNISHMENT_SEVERITY",
    "HARMS",
    "CLASHES",
    "DESTRUCTION",
    "STEM_CONFLICTS",
    "WUXING_ENERGY_FLOW",
    # Dong Gong
    "DONG_GONG_RATINGS",
    "DONG_GONG_DAY_OFFICERS",
    "DONG_GONG_OFFICER_ORDER",
    "DONG_GONG_BRANCH_ORDER",
    "DONG_GONG_MONTHS",
    "DONG_GONG_BRANCH_TO_MONTH",
    "DONG_GONG",
    "get_dong_gong_officer",
    "get_dong_gong_rating",
    "get_dong_gong_day_info",
    "check_consult_promotion",
    # Unit Story Tracker
    "UnitEvent",
    "UnitStory",
    "UnitTracker",
    # Qi Phase
    "QI_PHASES",
    "QI_PHASE_BY_ID",
    "QI_PHASE_TABLE",
    "QI_PHASE_STRENGTH_COLORS",
    "get_qi_phase",
    "get_qi_phase_id",
    "get_qi_phase_for_pillar",
    # Dynamic Scoring System
    "COMBINATION_MULTIPLIERS",
    "TRANSFORMATION_BONUS",
    "get_primary_qi_info",
    "get_primary_hidden_stem_info",  # Backward compatibility
    "get_current_qi_for_stem",
    "calculate_dynamic_combination_score",
    "calculate_dynamic_conflict_score",
    "calculate_symmetric_conflict_score",
    "format_combination_narrative",
    "format_conflict_narrative",
    # Life Aspects - Base
    "NODE_RELATIONSHIPS",
    "PILLAR_LIFE_PERIODS",
    "TEN_GOD_ASPECT_MAPPING",
    "ELEMENT_CONTROLS",
    "ELEMENT_GENERATES",
    "stems_to_element_totals",
    "get_node_relationship_context",
    "detect_control_imbalances",
    "calculate_aspect_severity",
    # Life Aspects - Health
    "ELEMENT_ORGANS",
    "CONFLICT_HEALTH_WEIGHTS",
    "SEASONAL_HEALTH_MODIFIER",
    "generate_health_analysis",
    # Life Aspects - Wealth
    "WEALTH_TEN_GODS",
    "WEALTH_INDICATORS",
    "generate_wealth_analysis",
    # Life Aspects - Learning
    "LEARNING_TEN_GODS",
    "LEARNING_INDICATORS",
    "generate_learning_analysis",
    # Life Aspects - Ten Gods Detail
    "TEN_GOD_PILLAR_MEANINGS",
    "get_ten_god_for_stem",
    "generate_ten_gods_detail",
    # Narrative Interpretation System
    "generate_narrative",
    "NARRATIVE_TEMPLATES",
    "calculate_priority_score",
    "prioritize_narratives",
    "apply_element_modifiers",
    "apply_shen_sha_modifiers",
    "get_element_balance_context",
    "generate_remedies",
    "REMEDY_TEMPLATES",
    "ELEMENT_REMEDIES",
    "build_narrative_text",
    "get_localized_template",
    "SUPPORTED_LOCALES",
]
