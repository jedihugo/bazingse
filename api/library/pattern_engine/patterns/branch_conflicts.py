# * =============================================================================
# * BRANCH CONFLICT PATTERNS (Declarative Format)
# * =============================================================================
# * All negative Earthly Branch interactions expressed as PatternSpecs.
# * Includes: CLASHES, PUNISHMENTS, HARMS, DESTRUCTION
# * =============================================================================

from typing import List

from ..pattern_spec import (
    PatternSpec,
    PatternCategory,
    NodeFilter,
    NodeType,
    SpatialRule,
    TemporalRule,
    QiEffect,
    PillarMeaning,
    EventMapping,
    LifeDomain,
    BadgeType,
    PunishmentType,
)


# =============================================================================
# CLASHES (地支沖) - Opposition Conflicts
# =============================================================================
# Branches 180 degrees apart on the zodiac clash with each other.
# Direct opposition - strongest conflict type.

CLASHES_PATTERNS: List[PatternSpec] = [
    # Zi-Wu Clash (Water vs Fire)
    PatternSpec(
        id="CLASH~Zi-Wu~opposite",
        category=PatternCategory.CLASH,
        priority=200,
        chinese_name="子午沖",
        english_name="Rat-Horse Clash",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Zi", "Wu"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=15.0,
        distance_multipliers=(1.0, 0.85, 0.7),
        qi_effects=(
            QiEffect(target="source", qi_change=-10.0, is_percentage=False),
            QiEffect(target="target", qi_change=-6.18, is_percentage=False),  # Golden ratio
        ),
        badge_type=BadgeType.CLASH,
        life_domains=frozenset([LifeDomain.HEALTH, LifeDomain.RELATIONSHIP, LifeDomain.CAREER]),
        pillar_meanings=PillarMeaning(
            year="Early life instability, family conflicts",
            month="Career disruptions, authority clashes",
            day="Relationship turmoil, inner conflict",
            hour="Late life changes, children's challenges"
        ),
        event_mapping=EventMapping(
            primary_domains=frozenset([LifeDomain.HEALTH, LifeDomain.RELATIONSHIP]),
            negative_events=(
                ("health", "illness_major"),
                ("health", "injury_accident"),
                ("relationship", "conflict_partner"),
                ("relationship", "divorce"),
                ("career", "job_loss"),
            ),
            domain_sentiment=(
                ("health", "negative"),
                ("relationship", "negative"),
                ("career", "negative"),
            ),
        ),
        description="Water-Fire opposition - emotional vs passionate conflict",
        classical_source="三命通會",
        notes="Opposite elements: Water controls Fire but Fire evaporates Water",
    ),

    # Chou-Wei Clash (Earth vs Earth)
    PatternSpec(
        id="CLASH~Chou-Wei~same",
        category=PatternCategory.CLASH,
        priority=200,
        chinese_name="丑未沖",
        english_name="Ox-Goat Clash",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Chou", "Wei"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=12.0,
        distance_multipliers=(1.0, 0.85, 0.7),
        qi_effects=(
            QiEffect(target="all", qi_change=-8.0, is_percentage=False),
        ),
        badge_type=BadgeType.CLASH,
        life_domains=frozenset([LifeDomain.FAMILY, LifeDomain.WEALTH, LifeDomain.HEALTH]),
        pillar_meanings=PillarMeaning(
            year="Property disputes, inheritance conflicts",
            month="Career stability issues",
            day="Relationship grounding problems",
            hour="Real estate challenges"
        ),
        description="Earth-Earth same element clash - stubborn conflict",
        notes="Same element: Both Earth, mutual depletion without control",
    ),

    # Yin-Shen Clash (Wood vs Metal)
    PatternSpec(
        id="CLASH~Yin-Shen~opposite",
        category=PatternCategory.CLASH,
        priority=200,
        chinese_name="寅申沖",
        english_name="Tiger-Monkey Clash",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Yin", "Shen"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=15.0,
        distance_multipliers=(1.0, 0.85, 0.7),
        qi_effects=(
            QiEffect(target="source", qi_change=-10.0, is_percentage=False),
            QiEffect(target="target", qi_change=-6.18, is_percentage=False),
        ),
        badge_type=BadgeType.CLASH,
        life_domains=frozenset([LifeDomain.HEALTH, LifeDomain.TRAVEL, LifeDomain.CAREER]),
        pillar_meanings=PillarMeaning(
            year="Travel accidents in youth, family moves",
            month="Career path conflicts",
            day="Personal growth obstacles",
            hour="Children's travel issues"
        ),
        event_mapping=EventMapping(
            primary_domains=frozenset([LifeDomain.TRAVEL, LifeDomain.HEALTH]),
            negative_events=(
                ("travel", "relocation_major"),
                ("health", "injury_accident"),
                ("career", "job_loss"),
            ),
        ),
        description="Wood-Metal opposition - growth vs cutting conflict",
        notes="Metal controls Wood: Shen controls Yin",
    ),

    # Mao-You Clash (Wood vs Metal)
    PatternSpec(
        id="CLASH~Mao-You~opposite",
        category=PatternCategory.CLASH,
        priority=200,
        chinese_name="卯酉沖",
        english_name="Rabbit-Rooster Clash",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Mao", "You"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=15.0,
        distance_multipliers=(1.0, 0.85, 0.7),
        qi_effects=(
            QiEffect(target="source", qi_change=-10.0, is_percentage=False),
            QiEffect(target="target", qi_change=-6.18, is_percentage=False),
        ),
        badge_type=BadgeType.CLASH,
        life_domains=frozenset([LifeDomain.HEALTH, LifeDomain.RELATIONSHIP, LifeDomain.LEGAL]),
        pillar_meanings=PillarMeaning(
            year="Family legal issues",
            month="Career confrontations",
            day="Marriage/partnership breakups",
            hour="Children's discipline problems"
        ),
        description="Pure Wood-Metal opposition - precision cuts growth",
        notes="Mao is pure Wood (Yi), You is pure Metal (Xin)",
    ),

    # Chen-Xu Clash (Earth vs Earth)
    PatternSpec(
        id="CLASH~Chen-Xu~same",
        category=PatternCategory.CLASH,
        priority=200,
        chinese_name="辰戌沖",
        english_name="Dragon-Dog Clash",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Chen", "Xu"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=12.0,
        distance_multipliers=(1.0, 0.85, 0.7),
        qi_effects=(
            QiEffect(target="all", qi_change=-8.0, is_percentage=False),
        ),
        badge_type=BadgeType.CLASH,
        life_domains=frozenset([LifeDomain.WEALTH, LifeDomain.CAREER, LifeDomain.FAMILY]),
        pillar_meanings=PillarMeaning(
            year="Ancestral wealth disputes",
            month="Career territory conflicts",
            day="Storage clash - wealth volatility",
            hour="Legacy/inheritance issues"
        ),
        description="Earth-Earth storage clash - both are element storages",
        notes="Both are storage branches: Chen stores Water, Xu stores Fire",
    ),

    # Si-Hai Clash (Fire vs Water)
    PatternSpec(
        id="CLASH~Si-Hai~opposite",
        category=PatternCategory.CLASH,
        priority=200,
        chinese_name="巳亥沖",
        english_name="Snake-Pig Clash",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Si", "Hai"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=15.0,
        distance_multipliers=(1.0, 0.85, 0.7),
        qi_effects=(
            QiEffect(target="source", qi_change=-10.0, is_percentage=False),
            QiEffect(target="target", qi_change=-6.18, is_percentage=False),
        ),
        badge_type=BadgeType.CLASH,
        life_domains=frozenset([LifeDomain.TRAVEL, LifeDomain.CAREER, LifeDomain.HEALTH]),
        pillar_meanings=PillarMeaning(
            year="International conflicts, immigration issues",
            month="Career relocations",
            day="Life direction changes",
            hour="Late life travels"
        ),
        event_mapping=EventMapping(
            primary_domains=frozenset([LifeDomain.TRAVEL, LifeDomain.CAREER]),
            negative_events=(
                ("travel", "immigration"),
                ("travel", "relocation_major"),
                ("career", "job_loss"),
            ),
        ),
        description="Fire-Water Yi Ma clash - travel and movement disruption",
        notes="Both are Yi Ma (travel stars) for each other's frame",
    ),
]


