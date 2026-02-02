# * =============================================================================
# * SPECIAL STARS PATTERNS (神煞 Shen Sha)
# * =============================================================================
# * Classical BaZi special stars expressed as PatternSpecs.
# * These are context-dependent patterns based on Day Master or Year Branch.
# * Includes: KONG_WANG, GUI_REN, TAO_HUA, YI_MA, YANG_REN, LU_SHEN, HUA_GAI
# * =============================================================================

from typing import List, Dict, FrozenSet

from ..pattern_spec import (
    PatternSpec,
    PatternCategory,
    NodeFilter,
    NodeType,
    TemporalRule,
    PillarMeaning,
    EventMapping,
    LifeDomain,
    BadgeType,
)


# =============================================================================
# KONG WANG (空亡) - Void/Empty Stars
# =============================================================================
# Each Jia-Zi decade has two "empty" branches where energy is void.
# Determined by Day Master's Jia-Zi pillar position.

# Lookup: Day Stem -> Empty Branches for that decade
KONG_WANG_LOOKUP: Dict[str, FrozenSet[str]] = {
    # Jia-Zi decade (pillars 1-10): Empty = Xu, Hai
    "Jia": frozenset(["Xu", "Hai"]),
    "Yi": frozenset(["Xu", "Hai"]),
    "Bing": frozenset(["Shen", "You"]),
    "Ding": frozenset(["Shen", "You"]),
    "Wu": frozenset(["Wu", "Wei"]),
    "Ji": frozenset(["Wu", "Wei"]),
    "Geng": frozenset(["Chen", "Si"]),
    "Xin": frozenset(["Chen", "Si"]),
    "Ren": frozenset(["Yin", "Mao"]),
    "Gui": frozenset(["Yin", "Mao"]),
}


def generate_kong_wang_patterns() -> List[PatternSpec]:
    """
    Generate Kong Wang patterns for all Day Stem → Empty Branch combinations.

    Kong Wang (空亡) indicates a void or emptiness in that branch's energy.
    Can manifest as:
    - Loss or absence in that pillar's domain
    - Unfulfilled potential
    - Spiritual/philosophical inclination
    """
    patterns = []

    for day_stem, empty_branches in KONG_WANG_LOOKUP.items():
        for branch in empty_branches:
            patterns.append(PatternSpec(
                id=f"KONG_WANG~{day_stem}~{branch}",
                category=PatternCategory.KONG_WANG,
                priority=300,
                chinese_name="空亡",
                english_name=f"Void Star ({branch})",
                node_filters=(
                    NodeFilter(
                        branches=frozenset([branch]),
                        node_types=frozenset([NodeType.EARTHLY_BRANCH])
                    ),
                ),
                min_nodes=1,
                base_score_combined=8.0,
                distance_multipliers=(1.0, 0.8, 0.6),
                badge_type=BadgeType.COMBINATION,
                life_domains=frozenset([LifeDomain.CAREER, LifeDomain.RELATIONSHIP, LifeDomain.FAMILY]),
                pillar_meanings=PillarMeaning(
                    year="Ancestral void - detachment from family legacy",
                    month="Career void - unconventional career path",
                    day="Spouse void - late marriage or unique partnership",
                    hour="Children void - fewer children or spiritual focus"
                ),
                description=f"Day Master {day_stem} has void in {branch} - emptiness in that domain",
                classical_source="三命通會",
                notes=f"Context-dependent: Only applies when Day Stem is {day_stem}",
            ))

    return patterns


KONG_WANG_PATTERNS = generate_kong_wang_patterns()


# =============================================================================
# GUI REN (貴人) - Noble Person Stars
# =============================================================================
# Based on Day Master, certain branches indicate noble helpers.

GUI_REN_LOOKUP: Dict[str, FrozenSet[str]] = {
    "Jia": frozenset(["Chou", "Wei"]),
    "Yi": frozenset(["Zi", "Shen"]),
    "Bing": frozenset(["Hai", "You"]),
    "Ding": frozenset(["Hai", "You"]),
    "Wu": frozenset(["Chou", "Wei"]),
    "Ji": frozenset(["Zi", "Shen"]),
    "Geng": frozenset(["Chou", "Wei"]),
    "Xin": frozenset(["Yin", "Wu"]),
    "Ren": frozenset(["Mao", "Si"]),
    "Gui": frozenset(["Mao", "Si"]),
}


