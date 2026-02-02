# * =============================================================================
# * LIFE EVENT TAXONOMY
# * =============================================================================
# * Comprehensive classification of life events for BaZi correlation analysis.
# * Every event type is mapped to affected TCM organs, elements, and pillars.
# * =============================================================================

from dataclasses import dataclass, field
from typing import Dict, List, FrozenSet, Optional
from enum import Enum


# =============================================================================
# DOMAIN DEFINITIONS
# =============================================================================

class LifeDomain(Enum):
    """Primary life domains for event classification."""
    HEALTH = "health"
    WEALTH = "wealth"
    CAREER = "career"
    RELATIONSHIP = "relationship"
    EDUCATION = "education"
    FAMILY = "family"
    LEGAL = "legal"
    TRAVEL = "travel"


class Sentiment(Enum):
    """Event sentiment classification."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    CONDITIONAL = "conditional"  # Depends on context


class Severity(Enum):
    """Event severity levels."""
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CRITICAL = "critical"


# =============================================================================
# TCM ORGAN MAPPING
# =============================================================================

@dataclass(frozen=True)
class TCMOrganSystem:
    """TCM organ system with element correlation."""
    element: str
    zang_organ: str          # Yin organ (solid)
    fu_organ: str            # Yang organ (hollow)
    chinese_zang: str
    chinese_fu: str
    body_parts: FrozenSet[str]
    emotion: str
    season: str
    color: str


TCM_ORGANS: Dict[str, TCMOrganSystem] = {
    "Wood": TCMOrganSystem(
        element="Wood",
        zang_organ="Liver",
        fu_organ="Gallbladder",
        chinese_zang="肝",
        chinese_fu="膽",
        body_parts=frozenset(["eyes", "tendons", "nails", "sinews"]),
        emotion="anger",
        season="Spring",
        color="green"
    ),
    "Fire": TCMOrganSystem(
        element="Fire",
        zang_organ="Heart",
        fu_organ="Small Intestine",
        chinese_zang="心",
        chinese_fu="小腸",
        body_parts=frozenset(["tongue", "blood_vessels", "complexion", "sweat"]),
        emotion="joy/anxiety",
        season="Summer",
        color="red"
    ),
    "Earth": TCMOrganSystem(
        element="Earth",
        zang_organ="Spleen",
        fu_organ="Stomach",
        chinese_zang="脾",
        chinese_fu="胃",
        body_parts=frozenset(["muscles", "mouth", "lips", "flesh"]),
        emotion="worry",
        season="Late Summer",
        color="yellow"
    ),
    "Metal": TCMOrganSystem(
        element="Metal",
        zang_organ="Lungs",
        fu_organ="Large Intestine",
        chinese_zang="肺",
        chinese_fu="大腸",
        body_parts=frozenset(["skin", "nose", "body_hair", "pores"]),
        emotion="grief",
        season="Autumn",
        color="white"
    ),
    "Water": TCMOrganSystem(
        element="Water",
        zang_organ="Kidneys",
        fu_organ="Bladder",
        chinese_zang="腎",
        chinese_fu="膀胱",
        body_parts=frozenset(["bones", "ears", "head_hair", "marrow", "brain"]),
        emotion="fear",
        season="Winter",
        color="black"
    ),
}


# =============================================================================
# EVENT TYPE DEFINITIONS
# =============================================================================

@dataclass(frozen=True)
class EventType:
    """
    Specification of a life event type.

    Contains all metadata needed for pattern correlation.
    """
    id: str                          # Unique identifier
    domain: LifeDomain              # Primary domain
    name: str                        # Display name
    chinese_name: str               # Chinese name
    default_sentiment: Sentiment     # Typical sentiment
    severity_range: FrozenSet[Severity]  # Valid severity levels

    # Element correlations
    primary_elements: FrozenSet[str] = frozenset()   # Most commonly affected
    secondary_elements: FrozenSet[str] = frozenset()  # Sometimes affected

    # Pillar correlations
    pillar_weights: Dict[str, float] = field(default_factory=dict)  # Position importance

    # TCM correlations (for health events)
    tcm_organs: FrozenSet[str] = frozenset()  # Affected organs

    # Pattern correlations
    common_patterns: FrozenSet[str] = frozenset()  # Frequently associated patterns

    description: str = ""


# =============================================================================
# HEALTH EVENTS
# =============================================================================

HEALTH_EVENTS: Dict[str, EventType] = {
    "illness_major": EventType(
        id="illness_major",
        domain=LifeDomain.HEALTH,
        name="Major Illness",
        chinese_name="大病",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MAJOR, Severity.CRITICAL]),
        primary_elements=frozenset(["Fire", "Water"]),
        tcm_organs=frozenset(["Heart", "Kidneys", "Liver"]),
        pillar_weights={"day": 1.5, "month": 1.2, "year": 1.0, "hour": 0.8},
        common_patterns=frozenset([
            "PUNISHMENT~Yin-Si-Shen~shi_xing",
            "CLASH~Zi-Wu~opposite",
            "STEM_CONFLICT~Bing-Ren~",
        ]),
        description="Severe illness requiring medical intervention"
    ),
    "illness_minor": EventType(
        id="illness_minor",
        domain=LifeDomain.HEALTH,
        name="Minor Illness",
        chinese_name="小病",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MINOR, Severity.MODERATE]),
        primary_elements=frozenset(["Metal", "Earth"]),
        tcm_organs=frozenset(["Lungs", "Spleen"]),
        pillar_weights={"day": 1.3, "month": 1.1, "year": 0.9, "hour": 0.9},
        description="Minor health issues, easily recoverable"
    ),
    "injury_accident": EventType(
        id="injury_accident",
        domain=LifeDomain.HEALTH,
        name="Injury/Accident",
        chinese_name="意外傷害",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Metal", "Wood"]),
        tcm_organs=frozenset(["Liver", "Gallbladder"]),
        pillar_weights={"day": 1.4, "year": 1.1, "month": 1.0, "hour": 1.0},
        common_patterns=frozenset([
            "CLASH~Yin-Shen~opposite",
            "PUNISHMENT~Yin-Si-Shen~shi_xing",
            "STEM_CONFLICT~Jia-Geng~",
        ]),
        description="Physical injury from accident or trauma"
    ),
    "surgery": EventType(
        id="surgery",
        domain=LifeDomain.HEALTH,
        name="Surgery",
        chinese_name="手術",
        default_sentiment=Sentiment.CONDITIONAL,
        severity_range=frozenset([Severity.MODERATE, Severity.MAJOR, Severity.CRITICAL]),
        primary_elements=frozenset(["Metal"]),
        tcm_organs=frozenset(["Lungs", "Large Intestine"]),
        pillar_weights={"day": 1.5, "month": 1.2, "year": 0.9, "hour": 0.9},
        common_patterns=frozenset([
            "STEM_CONFLICT~Jia-Geng~",
            "STEM_CONFLICT~Bing-Geng~",
        ]),
        description="Surgical procedure (can be positive if successful)"
    ),
    "recovery": EventType(
        id="recovery",
        domain=LifeDomain.HEALTH,
        name="Recovery",
        chinese_name="康復",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Wood", "Water"]),
        tcm_organs=frozenset(["Kidneys", "Liver"]),
        pillar_weights={"day": 1.3, "month": 1.1, "year": 1.0, "hour": 1.0},
        common_patterns=frozenset([
            "SIX_HARMONIES~Yin-Hai~Wood",
            "STEM_COMBINATION~Ding-Ren~Wood",
        ]),
        description="Recovery from illness or injury"
    ),
    "mental_health": EventType(
        id="mental_health",
        domain=LifeDomain.HEALTH,
        name="Mental Health Event",
        chinese_name="心理健康",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MODERATE, Severity.MAJOR, Severity.CRITICAL]),
        primary_elements=frozenset(["Fire", "Water"]),
        tcm_organs=frozenset(["Heart", "Kidneys"]),
        pillar_weights={"day": 1.6, "hour": 1.2, "month": 1.0, "year": 0.8},
        common_patterns=frozenset([
            "CLASH~Zi-Wu~opposite",
            "STEM_CONFLICT~Bing-Ren~",
            "PUNISHMENT~Chen-Chen~zi_xing",
        ]),
        description="Anxiety, depression, or other mental health challenges"
    ),
    "diagnosis": EventType(
        id="diagnosis",
        domain=LifeDomain.HEALTH,
        name="Medical Diagnosis",
        chinese_name="診斷",
        default_sentiment=Sentiment.NEUTRAL,
        severity_range=frozenset([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Metal", "Water"]),
        tcm_organs=frozenset(["Lungs", "Kidneys"]),
        pillar_weights={"day": 1.3, "month": 1.2, "year": 1.0, "hour": 0.9},
        description="Receiving a medical diagnosis (neutral - depends on outcome)"
    ),
    "seizure_neurological": EventType(
        id="seizure_neurological",
        domain=LifeDomain.HEALTH,
        name="Seizure/Neurological Event",
        chinese_name="癲癇/神經",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MODERATE, Severity.MAJOR, Severity.CRITICAL]),
        primary_elements=frozenset(["Fire", "Water", "Wood"]),
        tcm_organs=frozenset(["Heart", "Liver", "Kidneys"]),
        pillar_weights={"day": 1.5, "hour": 1.3, "month": 1.1, "year": 0.9},
        common_patterns=frozenset([
            "PUNISHMENT~Yin-Si-Shen~shi_xing",
            "CLASH~Zi-Wu~opposite",
            "STEM_CONFLICT~Bing-Ren~",
        ]),
        description="Epileptic seizure or other neurological event - Fire/Water imbalance affecting Heart/Brain"
    ),
}


# =============================================================================
# WEALTH EVENTS
# =============================================================================

WEALTH_EVENTS: Dict[str, EventType] = {
    "income_increase": EventType(
        id="income_increase",
        domain=LifeDomain.WEALTH,
        name="Income Increase",
        chinese_name="收入增加",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Metal", "Earth"]),
        pillar_weights={"month": 1.4, "day": 1.2, "year": 1.0, "hour": 0.8},
        common_patterns=frozenset([
            "SIX_HARMONIES~Chen-You~Metal",
            "STEM_COMBINATION~Yi-Geng~Metal",
        ]),
        description="Salary raise, bonus, or income growth"
    ),
    "income_decrease": EventType(
        id="income_decrease",
        domain=LifeDomain.WEALTH,
        name="Income Decrease",
        chinese_name="收入減少",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Metal", "Fire"]),
        pillar_weights={"month": 1.4, "day": 1.2, "year": 1.0, "hour": 0.8},
        common_patterns=frozenset([
            "STEM_CONFLICT~Bing-Geng~",
            "CLASH~Mao-You~opposite",
        ]),
        description="Salary cut or income loss"
    ),
    "investment_gain": EventType(
        id="investment_gain",
        domain=LifeDomain.WEALTH,
        name="Investment Gain",
        chinese_name="投資獲利",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Metal", "Water"]),
        pillar_weights={"month": 1.3, "year": 1.2, "day": 1.1, "hour": 0.9},
        description="Profit from investments"
    ),
    "investment_loss": EventType(
        id="investment_loss",
        domain=LifeDomain.WEALTH,
        name="Investment Loss",
        chinese_name="投資虧損",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MINOR, Severity.MODERATE, Severity.MAJOR, Severity.CRITICAL]),
        primary_elements=frozenset(["Metal", "Fire"]),
        pillar_weights={"month": 1.3, "year": 1.2, "day": 1.1, "hour": 0.9},
        common_patterns=frozenset([
            "STEM_CONFLICT~Bing-Geng~",
            "DESTRUCTION~Wei-Xu~",
        ]),
        description="Loss from investments"
    ),
    "property_purchase": EventType(
        id="property_purchase",
        domain=LifeDomain.WEALTH,
        name="Property Purchase",
        chinese_name="購置房產",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Earth"]),
        pillar_weights={"year": 1.4, "month": 1.2, "day": 1.0, "hour": 0.8},
        common_patterns=frozenset([
            "SIX_HARMONIES~Zi-Chou~Earth",
            "STEM_COMBINATION~Jia-Ji~Earth",
        ]),
        description="Buying real estate or property"
    ),
    "property_sale": EventType(
        id="property_sale",
        domain=LifeDomain.WEALTH,
        name="Property Sale",
        chinese_name="出售房產",
        default_sentiment=Sentiment.CONDITIONAL,
        severity_range=frozenset([Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Earth", "Metal"]),
        pillar_weights={"year": 1.3, "month": 1.2, "day": 1.0, "hour": 0.8},
        description="Selling real estate or property"
    ),
    "windfall": EventType(
        id="windfall",
        domain=LifeDomain.WEALTH,
        name="Windfall",
        chinese_name="橫財",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Water", "Metal"]),
        pillar_weights={"hour": 1.3, "day": 1.2, "month": 1.0, "year": 0.9},
        description="Unexpected financial gain (lottery, inheritance, etc.)"
    ),
    "bankruptcy": EventType(
        id="bankruptcy",
        domain=LifeDomain.WEALTH,
        name="Bankruptcy",
        chinese_name="破產",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.CRITICAL]),
        primary_elements=frozenset(["Metal", "Fire"]),
        pillar_weights={"month": 1.5, "year": 1.3, "day": 1.2, "hour": 0.8},
        common_patterns=frozenset([
            "STEM_CONFLICT~Bing-Geng~",
            "CLASH~Chen-Xu~same",
        ]),
        description="Financial ruin or bankruptcy"
    ),
}


# =============================================================================
# CAREER EVENTS
# =============================================================================

CAREER_EVENTS: Dict[str, EventType] = {
    "job_new": EventType(
        id="job_new",
        domain=LifeDomain.CAREER,
        name="New Job",
        chinese_name="新工作",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Wood", "Fire"]),
        pillar_weights={"month": 1.5, "day": 1.2, "year": 1.0, "hour": 0.8},
        common_patterns=frozenset([
            "THREE_MEETINGS~Yin-Mao-Chen~Wood",
            "STEM_COMBINATION~Ding-Ren~Wood",
        ]),
        description="Starting a new job or position"
    ),
    "job_loss": EventType(
        id="job_loss",
        domain=LifeDomain.CAREER,
        name="Job Loss",
        chinese_name="失業",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Metal", "Earth"]),
        pillar_weights={"month": 1.5, "day": 1.2, "year": 1.0, "hour": 0.8},
        common_patterns=frozenset([
            "CLASH~Yin-Shen~opposite",
            "PUNISHMENT~Yin-Si-Shen~shi_xing",
        ]),
        description="Losing employment"
    ),
    "promotion": EventType(
        id="promotion",
        domain=LifeDomain.CAREER,
        name="Promotion",
        chinese_name="升職",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Fire", "Wood"]),
        pillar_weights={"month": 1.5, "day": 1.2, "year": 1.1, "hour": 0.9},
        common_patterns=frozenset([
            "THREE_MEETINGS~Si-Wu-Wei~Fire",
            "STEM_COMBINATION~Wu-Gui~Fire",
        ]),
        description="Career advancement or promotion"
    ),
    "demotion": EventType(
        id="demotion",
        domain=LifeDomain.CAREER,
        name="Demotion",
        chinese_name="降職",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Fire", "Water"]),
        pillar_weights={"month": 1.5, "day": 1.2, "year": 1.0, "hour": 0.8},
        common_patterns=frozenset([
            "STEM_CONFLICT~Bing-Ren~",
            "HARM~Chou-Wu~",
        ]),
        description="Reduction in position or status"
    ),
    "business_start": EventType(
        id="business_start",
        domain=LifeDomain.CAREER,
        name="Start Business",
        chinese_name="創業",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MAJOR]),
        primary_elements=frozenset(["Wood", "Fire"]),
        pillar_weights={"day": 1.4, "month": 1.3, "year": 1.1, "hour": 1.0},
        description="Starting a new business venture"
    ),
    "business_close": EventType(
        id="business_close",
        domain=LifeDomain.CAREER,
        name="Close Business",
        chinese_name="結束經營",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MAJOR]),
        primary_elements=frozenset(["Metal", "Fire"]),
        pillar_weights={"day": 1.4, "month": 1.3, "year": 1.1, "hour": 1.0},
        description="Closing or failing a business"
    ),
    "recognition": EventType(
        id="recognition",
        domain=LifeDomain.CAREER,
        name="Recognition/Award",
        chinese_name="表彰",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Fire"]),
        pillar_weights={"month": 1.4, "day": 1.2, "year": 1.1, "hour": 0.9},
        common_patterns=frozenset([
            "THREE_MEETINGS~Si-Wu-Wei~Fire",
            "THREE_COMBINATIONS~Yin-Wu-Xu~Fire",
        ]),
        description="Public recognition, award, or honor"
    ),
}


# =============================================================================
# RELATIONSHIP EVENTS
# =============================================================================

RELATIONSHIP_EVENTS: Dict[str, EventType] = {
    "marriage": EventType(
        id="marriage",
        domain=LifeDomain.RELATIONSHIP,
        name="Marriage",
        chinese_name="結婚",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MAJOR]),
        primary_elements=frozenset(["Fire", "Earth"]),
        pillar_weights={"day": 1.6, "month": 1.2, "year": 1.0, "hour": 0.9},
        common_patterns=frozenset([
            "SIX_HARMONIES~Wu-Wei~Fire",
            "STEM_COMBINATION~Jia-Ji~Earth",
            "SIX_HARMONIES~Mao-Xu~Fire",
        ]),
        description="Getting married"
    ),
    "divorce": EventType(
        id="divorce",
        domain=LifeDomain.RELATIONSHIP,
        name="Divorce",
        chinese_name="離婚",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MAJOR]),
        primary_elements=frozenset(["Fire", "Water"]),
        pillar_weights={"day": 1.6, "month": 1.2, "year": 1.0, "hour": 0.8},
        common_patterns=frozenset([
            "CLASH~Zi-Wu~opposite",
            "PUNISHMENT~Zi-Mao~en_xing",
            "PUNISHMENT~Chou-Wei-Xu~wu_li_xing",
        ]),
        description="Marriage ending in divorce"
    ),
    "engagement": EventType(
        id="engagement",
        domain=LifeDomain.RELATIONSHIP,
        name="Engagement",
        chinese_name="訂婚",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MODERATE]),
        primary_elements=frozenset(["Fire", "Wood"]),
        pillar_weights={"day": 1.5, "month": 1.2, "year": 1.0, "hour": 0.9},
        description="Getting engaged to be married"
    ),
    "breakup": EventType(
        id="breakup",
        domain=LifeDomain.RELATIONSHIP,
        name="Breakup",
        chinese_name="分手",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Metal", "Wood"]),
        pillar_weights={"day": 1.5, "month": 1.1, "year": 0.9, "hour": 0.9},
        common_patterns=frozenset([
            "CLASH~Mao-You~opposite",
            "HARM~Zi-Wei~",
        ]),
        description="End of a romantic relationship"
    ),
    "new_relationship": EventType(
        id="new_relationship",
        domain=LifeDomain.RELATIONSHIP,
        name="New Relationship",
        chinese_name="新戀情",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MINOR, Severity.MODERATE]),
        primary_elements=frozenset(["Fire", "Wood"]),
        pillar_weights={"day": 1.4, "hour": 1.2, "month": 1.0, "year": 0.9},
        description="Starting a new romantic relationship"
    ),
    "conflict_partner": EventType(
        id="conflict_partner",
        domain=LifeDomain.RELATIONSHIP,
        name="Partner Conflict",
        chinese_name="伴侶衝突",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Fire", "Metal"]),
        pillar_weights={"day": 1.5, "month": 1.1, "year": 0.9, "hour": 1.0},
        common_patterns=frozenset([
            "PUNISHMENT~Chou-Wei-Xu~wu_li_xing",
            "HARM~You-Xu~",
        ]),
        description="Significant conflict with partner/spouse"
    ),
}


# =============================================================================
# EDUCATION EVENTS
# =============================================================================

EDUCATION_EVENTS: Dict[str, EventType] = {
    "enrollment": EventType(
        id="enrollment",
        domain=LifeDomain.EDUCATION,
        name="School Enrollment",
        chinese_name="入學",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MODERATE]),
        primary_elements=frozenset(["Wood", "Water"]),
        pillar_weights={"year": 1.3, "month": 1.2, "day": 1.0, "hour": 0.9},
        common_patterns=frozenset([
            "THREE_MEETINGS~Hai-Zi-Chou~Water",
            "SIX_HARMONIES~Yin-Hai~Wood",
        ]),
        description="Starting school or university"
    ),
    "graduation": EventType(
        id="graduation",
        domain=LifeDomain.EDUCATION,
        name="Graduation",
        chinese_name="畢業",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Fire", "Metal"]),
        pillar_weights={"year": 1.2, "month": 1.3, "day": 1.1, "hour": 0.9},
        description="Completing education and graduating"
    ),
    "exam_pass": EventType(
        id="exam_pass",
        domain=LifeDomain.EDUCATION,
        name="Pass Exam",
        chinese_name="考試通過",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Fire", "Water"]),
        pillar_weights={"month": 1.3, "day": 1.2, "year": 1.0, "hour": 1.0},
        description="Passing an important examination"
    ),
    "exam_fail": EventType(
        id="exam_fail",
        domain=LifeDomain.EDUCATION,
        name="Fail Exam",
        chinese_name="考試失敗",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MINOR, Severity.MODERATE]),
        primary_elements=frozenset(["Water", "Earth"]),
        pillar_weights={"month": 1.3, "day": 1.2, "year": 1.0, "hour": 1.0},
        common_patterns=frozenset([
            "STEM_CONFLICT~Wu-Ren~",
        ]),
        description="Failing an important examination"
    ),
}


# =============================================================================
# FAMILY EVENTS
# =============================================================================

FAMILY_EVENTS: Dict[str, EventType] = {
    "birth_child": EventType(
        id="birth_child",
        domain=LifeDomain.FAMILY,
        name="Child Birth",
        chinese_name="生子",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MAJOR]),
        primary_elements=frozenset(["Wood", "Fire"]),
        pillar_weights={"hour": 1.5, "day": 1.3, "month": 1.1, "year": 0.9},
        common_patterns=frozenset([
            "STEM_COMBINATION~Ding-Ren~Wood",
            "THREE_COMBINATIONS~Hai-Mao-Wei~Wood",
        ]),
        description="Birth of a child"
    ),
    "death_family": EventType(
        id="death_family",
        domain=LifeDomain.FAMILY,
        name="Family Death",
        chinese_name="喪親",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MAJOR, Severity.CRITICAL]),
        primary_elements=frozenset(["Metal", "Water"]),
        pillar_weights={"year": 1.4, "month": 1.2, "day": 1.1, "hour": 1.0},
        common_patterns=frozenset([
            "CLASH~Mao-You~opposite",
            "PUNISHMENT~Yin-Si-Shen~shi_xing",
        ]),
        description="Death of a family member"
    ),
    "parent_illness": EventType(
        id="parent_illness",
        domain=LifeDomain.FAMILY,
        name="Parent Illness",
        chinese_name="父母生病",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Metal", "Earth"]),
        pillar_weights={"year": 1.4, "month": 1.3, "day": 1.0, "hour": 0.8},
        description="Parent becoming seriously ill"
    ),
    "family_conflict": EventType(
        id="family_conflict",
        domain=LifeDomain.FAMILY,
        name="Family Conflict",
        chinese_name="家庭衝突",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Fire", "Metal"]),
        pillar_weights={"year": 1.3, "month": 1.2, "day": 1.1, "hour": 1.0},
        common_patterns=frozenset([
            "PUNISHMENT~Chou-Wei-Xu~wu_li_xing",
            "HARM~Zi-Wei~",
        ]),
        description="Significant family disagreement or conflict"
    ),
}


# =============================================================================
# LEGAL EVENTS
# =============================================================================

LEGAL_EVENTS: Dict[str, EventType] = {
    "lawsuit_filed": EventType(
        id="lawsuit_filed",
        domain=LifeDomain.LEGAL,
        name="Lawsuit Filed",
        chinese_name="訴訟",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Metal", "Fire"]),
        pillar_weights={"month": 1.4, "year": 1.2, "day": 1.1, "hour": 0.9},
        common_patterns=frozenset([
            "PUNISHMENT~Yin-Si-Shen~shi_xing",
            "CLASH~Mao-You~opposite",
        ]),
        description="Being involved in legal proceedings"
    ),
    "lawsuit_won": EventType(
        id="lawsuit_won",
        domain=LifeDomain.LEGAL,
        name="Lawsuit Won",
        chinese_name="勝訴",
        default_sentiment=Sentiment.POSITIVE,
        severity_range=frozenset([Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Metal", "Earth"]),
        pillar_weights={"month": 1.4, "year": 1.2, "day": 1.1, "hour": 0.9},
        description="Winning a legal case"
    ),
    "lawsuit_lost": EventType(
        id="lawsuit_lost",
        domain=LifeDomain.LEGAL,
        name="Lawsuit Lost",
        chinese_name="敗訴",
        default_sentiment=Sentiment.NEGATIVE,
        severity_range=frozenset([Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Metal", "Fire"]),
        pillar_weights={"month": 1.4, "year": 1.2, "day": 1.1, "hour": 0.9},
        description="Losing a legal case"
    ),
    "contract_signed": EventType(
        id="contract_signed",
        domain=LifeDomain.LEGAL,
        name="Contract Signed",
        chinese_name="簽約",
        default_sentiment=Sentiment.CONDITIONAL,
        severity_range=frozenset([Severity.MINOR, Severity.MODERATE, Severity.MAJOR]),
        primary_elements=frozenset(["Metal", "Earth"]),
        pillar_weights={"month": 1.3, "day": 1.2, "year": 1.0, "hour": 0.9},
        common_patterns=frozenset([
            "SIX_HARMONIES~Chen-You~Metal",
            "STEM_COMBINATION~Yi-Geng~Metal",
        ]),
        description="Signing an important contract"
    ),
}


# =============================================================================
# TRAVEL EVENTS
# =============================================================================

TRAVEL_EVENTS: Dict[str, EventType] = {
    "relocation_major": EventType(
        id="relocation_major",
        domain=LifeDomain.TRAVEL,
        name="Major Relocation",
        chinese_name="搬遷",
        default_sentiment=Sentiment.CONDITIONAL,
        severity_range=frozenset([Severity.MAJOR]),
        primary_elements=frozenset(["Water", "Wood"]),
        pillar_weights={"year": 1.3, "month": 1.2, "day": 1.1, "hour": 0.9},
        common_patterns=frozenset([
            "CLASH~Yin-Shen~opposite",
            "CLASH~Si-Hai~opposite",
        ]),
        description="Moving to a new city or country"
    ),
    "immigration": EventType(
        id="immigration",
        domain=LifeDomain.TRAVEL,
        name="Immigration",
        chinese_name="移民",
        default_sentiment=Sentiment.CONDITIONAL,
        severity_range=frozenset([Severity.MAJOR]),
        primary_elements=frozenset(["Water", "Metal"]),
        pillar_weights={"year": 1.4, "month": 1.2, "day": 1.0, "hour": 0.8},
        common_patterns=frozenset([
            "CLASH~Si-Hai~opposite",
            "THREE_COMBINATIONS~Shen-Zi-Chen~Water",
        ]),
        description="Immigration to another country"
    ),
}


# =============================================================================
# COMBINED EVENT REGISTRY
# =============================================================================

ALL_EVENT_TYPES: Dict[str, EventType] = {
    **HEALTH_EVENTS,
    **WEALTH_EVENTS,
    **CAREER_EVENTS,
    **RELATIONSHIP_EVENTS,
    **EDUCATION_EVENTS,
    **FAMILY_EVENTS,
    **LEGAL_EVENTS,
    **TRAVEL_EVENTS,
}


def get_events_by_domain(domain: LifeDomain) -> Dict[str, EventType]:
    """Get all event types for a specific domain."""
    return {k: v for k, v in ALL_EVENT_TYPES.items() if v.domain == domain}


def get_events_by_element(element: str) -> Dict[str, EventType]:
    """Get all event types associated with an element."""
    return {
        k: v for k, v in ALL_EVENT_TYPES.items()
        if element in v.primary_elements or element in v.secondary_elements
    }


def get_event_statistics() -> dict:
    """Get statistics about the event taxonomy."""
    by_domain = {}
    for event in ALL_EVENT_TYPES.values():
        dom = event.domain.value
        by_domain[dom] = by_domain.get(dom, 0) + 1

    by_sentiment = {}
    for event in ALL_EVENT_TYPES.values():
        sent = event.default_sentiment.value
        by_sentiment[sent] = by_sentiment.get(sent, 0) + 1

    return {
        "total_event_types": len(ALL_EVENT_TYPES),
        "by_domain": by_domain,
        "by_sentiment": by_sentiment,
        "with_pattern_correlations": sum(
            1 for e in ALL_EVENT_TYPES.values() if e.common_patterns
        ),
    }


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Enums
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

    # Functions
    "get_events_by_domain",
    "get_events_by_element",
    "get_event_statistics",
]
