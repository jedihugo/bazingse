# =============================================================================
# DATA MODELS for Comprehensive BaZi Analysis
# =============================================================================
# All structured data types used across the analysis engine.
# Frozen dataclasses for immutability and hashability.
# =============================================================================

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple


@dataclass
class Pillar:
    """A single BaZi pillar (stem + branch + hidden stems)."""
    position: str                   # "year", "month", "day", "hour"
    stem: str                       # Pinyin: "Jia", "Yi", ..., "Gui"
    branch: str                     # Pinyin: "Zi", "Chou", ..., "Hai"
    stem_chinese: str = ""
    branch_chinese: str = ""
    stem_element: str = ""
    stem_polarity: str = ""
    branch_element: str = ""
    branch_polarity: str = ""
    hidden_stems: List[Tuple[str, int]] = field(default_factory=list)

    @property
    def palace_name(self) -> str:
        return {
            "year": "Parents/Ancestry",
            "month": "Career/Social",
            "day": "Self/Spouse",
            "hour": "Children/Legacy",
            "luck_pillar": "Current Luck Pillar",
            "annual": "Annual Luck",
            "monthly": "Monthly Luck",
            "daily": "Daily Luck",
            "hourly": "Hourly Luck",
        }.get(self.position, self.position)

    @property
    def palace_chinese(self) -> str:
        return {
            "year": "年柱 (父母宫)",
            "month": "月柱 (事业宫)",
            "day": "日柱 (夫妻宫)",
            "hour": "时柱 (子女宫)",
            "luck_pillar": "大运",
            "annual": "流年",
            "monthly": "流月",
            "daily": "流日",
            "hourly": "流时",
        }.get(self.position, self.position)


@dataclass
class TenGodEntry:
    """A Ten God mapping for a specific stem."""
    stem: str                       # The stem being evaluated
    abbreviation: str               # "F", "RW", "EG", etc.
    english: str                    # "Friend", "Rob Wealth", etc.
    chinese: str                    # "比肩", "劫財", etc.
    location: str                   # "year_stem", "month_stem", "day_branch_hidden_1", etc.
    position: str                   # "year", "month", "day", "hour"
    visible: bool = True            # True if heavenly stem, False if hidden


@dataclass
class ShenShaResult:
    """Result of a Shen Sha star check."""
    name_english: str
    name_chinese: str
    present: bool
    location: Optional[str] = None          # Branch where it's found: "Chou", "Wu", etc.
    palace: Optional[str] = None            # "year", "month", "day", "hour", or "luck_pillar"
    activated_by: Optional[str] = None      # "luck_pillar", "annual_pillar", or None (natal)
    derivation: str = ""                    # How it was derived
    nature: str = "neutral"                 # "auspicious", "inauspicious", "mixed", "neutral"
    impact: str = ""                        # Short description of what it means
    life_areas: List[str] = field(default_factory=list)
    severity: str = "mild"                  # "mild", "moderate", "severe", "critical"
    is_void: bool = False                   # Whether the branch it sits on is Void


@dataclass
class BranchInteraction:
    """A detected branch interaction."""
    interaction_type: str           # "clash", "harmony", "punishment", etc.
    chinese_name: str               # "六冲", "六合", etc.
    branches: List[str]             # Branch IDs involved
    palaces: List[str]              # Palace names involved
    description: str = ""
    activated_by_lp: bool = False   # Whether activated by current luck pillar
    severity: str = "moderate"


@dataclass
class StrengthAssessment:
    """Day Master strength assessment result."""
    score: float                    # DM's element percentage (20% = balanced)
    verdict: str                    # "extremely_strong", "strong", "neutral", "weak", "extremely_weak"
    support_count: float
    drain_count: float
    seasonal_state: str             # "Prosperous", "Strengthening", "Resting", "Trapped", "Dead"
    is_following_chart: bool = False
    following_type: Optional[str] = None    # "wealth", "officer", "output", etc.
    useful_god: str = ""                    # Element name
    favorable_elements: List[str] = field(default_factory=list)
    unfavorable_elements: List[str] = field(default_factory=list)
    element_percentages: Dict[str, float] = field(default_factory=dict)


@dataclass
class RedFlag:
    """A consolidated red flag for a life area."""
    life_area: str                  # "marriage", "wealth", "career", "health", "character"
    indicator_type: str             # "ten_god", "branch_interaction", "shen_sha"
    indicator_name: str
    description: str
    severity: str = "moderate"      # "mild", "moderate", "severe", "critical"


@dataclass
class EventPrediction:
    """A predicted life event with year and score."""
    event_type: str                 # "marriage", "divorce", "child_birth", "career_peak", etc.
    year: int
    age: int
    score: float
    factors: List[str] = field(default_factory=list)    # Why this year scored high


@dataclass
class LuckPillarInfo:
    """Information about a luck pillar."""
    stem: str
    branch: str
    stem_chinese: str = ""
    branch_chinese: str = ""
    start_age: int = 0
    end_age: int = 0
    start_year: int = 0
    end_year: int = 0
    stem_ten_god: str = ""
    stem_ten_god_chinese: str = ""
    is_current: bool = False
    hidden_stems: List[Tuple[str, int]] = field(default_factory=list)


@dataclass
class EnvironmentAssessment:
    """Environmental qi and relocation assessment."""
    crosses_water_benefit: bool
    crosses_water_reason: str
    favorable_directions: List[str]
    unfavorable_directions: List[str]
    ideal_climate: str
    ideal_geography: str
    guo_jiang_long_score: int           # 0-5
    guo_jiang_long_verdict: str         # "strong", "moderate", "not_applicable"
    guo_jiang_long_factors: List[str]
    void_disruption_palaces: List[str]
    location_recommendations: str


@dataclass
class ChartData:
    """Complete chart data for analysis."""
    gender: str                     # "male" or "female"
    birth_year: int
    age: int
    pillars: Dict[str, Pillar]      # "year", "month", "day", "hour"
    day_master: str                 # Stem ID: "Gui", "Jia", etc.
    dm_element: str
    dm_polarity: str
    dm_chinese: str
    luck_pillar: Optional[Pillar] = None
    luck_pillars: List[LuckPillarInfo] = field(default_factory=list)
    time_period_pillars: Dict[str, Pillar] = field(default_factory=dict)
    current_year_stem: str = ""
    current_year_branch: str = ""
