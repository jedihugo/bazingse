# * =============================================================================
# * BAZI DERIVED - All data derived from STEMS and BRANCHES
# * =============================================================================
# * This file contains ALL derived data, lookups, and utility functions.
# * Everything here is computed from the core.py STEMS and BRANCHES.
# * =============================================================================

from .core import STEMS, BRANCHES

# =============================================================================
# DERIVED: Element Cycles (computed from STEMS)
# =============================================================================
# Build the generating and controlling cycles from stem element relationships

# Get unique elements from stems
ELEMENTS = list(dict.fromkeys(STEMS[s]["element"] for s in STEMS))

# Build generating cycle from Yang stem controls
# Wood→Fire→Earth→Metal→Water→Wood (follows the element order in Yang stems)
_yang_stems = [(s, STEMS[s]) for s in STEMS if STEMS[s]["polarity"] == "Yang"]
_yang_stems.sort(key=lambda x: x[1]["index"])

# The generating cycle: each Yang element generates the next element in Wu Xing order
# We can derive this: the element that a Yang stem's "combination_element" produces
ELEMENT_CYCLES = {
    "generating": {},
    "controlling": {},
}

# Build from the known Wu Xing sequence
_wuxing_order = ["Wood", "Fire", "Earth", "Metal", "Water"]
for i, elem in enumerate(_wuxing_order):
    next_elem = _wuxing_order[(i + 1) % 5]
    ELEMENT_CYCLES["generating"][elem] = next_elem

# Build controlling from the Wu Xing sequence (every 2nd element)
for i, elem in enumerate(_wuxing_order):
    controlled = _wuxing_order[(i + 2) % 5]
    ELEMENT_CYCLES["controlling"][elem] = controlled

# Reverse lookups
ELEMENT_CYCLES["generated_by"] = {v: k for k, v in ELEMENT_CYCLES["generating"].items()}
ELEMENT_CYCLES["controlled_by"] = {v: k for k, v in ELEMENT_CYCLES["controlling"].items()}

# Element Chinese characters
ELEMENT_CHINESE = {"Wood": "木", "Fire": "火", "Earth": "土", "Metal": "金", "Water": "水"}

# =============================================================================
# DERIVED: Day Officers (computed for Dong Gong)
# =============================================================================
DAY_OFFICERS = {
    0: {"id": "Jian", "chinese": "建", "english": "Establish"},
    1: {"id": "Chu", "chinese": "除", "english": "Remove"},
    2: {"id": "Man", "chinese": "滿", "english": "Full"},
    3: {"id": "Ping", "chinese": "平", "english": "Balance"},
    4: {"id": "Ding", "chinese": "定", "english": "Stable"},
    5: {"id": "Zhi", "chinese": "執", "english": "Initiate"},
    6: {"id": "Po", "chinese": "破", "english": "Destruction"},
    7: {"id": "Wei", "chinese": "危", "english": "Danger"},
    8: {"id": "Cheng", "chinese": "成", "english": "Success"},
    9: {"id": "Shou", "chinese": "收", "english": "Receive"},
    10: {"id": "Kai", "chinese": "開", "english": "Open"},
    11: {"id": "Bi", "chinese": "閉", "english": "Close"},
}
DAY_OFFICER_ORDER = [DAY_OFFICERS[i]["id"] for i in range(12)]

# =============================================================================
# DERIVED: Ordered Lists (for index lookups)
# =============================================================================
STEM_ORDER = sorted(STEMS.keys(), key=lambda s: STEMS[s]["index"])
STEM_CHINESE = [STEMS[s]["chinese"] for s in STEM_ORDER]

BRANCH_ORDER = sorted(BRANCHES.keys(), key=lambda b: BRANCHES[b]["index"])
BRANCH_CHINESE = [BRANCHES[b]["chinese"] for b in BRANCH_ORDER]

# =============================================================================
# DERIVED: Lookup Tables
# =============================================================================
# Chinese -> Pinyin mappings
STEM_CHINESE_TO_PINYIN = {STEMS[s]["chinese"]: s for s in STEMS}
BRANCH_CHINESE_TO_PINYIN = {BRANCHES[b]["chinese"]: b for b in BRANCHES}

# Element + Polarity -> Stem
ELEMENT_POLARITY_TO_STEM = {
    (STEMS[s]["element"], STEMS[s]["polarity"]): s for s in STEMS
}

# Storage branches
STORAGE_BRANCHES = {
    b: {"stored_element": BRANCHES[b]["stored_element"],
        "stored_stem": BRANCHES[b]["stored_stem"],
        "opener": BRANCHES[b]["opener"]}
    for b in BRANCHES if BRANCHES[b].get("is_storage")
}

