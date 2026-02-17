# =============================================================================
# TEMPLATE LIBRARY FOR INTERPRETATIONS
# =============================================================================
# Zero LLM — all interpretations are template-based with multiple
# phrasing variants for freshness.
# random.choice selects a variant at generation time.
# =============================================================================

import random
from typing import List, Dict, Optional


def _pick(variants: List[str]) -> str:
    """Pick a random variant from a list."""
    return random.choice(variants) if variants else ""


# =============================================================================
# DAY MASTER NATURE TEMPLATES
# =============================================================================

DM_NATURE = {
    ("Wood", "Yang"): {
        "name": "Jia Wood",
        "chinese": "甲木",
        "nature": [
            "Jia Wood = a giant tree. Tall, upright, principled, and immovable once rooted.",
            "Jia Wood is the towering oak. Strong convictions, natural leadership, rigid when challenged.",
            "As the great tree, Jia Wood stands firm with deep roots. Noble but stubborn.",
        ],
        "personality": "ambitious, principled, stubborn, leadership-oriented",
    },
    ("Wood", "Yin"): {
        "name": "Yi Wood",
        "chinese": "乙木",
        "nature": [
            "Yi Wood = flexible vine or grass. Adaptable, gentle, artistic, bends but doesn't break.",
            "Yi Wood is the climbing ivy. Finds support wherever it goes, flexible and resilient.",
            "As the delicate flower, Yi Wood is soft outside but surprisingly strong within.",
        ],
        "personality": "adaptable, diplomatic, artistic, people-pleasing",
    },
    ("Fire", "Yang"): {
        "name": "Bing Fire",
        "chinese": "丙火",
        "nature": [
            "Bing Fire = the blazing sun. Generous, warm, visible, center of attention.",
            "Bing Fire is the sun itself. Illuminates everything, generous to a fault, craves spotlight.",
            "As the great fireball in the sky, Bing Fire is impossible to ignore — warm, bright, and dominating.",
        ],
        "personality": "generous, attention-seeking, optimistic, impatient",
    },
    ("Fire", "Yin"): {
        "name": "Ding Fire",
        "chinese": "丁火",
        "nature": [
            "Ding Fire = candlelight or torch. Focused, warm, intimate, illuminates selectively.",
            "Ding Fire is the candle flame. Small but intense, mysterious, sees through darkness.",
            "As the flickering flame, Ding Fire is perceptive, sensitive, and quietly powerful.",
        ],
        "personality": "perceptive, sensitive, moody, spiritually inclined",
    },
    ("Earth", "Yang"): {
        "name": "Wu Earth",
        "chinese": "戊土",
        "nature": [
            "Wu Earth = the great mountain. Solid, reliable, unmovable, patient to a fault.",
            "Wu Earth is Mount Tai. Massive presence, dependable, but can be heavy and slow.",
            "As the mountain, Wu Earth is the rock others lean on — sturdy but sometimes crushingly heavy.",
        ],
        "personality": "reliable, patient, stubborn, protective, slow-to-change",
    },
    ("Earth", "Yin"): {
        "name": "Ji Earth",
        "chinese": "己土",
        "nature": [
            "Ji Earth = farmland soil. Nurturing, fertile, absorbs everything, endlessly giving.",
            "Ji Earth is the garden bed. Produces abundance, accepts all inputs, sometimes overwhelmed.",
            "As cultivated earth, Ji Earth is warm, accommodating, and endlessly productive.",
        ],
        "personality": "nurturing, accommodating, worrisome, detail-oriented",
    },
    ("Metal", "Yang"): {
        "name": "Geng Metal",
        "chinese": "庚金",
        "nature": [
            "Geng Metal = the battle axe or raw ore. Tough, decisive, sharp, confrontational.",
            "Geng Metal is the warrior's blade. Cuts through problems, sometimes cuts friends too.",
            "As raw iron, Geng Metal is blunt, strong, and unyielding — respects strength above all.",
        ],
        "personality": "decisive, blunt, confrontational, loyal, justice-oriented",
    },
    ("Metal", "Yin"): {
        "name": "Xin Metal",
        "chinese": "辛金",
        "nature": [
            "Xin Metal = polished jewelry or refined gem. Beautiful, sensitive, perfectionist.",
            "Xin Metal is the diamond. Brilliant under pressure, sharp-tongued, aesthetically driven.",
            "As the jewel, Xin Metal is refined, particular, and quietly cutting.",
        ],
        "personality": "refined, sensitive, perfectionist, critical, elegant",
    },
    ("Water", "Yang"): {
        "name": "Ren Water",
        "chinese": "壬水",
        "nature": [
            "Ren Water = the vast ocean or rushing river. Expansive, powerful, hard to contain.",
            "Ren Water is the great river. Flows with unstoppable force, ambitious, restless.",
            "As the ocean, Ren Water is deep, mysterious, and carries immense hidden power.",
        ],
        "personality": "ambitious, restless, intelligent, risk-taking, freedom-loving",
    },
    ("Water", "Yin"): {
        "name": "Gui Water",
        "chinese": "癸水",
        "nature": [
            "Gui Water = morning dew or gentle rain. Subtle, nourishing, intuitive, dissolves quietly.",
            "Gui Water is the rain cloud. Nourishes everything it touches, but often overlooked.",
            "As the dew drop, Gui Water is delicate, perceptive, and quietly powerful in persistence.",
        ],
        "personality": "intuitive, gentle, perceptive, quietly persistent, easily overwhelmed",
    },
}


