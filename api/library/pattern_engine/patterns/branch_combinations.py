# * =============================================================================
# * BRANCH COMBINATION PATTERNS (Declarative Format)
# * =============================================================================
# * All positive Earthly Branch combinations expressed as PatternSpecs.
# * Includes: THREE_MEETINGS, THREE_COMBINATIONS, SIX_HARMONIES, HALF_MEETINGS,
# *           HALF_COMBINATIONS, ARCHED_COMBINATIONS
# * =============================================================================

from typing import List

from ..pattern_spec import (
    PatternSpec,
    PatternCategory,
    NodeFilter,
    NodeType,
    SpatialRule,
    TemporalRule,
    TransformSpec,
    QiEffect,
    PillarMeaning,
    EventMapping,
    LifeDomain,
    BadgeType,
)


# =============================================================================
# THREE MEETINGS (三會方局) - Seasonal Directional Combinations
# =============================================================================
# Three consecutive branches from the same season combine into pure element.
# Strongest transformation type.

THREE_MEETINGS_PATTERNS: List[PatternSpec] = [
    # Spring/Wood: Yin-Mao-Chen (寅卯辰)
    PatternSpec(
        id="THREE_MEETINGS~Yin-Mao-Chen~Wood",
        category=PatternCategory.THREE_MEETINGS,
        priority=100,
        chinese_name="三會木局",
        english_name="Spring Wood Meeting",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Yin", "Mao", "Chen"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=3,
        transformation=TransformSpec(
            resulting_element="Wood",
            requires_element_support=True,
            supporting_elements=frozenset(["Wood"]),
            use_branch_polarity=True,
        ),
        base_score_combined=20.0,
        base_score_transformed=30.0,
        distance_multipliers=(1.0, 0.9, 0.7),
        qi_effects=(
            QiEffect(target="all", qi_change=15.0, is_percentage=False),
        ),
        badge_type=BadgeType.TRANSFORMATION,
        life_domains=frozenset([LifeDomain.CAREER, LifeDomain.HEALTH, LifeDomain.EDUCATION]),
        pillar_meanings=PillarMeaning(
            year="Ancestral Wood qi blessing, early growth supported",
            month="Career advancement through growth and expansion",
            day="Personal transformation, new beginnings",
            hour="Children's creativity and growth potential"
        ),
        description="Spring branches unite creating pure Wood energy - growth and expansion",
        classical_source="三命通會",
    ),

    # Summer/Fire: Si-Wu-Wei (巳午未)
    PatternSpec(
        id="THREE_MEETINGS~Si-Wu-Wei~Fire",
        category=PatternCategory.THREE_MEETINGS,
        priority=100,
        chinese_name="三會火局",
        english_name="Summer Fire Meeting",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Si", "Wu", "Wei"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=3,
        transformation=TransformSpec(
            resulting_element="Fire",
            requires_element_support=True,
            supporting_elements=frozenset(["Fire"]),
            use_branch_polarity=True,
        ),
        base_score_combined=20.0,
        base_score_transformed=30.0,
        distance_multipliers=(1.0, 0.9, 0.7),
        qi_effects=(
            QiEffect(target="all", qi_change=15.0, is_percentage=False),
        ),
        badge_type=BadgeType.TRANSFORMATION,
        life_domains=frozenset([LifeDomain.CAREER, LifeDomain.WEALTH, LifeDomain.RELATIONSHIP]),
        pillar_meanings=PillarMeaning(
            year="Family reputation and fame, ancestral passion",
            month="Public recognition, career breakthrough",
            day="Personal charisma, passionate relationships",
            hour="Legacy through creativity, children's achievements"
        ),
        description="Summer branches unite creating pure Fire energy - passion and recognition",
        classical_source="三命通會",
    ),

    # Autumn/Metal: Shen-You-Xu (申酉戌)
    PatternSpec(
        id="THREE_MEETINGS~Shen-You-Xu~Metal",
        category=PatternCategory.THREE_MEETINGS,
        priority=100,
        chinese_name="三會金局",
        english_name="Autumn Metal Meeting",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Shen", "You", "Xu"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=3,
        transformation=TransformSpec(
            resulting_element="Metal",
            requires_element_support=True,
            supporting_elements=frozenset(["Metal"]),
            use_branch_polarity=True,
        ),
        base_score_combined=20.0,
        base_score_transformed=30.0,
        distance_multipliers=(1.0, 0.9, 0.7),
        qi_effects=(
            QiEffect(target="all", qi_change=15.0, is_percentage=False),
        ),
        badge_type=BadgeType.TRANSFORMATION,
        life_domains=frozenset([LifeDomain.WEALTH, LifeDomain.LEGAL, LifeDomain.CAREER]),
        pillar_meanings=PillarMeaning(
            year="Ancestral wealth, inherited discipline",
            month="Career structure, authority position",
            day="Personal integrity, decisive nature",
            hour="Children's discipline, retirement security"
        ),
        description="Autumn branches unite creating pure Metal energy - structure and wealth",
        classical_source="三命通會",
    ),

    # Winter/Water: Hai-Zi-Chou (亥子丑)
    PatternSpec(
        id="THREE_MEETINGS~Hai-Zi-Chou~Water",
        category=PatternCategory.THREE_MEETINGS,
        priority=100,
        chinese_name="三會水局",
        english_name="Winter Water Meeting",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Hai", "Zi", "Chou"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=3,
        transformation=TransformSpec(
            resulting_element="Water",
            requires_element_support=True,
            supporting_elements=frozenset(["Water"]),
            use_branch_polarity=True,
        ),
        base_score_combined=20.0,
        base_score_transformed=30.0,
        distance_multipliers=(1.0, 0.9, 0.7),
        qi_effects=(
            QiEffect(target="all", qi_change=15.0, is_percentage=False),
        ),
        badge_type=BadgeType.TRANSFORMATION,
        life_domains=frozenset([LifeDomain.EDUCATION, LifeDomain.HEALTH, LifeDomain.TRAVEL]),
        pillar_meanings=PillarMeaning(
            year="Ancestral wisdom, inherited intelligence",
            month="Academic achievement, career through knowledge",
            day="Personal wisdom, emotional depth",
            hour="Children's education, retirement contemplation"
        ),
        description="Winter branches unite creating pure Water energy - wisdom and flow",
        classical_source="三命通會",
    ),
]