def generate_gui_ren_patterns() -> List[PatternSpec]:
    """
    Generate Gui Ren (Noble Person) patterns.

    Gui Ren indicates presence of helpful people, benefactors, mentors.
    Very auspicious star for career and social advancement.
    """
    patterns = []

    for day_stem, noble_branches in GUI_REN_LOOKUP.items():
        for branch in noble_branches:
            patterns.append(PatternSpec(
                id=f"GUI_REN~{day_stem}~{branch}",
                category=PatternCategory.GUI_REN,
                priority=310,
                chinese_name="貴人",
                english_name=f"Noble Person ({branch})",
                node_filters=(
                    NodeFilter(
                        branches=frozenset([branch]),
                        node_types=frozenset([NodeType.EARTHLY_BRANCH])
                    ),
                ),
                min_nodes=1,
                base_score_combined=12.0,
                distance_multipliers=(1.0, 0.85, 0.7),
                badge_type=BadgeType.COMBINATION,
                life_domains=frozenset([LifeDomain.CAREER, LifeDomain.RELATIONSHIP, LifeDomain.WEALTH]),
                pillar_meanings=PillarMeaning(
                    year="Noble ancestry - helpful family connections",
                    month="Noble career - mentors and sponsors at work",
                    day="Noble partner - spouse brings good fortune",
                    hour="Noble children - children bring honor"
                ),
                event_mapping=EventMapping(
                    primary_domains=frozenset([LifeDomain.CAREER, LifeDomain.RELATIONSHIP]),
                    positive_events=(
                        ("career", "promotion"),
                        ("career", "recognition"),
                        ("relationship", "new_relationship"),
                        ("wealth", "windfall"),
                    ),
                    domain_sentiment=(
                        ("career", "positive"),
                        ("relationship", "positive"),
                        ("wealth", "positive"),
                    ),
                ),
                description=f"Day Master {day_stem} has noble person in {branch} - benefactors and helpers",
                classical_source="三命通會",
                notes=f"Context-dependent: Only applies when Day Stem is {day_stem}",
            ))

    return patterns


GUI_REN_PATTERNS = generate_gui_ren_patterns()


# =============================================================================
# TAO HUA (桃花) - Peach Blossom Stars
# =============================================================================
# Romance/attraction stars based on Year/Day Branch.

TAO_HUA_LOOKUP: Dict[str, str] = {
    # Based on Year or Day Branch -> Peach Blossom Branch
    "Yin": "Mao",
    "Wu": "Mao",
    "Xu": "Mao",
    "Shen": "You",
    "Zi": "You",
    "Chen": "You",
    "Si": "Wu",
    "You": "Wu",
    "Chou": "Wu",
    "Hai": "Zi",
    "Mao": "Zi",
    "Wei": "Zi",
}


def generate_tao_hua_patterns() -> List[PatternSpec]:
    """
    Generate Tao Hua (Peach Blossom) patterns.

    Tao Hua indicates romance, attraction, charisma.
    Can be positive (romance, popularity) or negative (affairs, scandal).
    """
    patterns = []

    for base_branch, peach_branch in TAO_HUA_LOOKUP.items():
        patterns.append(PatternSpec(
            id=f"TAO_HUA~{base_branch}~{peach_branch}",
            category=PatternCategory.TAO_HUA,
            priority=320,
            chinese_name="桃花",
            english_name=f"Peach Blossom ({peach_branch})",
            node_filters=(
                NodeFilter(
                    branches=frozenset([peach_branch]),
                    node_types=frozenset([NodeType.EARTHLY_BRANCH])
                ),
            ),
            min_nodes=1,
            base_score_combined=10.0,
            distance_multipliers=(1.0, 0.8, 0.6),
            badge_type=BadgeType.COMBINATION,
            life_domains=frozenset([LifeDomain.RELATIONSHIP, LifeDomain.CAREER]),
            pillar_meanings=PillarMeaning(
                year="Family romance karma - attractive lineage",
                month="Career charisma - popular at work",
                day="Personal charm - romantic nature",
                hour="Late life romance - continued attraction"
            ),
            event_mapping=EventMapping(
                primary_domains=frozenset([LifeDomain.RELATIONSHIP]),
                positive_events=(
                    ("relationship", "new_relationship"),
                    ("relationship", "marriage"),
                    ("career", "recognition"),
                ),
                negative_events=(
                    ("relationship", "breakup"),
                    ("relationship", "conflict_partner"),
                ),
                domain_sentiment=(
                    ("relationship", "conditional"),
                ),
            ),
            description=f"Year/Day Branch {base_branch} has Peach Blossom in {peach_branch} - romance and attraction",
            classical_source="三命通會",
            notes=f"Context-dependent: Only applies when Year or Day Branch is {base_branch}",
        ))

    return patterns