# =============================================================================
# DM STRENGTH VERDICT TEMPLATES
# =============================================================================

STRENGTH_VERDICTS = {
    "extremely_strong": [
        "The Day Master is EXTREMELY STRONG. There is overwhelming support with very little opposition.",
        "This Day Master has far too much fuel. Energy is excessive — needs heavy draining.",
        "Extremely strong chart. The DM dominates everything, which creates imbalance.",
    ],
    "strong": [
        "The Day Master is STRONG. Good seasonal support and roots, but slightly top-heavy.",
        "A strong Day Master. Well-supported but needs more outlets to avoid stagnation.",
        "The DM is strong — above the balance point. Needs draining elements to thrive.",
    ],
    "neutral": [
        "The Day Master is NEUTRAL — reasonably balanced between support and drain.",
        "A balanced Day Master. Neither too strong nor too weak — flexible and adaptable.",
        "The DM sits near the balance point. Small shifts in luck pillars matter greatly.",
    ],
    "weak": [
        "The Day Master is WEAK. Insufficient support, overwhelmed by draining forces.",
        "A weak Day Master. Too many demands (wealth, output, officer) with not enough backing.",
        "The DM is weak — needs resource and companion elements urgently.",
    ],
    "extremely_weak": [
        "The Day Master is EXTREMELY WEAK. Almost no support, completely overwhelmed by opposition.",
        "This is a severely depleted Day Master. The chart may qualify as a Following Chart (从格).",
        "Extremely weak DM. Without strong roots, this person is at the mercy of external forces.",
    ],
}


# =============================================================================
# TEN GOD INTERPRETATION TEMPLATES
# =============================================================================

