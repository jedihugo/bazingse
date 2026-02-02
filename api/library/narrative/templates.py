# * =========================
# * NARRATIVE TEMPLATES (EN/ZH)
# * =========================
# Text templates for generating human-readable BaZi narratives.
# Each template has both English and Chinese versions with placeholders.
#
# Template placeholders use {variable_name} syntax for string formatting.

from typing import Dict, Any

# =============================================================================
# INTERACTION TYPE TEMPLATES
# =============================================================================
# Templates for each interaction type, organized by category

NARRATIVE_TEMPLATES: Dict[str, Dict[str, Any]] = {
    # =====================
    # POSITIVE COMBINATIONS (Earthly Branch)
    # =====================
    "THREE_MEETINGS": {
        "category": "combination",
        "polarity": "positive",
        "en": {
            "title": "Three Meetings",
            "summary": "The {branches} form a powerful Three Meetings ({element_zh}) combination, strengthening {element} energy.",
            "detail": "When {branch1}, {branch2}, and {branch3} come together, they create a directional alliance that amplifies {element} qi by {points}. This is one of the strongest combinations in BaZi.",
            "meaning": "This indicates a period of enhanced {element} influence in your chart, bringing qualities associated with this element.",
            "transformed": "Full transformation achieved - the combination is supported by {element} in the Heavenly Stems.",
            "partial": "Partial combination - {element} energy is boosted but not fully transformed (no {element} stem present).",
        },
        "zh": {
            "title": "三会",
            "summary": "{branches_zh}形成强大的三会{element_zh}局，增强{element_zh}能量。",
            "detail": "当{branch1_zh}、{branch2_zh}、{branch3_zh}相遇时，形成方位联盟，使{element_zh}气增加{points}。这是八字中最强大的组合之一。",
            "meaning": "这表明您的命盘中{element_zh}影响力增强的时期，带来与此五行相关的特质。",
            "transformed": "完全转化成功 - 组合得到天干中{element_zh}的支持。",
            "partial": "部分组合 - {element_zh}能量增强但未完全转化（无{element_zh}天干）。",
        },
        "icon": "meeting",
        "color_key": "combination",
    },

    "THREE_COMBINATIONS": {
        "category": "combination",
        "polarity": "positive",
        "en": {
            "title": "Three Combinations",
            "summary": "The {branches} form a harmonious Three Combinations ({element_zh}) pattern, boosting {element} energy.",
            "detail": "{branch1}, {branch2}, and {branch3} unite in a triangular harmony, generating {element} qi worth {points}. This represents a balanced and auspicious energy flow.",
            "meaning": "The three branches work together to strengthen {element} qualities in your life during this period.",
            "transformed": "Complete transformation - the heavenly stems support this combination with {element} energy.",
            "partial": "The combination is active but lacks heavenly stem support for full transformation.",
        },
        "zh": {
            "title": "三合",
            "summary": "{branches_zh}形成和谐的三合{element_zh}局，增强{element_zh}能量。",
            "detail": "{branch1_zh}、{branch2_zh}、{branch3_zh}在三角和谐中结合，产生{points}的{element_zh}气。这代表平衡吉祥的能量流动。",
            "meaning": "三个地支共同作用，在这段时期增强您生活中的{element_zh}特质。",
            "transformed": "完全转化 - 天干以{element_zh}能量支持此组合。",
            "partial": "组合活跃但缺乏天干支持以完全转化。",
        },
        "icon": "triangle",
        "color_key": "combination",
    },

    "SIX_HARMONIES": {
        "category": "combination",
        "polarity": "positive",
        "en": {
            "title": "Six Harmonies",
            "summary": "{branch1} and {branch2} form a Six Harmonies pair, generating {element} energy.",
            "detail": "The pairing of {branch1} and {branch2} creates a harmonious bond worth {points} {element} qi. This is a supportive and stabilizing combination.",
            "meaning": "This harmony brings cooperation and balance, enhancing {element} qualities in relationships and circumstances.",
            "transformed": "Full transformation with heavenly stem support.",
            "partial": "Harmony active but transformation incomplete without stem support.",
        },
        "zh": {
            "title": "六合",
            "summary": "{branch1_zh}与{branch2_zh}形成六合，产生{element_zh}能量。",
            "detail": "{branch1_zh}与{branch2_zh}的配对创造和谐纽带，产生{points}的{element_zh}气。这是一个支持和稳定的组合。",
            "meaning": "此和合带来合作与平衡，增强人际关系和环境中的{element_zh}特质。",
            "transformed": "完全转化，有天干支持。",
            "partial": "和合活跃但缺乏天干支持，转化不完整。",
        },
        "icon": "harmony",
        "color_key": "combination",
    },

    "HALF_MEETINGS": {
        "category": "combination",
        "polarity": "positive",
        "en": {
            "title": "Half Meetings",
            "summary": "{branches} form a Half Meetings pattern toward {element}.",
            "detail": "Two of the three branches needed for a full Three Meetings are present, creating partial {element} energy worth {points}.",
            "meaning": "This indicates potential for {element} enhancement if the missing branch appears in luck cycles.",
        },
        "zh": {
            "title": "半会",
            "summary": "{branches_zh}形成半会{element_zh}局。",
            "detail": "三会所需的三个地支中有两个出现，产生{points}的部分{element_zh}能量。",
            "meaning": "如果缺失的地支出现在运势周期中，{element_zh}有增强潜力。",
        },
        "icon": "half_meeting",
        "color_key": "combination",
    },

    "HALF_COMBINATIONS": {
        "category": "combination",
        "polarity": "positive",
        "en": {
            "title": "Half Combinations",
            "summary": "{branches} form a Half Combination toward {element}.",
            "detail": "Two branches of a Three Combinations pattern are present, generating {points} of partial {element} energy.",
            "meaning": "The combination is incomplete but still provides beneficial {element} influence.",
        },
        "zh": {
            "title": "半合",
            "summary": "{branches_zh}形成半合{element_zh}局。",
            "detail": "三合的两个地支出现，产生{points}的部分{element_zh}能量。",
            "meaning": "组合不完整但仍提供有益的{element_zh}影响。",
        },
        "icon": "half_combo",
        "color_key": "combination",
    },

    "ARCHED_COMBINATIONS": {
        "category": "combination",
        "polarity": "positive",
        "en": {
            "title": "Arched Combination",
            "summary": "{branches} arch over the missing branch to form {element} energy.",
            "detail": "Although one branch is missing, the present branches reach across to create {points} of {element} qi.",
            "meaning": "This arched connection provides subtle but present {element} influence.",
        },
        "zh": {
            "title": "拱合",
            "summary": "{branches_zh}拱合形成{element_zh}能量。",
            "detail": "虽然缺少一个地支，但现有地支跨越形成{points}的{element_zh}气。",
            "meaning": "这种拱合连接提供微妙但存在的{element_zh}影响。",
        },
        "icon": "arch",
        "color_key": "combination",
    },

    # =====================
    # POSITIVE COMBINATIONS (Heavenly Stem)
    # =====================
    "STEM_COMBINATIONS": {
        "category": "combination",
        "polarity": "positive",
        "en": {
            "title": "Stem Combination",
            "summary": "{stem1} and {stem2} combine harmoniously, generating {element} energy.",
            "detail": "The heavenly stems {stem1} and {stem2} form one of the five stem pairs, creating {points} of {element} qi.",
            "meaning": "Stem combinations indicate periods of cooperation, partnership, and merged energies.",
            "transformed": "Full transformation - earthly branch support confirms the {element} transformation.",
            "partial": "Combination present but lacks full branch support for complete transformation.",
        },
        "zh": {
            "title": "天干合",
            "summary": "{stem1_zh}与{stem2_zh}和谐相合，产生{element_zh}能量。",
            "detail": "天干{stem1_zh}与{stem2_zh}形成五合之一，产生{points}的{element_zh}气。",
            "meaning": "天干合表示合作、伙伴关系和能量融合的时期。",
            "transformed": "完全转化 - 地支支持确认{element_zh}转化。",
            "partial": "组合存在但缺乏完整的地支支持以完全转化。",
        },
        "icon": "stem_combo",
        "color_key": "combination",
    },

    # =====================
    # NEGATIVE CONFLICTS
    # =====================
    "CLASHES": {
        "category": "conflict",
        "polarity": "negative",
        "en": {
            "title": "Clash",
            "summary": "{branch1} and {branch2} clash directly, creating tension and disruption.",
            "detail": "The opposition of {branch1} and {branch2} generates conflict worth -{points} qi impact. Clashes bring sudden changes, obstacles, or breaking of existing patterns.",
            "meaning": "This clash may manifest as unexpected changes, disagreements, or the need to let go of something.",
            "advice": "Clashes often precede necessary transformations. Stay adaptable and avoid forcing situations.",
        },
        "zh": {
            "title": "冲",
            "summary": "{branch1_zh}与{branch2_zh}直接冲突，造成紧张和干扰。",
            "detail": "{branch1_zh}与{branch2_zh}的对冲产生-{points}的气影响。冲带来突然变化、障碍或打破现有模式。",
            "meaning": "此冲可能表现为意外变化、分歧或需要放手某事。",
            "advice": "冲往往预示必要的转变。保持灵活，避免强求。",
        },
        "icon": "clash",
        "color_key": "conflict",
    },

    "PUNISHMENTS": {
        "category": "conflict",
        "polarity": "negative",
        "en": {
            "title": "Punishment",
            "summary": "{branches} form a {punishment_type} punishment pattern.",
            "detail": "This punishment configuration creates internal friction worth -{points} impact. Punishments often relate to karmic lessons or self-sabotaging patterns.",
            "meaning": "The punishment indicates areas requiring self-reflection and personal growth.",
            "advice": "Punishment energy can be channeled into self-improvement when approached consciously.",
            "types": {
                "shi": "Power Punishment (Shi Xing) - conflicts involving power dynamics",
                "wu_li": "Rudeness Punishment (Wu Li Xing) - social friction and etiquette issues",
                "en": "Ungrateful Punishment (En Xing) - relationship imbalances and ingratitude",
                "zi": "Self-Punishment (Zi Xing) - internal struggles and self-criticism",
            },
        },
        "zh": {
            "title": "刑",
            "summary": "{branches_zh}形成{punishment_type_zh}刑。",
            "detail": "此刑配置产生-{points}的内部摩擦。刑通常与因果教训或自我破坏模式相关。",
            "meaning": "刑表明需要自我反思和个人成长的领域。",
            "advice": "有意识地面对时，刑的能量可以转化为自我提升。",
            "types": {
                "shi": "势刑 - 涉及权力动态的冲突",
                "wu_li": "无礼刑 - 社交摩擦和礼仪问题",
                "en": "恩刑 - 关系不平衡和忘恩负义",
                "zi": "自刑 - 内心挣扎和自我批评",
            },
        },
        "icon": "punishment",
        "color_key": "punishment",
    },

    "HARMS": {
        "category": "conflict",
        "polarity": "negative",
        "en": {
            "title": "Harm",
            "summary": "{branch1} and {branch2} form a harm relationship, causing hidden damage.",
            "detail": "The harm between {branch1} and {branch2} creates subtle but persistent negative effects worth -{points}. Unlike clashes, harms work slowly over time.",
            "meaning": "Harm relationships often manifest as chronic issues, lingering resentments, or slow-building problems.",
            "advice": "Address underlying issues proactively before they accumulate.",
        },
        "zh": {
            "title": "害",
            "summary": "{branch1_zh}与{branch2_zh}形成害关系，造成隐性损害。",
            "detail": "{branch1_zh}与{branch2_zh}之间的害产生-{points}的微妙但持续的负面影响。与冲不同，害是慢慢积累的。",
            "meaning": "害关系通常表现为慢性问题、挥之不去的怨恨或逐渐积累的问题。",
            "advice": "在问题积累前主动解决根本问题。",
        },
        "icon": "harm",
        "color_key": "harm",
    },

    "DESTRUCTION": {
        "category": "conflict",
        "polarity": "negative",
        "en": {
            "title": "Destruction",
            "summary": "{branch1} and {branch2} form a destruction pattern, breaking down structures.",
            "detail": "This destruction relationship creates disruptive energy worth -{points}. It tends to break down existing structures and systems.",
            "meaning": "Destruction can clear away what no longer serves, but may feel destabilizing.",
            "advice": "Use this energy for necessary endings and clearing of obstacles.",
        },
        "zh": {
            "title": "破",
            "summary": "{branch1_zh}与{branch2_zh}形成破的关系，打破结构。",
            "detail": "此破关系产生-{points}的破坏性能量。它倾向于打破现有结构和系统。",
            "meaning": "破可以清除不再有用的事物，但可能让人感到不稳定。",
            "advice": "利用这种能量进行必要的结束和清除障碍。",
        },
        "icon": "destruction",
        "color_key": "destruction",
    },

    "STEM_CONFLICTS": {
        "category": "conflict",
        "polarity": "negative",
        "en": {
            "title": "Stem Conflict",
            "summary": "{stem1} conflicts with {stem2} through the control cycle.",
            "detail": "The heavenly stem {stem1} controls {stem2}, creating tension worth -{points}. This represents external pressure or authority conflicts.",
            "meaning": "Stem conflicts often manifest as challenges from authority, competition, or external constraints.",
            "advice": "Work with the energy rather than against it. The controlling element may offer valuable structure.",
        },
        "zh": {
            "title": "天干克",
            "summary": "{stem1_zh}通过相克关系克制{stem2_zh}。",
            "detail": "天干{stem1_zh}克制{stem2_zh}，产生-{points}的紧张。这代表外部压力或权威冲突。",
            "meaning": "天干克通常表现为来自权威的挑战、竞争或外部约束。",
            "advice": "顺应能量而非对抗。克制的五行可能提供有价值的结构。",
        },
        "icon": "stem_conflict",
        "color_key": "conflict",
    },

    # Alternate key names (for backward compatibility)
    "STEM_CONFLICT": {
        "category": "conflict",
        "polarity": "negative",
        "en": {
            "title": "Stem Conflict",
            "summary": "Heavenly stems in conflict through the control cycle.",
            "detail": "A stem controls another, creating tension and representing external pressure.",
            "meaning": "This may manifest as challenges from authority, competition, or external constraints.",
        },
        "zh": {
            "title": "天干克",
            "summary": "天干通过相克关系产生冲突。",
            "detail": "一个天干克制另一个，产生紧张，代表外部压力。",
            "meaning": "这可能表现为来自权威的挑战、竞争或外部约束。",
        },
        "icon": "stem_conflict",
        "color_key": "conflict",
    },

    "STEM_COMBINATION": {
        "category": "combination",
        "polarity": "positive",
        "en": {
            "title": "Stem Combination",
            "summary": "Heavenly stems combine harmoniously, generating new energy.",
            "detail": "Two heavenly stems form one of the five stem pairs, creating harmonious energy.",
            "meaning": "Stem combinations indicate periods of cooperation, partnership, and merged energies.",
        },
        "zh": {
            "title": "天干合",
            "summary": "天干和谐相合，产生新能量。",
            "detail": "两个天干形成五合之一，产生和谐的能量。",
            "meaning": "天干合表示合作、伙伴关系和能量融合的时期。",
        },
        "icon": "stem_combo",
        "color_key": "combination",
    },

    "CLASH": {
        "category": "conflict",
        "polarity": "negative",
        "en": {
            "title": "Clash",
            "summary": "Earthly branches clash directly, creating tension and disruption.",
            "detail": "Opposition of earthly branches generates conflict. Clashes bring sudden changes, obstacles, or breaking of existing patterns.",
            "meaning": "This clash may manifest as unexpected changes, disagreements, or the need to let go of something.",
            "advice": "Clashes often precede necessary transformations. Stay adaptable and avoid forcing situations.",
        },
        "zh": {
            "title": "冲",
            "summary": "地支直接冲突，造成紧张和干扰。",
            "detail": "地支的对冲产生冲突。冲带来突然变化、障碍或打破现有模式。",
            "meaning": "此冲可能表现为意外变化、分歧或需要放手某事。",
            "advice": "冲往往预示必要的转变。保持灵活，避免强求。",
        },
        "icon": "clash",
        "color_key": "conflict",
    },

    "HARM": {
        "category": "conflict",
        "polarity": "negative",
        "en": {
            "title": "Harm",
            "summary": "Earthly branches form a harm relationship, causing hidden damage.",
            "detail": "Harm creates subtle but persistent negative effects. Unlike clashes, harms work slowly over time.",
            "meaning": "Harm relationships often manifest as chronic issues, lingering resentments, or slow-building problems.",
            "advice": "Address underlying issues proactively before they accumulate.",
        },
        "zh": {
            "title": "害",
            "summary": "地支形成害关系，造成隐性损害。",
            "detail": "害产生微妙但持续的负面影响。与冲不同，害是慢慢积累的。",
            "meaning": "害关系通常表现为慢性问题、挥之不去的怨恨或逐渐积累的问题。",
            "advice": "在问题积累前主动解决根本问题。",
        },
        "icon": "harm",
        "color_key": "harm",
    },

    "HALF_MEETING": {
        "category": "combination",
        "polarity": "positive",
        "en": {
            "title": "Half Meeting",
            "summary": "Partial Three Meeting pattern forming toward an element.",
            "detail": "Two of the three branches needed for a full Three Meeting are present, creating partial element energy.",
            "meaning": "This indicates potential for enhancement if the missing branch appears in luck cycles.",
        },
        "zh": {
            "title": "半会",
            "summary": "部分三会局正在形成。",
            "detail": "三会所需的三个地支中有两个出现，产生部分五行能量。",
            "meaning": "如果缺失的地支出现在运势周期中，有增强潜力。",
        },
        "icon": "half_meeting",
        "color_key": "combination",
    },

    "ARCHED_COMBINATION": {
        "category": "combination",
        "polarity": "positive",
        "en": {
            "title": "Arched Combination",
            "summary": "Branches arch over missing branch to form element energy.",
            "detail": "Although one branch is missing, the present branches reach across to create partial energy.",
            "meaning": "This arched connection provides subtle but present element influence.",
        },
        "zh": {
            "title": "拱合",
            "summary": "地支拱合形成五行能量。",
            "detail": "虽然缺少一个地支，但现有地支跨越形成部分能量。",
            "meaning": "这种拱合连接提供微妙但存在的五行影响。",
        },
        "icon": "arch",
        "color_key": "combination",
    },

    "HALF_COMBINATION": {
        "category": "combination",
        "polarity": "positive",
        "en": {
            "title": "Half Combination",
            "summary": "{branches} form a Half Combination toward {element}.",
            "detail": "Two branches of a Three Combinations pattern are present, generating {points} of partial {element} energy.",
            "meaning": "The combination is incomplete but still provides beneficial {element} influence.",
        },
        "zh": {
            "title": "半合",
            "summary": "{branches_zh}形成半合{element_zh}局。",
            "detail": "三合的两个地支出现，产生{points}的部分{element_zh}能量。",
            "meaning": "组合不完整但仍提供有益的{element_zh}影响。",
        },
        "icon": "half_combo",
        "color_key": "combination",
    },

    # =====================
    # CROSS-PILLAR INTERACTIONS
    # =====================
    "CROSS_PILLAR_WUXING": {
        "category": "energy",
        "polarity": "neutral",
        "en": {
            "title": "Cross-Pillar WuXing",
            "summary": "Energy flows between pillars through the WuXing cycle.",
            "detail": "The heavenly stem and earthly branch interact across different pillars, creating {interaction_type} relationship.",
            "meaning": "This cross-pillar connection shows how different areas of your life influence each other.",
        },
        "zh": {
            "title": "跨柱五行",
            "summary": "五行能量在柱间流动。",
            "detail": "天干和地支跨越不同柱位互动，形成{interaction_type_zh}关系。",
            "meaning": "这种跨柱连接展示了您生活不同领域如何相互影响。",
        },
        "icon": "cross_pillar",
        "color_key": "energy",
    },

    # =====================
    # SPECIAL INTERACTIONS
    # =====================
    "SEASONAL_ADJUSTMENT": {
        "category": "seasonal",
        "polarity": "neutral",
        "en": {
            "title": "Seasonal Influence",
            "summary": "{element} is {state} during {season}.",
            "detail": "The seasonal state of {element} ({state_zh}/{state}) affects its strength by {multiplier}x.",
            "meaning": "Elements wax and wane with the seasons, affecting their influence in your chart during different times.",
            "states": {
                "Prosperous": "At peak strength - this element dominates the season",
                "Strengthening": "Growing in power - preparing to become prosperous",
                "Resting": "Neutral - neither strengthened nor weakened",
                "Trapped": "Weakened - restricted by the dominant seasonal energy",
                "Dead": "At lowest strength - completely suppressed this season",
            },
        },
        "zh": {
            "title": "季节影响",
            "summary": "{element_zh}在{season_zh}为{state_zh}。",
            "detail": "{element_zh}的季节状态（{state_zh}）影响其强度{multiplier}倍。",
            "meaning": "五行随季节消长，在不同时期影响命盘中的作用。",
            "states": {
                "Prosperous": "旺 - 处于巅峰力量，此五行主宰季节",
                "Strengthening": "相 - 力量增长，准备变旺",
                "Resting": "休 - 中性，既不增强也不减弱",
                "Trapped": "囚 - 减弱，受季节主导能量限制",
                "Dead": "死 - 最低力量，本季完全被压制",
            },
        },
        "icon": "season",
        "color_key": "seasonal",
    },

    "ENERGY_FLOW": {
        "category": "energy",
        "polarity": "positive",
        "en": {
            "title": "Energy Flow",
            "summary": "{producer} naturally produces {receiver} through the generation cycle.",
            "detail": "The natural flow of energy from {producer} ({element1}) to {receiver} ({element2}) creates +{points} qi. This represents nurturing and supportive relationships.",
            "meaning": "Energy flows indicate areas where support and growth come naturally.",
        },
        "zh": {
            "title": "能量流动",
            "summary": "{producer_zh}通过相生循环自然生养{receiver_zh}。",
            "detail": "从{producer_zh}（{element1_zh}）到{receiver_zh}（{element2_zh}）的自然能量流动产生+{points}气。这代表滋养和支持的关系。",
            "meaning": "能量流动表明支持和成长自然而然的领域。",
        },
        "icon": "flow",
        "color_key": "generation",
    },

    # =====================
    # ELEMENT BALANCE NARRATIVES
    # =====================
    "ELEMENT_EXCESS": {
        "category": "balance",
        "polarity": "negative",
        "en": {
            "title": "Element Excess",
            "summary": "Your chart shows excess {element} energy ({percentage}%).",
            "detail": "With {element} significantly above average (20% balanced), there may be imbalances. {element} excess can manifest as: {manifestations}",
            "meaning": "Consider activities and environments that balance {element} with its controlling element ({controller}).",
        },
        "zh": {
            "title": "五行过旺",
            "summary": "您的命盘显示{element_zh}能量过旺（{percentage}%）。",
            "detail": "{element_zh}明显高于平均值（平衡为20%），可能存在失衡。{element_zh}过旺可能表现为：{manifestations_zh}",
            "meaning": "考虑用其克制五行（{controller_zh}）来平衡{element_zh}的活动和环境。",
        },
        "icon": "excess",
        "color_key": "warning",
    },

    "ELEMENT_DEFICIENCY": {
        "category": "balance",
        "polarity": "negative",
        "en": {
            "title": "Element Deficiency",
            "summary": "Your chart shows deficient {element} energy ({percentage}%).",
            "detail": "With {element} significantly below average, certain areas may feel lacking. {element} deficiency can manifest as: {manifestations}",
            "meaning": "Consider activities and environments that strengthen {element} or its supporting element ({producer}).",
        },
        "zh": {
            "title": "五行不足",
            "summary": "您的命盘显示{element_zh}能量不足（{percentage}%）。",
            "detail": "{element_zh}明显低于平均值，某些领域可能感到欠缺。{element_zh}不足可能表现为：{manifestations_zh}",
            "meaning": "考虑增强{element_zh}或其相生五行（{producer_zh}）的活动和环境。",
        },
        "icon": "deficiency",
        "color_key": "warning",
    },

    # =====================
    # DAYMASTER NARRATIVES
    # =====================
    "DAYMASTER_STRONG": {
        "category": "daymaster",
        "polarity": "positive",
        "en": {
            "title": "Strong Daymaster",
            "summary": "Your {daymaster} daymaster is strong ({percentage}% support).",
            "detail": "A strong daymaster indicates robust self-energy, confidence, and resilience. You may benefit from elements that provide outlets (output, wealth) rather than more support.",
            "meaning": "Strong charts do well with challenges and can handle pressure effectively.",
        },
        "zh": {
            "title": "身强",
            "summary": "您的{daymaster_zh}日主身强（{percentage}%支持）。",
            "detail": "身强表示强健的自我能量、自信和韧性。您可能受益于提供出口（食伤、财）的五行而非更多支持。",
            "meaning": "身强的命盘善于应对挑战，能有效处理压力。",
        },
        "icon": "strong",
        "color_key": "positive",
    },

    "DAYMASTER_BALANCED": {
        "category": "daymaster",
        "polarity": "neutral",
        "en": {
            "title": "Balanced Daymaster",
            "summary": "Your {daymaster} daymaster is balanced ({percentage}% support).",
            "detail": "A balanced daymaster (35-45% support) has adequate self-energy without excess. This provides flexibility - you can handle both opportunities and challenges. The key is maintaining balance through activities that don't tip too far in either direction.",
            "meaning": "Balanced charts are versatile and adaptable. Focus on harmonizing all five elements rather than strengthening or draining.",
        },
        "zh": {
            "title": "身中和",
            "summary": "您的{daymaster_zh}日主中和（{percentage}%支持）。",
            "detail": "中和日主（35-45%支持）有充足的自我能量而不过盛。这提供了灵活性 - 您可以处理机遇和挑战。关键是通过不偏向任一方向的活动保持平衡。",
            "meaning": "中和的命盘多才多艺且适应力强。专注于协调五行而非增强或消耗。",
        },
        "icon": "balanced",
        "color_key": "neutral",
    },

    "DAYMASTER_WEAK": {
        "category": "daymaster",
        "polarity": "neutral",
        "en": {
            "title": "Weak Daymaster",
            "summary": "Your {daymaster} daymaster is weak ({percentage}% support).",
            "detail": "A weak daymaster (below 35% support) benefits from supportive elements (resource, friend/rob wealth) to strengthen self-energy. Avoid overextending or taking on too much pressure.",
            "meaning": "Weak charts benefit from support, collaboration, and choosing battles wisely.",
        },
        "zh": {
            "title": "身弱",
            "summary": "您的{daymaster_zh}日主身弱（{percentage}%支持）。",
            "detail": "身弱日主（低于35%支持）受益于支持性五行（印、比劫）来增强自我能量。避免过度扩张或承担太大压力。",
            "meaning": "身弱的命盘受益于支持、合作和明智选择战斗。",
        },
        "icon": "weak",
        "color_key": "neutral",
    },

    # =====================
    # WEALTH STORAGE NARRATIVES
    # =====================
    "WEALTH_STORAGE_OPENED": {
        "category": "wealth",
        "polarity": "positive",
        "en": {
            "title": "Wealth Storage Opened",
            "summary": "Your {storage_branch} wealth storage is opened by {opener}.",
            "detail": "The {storage_branch} stores {stored_element} (your wealth element). With {opener} present, this storage is 'opened' - wealth becomes accessible and can flow more freely.",
            "meaning": "This is generally favorable for financial matters and material acquisition.",
        },
        "zh": {
            "title": "财库开启",
            "summary": "您的{storage_branch_zh}财库被{opener_zh}开启。",
            "detail": "{storage_branch_zh}储存{stored_element_zh}（您的财元素）。有{opener_zh}存在，财库被「开启」- 财富变得可获取，流动更自由。",
            "meaning": "这通常对财务事项和物质获取有利。",
        },
        "icon": "wealth_open",
        "color_key": "wealth",
    },

    "WEALTH_STORAGE_CLOSED": {
        "category": "wealth",
        "polarity": "neutral",
        "en": {
            "title": "Wealth Storage Present",
            "summary": "You have {storage_branch} as a wealth storage branch.",
            "detail": "The {storage_branch} stores {stored_element}. However, without its opener ({opener}), the wealth remains stored and less accessible.",
            "meaning": "Wealth may accumulate but require effort or timing to access. Look for the opener in luck cycles.",
        },
        "zh": {
            "title": "财库存在",
            "summary": "您有{storage_branch_zh}作为财库。",
            "detail": "{storage_branch_zh}储存{stored_element_zh}。然而，没有其开启者（{opener_zh}），财富保持储存状态，较难获取。",
            "meaning": "财富可能积累但需要努力或时机来获取。在运势周期中寻找开启者。",
        },
        "icon": "wealth_closed",
        "color_key": "neutral",
    },

    # =====================
    # TEN GODS NARRATIVES
    # =====================
    "TEN_GOD_WARNING": {
        "category": "ten_gods",
        "polarity": "negative",
        "en": {
            "title": "{ten_god_english} Affected",
            "summary": "{pillar_name} {ten_god_english}: {message}",
            "detail": "The {ten_god_english} represents {ten_god_meaning}. When affected by conflict, these areas require attention.",
            "meaning": "Consider how this Ten God relationship impacts the associated life areas.",
        },
        "zh": {
            "title": "{ten_god_chinese}受影响",
            "summary": "{pillar_name_zh}的{ten_god_chinese}：{message_zh}",
            "detail": "{ten_god_chinese}代表{ten_god_meaning_zh}。受冲克时，这些领域需要关注。",
            "meaning": "考虑此十神关系如何影响相关生活领域。",
        },
        "icon": "warning",
        "color_key": "warning",
    },

    "TEN_GOD_OPPORTUNITY": {
        "category": "ten_gods",
        "polarity": "positive",
        "en": {
            "title": "{ten_god_english} Opportunity",
            "summary": "{pillar_name} {ten_god_english}: {message}",
            "detail": "The {ten_god_english} is supported, bringing positive influence to its associated areas.",
            "meaning": "This is a favorable configuration for {ten_god_meaning}.",
        },
        "zh": {
            "title": "{ten_god_chinese}机遇",
            "summary": "{pillar_name_zh}的{ten_god_chinese}：{message_zh}",
            "detail": "{ten_god_chinese}得到支持，为相关领域带来积极影响。",
            "meaning": "这是{ten_god_meaning_zh}的有利配置。",
        },
        "icon": "opportunity",
        "color_key": "positive",
    },

    # =====================
    # PILLAR ANALYSIS NARRATIVES
    # =====================
    "PILLAR_ANALYSIS": {
        "category": "pillar",
        "polarity": "neutral",
        "en": {
            "title": "{pillar_name} Analysis",
            "summary": "{stem} {branch}: {stem_element} over {branch_element}",
            "detail": "This pillar represents {pillar_represents}. The heavenly stem {stem} ({stem_element}) sits over earthly branch {branch} ({branch_element}).",
            "meaning": "The stem-branch relationship influences how this life area manifests.",
        },
        "zh": {
            "title": "{pillar_name_zh}分析",
            "summary": "{stem_zh}{branch_zh}：{stem_element_zh}坐{branch_element_zh}",
            "detail": "此柱代表{pillar_represents_zh}。天干{stem_zh}（{stem_element_zh}）坐地支{branch_zh}（{branch_element_zh}）。",
            "meaning": "干支关系影响此生活领域的表现方式。",
        },
        "icon": "pillar",
        "color_key": "neutral",
    },
}

