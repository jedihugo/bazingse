# * =============================================================================
# * PATTERN SPECIFICATION LANGUAGE (PSL)
# * =============================================================================
# * Declarative system for expressing all BaZi patterns.
# * Every pattern is immutable, deterministic, and traceable.
# * =============================================================================

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Tuple, FrozenSet, Dict, Any, List


# =============================================================================
# ENUMS - Pattern Classification
# =============================================================================

class PatternCategory(Enum):
    """Primary classification of BaZi patterns."""

    # Positive Combinations (add qi, create harmony)
    STEM_COMBINATION = "stem_combination"        # 天干合 (5 pairs)
    THREE_MEETINGS = "three_meetings"            # 三會方局 (4 directional)
    THREE_COMBINATIONS = "three_combinations"    # 三合局 (4 triangular)
    HALF_MEETINGS = "half_meetings"              # 半會 (partial directional)
    SIX_HARMONIES = "six_harmonies"              # 六合 (6 pairs)
    HALF_COMBINATIONS = "half_combinations"      # 半合 (partial triangular)
    ARCHED_COMBINATIONS = "arched_combinations"  # 拱合 (arched patterns)

    # Negative Conflicts (reduce qi, create tension)
    STEM_CONFLICT = "stem_conflict"              # 天干沖/剋 (5 pairs)
    CLASH = "clash"                              # 地支沖 (6 pairs)
    PUNISHMENT = "punishment"                    # 刑 (4 types)
    HARM = "harm"                                # 害 (6 pairs)
    DESTRUCTION = "destruction"                  # 破 (6 pairs)

    # Structural Patterns (describe relationships)
    PILLAR_UNITY = "pillar_unity"                # 干支一體
    TEN_GODS = "ten_gods"                        # 十神
    QI_PHASE = "qi_phase"                        # 長生十二宮

    # Temporal Patterns (time-based)
    SEASONAL_STATE = "seasonal_state"            # 旺相休囚死
    ENERGY_FLOW = "energy_flow"                  # 五行生剋

    # Special Patterns (classical BaZi stars)
    KONG_WANG = "kong_wang"                      # 空亡 (Void)
    GUI_REN = "gui_ren"                          # 貴人 (Nobleman)
    TAO_HUA = "tao_hua"                          # 桃花 (Peach Blossom)
    YI_MA = "yi_ma"                              # 驛馬 (Traveling Horse)
    YANG_REN = "yang_ren"                        # 羊刃 (Yang Blade)
    LU_SHEN = "lu_shen"                          # 祿神 (Prosperity God)
    HUA_GAI = "hua_gai"                          # 華蓋 (Canopy Star)
    GU_CHEN = "gu_chen"                          # 孤辰 (Lonely Star)
    GUA_SU = "gua_su"                            # 寡宿 (Widow Star)

    # Storage Patterns
    WEALTH_STORAGE = "wealth_storage"            # 財庫


class PunishmentType(Enum):
    """Hierarchy of punishment severity (刑法輕重)."""
    SHI_XING = "shi_xing"      # 勢刑 - Power/Bullying (Yin-Si-Shen) - Severe
    WU_LI_XING = "wu_li_xing"  # 無禮刑 - Rudeness (Chou-Wei-Xu) - Moderate
    EN_XING = "en_xing"        # 恩刑 - Ungrateful (Zi-Mao) - Light
    ZI_XING = "zi_xing"        # 自刑 - Self-punishment - Self


class SeasonalState(Enum):
    """Seasonal strength states (旺相休囚死)."""
    PROSPEROUS = "Prosperous"    # 旺 Wang - Strongest
    STRENGTHENING = "Strengthening"  # 相 Xiang - Growing
    RESTING = "Resting"          # 休 Xiu - Baseline
    TRAPPED = "Trapped"          # 囚 Qiu - Weakened
    DEAD = "Dead"                # 死 Si - Weakest


class LifeDomain(Enum):
    """Life aspect domains for event mapping."""
    HEALTH = "health"
    WEALTH = "wealth"
    CAREER = "career"
    RELATIONSHIP = "relationship"
    EDUCATION = "education"
    FAMILY = "family"
    LEGAL = "legal"
    TRAVEL = "travel"


class NodeType(Enum):
    """Classification of chart nodes."""
    HEAVENLY_STEM = "hs"
    EARTHLY_BRANCH = "eb"
    HIDDEN_STEM = "hidden"