TEN_GOD_INTERPRETATIONS = {
    "F": {
        "PROMINENT": [
            "Friend (比肩) is PROMINENT — strong self-identity, competitive nature, many rivals in same field.",
            "Prominent Friend means fierce independence and competition. Wealth is shared or fought over.",
        ],
        "PRESENT": ["Friend (比肩) is present — healthy self-confidence and peer connections."],
        "ABSENT": ["Friend (比肩) is absent — lacks peer support, feels isolated in their field."],
    },
    "RW": {
        "PROMINENT": [
            "Rob Wealth (劫財) is PROMINENT — this is a major red flag for finances. Money comes and goes. Partnerships drain wealth. Competitive spending.",
            "Prominent Rob Wealth = money bleeds out. Others take what should be yours.",
        ],
        "PRESENT": ["Rob Wealth (劫財) is present — some financial leakage through competition."],
        "ABSENT": ["Rob Wealth (劫財) is absent — fewer competitors for resources."],
    },
    "EG": {
        "PROMINENT": [
            "Eating God (食神) is PROMINENT — creative talent, good appetite for life, but can be lazy.",
            "Prominent Eating God = artistic nature, food/lifestyle focus, natural optimism.",
        ],
        "PRESENT": ["Eating God (食神) is present — healthy creative outlet and enjoyment of life."],
        "ABSENT": ["Eating God (食神) is absent — lacks natural creative expression and easy joy."],
    },
    "HO": {
        "PROMINENT": [
            "Hurting Officer (傷官) is PROMINENT — brilliant but rebellious. Conflicts with authority are inevitable. Sharp tongue causes relationship damage.",
            "Prominent Hurting Officer = genius-level creativity but destructive to rules, bosses, and marriage.",
        ],
        "PRESENT": ["Hurting Officer (傷官) is present — creative edge with some authority conflicts."],
        "ABSENT": ["Hurting Officer (傷官) is absent — more conformist, less creative rebellion."],
    },
    "IW": {
        "PROMINENT": [
            "Indirect Wealth (偏財) is PROMINENT — windfall potential, generous with money, gambling tendency.",
            "Prominent Indirect Wealth = lucky with unexpected money, but also prone to risky ventures.",
        ],
        "PRESENT": ["Indirect Wealth (偏財) is present — some unexpected income opportunities."],
        "ABSENT": ["Indirect Wealth (偏財) is absent — windfall opportunities rare, must earn steadily."],
    },
    "DW": {
        "PROMINENT": [
            "Direct Wealth (正財) is PROMINENT — responsible with money, steady income, strong spouse bond (male).",
            "Prominent Direct Wealth = financially capable, loyal partner (for males = wife star).",
        ],
        "PRESENT": ["Direct Wealth (正財) is present — stable finances and commitment capacity."],
        "ABSENT": [
            "Direct Wealth (正財) is ABSENT — difficulty with stable income and committed relationships.",
            "Direct Wealth absent = for males, the wife star is missing. Marriage comes late or with difficulty.",
        ],
    },
    "7K": {
        "PROMINENT": [
            "Seven Killings (七殺) is PROMINENT — aggressive drive, power-hungry, risk of violence or legal issues.",
            "Prominent Seven Killings = intense ambition, domineering nature, fearless but dangerous.",
        ],
        "PRESENT": ["Seven Killings (七殺) is present — some authority and competitive edge."],
        "ABSENT": ["Seven Killings (七殺) is absent — less aggressive drive, fewer enemies."],
    },
    "DO": {
        "PROMINENT": [
            "Direct Officer (正官) is PROMINENT — disciplined, rule-following, career-focused, respected.",
            "Prominent Direct Officer = natural authority, good reputation, but can be rigid.",
        ],
        "PRESENT": ["Direct Officer (正官) is present — reasonable discipline and career structure."],
        "ABSENT": [
            "Direct Officer (正官) is ABSENT — lacks discipline and career structure.",
            "Direct Officer absent = for females, the husband star is missing. Marriage difficulty.",
        ],
    },
    "IR": {
        "PROMINENT": [
            "Indirect Resource (偏印) is PROMINENT — unconventional thinking, occult interests, isolation tendency.",
            "Prominent Indirect Resource = brilliant but eccentric. May indicate susceptibility to dark influences.",
        ],
        "PRESENT": ["Indirect Resource (偏印) is present — some unconventional wisdom and backing."],
        "ABSENT": ["Indirect Resource (偏印) is absent — more conventional thinking patterns."],
    },
    "DR": {
        "PROMINENT": [
            "Direct Resource (正印) is PROMINENT — strong support system, education, maternal bond, physical health.",
            "Prominent Direct Resource = well-educated, good health foundation, strong maternal connection.",
        ],
        "PRESENT": ["Direct Resource (正印) is present — reasonable educational and health foundation."],
        "ABSENT": ["Direct Resource (正印) is absent — weaker support system and health foundation."],
    },
}


# =============================================================================
# SHEN SHA IMPACT TEMPLATES
# =============================================================================