# Branch -> Month and reverse
BRANCH_TO_MONTH = {b: BRANCHES[b]["month"] for b in BRANCHES}
MONTH_TO_BRANCH = {BRANCHES[b]["month"]: b for b in BRANCHES}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_stem(identifier):
    """Get stem by pinyin, chinese, or index."""
    if isinstance(identifier, int) and 0 <= identifier < 10:
        return STEMS[STEM_ORDER[identifier]]
    if identifier in STEMS:
        return STEMS[identifier]
    if identifier in STEM_CHINESE_TO_PINYIN:
        return STEMS[STEM_CHINESE_TO_PINYIN[identifier]]
    return None

def get_branch(identifier):
    """Get branch by pinyin, chinese, or index."""
    if isinstance(identifier, int) and 0 <= identifier < 12:
        return BRANCHES[BRANCH_ORDER[identifier]]
    if identifier in BRANCHES:
        return BRANCHES[identifier]
    if identifier in BRANCH_CHINESE_TO_PINYIN:
        return BRANCHES[BRANCH_CHINESE_TO_PINYIN[identifier]]
    return None

def get_primary_qi(branch_id):
    """
    Get Primary Qi (本氣) for a branch - the main energy at index 0.

    PRIMARY QI is the dominant energy of the Earthly Branch.
    This is NOT a hidden stem - it's the visible, main energy.

    Args:
        branch_id: Branch ID like "Yin", "Si", etc.

    Returns:
        tuple: (stem_id, score) or (None, 0) if branch not found
    """
    branch = BRANCHES.get(branch_id)
    if branch and branch.get("qi"):
        return branch["qi"][0]
    return (None, 0)


def get_hidden_stems(branch_id):
    """
    Get Hidden Stems (藏干) for a branch - secondary/tertiary energies at index 1+.

    IMPORTANT: The PRIMARY QI at index 0 is NOT a hidden stem.
    Only index 1+ are actual hidden stems (藏干).

    Args:
        branch_id: Branch ID like "Yin", "Si", etc.

    Returns:
        list: List of (stem_id, score) tuples for hidden stems only.
              Empty list if branch has only Primary Qi (e.g., Zi, Mao, You).
    """
    branch = BRANCHES.get(branch_id)
    if branch and len(branch.get("qi", [])) > 1:
        return branch["qi"][1:]  # Skip index 0 (Primary Qi)
    return []


def get_all_branch_qi(branch_id):
    """
    Get all qi values for a branch (Primary Qi + Hidden Stems combined).

    This returns the complete qi list. Use get_primary_qi() for just the
    main energy, or get_hidden_stems() for just the secondary/tertiary energies.

    Args:
        branch_id: Branch ID like "Yin", "Si", etc.

    Returns:
        list: List of (stem_id, score) tuples for all qi values
    """
    branch = BRANCHES.get(branch_id)
    return branch["qi"] if branch else []

def get_stem_by_element_polarity(element, polarity):
    """Get stem ID for element + polarity combination."""
    return ELEMENT_POLARITY_TO_STEM.get((element, polarity))

def get_day_officer(month_branch, day_branch):
    """
    Calculate the Day Officer (十二建除) for a given month and day branch.
    Formula: officer_index = (day_dong_gong_index - month_dong_gong_index + 12) % 12
    """
    if month_branch not in BRANCHES or day_branch not in BRANCHES:
        return None
    month_idx = BRANCHES[month_branch]["dong_gong_index"]
    day_idx = BRANCHES[day_branch]["dong_gong_index"]
    officer_idx = (day_idx - month_idx + 12) % 12
    return DAY_OFFICERS[officer_idx]

def get_ten_god(daymaster, target_stem):
    """
    Compute the Ten God relationship between daymaster and target stem.
    Returns: (id, english, chinese)
    """
    if daymaster not in STEMS or target_stem not in STEMS:
        return None

    dm = STEMS[daymaster]
    tg = STEMS[target_stem]
    dm_elem, dm_pol = dm["element"], dm["polarity"]
    tg_elem, tg_pol = tg["element"], tg["polarity"]
    same_polarity = dm_pol == tg_pol

    # Same element
    if dm_elem == tg_elem:
        if same_polarity:
            return ("F", "Friend", "比肩")
        return ("RW", "Rob Wealth", "劫財")

    # I generate (output)
    if ELEMENT_CYCLES["generating"][dm_elem] == tg_elem:
        if same_polarity:
            return ("EG", "Eating God", "食神")
        return ("HO", "Hurting Officer", "傷官")

    # I control (wealth)
    if ELEMENT_CYCLES["controlling"][dm_elem] == tg_elem:
        if same_polarity:
            return ("IW", "Indirect Wealth", "偏財")
        return ("DW", "Direct Wealth", "正財")

    # Controls me (influence/officer)
    if ELEMENT_CYCLES["controlled_by"][dm_elem] == tg_elem:
        if same_polarity:
            return ("7K", "Seven Killings", "七殺")
        return ("DO", "Direct Officer", "正官")

    # Generates me (resource)
    if ELEMENT_CYCLES["generated_by"][dm_elem] == tg_elem:
        if same_polarity:
            return ("IR", "Indirect Resource", "偏印")
        return ("DR", "Direct Resource", "正印")

    return None