TAO_HUA_PATTERNS = generate_tao_hua_patterns()


# =============================================================================
# YI MA (驛馬) - Traveling Horse Stars
# =============================================================================
# Travel and movement stars based on Year/Day Branch.

YI_MA_LOOKUP: Dict[str, str] = {
    # Based on Year or Day Branch -> Travel Branch
    "Yin": "Shen",
    "Wu": "Shen",
    "Xu": "Shen",
    "Shen": "Yin",
    "Zi": "Yin",
    "Chen": "Yin",
    "Si": "Hai",
    "You": "Hai",
    "Chou": "Hai",
    "Hai": "Si",
    "Mao": "Si",
    "Wei": "Si",
}


def generate_yi_ma_patterns() -> List[PatternSpec]:
    """
    Generate Yi Ma (Traveling Horse) patterns.

    Yi Ma indicates travel, movement, relocation, change.
    Can manifest as physical travel or career/life changes.
    """
    patterns = []

    for base_branch, travel_branch in YI_MA_LOOKUP.items():
        patterns.append(PatternSpec(
            id=f"YI_MA~{base_branch}~{travel_branch}",
            category=PatternCategory.YI_MA,
            priority=330,
            chinese_name="驛馬",
            english_name=f"Traveling Horse ({travel_branch})",
            node_filters=(
                NodeFilter(
                    branches=frozenset([travel_branch]),
                    node_types=frozenset([NodeType.EARTHLY_BRANCH])
                ),
            ),
            min_nodes=1,
            base_score_combined=10.0,
            distance_multipliers=(1.0, 0.8, 0.6),
            badge_type=BadgeType.COMBINATION,
            life_domains=frozenset([LifeDomain.TRAVEL, LifeDomain.CAREER]),
            pillar_meanings=PillarMeaning(
                year="Ancestral travel - family immigration history",
                month="Career travel - work-related moves",
                day="Personal movement - restless nature",
                hour="Late life travel - retirement relocations"
            ),
            event_mapping=EventMapping(
                primary_domains=frozenset([LifeDomain.TRAVEL]),
                positive_events=(
                    ("travel", "relocation_major"),
                    ("travel", "immigration"),
                    ("career", "job_new"),
                ),
                domain_sentiment=(
                    ("travel", "conditional"),
                    ("career", "conditional"),
                ),
            ),
            description=f"Year/Day Branch {base_branch} has Travel Horse in {travel_branch} - movement and change",
            classical_source="三命通會",
            notes=f"Context-dependent: Only applies when Year or Day Branch is {base_branch}",
        ))

    return patterns


YI_MA_PATTERNS = generate_yi_ma_patterns()


# =============================================================================
# YANG REN (羊刃) - Yang Blade Stars
# =============================================================================
# Aggressive/cutting energy based on Day Master.

YANG_REN_LOOKUP: Dict[str, str] = {
    # Day Stem -> Yang Blade Branch
    "Jia": "Mao",
    "Bing": "Wu",
    "Wu": "Wu",
    "Geng": "You",
    "Ren": "Zi",
}