SHEN_SHA_IMPACTS = {
    "天乙贵人": {
        "present": [
            "Heavenly Noble — powerful protector. In trouble, help always comes from unexpected sources.",
            "Tian Yi present = a guardian angel energy. People naturally want to help you.",
        ],
        "absent": ["No Heavenly Noble = less natural protection. Must build own safety nets."],
    },
    "太极贵人": {
        "present": ["Tai Ji Noble — spiritual intelligence. Natural affinity for metaphysics and wisdom."],
        "absent": ["No Tai Ji Noble. Less natural spiritual inclination."],
    },
    "天德贵人": {
        "present": ["Heavenly Virtue — moral protection. Reduces severity of misfortune."],
        "absent": ["No Heavenly Virtue. Misfortunes hit at full force."],
    },
    "月德贵人": {
        "present": ["Monthly Virtue — secondary protection layer. Softens monthly negative events."],
        "absent": ["No Monthly Virtue."],
    },
    "文昌贵人": {
        "present": ["Academic Star — strong intellectual capacity, exam luck, writing talent."],
        "absent": ["No Academic Star. Education success requires more effort."],
    },
    "金舆": {
        "present": ["Golden Carriage — material comfort, good vehicles, luxury lifestyle potential."],
        "absent": ["No Golden Carriage."],
    },
    "天厨贵人": {
        "present": ["Heavenly Kitchen — food blessing. Never lacks sustenance, good taste."],
        "absent": ["No Heavenly Kitchen."],
    },
    "禄神": {
        "present": ["Prosperity Star — natural wealth magnet. Income comes relatively easily."],
        "absent": ["No Prosperity Star = wealth must be actively fought for."],
    },
    "将星": {
        "present": ["General Star — leadership energy. Commands respect, natural authority."],
        "absent": ["No General Star = must build authority from scratch."],
    },
    "天医": {
        "present": ["Heavenly Doctor — healing energy. Good constitution or medical talent."],
        "absent": ["No Heavenly Doctor = health needs more active management."],
    },
    "天赦": {
        "present": ["Heavenly Pardon — forgiveness energy. Crimes/mistakes get pardoned."],
        "absent": ["No Heavenly Pardon."],
    },
    "红鸾": {
        "present": ["Red Phoenix — romance star. Strong marriage/relationship energy."],
        "absent": ["No Red Phoenix = romance comes later or with less intensity."],
    },
    "天喜": {
        "present": ["Heavenly Happiness — joy and celebration energy."],
        "absent": ["No Heavenly Happiness."],
    },
    "福星贵人": {
        "present": ["Fortune Star — blessed luck energy. Good fortune surrounds you."],
        "absent": ["No Fortune Star = luck must be earned, not given."],
    },
    "三奇贵人": {
        "present": ["Three Wonders Noble — rare genius-level energy. Extraordinary talent."],
    },
    "羊刃": {
        "present": [
            "Sheep Blade — DANGER. Impulsive energy, risk of injury, surgery, legal issues.",
            "Yang Ren present = double-edged sword. Aggressive power, but self-harm risk.",
        ],
    },
    "空亡": {
        "present": [
            "Void Star — the branch is 'empty'. Whatever that palace governs feels hollow or unfulfilled.",
            "Kong Wang present = emptiness in that life area. Efforts feel futile until void is filled.",
        ],
    },
    "桃花": {
        "present": [
            "Peach Blossom — romantic attraction. Can be blessing (charisma) or curse (affairs).",
            "Tao Hua present = magnetic romantic energy. Context determines if it helps or hurts.",
        ],
    },
    "华盖": {
        "present": [
            "Canopy Star — solitary, spiritual, intellectual. Prefers isolation over crowds.",
            "Hua Gai present = the hermit's star. Deep thinker, but lonely unless embraced.",
        ],
    },
    "驿马": {
        "present": [
            "Traveling Horse — constant motion. Career involves travel, relocation, change.",
            "Yi Ma present = never stays still. Best careers involve movement and variety.",
        ],
    },
    "劫煞": {
        "present": ["Robbery Star — vulnerability to theft, fraud, sudden financial loss."],
    },
    "亡神": {
        "present": ["Lost Spirit — spiritual vulnerability. Scattered energy, loss of focus."],
    },
    "灾煞": {
        "present": ["Disaster Star — vulnerability to natural disasters and sudden misfortune."],
    },
    "天罗": {
        "present": ["Heaven's Net — feeling trapped, especially in legal or relationship matters."],
    },
    "地网": {
        "present": ["Earth's Snare — grounded but trapped. Difficulty escaping situations."],
    },
    "阴差阳错": {
        "present": [
            "Yin-Yang Disharmony Day — CRITICAL marriage indicator. Miscommunication between partners is the default state.",
            "Born on a Yin Cha Yang Cuo day = marriage requires extraordinary effort to maintain.",
        ],
    },
    "孤辰": {
        "present": ["Lonely Star — isolation tendency, especially for males. Difficulty maintaining close bonds."],
    },
    "寡宿": {
        "present": ["Widow Star — loneliness in relationships, especially for females."],
    },
    "四废": {
        "present": ["Four Wastes — DM born in its dead season. Severely weakened constitution."],
    },
    "十恶大败": {
        "present": ["Ten Evils Great Defeat — historical marker for extreme misfortune with wealth."],
    },
    "魁罡": {
        "present": ["Kui Gang — powerful, commanding, but hard on relationships and self."],
    },
    "血刃": {
        "present": ["Blood Blade — risk of surgery, blood-related issues, physical injury."],
    },
    "勾": {
        "present": ["Hook Star — prone to disputes and legal entanglements."],
    },
    "绞": {
        "present": ["Strangle Star — suffocating situations, trapped in conflicts."],
    },
    "丧门": {
        "present": ["Funeral Door — encounters with death, mourning, loss events."],
    },
    "吊客": {
        "present": ["Hanging Guest — attending funerals, dealing with grief."],
    },
    "咸池": {
        "present": ["Salty Pool — sexual excess, addiction tendencies, loss through pleasure."],
    },
    "白虎": {
        "present": ["White Tiger — violent energy. Risk of accidents, surgery, bloodshed."],
    },
    "童子": {
        "present": ["Child Star — soul of a celestial servant. Marriage difficulty, health issues, karmic debt."],
    },
    "財星": {
        "present": ["Wealth Star — small fortune energy. Wealth element naturally present, money comes with less friction."],
        "absent": ["No Wealth Star — wealth element not prominent in chart. Must work harder for financial gains."],
    },
}