# =============================================================================
# BACKWARD COMPATIBILITY ALIASES
# =============================================================================
HEAVENLY_STEMS = STEMS
EARTHLY_BRANCHES = BRANCHES
WUXING = ELEMENT_CYCLES

# For sxtwl compatibility
Gan = STEM_CHINESE
Zhi = BRANCH_CHINESE
GAN_MAP = STEM_CHINESE_TO_PINYIN
ZHI_MAP = BRANCH_CHINESE_TO_PINYIN

# =============================================================================
# DERIVED: Stem Lookup Maps (from stems.py)
# =============================================================================
STEM_COMBINATIONS_MAP = {
    stem_id: {"partner": stem["combines_with"], "element": stem["combination_element"]}
    for stem_id, stem in STEMS.items()
}

STEM_CONFLICTS_MAP = {
    stem_id: {"controls": stem["controls"], "controlled_by": stem["controlled_by"]}
    for stem_id, stem in STEMS.items()
}

# =============================================================================
# DERIVED: Branch Lookup Maps (from branches.py)
# =============================================================================
BRANCH_TO_SEASON = {branch_id: branch["season"] for branch_id, branch in BRANCHES.items()}

SIX_HARMONIES_MAP = {
    branch_id: {"partner": branch["harmonizes"], "element": branch["harmony_element"]}
    for branch_id, branch in BRANCHES.items()
}

CLASHES_MAP = {
    branch_id: {"partner": branch["clashes"], "type": "opposite" if BRANCHES[branch["clashes"]]["element"] != branch["element"] else "same"}
    for branch_id, branch in BRANCHES.items()
}

HARMS_MAP = {
    branch_id: {"partner": branch["harms"], "role": branch["harm_role"]}
    for branch_id, branch in BRANCHES.items()
}

SELF_PUNISHMENT_BRANCHES = [
    branch_id for branch_id, branch in BRANCHES.items()
    if branch.get("self_punishment")
]

def get_branch_by_month(month):
    """Get the branch for a Chinese calendar month (1-12)."""
    return MONTH_TO_BRANCH.get(month)

# =============================================================================
# DERIVED: Element Display Data (from elements.py)
# =============================================================================
ELEMENT_POLARITY_STEMS = ELEMENT_POLARITY_TO_STEM  # Alias

ELEMENT_COLORS = {
    "Wood": {
        "yang": {"text": "text-green-700", "bg": "bg-green-100", "border": "border-green-600"},
        "yin": {"text": "text-green-500", "bg": "bg-green-50", "border": "border-green-400"}
    },
    "Fire": {
        "yang": {"text": "text-red-600", "bg": "bg-red-100", "border": "border-red-500"},
        "yin": {"text": "text-red-400", "bg": "bg-red-50", "border": "border-red-300"}
    },
    "Earth": {
        "yang": {"text": "text-yellow-700", "bg": "bg-yellow-100", "border": "border-yellow-600"},
        "yin": {"text": "text-yellow-500", "bg": "bg-yellow-50", "border": "border-yellow-400"}
    },
    "Metal": {
        "yang": {"text": "text-gray-600", "bg": "bg-gray-100", "border": "border-gray-500"},
        "yin": {"text": "text-gray-400", "bg": "bg-gray-50", "border": "border-gray-300"}
    },
    "Water": {
        "yang": {"text": "text-blue-700", "bg": "bg-blue-100", "border": "border-blue-600"},
        "yin": {"text": "text-blue-500", "bg": "bg-blue-50", "border": "border-blue-400"}
    }
}

# Element characters including stem characters
ELEMENT_CHARACTERS = {
    "Wood": "木", "Fire": "火", "Earth": "土", "Metal": "金", "Water": "水",
}
for _stem_id, _stem in STEMS.items():
    ELEMENT_CHARACTERS[f"{_stem['polarity']} {_stem['element']}"] = _stem["chinese"]

# =============================================================================
# DERIVED: Ten Gods (十神) - built from STEMS.ten_gods static data
# =============================================================================
_TEN_GOD_PINYIN = {
    "F": "bǐ jiān", "RW": "jié cái", "EG": "shí shén", "HO": "shāng guān",
    "IW": "piān cái", "DW": "zhèng cái", "7K": "qī shā", "DO": "zhèng guān",
    "IR": "piān yìn", "DR": "zhèng yìn"
}

TEN_GODS = {
    dm_id: {
        target_id: {
            "id": tg[0], "abbreviation": tg[0], "english": tg[1], "chinese": tg[2],
            "pinyin": _TEN_GOD_PINYIN.get(tg[0], ""), "meaning_male": [], "meaning_female": [],
        }
        for target_id, tg in stem["ten_gods"].items()
    }
    for dm_id, stem in STEMS.items()
}