def generate_yang_ren_patterns() -> List[PatternSpec]:
    """
    Generate Yang Ren (Yang Blade) patterns.

    Yang Ren indicates aggressive energy, sharp/cutting nature.
    Can be powerful for action but dangerous if unchecked.
    Only applies to Yang Day Masters.
    """
    patterns = []

    for day_stem, blade_branch in YANG_REN_LOOKUP.items():
        patterns.append(PatternSpec(
            id=f"YANG_REN~{day_stem}~{blade_branch}",
            category=PatternCategory.YANG_REN,
            priority=340,
            chinese_name="羊刃",
            english_name=f"Yang Blade ({blade_branch})",
            node_filters=(
                NodeFilter(
                    branches=frozenset([blade_branch]),
                    node_types=frozenset([NodeType.EARTHLY_BRANCH])
                ),
            ),
            min_nodes=1,
            base_score_combined=12.0,
            distance_multipliers=(1.0, 0.85, 0.7),
            badge_type=BadgeType.CLASH,  # Aggressive nature
            life_domains=frozenset([LifeDomain.HEALTH, LifeDomain.CAREER, LifeDomain.LEGAL]),
            pillar_meanings=PillarMeaning(
                year="Ancestral blade - aggressive family nature",
                month="Career blade - competitive work environment",
                day="Personal blade - aggressive personality",
                hour="Late blade - sharp tongue in old age"
            ),
            event_mapping=EventMapping(
                primary_domains=frozenset([LifeDomain.HEALTH, LifeDomain.CAREER]),
                positive_events=(
                    ("career", "promotion"),
                    ("career", "business_start"),
                ),
                negative_events=(
                    ("health", "injury_accident"),
                    ("health", "surgery"),
                    ("legal", "lawsuit_filed"),
                ),
                domain_sentiment=(
                    ("health", "negative"),
                    ("career", "conditional"),
                    ("legal", "negative"),
                ),
            ),
            description=f"Day Master {day_stem} has Yang Blade in {blade_branch} - aggressive/cutting energy",
            classical_source="三命通會",
            notes=f"Context-dependent: Only applies when Day Stem is {day_stem} (Yang stems only)",
        ))

    return patterns


YANG_REN_PATTERNS = generate_yang_ren_patterns()


# =============================================================================
# LU SHEN (祿神) - Prosperity God Stars
# =============================================================================
# Self-prosperity based on Day Master.

LU_SHEN_LOOKUP: Dict[str, str] = {
    # Day Stem -> Prosperity Branch
    "Jia": "Yin",
    "Yi": "Mao",
    "Bing": "Si",
    "Ding": "Wu",
    "Wu": "Si",
    "Ji": "Wu",
    "Geng": "Shen",
    "Xin": "You",
    "Ren": "Hai",
    "Gui": "Zi",
}


def generate_lu_shen_patterns() -> List[PatternSpec]:
    """
    Generate Lu Shen (Prosperity God) patterns.

    Lu Shen indicates self-made prosperity, inherent wealth potential.
    Very auspicious for financial matters.
    """
    patterns = []

    for day_stem, prosperity_branch in LU_SHEN_LOOKUP.items():
        patterns.append(PatternSpec(
            id=f"LU_SHEN~{day_stem}~{prosperity_branch}",
            category=PatternCategory.LU_SHEN,
            priority=350,
            chinese_name="祿神",
            english_name=f"Prosperity God ({prosperity_branch})",
            node_filters=(
                NodeFilter(
                    branches=frozenset([prosperity_branch]),
                    node_types=frozenset([NodeType.EARTHLY_BRANCH])
                ),
            ),
            min_nodes=1,
            base_score_combined=12.0,
            distance_multipliers=(1.0, 0.85, 0.7),
            badge_type=BadgeType.COMBINATION,
            life_domains=frozenset([LifeDomain.WEALTH, LifeDomain.CAREER]),
            pillar_meanings=PillarMeaning(
                year="Ancestral prosperity - inherited wealth",
                month="Career prosperity - good salary",
                day="Personal prosperity - self-made wealth",
                hour="Late prosperity - comfortable retirement"
            ),
            event_mapping=EventMapping(
                primary_domains=frozenset([LifeDomain.WEALTH, LifeDomain.CAREER]),
                positive_events=(
                    ("wealth", "income_increase"),
                    ("wealth", "investment_gain"),
                    ("career", "promotion"),
                ),
                domain_sentiment=(
                    ("wealth", "positive"),
                    ("career", "positive"),
                ),
            ),
            description=f"Day Master {day_stem} has Prosperity God in {prosperity_branch} - self-made wealth",
            classical_source="三命通會",
            notes=f"Context-dependent: Only applies when Day Stem is {day_stem}",
        ))

    return patterns


LU_SHEN_PATTERNS = generate_lu_shen_patterns()


# =============================================================================
# HUA GAI (華蓋) - Canopy Stars
# =============================================================================
# Artistic/spiritual inclination based on Year/Day Branch.