# =============================================================================
# ELEMENT MANIFESTATION DESCRIPTIONS
# =============================================================================
# Describes how excess or deficiency of each element might manifest

ELEMENT_MANIFESTATIONS = {
    "Wood": {
        "excess": {
            "en": "impulsiveness, anger, excessive growth without direction, liver/gallbladder stress",
            "zh": "冲动、愤怒、无方向的过度扩张、肝胆压力",
        },
        "deficiency": {
            "en": "lack of direction, poor planning, weakness in tendons/muscles, indecisiveness",
            "zh": "缺乏方向、规划不佳、筋肉虚弱、优柔寡断",
        },
    },
    "Fire": {
        "excess": {
            "en": "anxiety, restlessness, heart stress, scattered energy, overexcitement",
            "zh": "焦虑、躁动、心脏压力、精力分散、过度兴奋",
        },
        "deficiency": {
            "en": "lack of joy, poor circulation, depression, difficulty expressing warmth",
            "zh": "缺乏喜悦、循环不佳、抑郁、难以表达温暖",
        },
    },
    "Earth": {
        "excess": {
            "en": "overthinking, worry, digestive issues, stubbornness, excessive caution",
            "zh": "过度思虑、担忧、消化问题、固执、过度谨慎",
        },
        "deficiency": {
            "en": "instability, lack of grounding, poor digestion, inability to nurture",
            "zh": "不稳定、缺乏根基、消化不良、无法滋养",
        },
    },
    "Metal": {
        "excess": {
            "en": "rigidity, grief held too long, respiratory issues, excessive judgment",
            "zh": "僵化、悲伤过久、呼吸问题、过度评判",
        },
        "deficiency": {
            "en": "lack of boundaries, respiratory weakness, inability to let go, poor structure",
            "zh": "缺乏边界、呼吸虚弱、无法放手、结构松散",
        },
    },
    "Water": {
        "excess": {
            "en": "fear, coldness, isolation, kidney/bladder stress, excessive introspection",
            "zh": "恐惧、冷漠、孤立、肾膀胱压力、过度内省",
        },
        "deficiency": {
            "en": "lack of wisdom, poor adaptability, kidney weakness, fear of the unknown",
            "zh": "缺乏智慧、适应力差、肾虚、对未知的恐惧",
        },
    },
}