# =============================================================================
# PUNISHMENTS (刑) - Penalty Relationships
# =============================================================================
# Four types with different severity levels.

PUNISHMENTS_PATTERNS: List[PatternSpec] = [
    # ==========================================================================
    # 勢刑 (SHI XING) - Bullying Punishment - SEVERE
    # Yin-Si-Shen: Three powerful branches in mutual conflict
    # ==========================================================================
    PatternSpec(
        id="PUNISHMENT~Yin-Si-Shen~shi_xing",
        category=PatternCategory.PUNISHMENT,
        priority=210,
        chinese_name="勢刑",
        english_name="Bullying Punishment (Tiger-Snake-Monkey)",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Yin", "Si", "Shen"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=3,
        base_score_combined=18.0,
        distance_multipliers=(1.0, 0.9, 0.8),
        qi_effects=(
            QiEffect(target="all", qi_change=-12.0, is_percentage=False),
        ),
        badge_type=BadgeType.PUNISHMENT,
        life_domains=frozenset([LifeDomain.HEALTH, LifeDomain.LEGAL, LifeDomain.CAREER]),
        pillar_meanings=PillarMeaning(
            year="Severe early life trauma, power struggles in family",
            month="Career destroyed by power plays, legal battles",
            day="Self-destructive patterns, health crises",
            hour="Children's severe challenges"
        ),
        event_mapping=EventMapping(
            primary_domains=frozenset([LifeDomain.HEALTH, LifeDomain.LEGAL]),
            negative_events=(
                ("health", "illness_major"),
                ("health", "injury_accident"),
                ("health", "surgery"),
                ("legal", "lawsuit_filed"),
                ("legal", "arrest"),
                ("career", "job_loss"),
            ),
            domain_sentiment=(
                ("health", "negative"),
                ("legal", "negative"),
                ("career", "negative"),
            ),
            pillar_severity_modifiers=(
                ("year", 1.2),
                ("month", 1.3),
                ("day", 1.5),
                ("hour", 1.1),
            ),
        ),
        description="Three powerful branches (Wood-Fire-Metal) in mutual conflict - severe trauma",
        classical_source="三命通會: 恃勢之刑",
        severity_formula="base * 1.0 * distance_mult * seasonal_mult * pillar_mult",
        notes="Most severe punishment type. Element conflict: Metal controls Wood, Fire controls Metal",
    ),

    # ==========================================================================
    # 無禮刑 (WU LI XING) - Rudeness Punishment - MODERATE
    # Chou-Wei-Xu: Earth branches showing disrespect
    # ==========================================================================
    PatternSpec(
        id="PUNISHMENT~Chou-Wei-Xu~wu_li_xing",
        category=PatternCategory.PUNISHMENT,
        priority=215,
        chinese_name="無禮刑",
        english_name="Rudeness Punishment (Ox-Goat-Dog)",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Chou", "Wei", "Xu"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=3,
        base_score_combined=15.0,
        distance_multipliers=(1.0, 0.85, 0.7),
        qi_effects=(
            QiEffect(target="all", qi_change=-10.0, is_percentage=False),
        ),
        badge_type=BadgeType.PUNISHMENT,
        life_domains=frozenset([LifeDomain.RELATIONSHIP, LifeDomain.FAMILY, LifeDomain.HEALTH]),
        pillar_meanings=PillarMeaning(
            year="Family disrespect, inheritance conflicts",
            month="Career undermined by rudeness",
            day="Relationship breakdowns from disrespect",
            hour="Disrespected by children"
        ),
        event_mapping=EventMapping(
            primary_domains=frozenset([LifeDomain.RELATIONSHIP, LifeDomain.FAMILY]),
            negative_events=(
                ("relationship", "divorce"),
                ("relationship", "conflict_partner"),
                ("family", "family_conflict"),
                ("health", "illness_minor"),
            ),
            domain_sentiment=(
                ("relationship", "negative"),
                ("family", "negative"),
            ),
        ),
        description="Three Earth branches in mutual disrespect - relationship damage",
        classical_source="三命通會: 無禮之刑",
        severity_formula="base * 0.85 * distance_mult * seasonal_mult",
        notes="Moderate severity. All Earth element - no elemental control, pure disharmony",
    ),

    # ==========================================================================
    # 恩刑 (EN XING) - Ungrateful Punishment - LIGHT
    # Zi-Mao: Beneficiary punishes benefactor
    # ==========================================================================
    PatternSpec(
        id="PUNISHMENT~Zi-Mao~en_xing",
        category=PatternCategory.PUNISHMENT,
        priority=220,
        chinese_name="恩刑",
        english_name="Ungrateful Punishment (Rat-Rabbit)",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Zi", "Mao"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=10.0,
        distance_multipliers=(1.0, 0.8, 0.6),
        qi_effects=(
            QiEffect(target="source", qi_change=-7.0, is_percentage=False),
            QiEffect(target="target", qi_change=-4.3, is_percentage=False),
        ),
        badge_type=BadgeType.PUNISHMENT,
        life_domains=frozenset([LifeDomain.RELATIONSHIP, LifeDomain.FAMILY, LifeDomain.CAREER]),
        pillar_meanings=PillarMeaning(
            year="Betrayed by those you helped in youth",
            month="Career betrayal from those you mentored",
            day="Partner/spouse ingratitude",
            hour="Children's ingratitude"
        ),
        event_mapping=EventMapping(
            primary_domains=frozenset([LifeDomain.RELATIONSHIP, LifeDomain.CAREER]),
            negative_events=(
                ("relationship", "breakup"),
                ("relationship", "conflict_partner"),
                ("career", "demotion"),
            ),
        ),
        description="Water nurtures Wood, but Wood punishes Water - betrayal by those you helped",
        classical_source="三命通會: 持恩之刑",
        severity_formula="base * 0.70 * distance_mult * seasonal_mult",
        notes="Light severity. Mao (Wood) punishes Zi (Water) despite Water generating Wood",
    ),

    # ==========================================================================
    # 自刑 (ZI XING) - Self-Punishment - SELF
    # Chen-Chen, Wu-Wu, You-You, Hai-Hai
    # ==========================================================================
    PatternSpec(
        id="PUNISHMENT~Chen-Chen~zi_xing",
        category=PatternCategory.PUNISHMENT,
        priority=230,
        chinese_name="辰自刑",
        english_name="Dragon Self-Punishment",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Chen"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,  # Same branch appears twice
        max_nodes=2,
        base_score_combined=8.0,
        distance_multipliers=(1.0, 0.75, 0.5),
        qi_effects=(
            QiEffect(target="all", qi_change=-6.0, is_percentage=False),
        ),
        badge_type=BadgeType.PUNISHMENT,
        life_domains=frozenset([LifeDomain.HEALTH, LifeDomain.CAREER]),
        pillar_meanings=PillarMeaning(
            year="Self-sabotage in early ambitions",
            month="Career self-destruction through pride",
            day="Personal stubbornness causing harm",
            hour="Isolation in old age"
        ),
        description="Earth Dragon - stubborn pride leads to isolation",
        severity_formula="base * 0.60 * distance_mult",
        notes="Self-inflicted through excessive pride and stubbornness",
    ),

    PatternSpec(
        id="PUNISHMENT~Wu-Wu~zi_xing",
        category=PatternCategory.PUNISHMENT,
        priority=230,
        chinese_name="午自刑",
        english_name="Horse Self-Punishment",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Wu"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=8.0,
        distance_multipliers=(1.0, 0.75, 0.5),
        qi_effects=(
            QiEffect(target="all", qi_change=-6.0, is_percentage=False),
        ),
        badge_type=BadgeType.PUNISHMENT,
        life_domains=frozenset([LifeDomain.HEALTH, LifeDomain.RELATIONSHIP]),
        pillar_meanings=PillarMeaning(
            year="Restless childhood",
            month="Career burnout",
            day="Relationship instability from restlessness",
            hour="Unable to settle in old age"
        ),
        description="Fire Horse - restless energy burns itself out",
        severity_formula="base * 0.60 * distance_mult",
        notes="Self-inflicted through inability to rest, constant motion",
    ),

    PatternSpec(
        id="PUNISHMENT~You-You~zi_xing",
        category=PatternCategory.PUNISHMENT,
        priority=230,
        chinese_name="酉自刑",
        english_name="Rooster Self-Punishment",
        node_filters=(
            NodeFilter(
                branches=frozenset(["You"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=8.0,
        distance_multipliers=(1.0, 0.75, 0.5),
        qi_effects=(
            QiEffect(target="all", qi_change=-6.0, is_percentage=False),
        ),
        badge_type=BadgeType.PUNISHMENT,
        life_domains=frozenset([LifeDomain.HEALTH, LifeDomain.RELATIONSHIP]),
        pillar_meanings=PillarMeaning(
            year="Perfectionist childhood trauma",
            month="Career paralysis from over-analysis",
            day="Relationship difficulties from criticism",
            hour="Loneliness from high standards"
        ),
        description="Metal Rooster - perfectionism leads to self-criticism",
        severity_formula="base * 0.60 * distance_mult",
        notes="Self-inflicted through excessive perfectionism and self-criticism",
    ),

    PatternSpec(
        id="PUNISHMENT~Hai-Hai~zi_xing",
        category=PatternCategory.PUNISHMENT,
        priority=230,
        chinese_name="亥自刑",
        english_name="Pig Self-Punishment",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Hai"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=8.0,
        distance_multipliers=(1.0, 0.75, 0.5),
        qi_effects=(
            QiEffect(target="all", qi_change=-6.0, is_percentage=False),
        ),
        badge_type=BadgeType.PUNISHMENT,
        life_domains=frozenset([LifeDomain.HEALTH, LifeDomain.WEALTH]),
        pillar_meanings=PillarMeaning(
            year="Childhood indulgence issues",
            month="Career setback from excess",
            day="Health issues from overindulgence",
            hour="Lonely indulgence in old age"
        ),
        description="Water Pig - indulgence leads to self-harm",
        severity_formula="base * 0.60 * distance_mult",
        notes="Self-inflicted through excessive indulgence and comfort-seeking",
    ),
]


# =============================================================================
# HARMS (害) - Mutual Harm Relationships
# =============================================================================
# Branches that harm each other - subtle undermining.

HARMS_PATTERNS: List[PatternSpec] = [
    # Zi-Wei Harm
    PatternSpec(
        id="HARM~Zi-Wei~",
        category=PatternCategory.HARM,
        priority=240,
        chinese_name="子未害",
        english_name="Rat-Goat Harm",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Zi", "Wei"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=10.0,
        distance_multipliers=(1.0, 0.8, 0.6),
        qi_effects=(
            QiEffect(target="source", qi_change=-7.0, is_percentage=False),
            QiEffect(target="target", qi_change=-4.3, is_percentage=False),
        ),
        badge_type=BadgeType.HARM,
        life_domains=frozenset([LifeDomain.RELATIONSHIP, LifeDomain.HEALTH]),
        pillar_meanings=PillarMeaning(
            year="Family undermining",
            month="Career sabotage",
            day="Relationship erosion",
            hour="Children's hidden resentment"
        ),
        description="Water meets Earth - subtle undermining through absorption",
        notes="Wei (Earth) controls Zi (Water) by absorption",
    ),

    # Chou-Wu Harm
    PatternSpec(
        id="HARM~Chou-Wu~",
        category=PatternCategory.HARM,
        priority=240,
        chinese_name="丑午害",
        english_name="Ox-Horse Harm",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Chou", "Wu"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=10.0,
        distance_multipliers=(1.0, 0.8, 0.6),
        qi_effects=(
            QiEffect(target="source", qi_change=-7.0, is_percentage=False),
            QiEffect(target="target", qi_change=-4.3, is_percentage=False),
        ),
        badge_type=BadgeType.HARM,
        life_domains=frozenset([LifeDomain.RELATIONSHIP, LifeDomain.HEALTH]),
        description="Fire meets Earth storage - passion smothered",
        notes="Wu (Fire) harms Chou (Earth Metal storage)",
    ),

    # Yin-Si Harm
    PatternSpec(
        id="HARM~Yin-Si~",
        category=PatternCategory.HARM,
        priority=240,
        chinese_name="寅巳害",
        english_name="Tiger-Snake Harm",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Yin", "Si"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=10.0,
        distance_multipliers=(1.0, 0.8, 0.6),
        qi_effects=(
            QiEffect(target="source", qi_change=-7.0, is_percentage=False),
            QiEffect(target="target", qi_change=-4.3, is_percentage=False),
        ),
        badge_type=BadgeType.HARM,
        life_domains=frozenset([LifeDomain.HEALTH, LifeDomain.CAREER]),
        description="Wood feeds Fire excessively - depletion through giving",
        notes="Yin (Wood) produces Si (Fire) but gets depleted",
    ),

    # Mao-Chen Harm
    PatternSpec(
        id="HARM~Mao-Chen~",
        category=PatternCategory.HARM,
        priority=240,
        chinese_name="卯辰害",
        english_name="Rabbit-Dragon Harm",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Mao", "Chen"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=10.0,
        distance_multipliers=(1.0, 0.8, 0.6),
        qi_effects=(
            QiEffect(target="source", qi_change=-7.0, is_percentage=False),
            QiEffect(target="target", qi_change=-4.3, is_percentage=False),
        ),
        badge_type=BadgeType.HARM,
        life_domains=frozenset([LifeDomain.CAREER, LifeDomain.RELATIONSHIP]),
        description="Wood controls Earth - overextension causing harm",
        notes="Mao (Wood) harms Chen (Earth) through control",
    ),

    # Shen-Hai Harm
    PatternSpec(
        id="HARM~Shen-Hai~",
        category=PatternCategory.HARM,
        priority=240,
        chinese_name="申亥害",
        english_name="Monkey-Pig Harm",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Shen", "Hai"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=10.0,
        distance_multipliers=(1.0, 0.8, 0.6),
        qi_effects=(
            QiEffect(target="source", qi_change=-7.0, is_percentage=False),
            QiEffect(target="target", qi_change=-4.3, is_percentage=False),
        ),
        badge_type=BadgeType.HARM,
        life_domains=frozenset([LifeDomain.TRAVEL, LifeDomain.CAREER]),
        description="Metal produces Water - excessive giving depletes",
        notes="Shen (Metal) produces Hai (Water) excessively",
    ),

    # You-Xu Harm
    PatternSpec(
        id="HARM~You-Xu~",
        category=PatternCategory.HARM,
        priority=240,
        chinese_name="酉戌害",
        english_name="Rooster-Dog Harm",
        node_filters=(
            NodeFilter(
                branches=frozenset(["You", "Xu"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=10.0,
        distance_multipliers=(1.0, 0.8, 0.6),
        qi_effects=(
            QiEffect(target="source", qi_change=-7.0, is_percentage=False),
            QiEffect(target="target", qi_change=-4.3, is_percentage=False),
        ),
        badge_type=BadgeType.HARM,
        life_domains=frozenset([LifeDomain.RELATIONSHIP, LifeDomain.FAMILY]),
        description="Metal meets Earth Fire storage - hidden fire harms metal",
        notes="Xu (Fire storage) harms You (Metal)",
    ),
]


# =============================================================================
# DESTRUCTION (破) - Destructive Relationships
# =============================================================================
# Weaker conflict - breaking or damaging.

DESTRUCTION_PATTERNS: List[PatternSpec] = [
    # Zi-You Destruction (Water vs Metal - same element effect)
    PatternSpec(
        id="DESTRUCTION~Zi-You~",
        category=PatternCategory.DESTRUCTION,
        priority=250,
        chinese_name="子酉破",
        english_name="Rat-Rooster Destruction",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Zi", "You"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=7.0,
        distance_multipliers=(1.0, 0.75, 0.5),
        qi_effects=(
            QiEffect(target="source", qi_change=-5.0, is_percentage=False),
            QiEffect(target="target", qi_change=-3.0, is_percentage=False),
        ),
        badge_type=BadgeType.DESTRUCTION,
        life_domains=frozenset([LifeDomain.RELATIONSHIP, LifeDomain.CAREER]),
        description="Metal produces Water but creates friction in process",
        notes="Generating relationship but with friction",
    ),

    # Chou-Chen Destruction
    PatternSpec(
        id="DESTRUCTION~Chou-Chen~",
        category=PatternCategory.DESTRUCTION,
        priority=250,
        chinese_name="丑辰破",
        english_name="Ox-Dragon Destruction",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Chou", "Chen"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=6.0,
        distance_multipliers=(1.0, 0.75, 0.5),
        qi_effects=(
            QiEffect(target="all", qi_change=-4.0, is_percentage=False),
        ),
        badge_type=BadgeType.DESTRUCTION,
        life_domains=frozenset([LifeDomain.WEALTH, LifeDomain.CAREER]),
        description="Two Earth storages in friction - storage conflicts",
        notes="Both are storage branches (Metal, Water)",
    ),

    # Mao-Wu Destruction
    PatternSpec(
        id="DESTRUCTION~Mao-Wu~",
        category=PatternCategory.DESTRUCTION,
        priority=250,
        chinese_name="卯午破",
        english_name="Rabbit-Horse Destruction",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Mao", "Wu"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=7.0,
        distance_multipliers=(1.0, 0.75, 0.5),
        qi_effects=(
            QiEffect(target="source", qi_change=-5.0, is_percentage=False),
            QiEffect(target="target", qi_change=-3.0, is_percentage=False),
        ),
        badge_type=BadgeType.DESTRUCTION,
        life_domains=frozenset([LifeDomain.HEALTH, LifeDomain.RELATIONSHIP]),
        description="Wood feeds Fire excessively in destruction",
        notes="Mao (Wood) produces Wu (Fire) with friction",
    ),

    # Wei-Xu Destruction
    PatternSpec(
        id="DESTRUCTION~Wei-Xu~",
        category=PatternCategory.DESTRUCTION,
        priority=250,
        chinese_name="未戌破",
        english_name="Goat-Dog Destruction",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Wei", "Xu"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=6.0,
        distance_multipliers=(1.0, 0.75, 0.5),
        qi_effects=(
            QiEffect(target="all", qi_change=-4.0, is_percentage=False),
        ),
        badge_type=BadgeType.DESTRUCTION,
        life_domains=frozenset([LifeDomain.FAMILY, LifeDomain.WEALTH]),
        description="Earth storage friction - Wood and Fire storages clash",
        notes="Wei stores Wood, Xu stores Fire",
    ),

    # Shen-Si Destruction (implied, though Si-Shen is also in punishment)
    PatternSpec(
        id="DESTRUCTION~Si-Shen~",
        category=PatternCategory.DESTRUCTION,
        priority=250,
        chinese_name="巳申破",
        english_name="Snake-Monkey Destruction",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Si", "Shen"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=7.0,
        distance_multipliers=(1.0, 0.75, 0.5),
        qi_effects=(
            QiEffect(target="source", qi_change=-5.0, is_percentage=False),
            QiEffect(target="target", qi_change=-3.0, is_percentage=False),
        ),
        badge_type=BadgeType.DESTRUCTION,
        life_domains=frozenset([LifeDomain.CAREER, LifeDomain.HEALTH]),
        description="Fire controls Metal with friction",
        notes="Also form Six Harmonies - complex relationship",
    ),

    # Hai-Yin Destruction
    PatternSpec(
        id="DESTRUCTION~Hai-Yin~",
        category=PatternCategory.DESTRUCTION,
        priority=250,
        chinese_name="亥寅破",
        english_name="Pig-Tiger Destruction",
        node_filters=(
            NodeFilter(
                branches=frozenset(["Hai", "Yin"]),
                node_types=frozenset([NodeType.EARTHLY_BRANCH])
            ),
        ),
        min_nodes=2,
        max_nodes=2,
        base_score_combined=7.0,
        distance_multipliers=(1.0, 0.75, 0.5),
        qi_effects=(
            QiEffect(target="source", qi_change=-5.0, is_percentage=False),
            QiEffect(target="target", qi_change=-3.0, is_percentage=False),
        ),
        badge_type=BadgeType.DESTRUCTION,
        life_domains=frozenset([LifeDomain.EDUCATION, LifeDomain.HEALTH]),
        description="Water produces Wood with friction",
        notes="Also form Six Harmonies - complex relationship",
    ),
]


# =============================================================================
# COMBINED EXPORT
# =============================================================================

ALL_BRANCH_CONFLICT_PATTERNS: List[PatternSpec] = (
    CLASHES_PATTERNS +
    PUNISHMENTS_PATTERNS +
    HARMS_PATTERNS +
    DESTRUCTION_PATTERNS
)


def get_all_branch_conflict_patterns() -> List[PatternSpec]:
    """Get all branch conflict patterns."""
    return ALL_BRANCH_CONFLICT_PATTERNS.copy()


__all__ = [
    "CLASHES_PATTERNS",
    "PUNISHMENTS_PATTERNS",
    "HARMS_PATTERNS",
    "DESTRUCTION_PATTERNS",
    "ALL_BRANCH_CONFLICT_PATTERNS",
    "get_all_branch_conflict_patterns",
]
