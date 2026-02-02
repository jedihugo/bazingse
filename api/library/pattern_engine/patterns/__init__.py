# * =============================================================================
# * PATTERN DEFINITIONS - Declarative BaZi Pattern Catalog
# * =============================================================================
# * All BaZi patterns expressed as immutable PatternSpec objects.
# * Import from here to access all pattern definitions.
# * =============================================================================

from typing import List

from ..pattern_spec import PatternSpec
from ..pattern_registry import PatternRegistry, get_global_registry

from .branch_combinations import (
    THREE_MEETINGS_PATTERNS,
    THREE_COMBINATIONS_PATTERNS,
    SIX_HARMONIES_PATTERNS,
    HALF_MEETINGS_PATTERNS,
    HALF_COMBINATIONS_PATTERNS,
    ARCHED_COMBINATIONS_PATTERNS,
    ALL_BRANCH_COMBINATION_PATTERNS,
    get_all_branch_combination_patterns,
)

from .branch_conflicts import (
    CLASHES_PATTERNS,
    PUNISHMENTS_PATTERNS,
    HARMS_PATTERNS,
    DESTRUCTION_PATTERNS,
    ALL_BRANCH_CONFLICT_PATTERNS,
    get_all_branch_conflict_patterns,
)

from .stem_patterns import (
    STEM_COMBINATIONS_PATTERNS,
    STEM_CONFLICTS_PATTERNS,
    ALL_STEM_PATTERNS,
    get_all_stem_patterns,
)

from .special_stars import (
    KONG_WANG_PATTERNS,
    GUI_REN_PATTERNS,
    TAO_HUA_PATTERNS,
    YI_MA_PATTERNS,
    YANG_REN_PATTERNS,
    LU_SHEN_PATTERNS,
    HUA_GAI_PATTERNS,
    GU_CHEN_PATTERNS,
    GUA_SU_PATTERNS,
    ALL_SPECIAL_STAR_PATTERNS,
    get_all_special_star_patterns,
    get_special_stars_for_day_master,
    get_special_stars_for_year_branch,
)


# =============================================================================
# COMBINED PATTERN ACCESS
# =============================================================================

def get_all_patterns() -> List[PatternSpec]:
    """
    Get all registered patterns across all categories.

    Returns a copy of the pattern list to prevent modification.
    """
    return (
        get_all_branch_combination_patterns() +
        get_all_branch_conflict_patterns() +
        get_all_stem_patterns() +
        get_all_special_star_patterns()
    )


def load_all_patterns(registry: PatternRegistry = None) -> PatternRegistry:
    """
    Load all patterns into a registry.

    Args:
        registry: Optional registry to load into. If None, uses global registry.

    Returns:
        The registry with all patterns loaded.
    """
    if registry is None:
        registry = get_global_registry()

    all_patterns = get_all_patterns()

    for pattern in all_patterns:
        if pattern.id not in registry:
            registry.register(pattern, validate=True)

    return registry


def get_pattern_statistics() -> dict:
    """Get statistics about all defined patterns."""
    all_patterns = get_all_patterns()

    # Count by category
    by_category = {}
    for pattern in all_patterns:
        cat = pattern.category.value
        by_category[cat] = by_category.get(cat, 0) + 1

    # Count by life domain
    by_domain = {}
    for pattern in all_patterns:
        for domain in pattern.life_domains:
            dom = domain.value
            by_domain[dom] = by_domain.get(dom, 0) + 1

    # Count transformations
    transformations = sum(1 for p in all_patterns if p.transformation)

    return {
        "total_patterns": len(all_patterns),
        "by_category": by_category,
        "by_domain": by_domain,
        "with_transformations": transformations,
        "with_event_mappings": sum(1 for p in all_patterns if p.event_mapping),
        "branch_combinations": len(ALL_BRANCH_COMBINATION_PATTERNS),
        "branch_conflicts": len(ALL_BRANCH_CONFLICT_PATTERNS),
        "stem_patterns": len(ALL_STEM_PATTERNS),
    }


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Branch Combinations
    "THREE_MEETINGS_PATTERNS",
    "THREE_COMBINATIONS_PATTERNS",
    "SIX_HARMONIES_PATTERNS",
    "HALF_MEETINGS_PATTERNS",
    "HALF_COMBINATIONS_PATTERNS",
    "ARCHED_COMBINATIONS_PATTERNS",
    "ALL_BRANCH_COMBINATION_PATTERNS",
    "get_all_branch_combination_patterns",

    # Branch Conflicts
    "CLASHES_PATTERNS",
    "PUNISHMENTS_PATTERNS",
    "HARMS_PATTERNS",
    "DESTRUCTION_PATTERNS",
    "ALL_BRANCH_CONFLICT_PATTERNS",
    "get_all_branch_conflict_patterns",

    # Stem Patterns
    "STEM_COMBINATIONS_PATTERNS",
    "STEM_CONFLICTS_PATTERNS",
    "ALL_STEM_PATTERNS",
    "get_all_stem_patterns",

    # Special Stars
    "KONG_WANG_PATTERNS",
    "GUI_REN_PATTERNS",
    "TAO_HUA_PATTERNS",
    "YI_MA_PATTERNS",
    "YANG_REN_PATTERNS",
    "LU_SHEN_PATTERNS",
    "HUA_GAI_PATTERNS",
    "GU_CHEN_PATTERNS",
    "GUA_SU_PATTERNS",
    "ALL_SPECIAL_STAR_PATTERNS",
    "get_all_special_star_patterns",
    "get_special_stars_for_day_master",
    "get_special_stars_for_year_branch",

    # Combined Access
    "get_all_patterns",
    "load_all_patterns",
    "get_pattern_statistics",
]
