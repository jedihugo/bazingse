# * =============================================================================
# * LIFE EVENTS MODULE
# * =============================================================================
# * Comprehensive life event taxonomy and severity calculation for BaZi analysis.
# * =============================================================================

from .taxonomy import (
    # Enums
    LifeDomain,
    Sentiment,
    Severity,

    # TCM
    TCMOrganSystem,
    TCM_ORGANS,

    # Event Types
    EventType,
    HEALTH_EVENTS,
    WEALTH_EVENTS,
    CAREER_EVENTS,
    RELATIONSHIP_EVENTS,
    EDUCATION_EVENTS,
    FAMILY_EVENTS,
    LEGAL_EVENTS,
    TRAVEL_EVENTS,
    ALL_EVENT_TYPES,

    # Functions
    get_events_by_domain,
    get_events_by_element,
    get_event_statistics,
)

from .severity import (
    # Multipliers
    DISTANCE_MULTIPLIERS,
    SEASONAL_STATE_MULTIPLIERS,
    PILLAR_POSITION_MULTIPLIERS,
    PATTERN_CATEGORY_WEIGHTS,

    # Classes
    SeverityResult,

    # Functions
    calculate_pattern_severity,
    calculate_compound_severity,
    calculate_health_severity,
    calculate_wealth_severity,
)


__all__ = [
    # Taxonomy Enums
    "LifeDomain",
    "Sentiment",
    "Severity",

    # TCM
    "TCMOrganSystem",
    "TCM_ORGANS",

    # Event Types
    "EventType",
    "HEALTH_EVENTS",
    "WEALTH_EVENTS",
    "CAREER_EVENTS",
    "RELATIONSHIP_EVENTS",
    "EDUCATION_EVENTS",
    "FAMILY_EVENTS",
    "LEGAL_EVENTS",
    "TRAVEL_EVENTS",
    "ALL_EVENT_TYPES",

    # Taxonomy Functions
    "get_events_by_domain",
    "get_events_by_element",
    "get_event_statistics",

    # Severity Multipliers
    "DISTANCE_MULTIPLIERS",
    "SEASONAL_STATE_MULTIPLIERS",
    "PILLAR_POSITION_MULTIPLIERS",
    "PATTERN_CATEGORY_WEIGHTS",

    # Severity Classes
    "SeverityResult",

    # Severity Functions
    "calculate_pattern_severity",
    "calculate_compound_severity",
    "calculate_health_severity",
    "calculate_wealth_severity",
]