# =============================================================================
# PILLAR POSITION CONTEXT
# =============================================================================
# Describes the meaning of interactions based on pillar position

PILLAR_CONTEXT = {
    "hour": {
        "en": {
            "name": "Hour Pillar",
            "represents": "children, students, subordinates, late life, inner self",
            "timing": "later years (after 50), daily details",
        },
        "zh": {
            "name": "时柱",
            "represents": "子女、学生、下属、晚年、内在自我",
            "timing": "晚年（50岁后）、日常细节",
        },
    },
    "day": {
        "en": {
            "name": "Day Pillar",
            "represents": "self, spouse, marriage, core identity",
            "timing": "middle age (35-50), personal matters",
        },
        "zh": {
            "name": "日柱",
            "represents": "自己、配偶、婚姻、核心身份",
            "timing": "中年（35-50岁）、个人事务",
        },
    },
    "month": {
        "en": {
            "name": "Month Pillar",
            "represents": "parents, career, social status, achievements",
            "timing": "early adulthood (18-35), career matters",
        },
        "zh": {
            "name": "月柱",
            "represents": "父母、事业、社会地位、成就",
            "timing": "青年（18-35岁）、事业事务",
        },
    },
    "year": {
        "en": {
            "name": "Year Pillar",
            "represents": "ancestors, grandparents, early environment, foundation",
            "timing": "childhood (0-18), foundation and origins",
        },
        "zh": {
            "name": "年柱",
            "represents": "祖先、祖父母、早期环境、根基",
            "timing": "童年（0-18岁）、根基和起源",
        },
    },
    "luck_10y": {
        "en": {
            "name": "10-Year Luck",
            "represents": "major life phase, decade themes, significant opportunities",
            "timing": "current decade of life",
        },
        "zh": {
            "name": "大运",
            "represents": "人生主要阶段、十年主题、重大机遇",
            "timing": "当前人生十年",
        },
    },
    "annual": {
        "en": {
            "name": "Annual Luck",
            "represents": "yearly themes, seasonal opportunities, annual focus",
            "timing": "current year",
        },
        "zh": {
            "name": "流年",
            "represents": "年度主题、季节机遇、年度重点",
            "timing": "当前年份",
        },
    },
    "monthly": {
        "en": {
            "name": "Monthly Luck",
            "represents": "monthly rhythms, short-term focus, immediate concerns",
            "timing": "current month",
        },
        "zh": {
            "name": "流月",
            "represents": "月度节奏、短期重点、即时关注",
            "timing": "当前月份",
        },
    },
    "daily": {
        "en": {
            "name": "Daily Luck",
            "represents": "daily energy, immediate timing, specific events",
            "timing": "current day",
        },
        "zh": {
            "name": "流日",
            "represents": "每日能量、即时时机、具体事件",
            "timing": "当前日期",
        },
    },
}