class PillarType(Enum):
    """Classification of pillar sources."""
    NATAL = "natal"          # Birth chart (Year, Month, Day, Hour)
    TEN_YEAR = "10yl"        # 10-year luck pillar
    ANNUAL = "annual"        # Annual luck
    MONTHLY = "monthly"      # Monthly luck
    DAILY = "daily"          # Daily luck
    HOURLY = "hourly"        # Hourly luck
    TALISMAN = "talisman"    # Talisman overrides


class BadgeType(Enum):
    """Visual badge classifications."""
    TRANSFORMATION = "transformation"  # Successful combination
    COMBINATION = "combination"        # Partial combination
    PUNISHMENT = "punishment"          # 刑
    HARM = "harm"                      # 害
    CLASH = "clash"                    # 沖
    DESTRUCTION = "destruction"        # 破
    STEM_CONFLICT = "stem_conflict"    # 剋


# =============================================================================
# CORE DATA STRUCTURES - Immutable Pattern Specifications
# =============================================================================

@dataclass(frozen=True)
class NodeFilter:
    """
    Declarative filter for matching chart nodes.

    All conditions are AND-ed together (node must match ALL specified criteria).
    Within each set, values are OR-ed (match ANY of the specified values).
    """

    # Value matching (ANY of these conditions)
    stems: Optional[FrozenSet[str]] = None       # Match specific stems (e.g., {"Jia", "Yi"})
    branches: Optional[FrozenSet[str]] = None    # Match specific branches
    elements: Optional[FrozenSet[str]] = None    # Match by element
    polarities: Optional[FrozenSet[str]] = None  # Match Yang/Yin

    # Position matching
    positions: Optional[FrozenSet[int]] = None   # Specific position indices (0-12)
    pillar_types: Optional[FrozenSet[PillarType]] = None  # natal/luck/talisman
    node_types: Optional[FrozenSet[NodeType]] = None  # hs/eb/hidden

    # Qi state matching
    min_qi: Optional[float] = None               # Minimum qi threshold
    max_qi: Optional[float] = None               # Maximum qi threshold
    seasonal_states: Optional[FrozenSet[SeasonalState]] = None

    def matches(self, node_state: Dict[str, Any]) -> bool:
        """
        Check if a node matches this filter.

        Args:
            node_state: Dict with keys like 'value', 'element', 'polarity',
                       'position', 'pillar_type', 'node_type', 'qi', 'seasonal_state'

        Returns:
            True if node matches ALL specified criteria
        """
        # Value matching
        if self.stems and node_state.get("value") not in self.stems:
            return False
        if self.branches and node_state.get("value") not in self.branches:
            return False
        if self.elements and node_state.get("element") not in self.elements:
            return False
        if self.polarities and node_state.get("polarity") not in self.polarities:
            return False

        # Position matching
        if self.positions and node_state.get("position") not in self.positions:
            return False
        if self.pillar_types:
            ptype = node_state.get("pillar_type")
            if ptype and ptype not in self.pillar_types:
                return False
        if self.node_types:
            ntype = node_state.get("node_type")
            if ntype and ntype not in self.node_types:
                return False

        # Qi state matching
        qi = node_state.get("qi", 0)
        if self.min_qi is not None and qi < self.min_qi:
            return False
        if self.max_qi is not None and qi > self.max_qi:
            return False
        if self.seasonal_states:
            sstate = node_state.get("seasonal_state")
            if sstate and sstate not in self.seasonal_states:
                return False

        return True