HUA_GAI_LOOKUP: Dict[str, str] = {
    # Based on Year or Day Branch -> Canopy Branch
    "Yin": "Xu",
    "Wu": "Xu",
    "Xu": "Xu",
    "Shen": "Chen",
    "Zi": "Chen",
    "Chen": "Chen",
    "Si": "Chou",
    "You": "Chou",
    "Chou": "Chou",
    "Hai": "Wei",
    "Mao": "Wei",
    "Wei": "Wei",
}


def generate_hua_gai_patterns() -> List[PatternSpec]:
    """
    Generate Hua Gai (Canopy Star) patterns.

    Hua Gai indicates artistic, spiritual, or scholarly inclination.
    Can manifest as creativity, isolation, or religious interest.
    """
    patterns = []

    for base_branch, canopy_branch in HUA_GAI_LOOKUP.items():
        patterns.append(PatternSpec(
            id=f"HUA_GAI~{base_branch}~{canopy_branch}",
            category=PatternCategory.HUA_GAI,
            priority=360,
            chinese_name="華蓋",
            english_name=f"Canopy Star ({canopy_branch})",
            node_filters=(
                NodeFilter(
                    branches=frozenset([canopy_branch]),
                    node_types=frozenset([NodeType.EARTHLY_BRANCH])
                ),
            ),
            min_nodes=1,
            base_score_combined=8.0,
            distance_multipliers=(1.0, 0.8, 0.6),
            badge_type=BadgeType.COMBINATION,
            life_domains=frozenset([LifeDomain.EDUCATION, LifeDomain.CAREER]),
            pillar_meanings=PillarMeaning(
                year="Ancestral canopy - artistic/spiritual lineage",
                month="Career canopy - creative profession",
                day="Personal canopy - artistic/spiritual nature",
                hour="Late canopy - contemplative old age"
            ),
            event_mapping=EventMapping(
                primary_domains=frozenset([LifeDomain.EDUCATION]),
                positive_events=(
                    ("education", "certification"),
                    ("career", "recognition"),
                ),
                domain_sentiment=(
                    ("education", "positive"),
                    ("career", "positive"),
                ),
            ),
            description=f"Year/Day Branch {base_branch} has Canopy in {canopy_branch} - artistic/spiritual inclination",
            classical_source="三命通會",
            notes=f"Context-dependent: Only applies when Year or Day Branch is {base_branch}",
        ))

    return patterns


HUA_GAI_PATTERNS = generate_hua_gai_patterns()


# =============================================================================
# GU CHEN & GUA SU (孤辰寡宿) - Lonely and Widow Stars
# =============================================================================
# Critical for marriage analysis. Based on Year Branch.
# Gu Chen (孤辰) - Lonely Star - affects males more
# Gua Su (寡宿) - Widow Star - affects females more

GU_CHEN_GUA_SU_LOOKUP: Dict[str, Dict[str, str]] = {
    # Year Branch -> {"gu_chen": branch, "gua_su": branch}
    "Zi": {"gu_chen": "Yin", "gua_su": "Xu"},
    "Chou": {"gu_chen": "Yin", "gua_su": "Xu"},
    "Yin": {"gu_chen": "Si", "gua_su": "Chou"},
    "Mao": {"gu_chen": "Si", "gua_su": "Chou"},
    "Chen": {"gu_chen": "Si", "gua_su": "Chou"},
    "Si": {"gu_chen": "Shen", "gua_su": "Chen"},
    "Wu": {"gu_chen": "Shen", "gua_su": "Chen"},
    "Wei": {"gu_chen": "Shen", "gua_su": "Chen"},
    "Shen": {"gu_chen": "Hai", "gua_su": "Wei"},
    "You": {"gu_chen": "Hai", "gua_su": "Wei"},
    "Xu": {"gu_chen": "Hai", "gua_su": "Wei"},
    "Hai": {"gu_chen": "Yin", "gua_su": "Xu"},
}