# =============================================================================
# THREE COMBINATIONS (三合局) - Triangular Combinations
# =============================================================================
# Three branches forming a triangle on the zodiac combine into element.

THREE_COMBINATIONS_PATTERNS: List[PatternSpec] = [
    # Water Frame: Shen-Zi-Chen (申子辰)
    PatternSpec(
        id="THREE_COMBINATIONS~Shen-Zi-Chen~Water",
        category=PatternCategory.THREE_COMBINATIONS,
        priority=110,
        chinese_name="三合水局",
        english_name="Water Triangle",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Shen", "Zi", "Chen"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=3,
        transformation=TransformSpec(
            resulting_element="Water",
            requires_element_support=True,
            supporting_elements=frozenset(["Water"]),
            use_branch_polarity=True,
        ),
        base_score_combined=18.0,
        base_score_transformed=25.0,
        distance_multipliers=(1.0, 0.85, 0.65),
        qi_effects=(
            QiEffect(target="all", qi_change=12.0, is_percentage=False),
        ),
        badge_type=BadgeType.TRANSFORMATION,
        life_domains=frozenset([LifeDomain.EDUCATION, LifeDomain.CAREER, LifeDomain.TRAVEL]),
        pillar_meanings=PillarMeaning(
            year="Wisdom inheritance, adaptable early life",
            month="Career through intelligence, fluid success",
            day="Personal adaptability, emotional intelligence",
            hour="Children's academic success"
        ),
        description="Triangular Water combination - adaptability and intelligence",
        classical_source="三命通會",
    ),

    # Wood Frame: Hai-Mao-Wei (亥卯未)
    PatternSpec(
        id="THREE_COMBINATIONS~Hai-Mao-Wei~Wood",
        category=PatternCategory.THREE_COMBINATIONS,
        priority=110,
        chinese_name="三合木局",
        english_name="Wood Triangle",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Hai", "Mao", "Wei"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=3,
        transformation=TransformSpec(
            resulting_element="Wood",
            requires_element_support=True,
            supporting_elements=frozenset(["Wood"]),
            use_branch_polarity=True,
        ),
        base_score_combined=18.0,
        base_score_transformed=25.0,
        distance_multipliers=(1.0, 0.85, 0.65),
        qi_effects=(
            QiEffect(target="all", qi_change=12.0, is_percentage=False),
        ),
        badge_type=BadgeType.TRANSFORMATION,
        life_domains=frozenset([LifeDomain.HEALTH, LifeDomain.EDUCATION, LifeDomain.FAMILY]),
        pillar_meanings=PillarMeaning(
            year="Growth-oriented ancestry, benevolent family",
            month="Career growth, compassionate leadership",
            day="Personal growth, kindness",
            hour="Children's development, nurturing legacy"
        ),
        description="Triangular Wood combination - growth and benevolence",
        classical_source="三命通會",
    ),

    # Fire Frame: Yin-Wu-Xu (寅午戌)
    PatternSpec(
        id="THREE_COMBINATIONS~Yin-Wu-Xu~Fire",
        category=PatternCategory.THREE_COMBINATIONS,
        priority=110,
        chinese_name="三合火局",
        english_name="Fire Triangle",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Yin", "Wu", "Xu"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=3,
        transformation=TransformSpec(
            resulting_element="Fire",
            requires_element_support=True,
            supporting_elements=frozenset(["Fire"]),
            use_branch_polarity=True,
        ),
        base_score_combined=18.0,
        base_score_transformed=25.0,
        distance_multipliers=(1.0, 0.85, 0.65),
        qi_effects=(
            QiEffect(target="all", qi_change=12.0, is_percentage=False),
        ),
        badge_type=BadgeType.TRANSFORMATION,
        life_domains=frozenset([LifeDomain.CAREER, LifeDomain.RELATIONSHIP, LifeDomain.WEALTH]),
        pillar_meanings=PillarMeaning(
            year="Passionate heritage, famous lineage",
            month="Career recognition, leadership",
            day="Personal passion, charismatic",
            hour="Children's fame, inspiring legacy"
        ),
        description="Triangular Fire combination - passion and fame",
        classical_source="三命通會",
    ),

    # Metal Frame: Si-You-Chou (巳酉丑)
    PatternSpec(
        id="THREE_COMBINATIONS~Si-You-Chou~Metal",
        category=PatternCategory.THREE_COMBINATIONS,
        priority=110,
        chinese_name="三合金局",
        english_name="Metal Triangle",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Si", "You", "Chou"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=3,
        transformation=TransformSpec(
            resulting_element="Metal",
            requires_element_support=True,
            supporting_elements=frozenset(["Metal"]),
            use_branch_polarity=True,
        ),
        base_score_combined=18.0,
        base_score_transformed=25.0,
        distance_multipliers=(1.0, 0.85, 0.65),
        qi_effects=(
            QiEffect(target="all", qi_change=12.0, is_percentage=False),
        ),
        badge_type=BadgeType.TRANSFORMATION,
        life_domains=frozenset([LifeDomain.WEALTH, LifeDomain.LEGAL, LifeDomain.CAREER]),
        pillar_meanings=PillarMeaning(
            year="Wealthy heritage, disciplined upbringing",
            month="Career authority, financial success",
            day="Personal integrity, decisive",
            hour="Children's discipline, secure legacy"
        ),
        description="Triangular Metal combination - wealth and integrity",
        classical_source="三命通會",
    ),
]