@dataclass(frozen=True)
class SpatialRule:
    """
    Distance and position constraints for pattern detection.

    Patterns can require specific spatial relationships between nodes.
    """

    # Distance constraints
    max_distance: Optional[int] = None  # Maximum allowed distance between nodes
    require_adjacent: bool = False       # Nodes must be distance 0 or 1

    # Position constraints
    same_pillar: bool = False            # All nodes in same pillar
    cross_pillar: bool = False           # Nodes must span different pillars

    # Specific position requirements
    requires_day_pillar: bool = False    # At least one node in Day pillar
    requires_month_pillar: bool = False  # At least one node in Month pillar

    def validate(self, node_positions: List[int]) -> bool:
        """Check if node positions satisfy spatial constraints."""
        if not node_positions:
            return True

        # Same pillar check
        if self.same_pillar:
            # Positions 0-3 are natal, grouped as pillar pairs
            pillars = {pos // 2 for pos in node_positions if pos < 8}
            if len(pillars) > 1:
                return False

        # Cross pillar check
        if self.cross_pillar:
            pillars = {pos // 2 for pos in node_positions if pos < 8}
            if len(pillars) < 2:
                return False

        # Day pillar (position 1)
        if self.requires_day_pillar:
            if 1 not in {pos // 2 for pos in node_positions}:
                return False

        # Month pillar (position 2)
        if self.requires_month_pillar:
            if 2 not in {pos // 2 for pos in node_positions}:
                return False

        return True


@dataclass(frozen=True)
class TemporalRule:
    """
    Timing constraints for pattern activation.

    Controls when patterns are active based on luck pillars.
    """

    # Luck pillar requirements
    requires_luck_pillar: bool = False   # Pattern only activates during luck periods
    luck_types: Optional[FrozenSet[PillarType]] = None  # Which luck pillars activate

    # Temporal overlay behavior
    is_temporal_overlay: bool = True     # Luck pillars interact with ALL natal (default BaZi behavior)

    # Activation conditions
    min_year_span: Optional[int] = None  # Minimum years for pattern to be significant

    def applies_to(self, pillar_type: PillarType) -> bool:
        """Check if this rule applies to a specific pillar type."""
        if not self.requires_luck_pillar:
            return True
        if self.luck_types:
            return pillar_type in self.luck_types
        return pillar_type != PillarType.NATAL


@dataclass(frozen=True)
class TransformSpec:
    """
    Specification for element transformations.

    When combinations activate, they can transform into new elements.
    """

    # Target element
    resulting_element: str               # Element produced (e.g., "Fire")

    # Transformation conditions
    requires_element_support: bool = True  # Needs supporting element in chart
    supporting_elements: Optional[FrozenSet[str]] = None  # Which elements enable transformation

    # Badge generation
    use_branch_polarity: bool = True     # Use branch polarity for badge (EB transformations)
    use_primary_qi_polarity: bool = False  # Use primary qi polarity (energy flow)

    # Strength modifiers
    base_score_multiplier: float = 1.0   # Transformation strength modifier


@dataclass(frozen=True)
class QiEffect:
    """
    Specification for qi changes from a pattern.

    Describes how qi flows between nodes when pattern activates.
    """

    # Target specification
    target: str                          # "source" | "target" | "all" | specific node filter

    # Qi modification
    qi_change: float                     # Positive (add) or negative (reduce)
    is_percentage: bool = False          # True if qi_change is percentage, False if absolute

    # Conditional application
    only_if_stronger: bool = False       # Only apply if source stronger than target
    seasonal_multiplier: bool = True     # Apply seasonal state modifiers


@dataclass(frozen=True)
class PillarMeaning:
    """
    Position-specific interpretation of a pattern.

    Same pattern has different meanings based on which pillar it appears in.
    """

    year: str = ""       # Ancestral, early childhood, external
    month: str = ""      # Career, parents, social standing
    day: str = ""        # Self, spouse, personal core
    hour: str = ""       # Children, old age, legacy


@dataclass(frozen=True)
class EventMapping:
    """
    Mapping from pattern to life event predictions.

    Defines what life events a pattern correlates with.
    """

    # Domain classification
    primary_domains: FrozenSet[LifeDomain] = field(default_factory=frozenset)
    secondary_domains: FrozenSet[LifeDomain] = field(default_factory=frozenset)

    # Event types per domain (domain -> list of event type strings)
    positive_events: Tuple[Tuple[str, str], ...] = ()  # ((domain, event_type), ...)
    negative_events: Tuple[Tuple[str, str], ...] = ()

    # Sentiment by domain
    domain_sentiment: Tuple[Tuple[str, str], ...] = ()  # ((domain, "positive"|"negative"|"conditional"), ...)

    # Severity modifiers by position
    pillar_severity_modifiers: Tuple[Tuple[str, float], ...] = (
        ("year", 1.0),
        ("month", 1.2),
        ("day", 1.5),
        ("hour", 1.0),
    )


# =============================================================================
# MAIN PATTERN SPECIFICATION
# =============================================================================

@dataclass(frozen=True)
class PatternSpec:
    """
    Immutable specification of a BaZi pattern.

    This is the core data structure that describes everything about a pattern:
    - How to detect it (filters, spatial rules, temporal rules)
    - What it does (transformations, qi effects)
    - What it means (life domains, pillar meanings)
    - How to score it (base scores, multipliers)

    All patterns are deterministic - same inputs always produce same outputs.
    """

    # ==========================================================================
    # Identity
    # ==========================================================================
    id: str                              # Unique ID (e.g., "THREE_MEETINGS~Si-Wu-Wei~Fire")
    category: PatternCategory            # Primary classification
    priority: int                        # Lower = processed earlier (0-1000)
    chinese_name: str                    # Chinese characters (e.g., "三會")
    english_name: str                    # English name (e.g., "Three Meetings")

    # ==========================================================================
    # Detection Criteria
    # ==========================================================================
    node_filters: Tuple[NodeFilter, ...]  # What nodes must be present
    min_nodes: int = 2                   # Minimum matching nodes required
    max_nodes: Optional[int] = None      # Maximum nodes (None = unlimited)

    spatial_rule: SpatialRule = field(default_factory=SpatialRule)
    temporal_rule: TemporalRule = field(default_factory=TemporalRule)

    # ==========================================================================
    # Prerequisites & Blockers
    # ==========================================================================
    requires: FrozenSet[str] = field(default_factory=frozenset)  # Pattern IDs that must be active
    blocked_by: FrozenSet[str] = field(default_factory=frozenset)  # Pattern IDs that prevent this

    # ==========================================================================
    # Transformation Logic
    # ==========================================================================
    transformation: Optional[TransformSpec] = None

    # ==========================================================================
    # Scoring
    # ==========================================================================
    base_score_combined: float = 10.0    # Score when pattern detected
    base_score_transformed: float = 15.0  # Score when transformation activates

    # Distance multipliers: (adjacent, nearby, far)
    distance_multipliers: Tuple[float, ...] = (1.0, 0.7, 0.5)

    # ==========================================================================
    # Effects
    # ==========================================================================
    qi_effects: Tuple[QiEffect, ...] = ()  # How qi changes
    badge_type: BadgeType = BadgeType.COMBINATION

    # ==========================================================================
    # Life Event Mapping
    # ==========================================================================
    life_domains: FrozenSet[LifeDomain] = field(default_factory=frozenset)
    pillar_meanings: PillarMeaning = field(default_factory=PillarMeaning)
    event_mapping: Optional[EventMapping] = None

    # Severity calculation formula (string expression evaluated at runtime)
    severity_formula: str = "base * strength * distance_mult * seasonal_mult"

    # ==========================================================================
    # Metadata
    # ==========================================================================
    description: str = ""                # Human-readable description
    classical_source: str = ""           # Reference to classical text
    notes: str = ""                      # Implementation notes

    def get_id_parts(self) -> Tuple[str, str, str]:
        """
        Parse pattern ID into components.

        Format: TYPE~PARTICIPANTS~RESULT
        Example: "THREE_MEETINGS~Si-Wu-Wei~Fire" -> ("THREE_MEETINGS", "Si-Wu-Wei", "Fire")
        """
        parts = self.id.split("~")
        if len(parts) >= 3:
            return (parts[0], parts[1], parts[2])
        elif len(parts) == 2:
            return (parts[0], parts[1], "")
        else:
            return (parts[0], "", "")

    def get_participants(self) -> List[str]:
        """Extract participant names from pattern ID."""
        _, participants, _ = self.get_id_parts()
        if participants:
            return participants.split("-")
        return []


# =============================================================================
# PATTERN MATCH RESULT
# =============================================================================

@dataclass
class PatternMatch:
    """
    Result of matching a pattern against a chart state.

    Contains all information needed to apply the pattern's effects.
    """

    pattern: PatternSpec                 # The matched pattern
    matched_nodes: List[Dict[str, Any]]  # Nodes that matched
    distance: int                        # Distance between matched nodes
    score: float                         # Calculated score
    is_transformed: bool                 # Whether transformation activated

    # Traceability
    match_reason: str = ""               # Why this pattern matched
    blocked_patterns: List[str] = field(default_factory=list)  # Patterns this blocks

    def get_distance_multiplier(self) -> float:
        """Get distance multiplier for this match."""
        mults = self.pattern.distance_multipliers
        if self.distance < len(mults):
            return mults[self.distance]
        return mults[-1] if mults else 0.5


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_branch_filter(*branches: str, **kwargs) -> NodeFilter:
    """Helper to create a NodeFilter for specific branches."""
    return NodeFilter(
        branches=frozenset(branches),
        node_types=frozenset([NodeType.EARTHLY_BRANCH]),
        **kwargs
    )


def create_stem_filter(*stems: str, **kwargs) -> NodeFilter:
    """Helper to create a NodeFilter for specific stems."""
    return NodeFilter(
        stems=frozenset(stems),
        node_types=frozenset([NodeType.HEAVENLY_STEM]),
        **kwargs
    )


def create_element_filter(element: str, **kwargs) -> NodeFilter:
    """Helper to create a NodeFilter for a specific element."""
    return NodeFilter(
        elements=frozenset([element]),
        **kwargs
    )


# =============================================================================
# EXPORTS
# =============================================================================

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
]