def generate_gu_chen_patterns() -> List[PatternSpec]:
    """
    Generate Gu Chen (孤辰 Lonely Star) patterns.

    Gu Chen indicates:
    - Tendency toward isolation
    - Independence and self-reliance
    - Difficulty in relationships
    - In Spouse Palace: late marriage or solitary life
    - Affects males more significantly
    """
    patterns = []

    for year_branch, stars in GU_CHEN_GUA_SU_LOOKUP.items():
        lonely_branch = stars["gu_chen"]
        patterns.append(PatternSpec(
            id=f"GU_CHEN~{year_branch}~{lonely_branch}",
            category=PatternCategory.GU_CHEN,
            priority=370,
            chinese_name="孤辰",
            english_name=f"Lonely Star ({lonely_branch})",
            node_filters=(
                NodeFilter(
                    branches=frozenset([lonely_branch]),
                    node_types=frozenset([NodeType.EARTHLY_BRANCH])
                ),
            ),
            min_nodes=1,
            base_score_combined=10.0,
            distance_multipliers=(1.0, 0.85, 0.7),
            badge_type=BadgeType.CLASH,  # Negative connotation
            life_domains=frozenset([LifeDomain.RELATIONSHIP, LifeDomain.FAMILY]),
            pillar_meanings=PillarMeaning(
                year="Ancestral loneliness - isolated family history",
                month="Career loneliness - works alone, independent",
                day="Personal loneliness - difficulty finding/keeping spouse",
                hour="Late loneliness - solitary in old age"
            ),
            event_mapping=EventMapping(
                primary_domains=frozenset([LifeDomain.RELATIONSHIP]),
                negative_events=(
                    ("relationship", "breakup"),
                    ("relationship", "divorce"),
                    ("family", "separation"),
                ),
                domain_sentiment=(
                    ("relationship", "negative"),
                    ("family", "negative"),
                ),
            ),
            description=f"Year Branch {year_branch} has Lonely Star in {lonely_branch} - isolation tendency",
            classical_source="三命通會",
            notes=f"Context-dependent: Only applies when Year Branch is {year_branch}. In Spouse Palace indicates marriage difficulty.",
        ))

    return patterns


def generate_gua_su_patterns() -> List[PatternSpec]:
    """
    Generate Gua Su (寡宿 Widow Star) patterns.

    Gua Su indicates:
    - Tendency toward solitude
    - Self-reliance, independence
    - Potential for loss of partner
    - In Spouse Palace: widowhood risk or very late marriage
    - Affects females more significantly
    """
    patterns = []

    for year_branch, stars in GU_CHEN_GUA_SU_LOOKUP.items():
        widow_branch = stars["gua_su"]
        patterns.append(PatternSpec(
            id=f"GUA_SU~{year_branch}~{widow_branch}",
            category=PatternCategory.GUA_SU,
            priority=375,
            chinese_name="寡宿",
            english_name=f"Widow Star ({widow_branch})",
            node_filters=(
                NodeFilter(
                    branches=frozenset([widow_branch]),
                    node_types=frozenset([NodeType.EARTHLY_BRANCH])
                ),
            ),
            min_nodes=1,
            base_score_combined=10.0,
            distance_multipliers=(1.0, 0.85, 0.7),
            badge_type=BadgeType.CLASH,  # Negative connotation
            life_domains=frozenset([LifeDomain.RELATIONSHIP, LifeDomain.FAMILY]),
            pillar_meanings=PillarMeaning(
                year="Ancestral widow - widowhood in family history",
                month="Career solitude - professional independence",
                day="Personal widow - risk of losing partner or no marriage",
                hour="Late solitude - alone in old age"
            ),
            event_mapping=EventMapping(
                primary_domains=frozenset([LifeDomain.RELATIONSHIP]),
                negative_events=(
                    ("relationship", "breakup"),
                    ("relationship", "divorce"),
                    ("family", "loss_death"),
                ),
                domain_sentiment=(
                    ("relationship", "negative"),
                    ("family", "negative"),
                ),
            ),
            description=f"Year Branch {year_branch} has Widow Star in {widow_branch} - solitude tendency",
            classical_source="三命通會",
            notes=f"Context-dependent: Only applies when Year Branch is {year_branch}. In Spouse Palace indicates widowhood risk.",
        ))

    return patterns


GU_CHEN_PATTERNS = generate_gu_chen_patterns()
GUA_SU_PATTERNS = generate_gua_su_patterns()


# =============================================================================
# COMBINED EXPORT
# =============================================================================

ALL_SPECIAL_STAR_PATTERNS: List[PatternSpec] = (
    KONG_WANG_PATTERNS +
    GUI_REN_PATTERNS +
    TAO_HUA_PATTERNS +
    YI_MA_PATTERNS +
    YANG_REN_PATTERNS +
    LU_SHEN_PATTERNS +
    HUA_GAI_PATTERNS +
    GU_CHEN_PATTERNS +
    GUA_SU_PATTERNS
)