# =============================================================================
# SIX HARMONIES (六合) - Pair Combinations
# =============================================================================
# Adjacent zodiac pairs that harmonize into elements.

SIX_HARMONIES_PATTERNS: List[PatternSpec] = [
    # Zi-Chou → Earth
    PatternSpec(
        id="SIX_HARMONIES~Zi-Chou~Earth",
        category=PatternCategory.SIX_HARMONIES,
        priority=120,
        chinese_name="子丑合土",
        english_name="Rat-Ox Harmony (Earth)",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Zi", "Chou"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        transformation=TransformSpec(
            resulting_element="Earth",
            requires_element_support=True,
            supporting_elements=frozenset(["Earth"]),
            use_branch_polarity=True,
        ),
        base_score_combined=12.0,
        base_score_transformed=18.0,
        distance_multipliers=(1.0, 0.8, 0.6),
        badge_type=BadgeType.TRANSFORMATION,
        life_domains=frozenset([LifeDomain.RELATIONSHIP, LifeDomain.FAMILY, LifeDomain.CAREER]),
        pillar_meanings=PillarMeaning(
            year="Stable family foundation",
            month="Career stability through partnership",
            day="Harmonious marriage, grounded self",
            hour="Children's security"
        ),
        description="Water meets Earth storage - grounding and stability",
        classical_source="三命通會",
    ),

    # Yin-Hai → Wood
    PatternSpec(
        id="SIX_HARMONIES~Yin-Hai~Wood",
        category=PatternCategory.SIX_HARMONIES,
        priority=120,
        chinese_name="寅亥合木",
        english_name="Tiger-Pig Harmony (Wood)",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Yin", "Hai"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        transformation=TransformSpec(
            resulting_element="Wood",
            requires_element_support=True,
            supporting_elements=frozenset(["Wood"]),
            use_branch_polarity=True,
        ),
        base_score_combined=12.0,
        base_score_transformed=18.0,
        distance_multipliers=(1.0, 0.8, 0.6),
        badge_type=BadgeType.TRANSFORMATION,
        life_domains=frozenset([LifeDomain.HEALTH, LifeDomain.EDUCATION, LifeDomain.CAREER]),
        pillar_meanings=PillarMeaning(
            year="Growth-oriented upbringing",
            month="Career expansion",
            day="Personal growth through partnership",
            hour="Children's development"
        ),
        description="Wood Tiger meets Water Pig - nurturing growth",
        classical_source="三命通會",
    ),

    # Mao-Xu → Fire
    PatternSpec(
        id="SIX_HARMONIES~Mao-Xu~Fire",
        category=PatternCategory.SIX_HARMONIES,
        priority=120,
        chinese_name="卯戌合火",
        english_name="Rabbit-Dog Harmony (Fire)",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Mao", "Xu"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        transformation=TransformSpec(
            resulting_element="Fire",
            requires_element_support=True,
            supporting_elements=frozenset(["Fire"]),
            use_branch_polarity=True,
        ),
        base_score_combined=12.0,
        base_score_transformed=18.0,
        distance_multipliers=(1.0, 0.8, 0.6),
        badge_type=BadgeType.TRANSFORMATION,
        life_domains=frozenset([LifeDomain.RELATIONSHIP, LifeDomain.CAREER, LifeDomain.WEALTH]),
        pillar_meanings=PillarMeaning(
            year="Passionate family dynamics",
            month="Recognition through partnership",
            day="Romantic passion, warm relationships",
            hour="Children's warmth"
        ),
        description="Wood Rabbit meets Earth Dog - creating Fire passion",
        classical_source="三命通會",
    ),

    # Chen-You → Metal
    PatternSpec(
        id="SIX_HARMONIES~Chen-You~Metal",
        category=PatternCategory.SIX_HARMONIES,
        priority=120,
        chinese_name="辰酉合金",
        english_name="Dragon-Rooster Harmony (Metal)",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Chen", "You"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        transformation=TransformSpec(
            resulting_element="Metal",
            requires_element_support=True,
            supporting_elements=frozenset(["Metal"]),
            use_branch_polarity=True,
        ),
        base_score_combined=12.0,
        base_score_transformed=18.0,
        distance_multipliers=(1.0, 0.8, 0.6),
        badge_type=BadgeType.TRANSFORMATION,
        life_domains=frozenset([LifeDomain.WEALTH, LifeDomain.CAREER, LifeDomain.LEGAL]),
        pillar_meanings=PillarMeaning(
            year="Wealthy heritage through discipline",
            month="Career through precision",
            day="Wealth through partnership",
            hour="Children's financial acumen"
        ),
        description="Earth Dragon meets Metal Rooster - refining wealth",
        classical_source="三命通會",
    ),

    # Si-Shen → Water
    PatternSpec(
        id="SIX_HARMONIES~Si-Shen~Water",
        category=PatternCategory.SIX_HARMONIES,
        priority=120,
        chinese_name="巳申合水",
        english_name="Snake-Monkey Harmony (Water)",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Si", "Shen"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        transformation=TransformSpec(
            resulting_element="Water",
            requires_element_support=True,
            supporting_elements=frozenset(["Water"]),
            use_branch_polarity=True,
        ),
        base_score_combined=12.0,
        base_score_transformed=18.0,
        distance_multipliers=(1.0, 0.8, 0.6),
        badge_type=BadgeType.TRANSFORMATION,
        life_domains=frozenset([LifeDomain.EDUCATION, LifeDomain.TRAVEL, LifeDomain.CAREER]),
        pillar_meanings=PillarMeaning(
            year="Intelligent upbringing",
            month="Career through cleverness",
            day="Adaptive partnerships",
            hour="Children's wit"
        ),
        description="Fire Snake meets Metal Monkey - generating Water wisdom",
        classical_source="三命通會",
    ),

    # Wu-Wei → Fire (sometimes Earth)
    PatternSpec(
        id="SIX_HARMONIES~Wu-Wei~Fire",
        category=PatternCategory.SIX_HARMONIES,
        priority=120,
        chinese_name="午未合火",
        english_name="Horse-Goat Harmony (Fire)",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Wu", "Wei"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        transformation=TransformSpec(
            resulting_element="Fire",
            requires_element_support=True,
            supporting_elements=frozenset(["Fire"]),
            use_branch_polarity=True,
        ),
        base_score_combined=12.0,
        base_score_transformed=18.0,
        distance_multipliers=(1.0, 0.8, 0.6),
        badge_type=BadgeType.TRANSFORMATION,
        life_domains=frozenset([LifeDomain.RELATIONSHIP, LifeDomain.CAREER, LifeDomain.FAMILY]),
        pillar_meanings=PillarMeaning(
            year="Warm family atmosphere",
            month="Career recognition through warmth",
            day="Passionate relationships, heart connection",
            hour="Nurturing children"
        ),
        description="Fire Horse meets Earth Goat - sustained warmth",
        classical_source="三命通會",
    ),
]