# =============================================================================
# BRANCH INTERACTION IMPACT TEMPLATES
# =============================================================================

INTERACTION_IMPACTS = {
    "clash": {
        "year-month": [
            "Clash between Year and Month = conflict between family/roots and career/society.",
            "Year-Month clash = person's background fights against their career path.",
        ],
        "year-day": [
            "Clash between Year and Day = conflict between parents and self/spouse.",
        ],
        "year-hour": [
            "Clash between Year and Hour = ancestry conflicts with children/legacy.",
        ],
        "month-day": [
            "Clash between Month and Day = career and marriage in constant tension.",
        ],
        "month-hour": [
            "Clash between Month and Hour = career and children compete for attention.",
        ],
        "day-hour": [
            "Clash between Day and Hour = self/spouse and children in conflict.",
        ],
        "default": [
            "Clash = direct confrontation between these life areas.",
        ],
    },
    "harmony": {
        "default": [
            "Harmony between these palaces = smooth energy flow, mutual support.",
        ],
    },
    "punishment": {
        "default": [
            "Punishment = karmic conflict. Pain that teaches through suffering.",
        ],
    },
    "harm": {
        "default": [
            "Harm = hidden damage. Subtle undermining between these life areas.",
        ],
    },
}


# =============================================================================
# RED FLAG SEVERITY TEMPLATES
# =============================================================================

SEVERITY_LANGUAGE = {
    "mild": [
        "This is a mild indicator. Noticeable but not life-altering.",
        "Minor flag. Worth awareness but not urgent action.",
    ],
    "moderate": [
        "This is a moderate concern. Requires conscious management.",
        "Moderate flag. Left unchecked, this will create problems.",
    ],
    "severe": [
        "This is SEVERE. Active intervention is required.",
        "Severe indicator. Ignoring this leads to serious consequences.",
    ],
    "critical": [
        "This is CRITICAL. This is not optional — immediate attention needed.",
        "Critical flag. This is the single biggest challenge in this area.",
    ],
}


# =============================================================================
# HEALTH TEMPLATES
# =============================================================================