def get_all_special_star_patterns() -> List[PatternSpec]:
    """Get all special star patterns."""
    return ALL_SPECIAL_STAR_PATTERNS.copy()


def get_special_stars_for_day_master(day_stem: str) -> List[PatternSpec]:
    """Get special star patterns applicable to a specific Day Master."""
    applicable = []

    # Kong Wang
    if day_stem in KONG_WANG_LOOKUP:
        for branch in KONG_WANG_LOOKUP[day_stem]:
            applicable.extend([p for p in KONG_WANG_PATTERNS if f"~{day_stem}~{branch}" in p.id])

    # Gui Ren
    if day_stem in GUI_REN_LOOKUP:
        for branch in GUI_REN_LOOKUP[day_stem]:
            applicable.extend([p for p in GUI_REN_PATTERNS if f"~{day_stem}~{branch}" in p.id])

    # Yang Ren (only Yang stems)
    if day_stem in YANG_REN_LOOKUP:
        branch = YANG_REN_LOOKUP[day_stem]
        applicable.extend([p for p in YANG_REN_PATTERNS if f"~{day_stem}~{branch}" in p.id])

    # Lu Shen
    if day_stem in LU_SHEN_LOOKUP:
        branch = LU_SHEN_LOOKUP[day_stem]
        applicable.extend([p for p in LU_SHEN_PATTERNS if f"~{day_stem}~{branch}" in p.id])

    return applicable


def get_special_stars_for_year_branch(year_branch: str) -> List[PatternSpec]:
    """
    Get special star patterns applicable to a specific Year Branch.

    These are context-dependent stars that only apply when the Year Branch
    matches the pattern's requirement.

    Year Branch-dependent stars:
    - Gu Chen (孤辰 Lonely Star)
    - Gua Su (寡宿 Widow Star)
    - Hua Gai (华盖 Imperial Canopy)
    - Tao Hua (桃花 Peach Blossom)
    - Yi Ma (驿马 Travel Horse)
    """
    applicable = []

    # Gu Chen (Lonely Star) - based on Year Branch
    if year_branch in GU_CHEN_GUA_SU_LOOKUP:
        lonely_branch = GU_CHEN_GUA_SU_LOOKUP[year_branch]["gu_chen"]
        applicable.extend([
            p for p in GU_CHEN_PATTERNS
            if f"~{year_branch}~{lonely_branch}" in p.id
        ])

    # Gua Su (Widow Star) - based on Year Branch
    if year_branch in GU_CHEN_GUA_SU_LOOKUP:
        widow_branch = GU_CHEN_GUA_SU_LOOKUP[year_branch]["gua_su"]
        applicable.extend([
            p for p in GUA_SU_PATTERNS
            if f"~{year_branch}~{widow_branch}" in p.id
        ])

    # Hua Gai (Imperial Canopy) - based on Year Branch
    if year_branch in HUA_GAI_LOOKUP:
        canopy_branch = HUA_GAI_LOOKUP[year_branch]
        applicable.extend([
            p for p in HUA_GAI_PATTERNS
            if f"~{year_branch}~{canopy_branch}" in p.id
        ])

    # Tao Hua (Peach Blossom) - based on Year Branch
    if year_branch in TAO_HUA_LOOKUP:
        peach_branch = TAO_HUA_LOOKUP[year_branch]
        applicable.extend([
            p for p in TAO_HUA_PATTERNS
            if f"~{year_branch}~{peach_branch}" in p.id
        ])

    # Yi Ma (Travel Horse) - based on Year Branch
    if year_branch in YI_MA_LOOKUP:
        horse_branch = YI_MA_LOOKUP[year_branch]
        applicable.extend([
            p for p in YI_MA_PATTERNS
            if f"~{year_branch}~{horse_branch}" in p.id
        ])

    return applicable


__all__ = [
    # Lookups
    "KONG_WANG_LOOKUP",
    "GUI_REN_LOOKUP",
    "TAO_HUA_LOOKUP",
    "YI_MA_LOOKUP",
    "YANG_REN_LOOKUP",
    "LU_SHEN_LOOKUP",
    "HUA_GAI_LOOKUP",
    "GU_CHEN_GUA_SU_LOOKUP",

    # Pattern lists
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

    # Functions
    "get_all_special_star_patterns",
    "get_special_stars_for_day_master",
    "get_special_stars_for_year_branch",
]
