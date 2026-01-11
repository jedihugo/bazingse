# * =========================
# * WEALTH STORAGE (财库) SYSTEM
# * =========================
# Storage branch information is now in branches.py.
# This file provides wealth-specific interpretations and pillar combinations.

from .derived import STORAGE_BRANCHES, WUXING

# The Four Earth Storage Branches (四库) - derived from branches.py
EARTH_STORAGE_BRANCHES = STORAGE_BRANCHES

# Large Wealth Storage Pillars (大财库)
# HS sits on Earth Storage branch containing its WEALTH element
# Format: "HS-EB" -> {details}
LARGE_WEALTH_STORAGE = {
    "Ding-Chou": {
        "chinese": "丁丑",
        "hs": "Ding",
        "eb": "Chou",
        "hs_element": "Fire",
        "wealth_element": "Metal",  # Fire controls Metal (wealth)
        "stored_stem": "Xin",
        "opener": "Wei",
        "description": "Fire Ox - Metal wealth storage for Fire DM"
    },
    "Xin-Wei": {
        "chinese": "辛未",
        "hs": "Xin",
        "eb": "Wei",
        "hs_element": "Metal",
        "wealth_element": "Wood",  # Metal controls Wood (wealth)
        "stored_stem": "Yi",
        "opener": "Chou",
        "description": "Metal Ram - Wood wealth storage for Metal DM"
    },
    "Wu-Chen": {
        "chinese": "戊辰",
        "hs": "Wu",
        "eb": "Chen",
        "hs_element": "Earth",
        "wealth_element": "Water",  # Earth controls Water (wealth)
        "stored_stem": "Gui",
        "opener": "Xu",
        "description": "Earth Dragon - Water wealth storage for Earth DM"
    },
    "Ren-Xu": {
        "chinese": "壬戌",
        "hs": "Ren",
        "eb": "Xu",
        "hs_element": "Water",
        "wealth_element": "Fire",  # Water controls Fire (wealth)
        "stored_stem": "Ding",
        "opener": "Chen",
        "description": "Water Dog - Fire wealth storage for Water DM"
    }
}

# Small Wealth Storage Pillars (小财库)
# HS sits on regular branch (NOT 库) containing its wealth element
SMALL_WEALTH_STORAGE = {
    # Fire DM wealth (Metal) in non-storage branches
    "Bing-Shen": {
        "chinese": "丙申",
        "hs": "Bing",
        "eb": "Shen",
        "hs_element": "Fire",
        "wealth_element": "Metal",
        "wealth_stem": "Geng",
        "description": "Fire Monkey - Metal wealth for Fire DM"
    },
    "Ding-You": {
        "chinese": "丁酉",
        "hs": "Ding",
        "eb": "You",
        "hs_element": "Fire",
        "wealth_element": "Metal",
        "wealth_stem": "Xin",
        "description": "Fire Rooster - Metal wealth for Fire DM"
    },
    # Earth DM wealth (Water) in non-storage branches
    "Wu-Zi": {
        "chinese": "戊子",
        "hs": "Wu",
        "eb": "Zi",
        "hs_element": "Earth",
        "wealth_element": "Water",
        "wealth_stem": "Gui",
        "description": "Earth Rat - Water wealth for Earth DM"
    },
    "Ji-Hai": {
        "chinese": "己亥",
        "hs": "Ji",
        "eb": "Hai",
        "hs_element": "Earth",
        "wealth_element": "Water",
        "wealth_stem": "Ren",
        "description": "Earth Pig - Water wealth for Earth DM"
    },
    # Metal DM wealth (Wood) in non-storage branches
    "Geng-Yin": {
        "chinese": "庚寅",
        "hs": "Geng",
        "eb": "Yin",
        "hs_element": "Metal",
        "wealth_element": "Wood",
        "wealth_stem": "Jia",
        "description": "Metal Tiger - Wood wealth for Metal DM"
    },
    "Xin-Mao": {
        "chinese": "辛卯",
        "hs": "Xin",
        "eb": "Mao",
        "hs_element": "Metal",
        "wealth_element": "Wood",
        "wealth_stem": "Yi",
        "description": "Metal Rabbit - Wood wealth for Metal DM"
    },
    # Water DM wealth (Fire) in non-storage branches
    "Ren-Wu": {
        "chinese": "壬午",
        "hs": "Ren",
        "eb": "Wu",
        "hs_element": "Water",
        "wealth_element": "Fire",
        "wealth_stem": "Bing",
        "description": "Water Horse - Fire wealth for Water DM"
    },
    "Gui-Si": {
        "chinese": "癸巳",
        "hs": "Gui",
        "eb": "Si",
        "hs_element": "Water",
        "wealth_element": "Fire",
        "wealth_stem": "Ding",
        "description": "Water Snake - Fire wealth for Water DM"
    },
    # Wood DM wealth (Earth) in storage branches
    "Jia-Chen": {
        "chinese": "甲辰",
        "hs": "Jia",
        "eb": "Chen",
        "hs_element": "Wood",
        "wealth_element": "Earth",
        "wealth_stem": "Wu",
        "description": "Wood Dragon - Earth wealth for Wood DM"
    },
    "Jia-Xu": {
        "chinese": "甲戌",
        "hs": "Jia",
        "eb": "Xu",
        "hs_element": "Wood",
        "wealth_element": "Earth",
        "wealth_stem": "Wu",
        "description": "Wood Dog - Earth wealth for Wood DM"
    }
}

# Map Day Master element to its wealth element (derived from controlling cycle)
DM_WEALTH_ELEMENT = WUXING["controlling"]

# Build WEALTH_ELEMENT_STEMS from STEMS (element -> [stems])
from .core import STEMS
WEALTH_ELEMENT_STEMS = {}
for stem_id, stem in STEMS.items():
    elem = stem["element"]
    if elem not in WEALTH_ELEMENT_STEMS:
        WEALTH_ELEMENT_STEMS[elem] = []
    WEALTH_ELEMENT_STEMS[elem].append(stem_id)