HEALTH_ELEMENT_MAP = {
    "Wood": {
        "yin_organ": "Liver (肝)",
        "yang_organ": "Gallbladder (胆)",
        "body_parts": "eyes, tendons, nails",
        "excess": "anger, headaches, high blood pressure, eye problems",
        "deficiency": "fatigue, poor vision, weak tendons, indecisiveness",
    },
    "Fire": {
        "yin_organ": "Heart (心)",
        "yang_organ": "Small Intestine (小肠)",
        "body_parts": "tongue, blood vessels, complexion",
        "excess": "anxiety, insomnia, heart palpitations, inflammation",
        "deficiency": "poor circulation, cold extremities, depression, low energy",
    },
    "Earth": {
        "yin_organ": "Spleen (脾)",
        "yang_organ": "Stomach (胃)",
        "body_parts": "mouth, muscles, flesh",
        "excess": "overthinking, bloating, weight gain, obsessive worry",
        "deficiency": "poor digestion, loose muscles, poor appetite, anemia",
    },
    "Metal": {
        "yin_organ": "Lungs (肺)",
        "yang_organ": "Large Intestine (大肠)",
        "body_parts": "nose, skin, body hair",
        "excess": "grief, skin problems, respiratory tightness, constipation",
        "deficiency": "weak immune system, asthma, dry skin, frequent colds",
    },
    "Water": {
        "yin_organ": "Kidneys (肾)",
        "yang_organ": "Bladder (膀胱)",
        "body_parts": "ears, bones, reproductive system",
        "excess": "fear, edema, urinary issues, hormonal excess",
        "deficiency": "lower back pain, weak bones, hearing loss, infertility, premature aging",
    },
}


# =============================================================================
# REMEDY TEMPLATES
# =============================================================================

ELEMENT_REMEDIES = {
    "Wood": {
        "colors": ["green", "emerald", "jade green"],
        "avoid_colors": ["white", "gold", "silver"],
        "industries": ["education", "publishing", "forestry", "fashion", "health food"],
        "environment": ["plants, especially tall leafy ones", "wooden furniture"],
        "direction": "East",
    },
    "Fire": {
        "colors": ["red", "orange", "purple", "pink"],
        "avoid_colors": ["black", "dark blue"],
        "industries": ["technology", "media", "entertainment", "energy", "restaurant"],
        "environment": ["bright lighting", "candles", "south-facing windows"],
        "direction": "South",
    },
    "Earth": {
        "colors": ["yellow", "brown", "beige", "terracotta"],
        "avoid_colors": ["green", "teal"],
        "industries": ["real estate", "construction", "agriculture", "mining", "ceramics"],
        "environment": ["stone/ceramic decor", "crystals", "earth tones"],
        "direction": "Center, Southwest, Northeast",
    },
    "Metal": {
        "colors": ["white", "gold", "silver", "grey"],
        "avoid_colors": ["red", "orange"],
        "industries": ["finance", "engineering", "legal", "automotive", "jewelry"],
        "environment": ["metal objects", "wind chimes", "clean minimalist spaces"],
        "direction": "West, Northwest",
    },
    "Water": {
        "colors": ["black", "dark blue", "navy"],
        "avoid_colors": ["yellow", "brown"],
        "industries": ["shipping", "tourism", "aquaculture", "logistics", "IT/data"],
        "environment": ["water features", "fish tanks", "flowing water sounds"],
        "direction": "North",
    },
}


# =============================================================================
# HONEST SUMMARY TEMPLATES
# =============================================================================

LIFE_LESSON_TEMPLATES = {
    "weak_water": [
        "You are a raindrop trying to survive in a desert of Fire and Earth. "
        "Your life lesson is learning that you cannot do everything alone — "
        "you need to find your river (support systems, right environment) to thrive.",
    ],
    "weak_fire": [
        "You are a candle in a storm. Your life lesson is finding shelter — "
        "the right people, places, and habits that protect your flame.",
    ],
    "weak_wood": [
        "You are a seedling in rocky soil. Your lesson is patience and finding "
        "the right nourishment — Water (wisdom) and Wood (community) are your lifelines.",
    ],
    "weak_earth": [
        "You are fertile soil that's been over-farmed. Your lesson is learning to "
        "set boundaries and stop giving more than you receive.",
    ],
    "weak_metal": [
        "You are a blade that needs sharpening. Your lesson is discipline and "
        "finding the right structure to channel your potential.",
    ],
    "strong_general": [
        "You have abundant energy but it needs direction. Your lesson is "
        "channeling power into productive outlets rather than letting it stagnate.",
    ],
    "following": [
        "Your chart follows the dominant force rather than fighting it. "
        "Your lesson is surrender — not weakness, but strategic alignment with "
        "the universe's flow. Fighting your nature is the worst thing you can do.",
    ],
}