# =============================================================================
# HALF MEETINGS (半會) - Partial Seasonal Combinations
# =============================================================================
# Two branches from THREE_MEETINGS with Earth storage branch present.

HALF_MEETINGS_PATTERNS: List[PatternSpec] = [
    # Winter/Water - Hai-Chou (missing Zi)
    PatternSpec(
        id="HALF_MEETINGS~Hai-Chou~Water",
        category=PatternCategory.HALF_MEETINGS,
        priority=130,
        chinese_name="半會水局",
        english_name="Half Water Meeting",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Hai", "Chou"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        transformation=TransformSpec(
            resulting_element="Water",
            requires_element_support=True,
            supporting_elements=frozenset(["Water"]),
            use_branch_polarity=True,
            base_score_multiplier=0.7,
        ),
        base_score_combined=10.0,
        base_score_transformed=14.0,
        distance_multipliers=(1.0, 0.75, 0.5),
        badge_type=BadgeType.COMBINATION,
        life_domains=frozenset([LifeDomain.EDUCATION, LifeDomain.TRAVEL]),
        description="Partial Winter meeting - Water potential",
        notes="Missing Zi, storage branch Chou present",
    ),

    # Spring/Wood - Yin-Chen (missing Mao)
    PatternSpec(
        id="HALF_MEETINGS~Yin-Chen~Wood",
        category=PatternCategory.HALF_MEETINGS,
        priority=130,
        chinese_name="半會木局",
        english_name="Half Wood Meeting (Yin-Chen)",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Yin", "Chen"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        transformation=TransformSpec(
            resulting_element="Wood",
            requires_element_support=True,
            supporting_elements=frozenset(["Wood"]),
            use_branch_polarity=True,
            base_score_multiplier=0.7,
        ),
        base_score_combined=10.0,
        base_score_transformed=14.0,
        distance_multipliers=(1.0, 0.75, 0.5),
        badge_type=BadgeType.COMBINATION,
        life_domains=frozenset([LifeDomain.HEALTH, LifeDomain.EDUCATION]),
        description="Partial Spring meeting - Wood potential",
        notes="Missing Mao, storage branch Chen present",
    ),

    # Spring/Wood - Mao-Chen (missing Yin)
    PatternSpec(
        id="HALF_MEETINGS~Mao-Chen~Wood",
        category=PatternCategory.HALF_MEETINGS,
        priority=130,
        chinese_name="半會木局",
        english_name="Half Wood Meeting (Mao-Chen)",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Mao", "Chen"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        transformation=TransformSpec(
            resulting_element="Wood",
            requires_element_support=True,
            supporting_elements=frozenset(["Wood"]),
            use_branch_polarity=True,
            base_score_multiplier=0.7,
        ),
        base_score_combined=10.0,
        base_score_transformed=14.0,
        distance_multipliers=(1.0, 0.75, 0.5),
        badge_type=BadgeType.COMBINATION,
        life_domains=frozenset([LifeDomain.HEALTH, LifeDomain.EDUCATION]),
        description="Partial Spring meeting - Wood potential",
        notes="Missing Yin, storage branch Chen present",
    ),

    # Summer/Fire - Si-Wei (missing Wu)
    PatternSpec(
        id="HALF_MEETINGS~Si-Wei~Fire",
        category=PatternCategory.HALF_MEETINGS,
        priority=130,
        chinese_name="半會火局",
        english_name="Half Fire Meeting",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Si", "Wei"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        transformation=TransformSpec(
            resulting_element="Fire",
            requires_element_support=True,
            supporting_elements=frozenset(["Fire"]),
            use_branch_polarity=True,
            base_score_multiplier=0.7,
        ),
        base_score_combined=10.0,
        base_score_transformed=14.0,
        distance_multipliers=(1.0, 0.75, 0.5),
        badge_type=BadgeType.COMBINATION,
        life_domains=frozenset([LifeDomain.CAREER, LifeDomain.RELATIONSHIP]),
        description="Partial Summer meeting - Fire potential",
        notes="Missing Wu, storage branch Wei present",
    ),

    # Autumn/Metal - Shen-Xu (missing You)
    PatternSpec(
        id="HALF_MEETINGS~Shen-Xu~Metal",
        category=PatternCategory.HALF_MEETINGS,
        priority=130,
        chinese_name="半會金局",
        english_name="Half Metal Meeting (Shen-Xu)",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Shen", "Xu"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        transformation=TransformSpec(
            resulting_element="Metal",
            requires_element_support=True,
            supporting_elements=frozenset(["Metal"]),
            use_branch_polarity=True,
            base_score_multiplier=0.7,
        ),
        base_score_combined=10.0,
        base_score_transformed=14.0,
        distance_multipliers=(1.0, 0.75, 0.5),
        badge_type=BadgeType.COMBINATION,
        life_domains=frozenset([LifeDomain.WEALTH, LifeDomain.CAREER]),
        description="Partial Autumn meeting - Metal potential",
        notes="Missing You, storage branch Xu present",
    ),

    # Autumn/Metal - You-Xu (missing Shen)
    PatternSpec(
        id="HALF_MEETINGS~You-Xu~Metal",
        category=PatternCategory.HALF_MEETINGS,
        priority=130,
        chinese_name="半會金局",
        english_name="Half Metal Meeting (You-Xu)",
        node_filters=(
            NodeFilter(
                branches=frozenset(["You", "Xu"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        transformation=TransformSpec(
            resulting_element="Metal",
            requires_element_support=True,
            supporting_elements=frozenset(["Metal"]),
            use_branch_polarity=True,
            base_score_multiplier=0.7,
        ),
        base_score_combined=10.0,
        base_score_transformed=14.0,
        distance_multipliers=(1.0, 0.75, 0.5),
        badge_type=BadgeType.COMBINATION,
        life_domains=frozenset([LifeDomain.WEALTH, LifeDomain.CAREER]),
        description="Partial Autumn meeting - Metal potential",
        notes="Missing Shen, storage branch Xu present",
    ),
]


# =============================================================================
# HALF COMBINATIONS (半合) - Partial Triangular Combinations
# =============================================================================
# Two branches from THREE_COMBINATIONS (center + start/end).

def _generate_half_combinations() -> List[PatternSpec]:
    """Generate half combination patterns from three combinations."""
    patterns = []

    # Each three combination generates 2 valid half combinations
    # (center + start) and (center + end), excluding (start + end)
    half_combos = [
        # Water (Shen-Zi-Chen): Shen-Zi, Zi-Chen
        ("HALF_COMBINATIONS~Shen-Zi~Water", ["Shen", "Zi"], "Water", "Chen"),
        ("HALF_COMBINATIONS~Zi-Chen~Water", ["Zi", "Chen"], "Water", "Shen"),

        # Wood (Hai-Mao-Wei): Hai-Mao, Mao-Wei
        ("HALF_COMBINATIONS~Hai-Mao~Wood", ["Hai", "Mao"], "Wood", "Wei"),
        ("HALF_COMBINATIONS~Mao-Wei~Wood", ["Mao", "Wei"], "Wood", "Hai"),

        # Fire (Yin-Wu-Xu): Yin-Wu, Wu-Xu
        ("HALF_COMBINATIONS~Yin-Wu~Fire", ["Yin", "Wu"], "Fire", "Xu"),
        ("HALF_COMBINATIONS~Wu-Xu~Fire", ["Wu", "Xu"], "Fire", "Yin"),

        # Metal (Si-You-Chou): Si-You, You-Chou
        ("HALF_COMBINATIONS~Si-You~Metal", ["Si", "You"], "Metal", "Chou"),
        ("HALF_COMBINATIONS~You-Chou~Metal", ["You", "Chou"], "Metal", "Si"),
    ]

    for pattern_id, branches, element, missing in half_combos:
        patterns.append(PatternSpec(
            id=pattern_id,
            category=PatternCategory.HALF_COMBINATIONS,
            priority=140,
            chinese_name=f"半合{element}局",
            english_name=f"Half {element} Combination",
            node_filters=(
                NodeFilter(
                    branches=frozenset(branches),
                    node_types=frozenset([NodeType.EARTHLY_BRANCH])
                ),
            ),
            min_nodes=2,
            max_nodes=2,
            transformation=TransformSpec(
                resulting_element=element,
                requires_element_support=True,
                supporting_elements=frozenset([element]),
                use_branch_polarity=True,
                base_score_multiplier=0.6,
            ),
            base_score_combined=8.0,
            base_score_transformed=12.0,
            distance_multipliers=(1.0, 0.7, 0.5),
            badge_type=BadgeType.COMBINATION,
            life_domains=frozenset([LifeDomain.CAREER, LifeDomain.RELATIONSHIP]),
            description=f"Partial {element} triangle - incomplete combination",
            notes=f"Missing {missing}",
        ))

    return patterns


HALF_COMBINATIONS_PATTERNS = _generate_half_combinations()


# =============================================================================
# ARCHED COMBINATIONS (拱合) - Any 2 of 3 from Three Combinations
# =============================================================================
# Weaker form - any two branches that are part of a three combination.

def _generate_arched_combinations() -> List[PatternSpec]:
    """Generate arched combination patterns."""
    patterns = []

    # All possible pairs from three combinations
    arched = [
        # Water frame (Shen-Zi-Chen)
        ("ARCHED_COMBINATIONS~Shen-Chen~Water", ["Shen", "Chen"], "Water", "Zi"),

        # Wood frame (Hai-Mao-Wei)
        ("ARCHED_COMBINATIONS~Hai-Wei~Wood", ["Hai", "Wei"], "Wood", "Mao"),

        # Fire frame (Yin-Wu-Xu)
        ("ARCHED_COMBINATIONS~Yin-Xu~Fire", ["Yin", "Xu"], "Fire", "Wu"),

        # Metal frame (Si-You-Chou)
        ("ARCHED_COMBINATIONS~Si-Chou~Metal", ["Si", "Chou"], "Metal", "You"),
    ]

    for pattern_id, branches, element, missing in arched:
        patterns.append(PatternSpec(
            id=pattern_id,
            category=PatternCategory.ARCHED_COMBINATIONS,
            priority=150,
            chinese_name=f"拱合{element}局",
            english_name=f"Arched {element} Combination",
            node_filters=(
                NodeFilter(
                    branches=frozenset(branches),
                    node_types=frozenset([NodeType.EARTHLY_BRANCH])
                ),
            ),
            min_nodes=2,
            max_nodes=2,
            transformation=TransformSpec(
                resulting_element=element,
                requires_element_support=True,
                supporting_elements=frozenset([element]),
                use_branch_polarity=True,
                base_score_multiplier=0.5,
            ),
            base_score_combined=6.0,
            base_score_transformed=9.0,
            distance_multipliers=(1.0, 0.65, 0.4),
            badge_type=BadgeType.COMBINATION,
            life_domains=frozenset([LifeDomain.CAREER]),
            description=f"Arched {element} - weakest combination form, missing center",
            notes=f"Missing center branch {missing}",
        ))

    return patterns


ARCHED_COMBINATIONS_PATTERNS = _generate_arched_combinations()


# =============================================================================
# COMBINED EXPORT
# =============================================================================

ALL_BRANCH_COMBINATION_PATTERNS: List[PatternSpec] = (
    THREE_MEETINGS_PATTERNS +
    THREE_COMBINATIONS_PATTERNS +
    SIX_HARMONIES_PATTERNS +
    HALF_MEETINGS_PATTERNS +
    HALF_COMBINATIONS_PATTERNS +
    ARCHED_COMBINATIONS_PATTERNS
)


def get_all_branch_combination_patterns() -> List[PatternSpec]:
    """Get all branch combination patterns."""
    return ALL_BRANCH_COMBINATION_PATTERNS.copy()


__all__ = [
    "THREE_MEETINGS_PATTERNS",
    "THREE_COMBINATIONS_PATTERNS",
    "SIX_HARMONIES_PATTERNS",
    "HALF_MEETINGS_PATTERNS",
    "HALF_COMBINATIONS_PATTERNS",
    "ARCHED_COMBINATIONS_PATTERNS",
    "ALL_BRANCH_COMBINATION_PATTERNS",
    "get_all_branch_combination_patterns",
]
