# * =============================================================================
# * PATTERN ENGINE - Universal BaZi Pattern System
# * =============================================================================
# * Declarative, deterministic pattern detection for 100% accurate BaZi analysis.
# * =============================================================================

from .pattern_spec import (
    # Enums
    PatternCategory,
    PunishmentType,
    SeasonalState,
    LifeDomain,
    NodeType,
    PillarType,
    BadgeType,

    # Core dataclasses
    NodeFilter,
    SpatialRule,
    TemporalRule,
    TransformSpec,
    QiEffect,
    PillarMeaning,
    EventMapping,
    PatternSpec,
    PatternMatch,

    # Helpers
    create_branch_filter,
    create_stem_filter,
    create_element_filter,
)

from .pattern_registry import (
    # Errors
    PatternRegistryError,
    DuplicatePatternError,
    CircularDependencyError,
    MissingDependencyError,
    ContradictionError,

    # Classes
    DependencyGraph,
    PatternRegistry,

    # Functions
    get_global_registry,
    reset_global_registry,
)

__all__ = [
    # Enums
    "PatternCategory",
    "PunishmentType",
    "SeasonalState",
    "LifeDomain",
    "NodeType",
    "PillarType",
    "BadgeType",

    # Core dataclasses
    "NodeFilter",
    "SpatialRule",
    "TemporalRule",
    "TransformSpec",
    "QiEffect",
    "PillarMeaning",
    "EventMapping",
    "PatternSpec",
    "PatternMatch",

    # Helpers
    "create_branch_filter",
    "create_stem_filter",
    "create_element_filter",

    # Errors
    "PatternRegistryError",
    "DuplicatePatternError",
    "CircularDependencyError",
    "MissingDependencyError",
    "ContradictionError",

    # Classes
    "DependencyGraph",
    "PatternRegistry",

    # Functions
    "get_global_registry",
    "reset_global_registry",
]

__version__ = "1.0.0"
