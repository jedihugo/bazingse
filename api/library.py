# * =================
# * BAZI DEFINITIONS (library.py)
# * =================

# * -------------------------
# * NODE-BASED DISTANCE MAPPING (2D GRID SYSTEM)
# * -------------------------
# Simple 2D grid coordinates (like a chessboard)
# Manhattan distance: distance = abs(x1 - x2) + abs(y1 - y2)
# CRITICAL: 10-year luck has special rule (distance = 1 to all natal)

# Position coordinates (x, y) where x = pillar column, y = layer (HS=0, EB=1)
NODE_COORDINATES = {
    # Natal chart (4 pillars x 2 layers = 8 nodes)
    "hs_y": (0, 0), "eb_y": (0, 1),
    "hs_m": (1, 0), "eb_m": (1, 1),
    "hs_d": (2, 0), "eb_d": (2, 1),
    "hs_h": (3, 0), "eb_h": (3, 1),
    
    # 10-year luck (special: distance = 1 to all natal)
    "hs_10yl": None,  # Special handling
    "eb_10yl": None,  # Special handling
    
    # Luck sequence (follows same 4x2 grid as natal)
    "hs_yl": (0, 0), "eb_yl": (0, 1),
    "hs_ml": (1, 0), "eb_ml": (1, 1),
    "hs_dl": (2, 0), "eb_dl": (2, 1),
    "hs_hl": (3, 0), "eb_hl": (3, 1),
    
    # Talisman nodes (special: distance = 1 to all natal, like luck pillars)
    "hs_ty": None,  # Special handling (external harmony tool)
    "eb_ty": None,  # Special handling
    "hs_tm": None,  # Special handling
    "eb_tm": None,  # Special handling
    "hs_td": None,  # Special handling
    "eb_td": None,  # Special handling
    "hs_th": None,  # Special handling
    "eb_th": None,  # Special handling
}

def get_distance_key(node1, node2):
    """
    Get distance key for two nodes using 2D grid coordinates (Manhattan distance).
    
    Grid layout (4x2 chessboard):
         y    m    d    h
    HS: (0,0)(1,0)(2,0)(3,0)
    EB: (0,1)(1,1)(2,1)(3,1)
    
    Manhattan distance = abs(x1 - x2) + abs(y1 - y2)
    
    Args:
        node1: Node ID (e.g., "hs_y", "eb_m", "hs_10yl")
        node2: Node ID (e.g., "hs_d", "eb_yl", "hs_h")
    
    Returns:
        str: "1", "2", "3", or "4"
    
    Examples:
        get_distance_key("hs_y", "hs_m") → "1" (adjacent same layer)
        get_distance_key("hs_y", "eb_y") → "1" (same pillar cross layer)
        get_distance_key("hs_y", "eb_m") → "2" (adjacent cross layer: 1+1)
        get_distance_key("hs_y", "eb_h") → "4" (far cross layer: 3+1)
        get_distance_key("hs_10yl", "eb_m") → "1" (10-year luck always 1 to natal)
    """
    # Special case: Luck and talisman nodes are always distance 1 to all natal nodes
    # (temporal overlays and external harmony tools have full adjacency to natal)
    natal_nodes = {"hs_y", "eb_y", "hs_m", "eb_m", "hs_d", "eb_d", "hs_h", "eb_h"}
    special_nodes = {"hs_10yl", "eb_10yl", "hs_ty", "eb_ty", "hs_tm", "eb_tm", "hs_td", "eb_td", "hs_th", "eb_th"}
    
    if (node1 in special_nodes and node2 in natal_nodes) or \
       (node2 in special_nodes and node1 in natal_nodes):
        return "1"
    
    # Special case: Within same pillar (HS/EB pairs of luck or talisman)
    same_pillar_pairs = [
        ("hs_10yl", "eb_10yl"),
        ("hs_ty", "eb_ty"),
        ("hs_tm", "eb_tm"),
        ("hs_td", "eb_td"),
        ("hs_th", "eb_th")
    ]
    for hs, eb in same_pillar_pairs:
        if (node1 == hs and node2 == eb) or (node1 == eb and node2 == hs):
            return "1"
    
    # Get coordinates
    coord1 = NODE_COORDINATES.get(node1)
    coord2 = NODE_COORDINATES.get(node2)
    
    if coord1 is None or coord2 is None:
        # One is special node (luck/talisman), but not covered by special cases above
        # (e.g., 10-year luck to other luck nodes, talisman to talisman, etc.)
        # Treat special nodes as position (0,0) for special-to-special or special-to-luck distance
        if node1 in special_nodes:
            # HS nodes at layer 0, EB nodes at layer 1
            layer = 0 if node1.startswith("hs_") else 1
            coord1 = (0, layer)
        if node2 in special_nodes:
            layer = 0 if node2.startswith("hs_") else 1
            coord2 = (0, layer)
    
    # Calculate Manhattan distance (pure, no adjustments)
    # Luck pillars OVERLAP their corresponding natal pillars at same coordinates
    # Example: hs_yl (0,0) overlaps hs_y (0,0), so hs_yl-to-hs_h = hs_y-to-hs_h = 3
    distance = abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])
    
    # Ensure minimum distance of 1 (overlapping nodes like eb_yl-eb_y are still distinct)
    distance = max(1, distance)
    
    return str(distance)

def get_distance_key_3nodes(node1, node2, node3):
    """
    Get distance key for three nodes (for THREE_MEETINGS, THREE_COMBINATIONS).
    Returns the maximum pairwise distance (the "span" of the 3-node formation).
    
    Formula: max(d12, d13, d23) where dXY = Manhattan distance between nodes X and Y
    
    Args:
        node1, node2, node3: Node IDs
    
    Returns:
        str: "2", "3", "4", "5", "6", "7", "8" (max pairwise distance)
    
    Examples:
        get_distance_key_3nodes("eb_y", "eb_m", "eb_d") → "2" 
            (distances: y-m=1, m-d=1, y-d=2, max=2)
        get_distance_key_3nodes("eb_y", "eb_m", "eb_h") → "3"
            (distances: y-m=1, m-h=2, y-h=3, max=3)
        get_distance_key_3nodes("hs_y", "eb_m", "hs_d") → "3"
            (distances: y-m=2(cross), m-d=2(cross), y-d=2, max=2... wait, let me recalculate)
    """
    # Calculate all three pairwise distances
    d12 = int(get_distance_key(node1, node2))
    d13 = int(get_distance_key(node1, node3))
    d23 = int(get_distance_key(node2, node3))
    
    # Return the maximum pairwise distance (the "span")
    return str(max(d12, d13, d23))

# * -------------------------
# * SCORING SYSTEM - FORMULA-BASED
# * -------------------------
# Define multipliers for distance-based scoring
DISTANCE_MULTIPLIERS = {
    "three_branch": {  # For THREE_MEETINGS and THREE_COMBINATIONS
        "2": 1.0,      # Three consecutive nodes (best)
        "3": 0.786,    
        "4": 0.618,    
        "5": 0.500,    
        "6": 0.382,
        "7": 0.236,    
    },
    "two_branch": {  # For all other branch interactions
        "1": 1.0,      # Gap = 1 (adjacent pillars, luck-natal)
        "2": 0.618,    # Gap = 2
        "3": 0.382,    # Gap = 3
        "4": 0.236,    # Gap = 4 (cross-layer at gap=3)
    }
}

# Base scores for each interaction type
# POSITIVE: p = combined (detected), q = transformed (fully activated)
# NEGATIVE: p = impact (initial conflict), q = severity (intensified conflict)
BASE_SCORES = {
    # Positive Interactions (supportive, generative)
    "THREE_MEETINGS": {"combined": 35, "transformed": 61.8},
    "THREE_COMBINATIONS": {"combined": 25, "transformed": 45},
    "HALF_MEETINGS": {"combined": 20, "transformed": 40},
    "STEM_COMBINATIONS": {"combined": 19, "transformed": 38},
    "SIX_HARMONIES": {"combined": 18, "transformed": 35},
    "HALF_COMBINATIONS": {"combined": 15, "transformed": 30},
    "ARCHED_COMBINATIONS": {"combined": 12, "transformed": 25},
    
    # Negative Interactions (conflicting, destructive)
    "CLASHES_OPPOSITE": {"damage": 38},  # Opposite elements: asymmetric (victim 1.0, controller 0.618)
    "CLASHES_SAME": {"damage": 38},  # Same element: equal mutual damage
    "PUNISHMENTS_3NODE": {"damage": 38},  # 3-node: equal 1:1:1, ELEVATED severity
    "STEM_CONFLICTS": {"damage": 35},  # HS asymmetric (victim 1.0, controller 0.618)
    "HARMS": {"damage": 20},  # EB asymmetric (victim 1.0, controller 0.618)
    "DESTRUCTION_OPPOSITE": {"damage": 20},  # Opposite elements: asymmetric, distance 0 only
    "DESTRUCTION_SAME": {"damage": 20},  # Same element: equal mutual, distance 0 only
    "PUNISHMENTS_2NODE": {"damage": 16},  # 2-node: asymmetric 0.618:1 (less than HARMS)
}

def generate_scoring(base_1, base_2, pattern_type, state_1="combined", state_2="transformed"):
    """
    Generate scoring dictionary with distance multipliers applied.
    
    Formula: score = base_score * multiplier
    
    Args:
        base_1 (int): Base score for first state (e.g., combined/impact)
        base_2 (int): Base score for second state (e.g., transformed/severity)
        pattern_type (str): "three_branch" or "two_branch"
        state_1 (str): Name for first state (default: "combined")
        state_2 (str): Name for second state (default: "transformed")
    
    Returns:
        dict: Complete scoring dictionary with all distance levels calculated
    
    Examples:
        Positive: generate_scoring(19, 38, "two_branch")
        Negative: generate_scoring(22, 42, "two_branch", "impact", "severity")
    """
    multipliers = DISTANCE_MULTIPLIERS[pattern_type]
    
    scoring = {
        state_1: {},
        state_2: {}
    }
    
    for distance_key, multiplier in multipliers.items():
        scoring[state_1][distance_key] = round(base_1 * multiplier)
        scoring[state_2][distance_key] = round(base_2 * multiplier)
    
    return scoring

def generate_single_scoring(base, pattern_type):
    """
    Generate simple scoring with only distance decay (no states).
    Used for mutual/equal damage patterns like CLASHES.
    
    Formula: score = base * distance_multiplier
    
    Args:
        base (int): Base damage/score
        pattern_type (str): "three_branch" or "two_branch"
    
    Returns:
        dict: Flat scoring dictionary with distance levels
    
    Example:
        CLASHES: generate_single_scoring(38, "two_branch")
        → {"1": 38, "2": 24, "3": 15, "4": 9}
    """
    multipliers = DISTANCE_MULTIPLIERS[pattern_type]
    scoring = {}
    
    for distance_key, multiplier in multipliers.items():
        scoring[distance_key] = round(base * multiplier)
    
    return scoring

def generate_asymmetric_scoring(base, pattern_type, ratio=0.618):
    """
    Generate asymmetric scoring for controller-victim relationships.
    Used for STEM_CONFLICTS where controller expends less energy than victim suffers.
    
    Formula: 
        victim_score = base * distance_multiplier
        controller_score = base * ratio * distance_multiplier
    
    Args:
        base (int): Base damage (victim's full damage)
        pattern_type (str): "three_branch" or "two_branch"
        ratio (float): Controller-to-victim ratio (default: 0.618, golden ratio)
    
    Returns:
        dict: Scoring with separate controller and victim dictionaries
    
    Example:
        STEM_CONFLICTS: generate_asymmetric_scoring(35, "two_branch", 0.618)
        → {
            "victim": {"1": 35, "2": 22, "3": 13, "4": 8},
            "controller": {"1": 22, "2": 14, "3": 8, "4": 5}
          }
    """
    multipliers = DISTANCE_MULTIPLIERS[pattern_type]
    
    scoring = {
        "victim": {},
        "controller": {}
    }
    
    for distance_key, multiplier in multipliers.items():
        scoring["victim"][distance_key] = round(base * multiplier)
        scoring["controller"][distance_key] = round(base * ratio * multiplier)
    
    return scoring

# * -------------------------

# Lists for Heavenly Stems and Earthly Branches (used with sxtwl)
Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]  # Heavenly Stems
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]  # Earthly Branches

# Map Chinese characters to romanized names
GAN_MAP = {
    "甲": "Jia", "乙": "Yi", "丙": "Bing", "丁": "Ding", "戊": "Wu",
    "己": "Ji", "庚": "Geng", "辛": "Xin", "壬": "Ren", "癸": "Gui"
}

ZHI_MAP = {
    "子": "Zi", "丑": "Chou", "寅": "Yin", "卯": "Mao", "辰": "Chen", "巳": "Si",
    "午": "Wu", "未": "Wei", "申": "Shen", "酉": "You", "戌": "Xu", "亥": "Hai"
}

HEAVENLY_STEMS = {
    "Jia": {
        "id": "Jia",
        "pinyin": "Jia",
        "chinese": "甲",
        "english": "Yang Wood",
        "element": "Wood",
        "polarity": "Yang",
        "hex_color": "#c2d4be",  # Light sage green
        "qi_score": 100,
    },
    "Yi": {
        "id": "Yi",
        "pinyin": "Yi",
        "chinese": "乙",
        "english": "Yin Wood",
        "element": "Wood",
        "polarity": "Yin",
        "hex_color": "#d6e2bb",  # Light lime green
        "qi_score": 100,
    },
    "Bing": {
        "id": "Bing",
        "pinyin": "Bing",
        "chinese": "丙",
        "english": "Yang Fire",
        "element": "Fire",
        "polarity": "Yang",
        "hex_color": "#f3adae",  # Light coral red
        "qi_score": 100,
    },
    "Ding": {
        "id": "Ding",
        "pinyin": "Ding",
        "chinese": "丁",
        "english": "Yin Fire",
        "element": "Fire",
        "polarity": "Yin",
        "hex_color": "#f9d3ad",  # Light peach
        "qi_score": 100,
    },
    "Wu": {
        "id": "Wu",
        "pinyin": "Wu",
        "chinese": "戊",
        "english": "Yang Earth",
        "element": "Earth",
        "polarity": "Yang",
        "hex_color": "#e6ceb7",  # Light tan brown
        "qi_score": 100,
    },
    "Ji": {
        "id": "Ji",
        "pinyin": "Ji",
        "chinese": "己",
        "english": "Yin Earth",
        "element": "Earth",
        "polarity": "Yin",
        "hex_color": "#efe3cc",  # Light cream beige
        "qi_score": 100,
    },
    "Geng": {
        "id": "Geng",
        "pinyin": "Geng",
        "chinese": "庚",
        "english": "Yang Metal",
        "element": "Metal",
        "polarity": "Yang",
        "hex_color": "#ccd8e6",  # Light steel blue
        "qi_score": 100,
    },
    "Xin": {
        "id": "Xin",
        "pinyin": "Xin",
        "chinese": "辛",
        "english": "Yin Metal",
        "element": "Metal",
        "polarity": "Yin",
        "hex_color": "#e6e8f7",  # Light lavender gray
        "qi_score": 100,
    },
    "Ren": {
        "id": "Ren",
        "pinyin": "Ren",
        "chinese": "壬",
        "english": "Yang Water",
        "element": "Water",
        "polarity": "Yang",
        "hex_color": "#b9cbff",  # Light sky blue
        "qi_score": 100,
    },
    "Gui": {
        "id": "Gui",
        "pinyin": "Gui",
        "chinese": "癸",
        "english": "Yin Water",
        "element": "Water",
        "polarity": "Yin",
        "hex_color": "#e0e9ff",  # Light ice blue
        "qi_score": 100,
    },
}

EARTHLY_BRANCHES = {
    "Zi": {
        "id": "Zi",
        "chinese": "子",
        "element": "Water",
        "polarity": "Yang",
        "animal": "Rat",
        "hex_color": "#b9cbff",
        "qi": [
            {"stem": "Ren", "score": 80},
            {"stem": "Gui", "score": 40},
        ]
    },
    "Chou": {
        "id": "Chou",
        "chinese": "丑",
        "element": "Earth",
        "polarity": "Yin",
        "animal": "Ox",
        "hex_color": "#efe3cc",
        "qi": [
            {"stem": "Ji", "score": 95},
            {"stem": "Gui", "score": 15},
            {"stem": "Xin", "score": 10}
        ]
    },
    "Yin": {
        "id": "Yin",
        "chinese": "寅",
        "element": "Wood",
        "polarity": "Yang",
        "animal": "Tiger",
        "hex_color": "#c2d4be",
        "qi": [
            {"stem": "Jia", "score": 100},
            {"stem": "Bing", "score": 15},
            {"stem": "Wu", "score": 5}
        ]
    },
    "Mao": {
        "id": "Mao",
        "chinese": "卯",
        "element": "Wood",
        "polarity": "Yin",
        "animal": "Rabbit",
        "hex_color": "#d6e2bb",
        "qi": [
            {"stem": "Yi", "score": 100},
            {"stem": "Jia", "score": 20}
        ]
    },
    "Chen": {
        "id": "Chen",
        "chinese": "辰",
        "element": "Earth",
        "polarity": "Yang",
        "animal": "Dragon",
        "hex_color": "#e6ceb7",
        "qi": [
            {"stem": "Wu", "score": 95},
            {"stem": "Yi", "score": 15},
            {"stem": "Gui", "score": 10}
        ]
    },
    "Si": {
        "id": "Si",
        "chinese": "巳",
        "element": "Fire",
        "polarity": "Yin",
        "animal": "Snake",
        "hex_color": "#f9d3ad",
        "qi": [
            {"stem": "Ding", "score": 80},
            {"stem": "Bing", "score": 20},
            {"stem": "Geng", "score": 10},
            {"stem": "Wu", "score": 10}
        ]
    },
    "Wu": {
        "id": "Wu",
        "chinese": "午",
        "element": "Fire",
        "polarity": "Yang",
        "animal": "Horse",
        "hex_color": "#f3adae",
        "qi": [
            {"stem": "Bing", "score": 90},
            {"stem": "Ding", "score": 15},
            {"stem": "Ji", "score": 15}
        ]
    },
    "Wei": {
        "id": "Wei",
        "chinese": "未",
        "element": "Earth",
        "polarity": "Yin",
        "animal": "Goat",
        "hex_color": "#efe3cc",
        "qi": [
            {"stem": "Ji", "score": 95},
            {"stem": "Ding", "score": 20},
            {"stem": "Yi", "score": 10}
        ]
    },
    "Shen": {
        "id": "Shen",
        "chinese": "申",
        "element": "Metal",
        "polarity": "Yang",
        "animal": "Monkey",
        "hex_color": "#ccd8e6",
        "qi": [
            {"stem": "Geng", "score": 100},
            {"stem": "Ren", "score": 10},
            {"stem": "Ji", "score": 5},
            {"stem": "Wu", "score": 5}
        ]
    },
    "You": {
        "id": "You",
        "chinese": "酉",
        "element": "Metal",
        "polarity": "Yin",
        "animal": "Rooster",
        "hex_color": "#e6e8f7",
        "qi": [
            {"stem": "Xin", "score": 100},
            {"stem": "Geng", "score": 20}
        ]
    },
    "Xu": {
        "id": "Xu",
        "chinese": "戌",
        "element": "Earth",
        "polarity": "Yang",
        "animal": "Dog",
        "hex_color": "#e6ceb7",
        "qi": [
            {"stem": "Wu", "score": 95},
            {"stem": "Xin", "score": 20},
            {"stem": "Ding", "score": 10}
        ]
    },
    "Hai": {
        "id": "Hai",
        "chinese": "亥",
        "element": "Water",
        "polarity": "Yin",
        "animal": "Pig",
        "hex_color": "#e0e9ff",
        "qi": [
            {"stem": "Gui", "score": 70},
            {"stem": "Ren", "score": 30},
            {"stem": "Jia", "score": 10},
            {"stem": "Wu", "score": 10}
        ]
    }
}

# * =========================
# * TRANSFORMATION CONSTANTS (Polarity-Based)
# * =========================

# Element + Polarity → Stem mapping (Tuple key format for direct lookups)
# CORE BAZI PRINCIPLE: Transformation depends on node's polarity
# Example: Si (Yin) transforms to Fire → Ding (Yin Fire)
#          Wu (Yang) transforms to Fire → Bing (Yang Fire)
# NOTE: This is the authoritative mapping. ELEMENT_POLARITY_TO_STEM and ELEMENT_CHARACTERS
#       are derived from this for different lookup formats.
ELEMENT_POLARITY_STEMS = {
    ("Wood", "Yang"): "Jia",
    ("Wood", "Yin"): "Yi",
    ("Fire", "Yang"): "Bing",
    ("Fire", "Yin"): "Ding",
    ("Earth", "Yang"): "Wu",
    ("Earth", "Yin"): "Ji",
    ("Metal", "Yang"): "Geng",
    ("Metal", "Yin"): "Xin",
    ("Water", "Yang"): "Ren",
    ("Water", "Yin"): "Gui",
}

# Element → Chinese character mapping
ELEMENT_CHINESE = {
    "Wood": "木",
    "Fire": "火",
    "Earth": "土",
    "Metal": "金",
    "Water": "水"
}

# Element Colors for UI display
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

# * =========================
# * ELEMENT CHARACTER MAPPINGS (Deterministic BaZi Constants)
# * =========================

# Base element characters (五行)
ELEMENT_CHARACTERS = {
    # Base elements
    "Wood": "木",
    "Fire": "火",
    "Earth": "土",
    "Metal": "金",
    "Water": "水",
    # Polarity + Element (mapped to their Heavenly Stem characters)
    "Yang Wood": "甲",   # Jia
    "Yin Wood": "乙",    # Yi
    "Yang Fire": "丙",   # Bing
    "Yin Fire": "丁",    # Ding
    "Yang Earth": "戊",  # Wu
    "Yin Earth": "己",   # Ji
    "Yang Metal": "庚",  # Geng
    "Yin Metal": "辛",   # Xin
    "Yang Water": "壬",  # Ren
    "Yin Water": "癸"    # Gui
}

# Polarity + Element → Heavenly Stem mapping (for element production/transformation)
ELEMENT_POLARITY_TO_STEM = {
    "Yang Wood": "Jia",
    "Yin Wood": "Yi",
    "Yang Fire": "Bing",
    "Yin Fire": "Ding",
    "Yang Earth": "Wu",
    "Yin Earth": "Ji",
    "Yang Metal": "Geng",
    "Yin Metal": "Xin",
    "Yang Water": "Ren",
    "Yin Water": "Gui"
}

# * =========================
# * SEASONAL STRENGTH DEFINITIONS
# * =========================

SEASONAL_STRENGTH = {
    "Wood": {
        "Prosperous": ["Yin", "Mao"],       # Spring months - Wood is strongest
        "Growing": ["Hai", "Zi"],           # Winter months - Water feeds Wood
        "Resting": ["Si", "Wu"],            # Summer months
        "Imprisoned": ["Shen", "You"],       # Autumn months - Metal cuts Wood
        "Dead": ["Chen", "Chou", "Wei", "Xu"]  # Earth months - Earth depletes Wood
    },
    "Fire": {
        "Prosperous": ["Si", "Wu"],         # Summer months - Fire is strongest
        "Growing": ["Yin", "Mao"],          # Spring months - Wood feeds Fire
        "Resting": ["Chen", "Chou", "Wei", "Xu"],  # Earth months
        "Imprisoned": ["Hai", "Zi"],         # Winter months - Water extinguishes Fire
        "Dead": ["Shen", "You"]            # Autumn months - Metal consumes Fire
    },
    "Earth": {
        "Prosperous": ["Chen", "Chou", "Wei", "Xu"],  # Earth months - Earth is strongest
        "Growing": ["Si", "Wu"],            # Summer months - Fire creates Earth
        "Resting": ["Shen", "You"],         # Autumn months
        "Imprisoned": ["Hai", "Zi"],        # Winter months - Water exhausts Earth
        "Dead": ["Yin", "Mao"]             # Spring months - Wood breaks Earth
    },
    "Metal": {
        "Prosperous": ["Shen", "You"],      # Autumn months - Metal is strongest
        "Growing": ["Chen", "Chou", "Wei", "Xu"],  # Earth months - Earth produces Metal
        "Resting": ["Hai", "Zi"],           # Winter months
        "Imprisoned": ["Yin", "Mao"],       # Spring months - Wood exhausts Metal
        "Dead": ["Si", "Wu"]               # Summer months - Fire melts Metal
    },
    "Water": {
        "Prosperous": ["Hai", "Zi"],        # Winter months - Water is strongest
        "Growing": ["Shen", "You"],         # Autumn months - Metal produces Water
        "Resting": ["Yin", "Mao"],          # Spring months
        "Imprisoned": ["Chen", "Chou", "Wei", "Xu"],  # Earth months - Earth absorbs Water
        "Dead": ["Si", "Wu"]               # Summer months - Fire evaporates Water
    }
}

# Combined WUXING relationships for V2 architecture
WUXING = {
    "generating": {         # 生 - Supporting cycle
        "Wood": "Fire",
        "Fire": "Earth",
        "Earth": "Metal",
        "Metal": "Water",
        "Water": "Wood"
    },
    "controlling": {        # 剋 - Controlling cycle
        "Wood": "Earth",
        "Earth": "Water",
        "Water": "Fire",
        "Fire": "Metal",
        "Metal": "Wood"
    },
    "generated_by": {       # Reverse of generating
        "Fire": "Wood",
        "Earth": "Fire",
        "Metal": "Earth",
        "Water": "Metal",
        "Wood": "Water"
    },
    "controlled_by": {      # Reverse of controlling
        "Earth": "Wood",
        "Water": "Earth",
        "Fire": "Water",
        "Metal": "Fire",
        "Wood": "Metal"
    }
}
# * =========================
# * TEN GODS RELATIONSHIPS
# * =========================

TEN_GODS = {
    "Jia": {  # Yang Wood Day Master
        "Jia": {
            "id": "F",
            "abbreviation": "F",
            "english": "Friend",
            "chinese": "比肩",
            "pinyin": "bǐ jiān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Yi": {
            "id": "RW",
            "abbreviation": "RW",
            "english": "Rob Wealth",
            "chinese": "劫財",
            "pinyin": "jié cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Bing": {
            "id": "EG",
            "abbreviation": "EG",
            "english": "Eating God",
            "chinese": "食神",
            "pinyin": "shí shén",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ding": {
            "id": "HO",
            "abbreviation": "HO",
            "english": "Hurting Officer",
            "chinese": "傷官",
            "pinyin": "shāng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Wu": {
            "id": "IW",
            "abbreviation": "IW",
            "english": "Indirect Wealth",
            "chinese": "偏財",
            "pinyin": "piān cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ji": {
            "id": "DW",
            "abbreviation": "DW",
            "english": "Direct Wealth",
            "chinese": "正財",
            "pinyin": "zhèng cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Geng": {
            "id": "7K",
            "abbreviation": "7K",
            "english": "Seven Killings",
            "chinese": "七殺",
            "pinyin": "qī shā",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Xin": {
            "id": "DO",
            "abbreviation": "DO",
            "english": "Direct Officer",
            "chinese": "正官",
            "pinyin": "zhèng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ren": {
            "id": "IR",
            "abbreviation": "IR",
            "english": "Indirect Resource",
            "chinese": "偏印",
            "pinyin": "piān yìn",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Gui": {
            "id": "DR",
            "abbreviation": "DR",
            "english": "Direct Resource",
            "chinese": "正印",
            "pinyin": "zhèng yìn",
            "meaning_male": [],
            "meaning_female": [],
        }
    },
    "Yi": {  # Yin Wood Day Master
        "Yi": {
            "id": "F",
            "abbreviation": "F",
            "english": "Friend",
            "chinese": "比肩",
            "pinyin": "bǐ jiān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Jia": {
            "id": "RW",
            "abbreviation": "RW",
            "english": "Rob Wealth",
            "chinese": "劫財",
            "pinyin": "jié cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ding": {
            "id": "EG",
            "abbreviation": "EG",
            "english": "Eating God",
            "chinese": "食神",
            "pinyin": "shí shén",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Bing": {
            "id": "HO",
            "abbreviation": "HO",
            "english": "Hurting Officer",
            "chinese": "傷官",
            "pinyin": "shāng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ji": {
            "id": "IW",
            "abbreviation": "IW",
            "english": "Indirect Wealth",
            "chinese": "偏財",
            "pinyin": "piān cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Wu": {
            "id": "DW",
            "abbreviation": "DW",
            "english": "Direct Wealth",
            "chinese": "正財",
            "pinyin": "zhèng cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Xin": {
            "id": "7K",
            "abbreviation": "7K",
            "english": "Seven Killings",
            "chinese": "七殺",
            "pinyin": "qī shā",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Geng": {
            "id": "DO",
            "abbreviation": "DO",
            "english": "Direct Officer",
            "chinese": "正官",
            "pinyin": "zhèng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Gui": {
            "id": "IR",
            "abbreviation": "IR",
            "english": "Indirect Resource",
            "chinese": "偏印",
            "pinyin": "piān yìn",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ren": {
            "id": "DR",
            "abbreviation": "DR",
            "english": "Direct Resource",
            "chinese": "正印",
            "pinyin": "zhèng yìn",
            "meaning_male": [],
            "meaning_female": [],
        }
    },
    "Bing": {  # Yang Fire Day Master
        "Bing": {
            "id": "F",
            "abbreviation": "F",
            "english": "Friend",
            "chinese": "比肩",
            "pinyin": "bǐ jiān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ding": {
            "id": "RW",
            "abbreviation": "RW",
            "english": "Rob Wealth",
            "chinese": "劫財",
            "pinyin": "jié cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Wu": {
            "id": "EG",
            "abbreviation": "EG",
            "english": "Eating God",
            "chinese": "食神",
            "pinyin": "shí shén",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ji": {
            "id": "HO",
            "abbreviation": "HO",
            "english": "Hurting Officer",
            "chinese": "傷官",
            "pinyin": "shāng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Geng": {
            "id": "IW",
            "abbreviation": "IW",
            "english": "Indirect Wealth",
            "chinese": "偏財",
            "pinyin": "piān cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Xin": {
            "id": "DW",
            "abbreviation": "DW",
            "english": "Direct Wealth",
            "chinese": "正財",
            "pinyin": "zhèng cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ren": {
            "id": "7K",
            "abbreviation": "7K",
            "english": "Seven Killings",
            "chinese": "七殺",
            "pinyin": "qī shā",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Gui": {
            "id": "DO",
            "abbreviation": "DO",
            "english": "Direct Officer",
            "chinese": "正官",
            "pinyin": "zhèng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Jia": {
            "id": "IR",
            "abbreviation": "IR",
            "english": "Indirect Resource",
            "chinese": "偏印",
            "pinyin": "piān yìn",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Yi": {
            "id": "DR",
            "abbreviation": "DR",
            "english": "Direct Resource",
            "chinese": "正印",
            "pinyin": "zhèng yìn",
            "meaning_male": [],
            "meaning_female": [],
        }
    },
    "Ding": {  # Yin Fire Day Master
        "Ding": {
            "id": "F",
            "abbreviation": "F",
            "english": "Friend",
            "chinese": "比肩",
            "pinyin": "bǐ jiān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Bing": {
            "id": "RW",
            "abbreviation": "RW",
            "english": "Rob Wealth",
            "chinese": "劫財",
            "pinyin": "jié cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ji": {
            "id": "EG",
            "abbreviation": "EG",
            "english": "Eating God",
            "chinese": "食神",
            "pinyin": "shí shén",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Wu": {
            "id": "HO",
            "abbreviation": "HO",
            "english": "Hurting Officer",
            "chinese": "傷官",
            "pinyin": "shāng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Xin": {
            "id": "IW",
            "abbreviation": "IW",
            "english": "Indirect Wealth",
            "chinese": "偏財",
            "pinyin": "piān cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Geng": {
            "id": "DW",
            "abbreviation": "DW",
            "english": "Direct Wealth",
            "chinese": "正財",
            "pinyin": "zhèng cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Gui": {
            "id": "7K",
            "abbreviation": "7K",
            "english": "Seven Killings",
            "chinese": "七殺",
            "pinyin": "qī shā",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ren": {
            "id": "DO",
            "abbreviation": "DO",
            "english": "Direct Officer",
            "chinese": "正官",
            "pinyin": "zhèng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Yi": {
            "id": "IR",
            "abbreviation": "IR",
            "english": "Indirect Resource",
            "chinese": "偏印",
            "pinyin": "piān yìn",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Jia": {
            "id": "DR",
            "abbreviation": "DR",
            "english": "Direct Resource",
            "chinese": "正印",
            "pinyin": "zhèng yìn",
            "meaning_male": [],
            "meaning_female": [],
        }
    },
    "Wu": {  # Yang Earth Day Master
        "Wu": {
            "id": "F",
            "abbreviation": "F",
            "english": "Friend",
            "chinese": "比肩",
            "pinyin": "bǐ jiān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ji": {
            "id": "RW",
            "abbreviation": "RW",
            "english": "Rob Wealth",
            "chinese": "劫財",
            "pinyin": "jié cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Geng": {
            "id": "EG",
            "abbreviation": "EG",
            "english": "Eating God",
            "chinese": "食神",
            "pinyin": "shí shén",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Xin": {
            "id": "HO",
            "abbreviation": "HO",
            "english": "Hurting Officer",
            "chinese": "傷官",
            "pinyin": "shāng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ren": {
            "id": "IW",
            "abbreviation": "IW",
            "english": "Indirect Wealth",
            "chinese": "偏財",
            "pinyin": "piān cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Gui": {
            "id": "DW",
            "abbreviation": "DW",
            "english": "Direct Wealth",
            "chinese": "正財",
            "pinyin": "zhèng cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Jia": {
            "id": "7K",
            "abbreviation": "7K",
            "english": "Seven Killings",
            "chinese": "七殺",
            "pinyin": "qī shā",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Yi": {
            "id": "DO",
            "abbreviation": "DO",
            "english": "Direct Officer",
            "chinese": "正官",
            "pinyin": "zhèng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Bing": {
            "id": "IR",
            "abbreviation": "IR",
            "english": "Indirect Resource",
            "chinese": "偏印",
            "pinyin": "piān yìn",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ding": {
            "id": "DR",
            "abbreviation": "DR",
            "english": "Direct Resource",
            "chinese": "正印",
            "pinyin": "zhèng yìn",
            "meaning_male": [],
            "meaning_female": [],
        }
    },
    "Ji": {  # Yin Earth Day Master
        "Ji": {
            "id": "F",
            "abbreviation": "F",
            "english": "Friend",
            "chinese": "比肩",
            "pinyin": "bǐ jiān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Wu": {
            "id": "RW",
            "abbreviation": "RW",
            "english": "Rob Wealth",
            "chinese": "劫財",
            "pinyin": "jié cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Xin": {
            "id": "EG",
            "abbreviation": "EG",
            "english": "Eating God",
            "chinese": "食神",
            "pinyin": "shí shén",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Geng": {
            "id": "HO",
            "abbreviation": "HO",
            "english": "Hurting Officer",
            "chinese": "傷官",
            "pinyin": "shāng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Gui": {
            "id": "IW",
            "abbreviation": "IW",
            "english": "Indirect Wealth",
            "chinese": "偏財",
            "pinyin": "piān cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ren": {
            "id": "DW",
            "abbreviation": "DW",
            "english": "Direct Wealth",
            "chinese": "正財",
            "pinyin": "zhèng cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Yi": {
            "id": "7K",
            "abbreviation": "7K",
            "english": "Seven Killings",
            "chinese": "七殺",
            "pinyin": "qī shā",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Jia": {
            "id": "DO",
            "abbreviation": "DO",
            "english": "Direct Officer",
            "chinese": "正官",
            "pinyin": "zhèng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ding": {
            "id": "IR",
            "abbreviation": "IR",
            "english": "Indirect Resource",
            "chinese": "偏印",
            "pinyin": "piān yìn",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Bing": {
            "id": "DR",
            "abbreviation": "DR",
            "english": "Direct Resource",
            "chinese": "正印",
            "pinyin": "zhèng yìn",
            "meaning_male": [],
            "meaning_female": [],
        }
    },
    "Geng": {  # Yang Metal Day Master
        "Geng": {
            "id": "F",
            "abbreviation": "F",
            "english": "Friend",
            "chinese": "比肩",
            "pinyin": "bǐ jiān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Xin": {
            "id": "RW",
            "abbreviation": "RW",
            "english": "Rob Wealth",
            "chinese": "劫財",
            "pinyin": "jié cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ren": {
            "id": "EG",
            "abbreviation": "EG",
            "english": "Eating God",
            "chinese": "食神",
            "pinyin": "shí shén",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Gui": {
            "id": "HO",
            "abbreviation": "HO",
            "english": "Hurting Officer",
            "chinese": "傷官",
            "pinyin": "shāng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Jia": {
            "id": "IW",
            "abbreviation": "IW",
            "english": "Indirect Wealth",
            "chinese": "偏財",
            "pinyin": "piān cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Yi": {
            "id": "DW",
            "abbreviation": "DW",
            "english": "Direct Wealth",
            "chinese": "正財",
            "pinyin": "zhèng cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Bing": {
            "id": "7K",
            "abbreviation": "7K",
            "english": "Seven Killings",
            "chinese": "七殺",
            "pinyin": "qī shā",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ding": {
            "id": "DO",
            "abbreviation": "DO",
            "english": "Direct Officer",
            "chinese": "正官",
            "pinyin": "zhèng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Wu": {
            "id": "IR",
            "abbreviation": "IR",
            "english": "Indirect Resource",
            "chinese": "偏印",
            "pinyin": "piān yìn",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ji": {
            "id": "DR",
            "abbreviation": "DR",
            "english": "Direct Resource",
            "chinese": "正印",
            "pinyin": "zhèng yìn",
            "meaning_male": [],
            "meaning_female": [],
        }
    },
    "Xin": {  # Yin Metal Day Master
        "Xin": {
            "id": "F",
            "abbreviation": "F",
            "english": "Friend",
            "chinese": "比肩",
            "pinyin": "bǐ jiān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Geng": {
            "id": "RW",
            "abbreviation": "RW",
            "english": "Rob Wealth",
            "chinese": "劫財",
            "pinyin": "jié cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Gui": {
            "id": "EG",
            "abbreviation": "EG",
            "english": "Eating God",
            "chinese": "食神",
            "pinyin": "shí shén",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ren": {
            "id": "HO",
            "abbreviation": "HO",
            "english": "Hurting Officer",
            "chinese": "傷官",
            "pinyin": "shāng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Yi": {
            "id": "IW",
            "abbreviation": "IW",
            "english": "Indirect Wealth",
            "chinese": "偏財",
            "pinyin": "piān cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Jia": {
            "id": "DW",
            "abbreviation": "DW",
            "english": "Direct Wealth",
            "chinese": "正財",
            "pinyin": "zhèng cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ding": {
            "id": "7K",
            "abbreviation": "7K",
            "english": "Seven Killings",
            "chinese": "七殺",
            "pinyin": "qī shā",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Bing": {
            "id": "DO",
            "abbreviation": "DO",
            "english": "Direct Officer",
            "chinese": "正官",
            "pinyin": "zhèng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ji": {
            "id": "IR",
            "abbreviation": "IR",
            "english": "Indirect Resource",
            "chinese": "偏印",
            "pinyin": "piān yìn",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Wu": {
            "id": "DR",
            "abbreviation": "DR",
            "english": "Direct Resource",
            "chinese": "正印",
            "pinyin": "zhèng yìn",
            "meaning_male": [],
            "meaning_female": [],
        }
    },
    "Ren": {  # Yang Water Day Master
        "Ren": {
            "id": "F",
            "abbreviation": "F",
            "english": "Friend",
            "chinese": "比肩",
            "pinyin": "bǐ jiān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Gui": {
            "id": "RW",
            "abbreviation": "RW",
            "english": "Rob Wealth",
            "chinese": "劫財",
            "pinyin": "jié cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Jia": {
            "id": "EG",
            "abbreviation": "EG",
            "english": "Eating God",
            "chinese": "食神",
            "pinyin": "shí shén",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Yi": {
            "id": "HO",
            "abbreviation": "HO",
            "english": "Hurting Officer",
            "chinese": "傷官",
            "pinyin": "shāng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Bing": {
            "id": "IW",
            "abbreviation": "IW",
            "english": "Indirect Wealth",
            "chinese": "偏財",
            "pinyin": "piān cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ding": {
            "id": "DW",
            "abbreviation": "DW",
            "english": "Direct Wealth",
            "chinese": "正財",
            "pinyin": "zhèng cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Wu": {
            "id": "7K",
            "abbreviation": "7K",
            "english": "Seven Killings",
            "chinese": "七殺",
            "pinyin": "qī shā",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ji": {
            "id": "DO",
            "abbreviation": "DO",
            "english": "Direct Officer",
            "chinese": "正官",
            "pinyin": "zhèng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Geng": {
            "id": "IR",
            "abbreviation": "IR",
            "english": "Indirect Resource",
            "chinese": "偏印",
            "pinyin": "piān yìn",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Xin": {
            "id": "DR",
            "abbreviation": "DR",
            "english": "Direct Resource",
            "chinese": "正印",
            "pinyin": "zhèng yìn",
            "meaning_male": [],
            "meaning_female": [],
        }
    },
    "Gui": {  # Yin Water Day Master
        "Gui": {
            "id": "F",
            "abbreviation": "F",
            "english": "Friend",
            "chinese": "比肩",
            "pinyin": "bǐ jiān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ren": {
            "id": "RW",
            "abbreviation": "RW",
            "english": "Rob Wealth",
            "chinese": "劫財",
            "pinyin": "jié cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Yi": {
            "id": "EG",
            "abbreviation": "EG",
            "english": "Eating God",
            "chinese": "食神",
            "pinyin": "shí shén",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Jia": {
            "id": "HO",
            "abbreviation": "HO",
            "english": "Hurting Officer",
            "chinese": "傷官",
            "pinyin": "shāng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ding": {
            "id": "IW",
            "abbreviation": "IW",
            "english": "Indirect Wealth",
            "chinese": "偏財",
            "pinyin": "piān cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Bing": {
            "id": "DW",
            "abbreviation": "DW",
            "english": "Direct Wealth",
            "chinese": "正財",
            "pinyin": "zhèng cái",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Ji": {
            "id": "7K",
            "abbreviation": "7K",
            "english": "Seven Killings",
            "chinese": "七殺",
            "pinyin": "qī shā",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Wu": {
            "id": "DO",
            "abbreviation": "DO",
            "english": "Direct Officer",
            "chinese": "正官",
            "pinyin": "zhèng guān",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Xin": {
            "id": "IR",
            "abbreviation": "IR",
            "english": "Indirect Resource",
            "chinese": "偏印",
            "pinyin": "piān yìn",
            "meaning_male": [],
            "meaning_female": [],
        },
        "Geng": {
            "id": "DR",
            "abbreviation": "DR",
            "english": "Direct Resource",
            "chinese": "正印",
            "pinyin": "zhèng yìn",
            "meaning_male": [],
            "meaning_female": [],
        }
    }
}

# * =========================
# * INTERACTION SCORING CONFIGURATIONS
# * =========================
# NOTE: All scoring configurations have been moved into their respective interaction definitions
# - STEM_CONFLICTS: Each pattern now has embedded "scoring" dict
# - WUXING_ENERGY_FLOW: Contains "scoring" dict for generating/controlling
# - HIDDEN_QI_INTERACTIONS: Contains "damage" dict
# - PUNISHMENTS, HARMS, CLASHES, DESTRUCTION: Each pattern has embedded "scoring" dict

# * =========================
# * SEASONAL CONFIGURATIONS  
# * =========================

BRANCH_TO_SEASON = {
    "Yin": "Spring", "Mao": "Spring",
    "Si": "Summer", "Wu": "Summer",
    "Shen": "Autumn", "You": "Autumn",
    "Hai": "Winter", "Zi": "Winter",
    "Chen": "Spring-Earth", "Wei": "Summer-Earth", 
    "Xu": "Autumn-Earth", "Chou": "Winter-Earth"
}

SEASONAL_ADJUSTMENT = {
    "prosperous": 1.2,
    "growing": 1.1,
    "resting": 1.0,
    "imprisoned": 0.9,
    "dead": 0.8
}

ELEMENT_SEASONAL_STATES = SEASONAL_STRENGTH  # Alias for backward compatibility

HIDDEN_QI_INTERACTIONS = {
    "PRIMARY_PRIMARY": 1.0,    # Full interaction between primary Qi
    "PRIMARY_SECONDARY": 0.5,  # Half interaction with secondary Qi
    "SECONDARY_SECONDARY": 0.25, # Quarter interaction between secondary Qi
    "damage": {
        "damage_factor": 0.15  # For negative interactions on hidden qi
    }
}


# * =========================
# * BAZI INTERACTION PATTERNS
# * =========================

# * -------------------------
# * POSITIVE COMBINATION PATTERNS (Earthly Branches)
# * -------------------------

# Use formula-based scoring (defined at top of file)
_THREE_MEETINGS_SCORING = generate_scoring(
    BASE_SCORES["THREE_MEETINGS"]["combined"],
    BASE_SCORES["THREE_MEETINGS"]["transformed"],
    "three_branch"
)

THREE_MEETINGS = {
    "Yin-Mao-Chen": {
        "branches": ["Yin", "Mao", "Chen"], 
        "element": "Wood",
        "scoring": _THREE_MEETINGS_SCORING
    },
    "Si-Wu-Wei": {
        "branches": ["Si", "Wu", "Wei"], 
        "element": "Fire",
        "scoring": _THREE_MEETINGS_SCORING
    },
    "Shen-You-Xu": {
        "branches": ["Shen", "You", "Xu"], 
        "element": "Metal",
        "scoring": _THREE_MEETINGS_SCORING
    },
    "Hai-Zi-Chou": {
        "branches": ["Hai", "Zi", "Chou"], 
        "element": "Water",
        "scoring": _THREE_MEETINGS_SCORING
    }
}

_THREE_COMBINATIONS_SCORING = generate_scoring(
    BASE_SCORES["THREE_COMBINATIONS"]["combined"],
    BASE_SCORES["THREE_COMBINATIONS"]["transformed"],
    "three_branch"
)

THREE_COMBINATIONS = {
    "Yin-Wu-Xu": {       # 寅午戌合火
        "branches": ["Yin", "Wu", "Xu"],
        "element": "Fire",
        "scoring": _THREE_COMBINATIONS_SCORING
    },
    "Si-You-Chou": {    # 巳酉丑合金
        "branches": ["Si", "You", "Chou"],
        "element": "Metal",
        "scoring": _THREE_COMBINATIONS_SCORING
    },
    "Shen-Zi-Chen": {   # 申子辰合水
        "branches": ["Shen", "Zi", "Chen"],
        "element": "Water",
        "scoring": _THREE_COMBINATIONS_SCORING
    },
    "Hai-Mao-Wei": {    # 亥卯未合木
        "branches": ["Hai", "Mao", "Wei"],
        "element": "Wood",
        "scoring": _THREE_COMBINATIONS_SCORING
    }
}

_HALF_MEETINGS_SCORING = generate_scoring(
    BASE_SCORES["HALF_MEETINGS"]["combined"],
    BASE_SCORES["HALF_MEETINGS"]["transformed"],
    "two_branch"
)

HALF_MEETINGS = {
    # Wood (from Yin-Mao-Chen)
    "Yin-Chen": {
        "branches": ["Yin", "Chen"],
        "element": "Wood",
        "missing": "Mao",
        "blocked_by": ["Wu", "You", "Zi", "Chen"],
        "scoring": _HALF_MEETINGS_SCORING
    },
    # Fire (from Si-Wu-Wei)
    "Si-Wei": {
        "branches": ["Si", "Wei"],
        "element": "Fire",
        "missing": "Wu",
        "blocked_by": ["Mao", "Chou", "Zi"],
        "scoring": _HALF_MEETINGS_SCORING
    },
    # Metal (from Shen-You-Xu)
    "Shen-Xu": {
        "branches": ["Shen", "Xu"],
        "element": "Metal",
        "missing": "You",
        "blocked_by": ["Xu", "Mao", "Zi"],
        "scoring": _HALF_MEETINGS_SCORING
    },
    # Water (from Hai-Zi-Chou)
    "Hai-Chou": {
        "branches": ["Hai", "Chou"],
        "element": "Water",
        "missing": "Zi",
        "blocked_by": ["Wu", "Mao", "You", "Wei"],
        "scoring": _HALF_MEETINGS_SCORING
    },
}

_SIX_HARMONIES_SCORING = generate_scoring(
    BASE_SCORES["SIX_HARMONIES"]["combined"],
    BASE_SCORES["SIX_HARMONIES"]["transformed"],
    "two_branch"
)

SIX_HARMONIES = {
    "Zi-Chou": {
        "branches": ["Zi", "Chou"], 
        "element": "Earth",
        "scoring": _SIX_HARMONIES_SCORING
    },
    "Yin-Hai": {
        "branches": ["Yin", "Hai"], 
        "element": "Wood",
        "scoring": _SIX_HARMONIES_SCORING
    },
    "Mao-Xu": {
        "branches": ["Mao", "Xu"], 
        "element": "Fire",
        "scoring": _SIX_HARMONIES_SCORING
    },
    "Chen-You": {
        "branches": ["Chen", "You"], 
        "element": "Metal",
        "scoring": _SIX_HARMONIES_SCORING
    },
    "Si-Shen": {
        "branches": ["Si", "Shen"], 
        "element": "Water",
        "scoring": _SIX_HARMONIES_SCORING
    },
    "Wu-Wei": {
        "branches": ["Wu", "Wei"], 
        "element": "Fire",
        "scoring": _SIX_HARMONIES_SCORING
    }
}

# HALF_COMBINATIONS cannot transform (derivative of THREE_COMBINATIONS)
# Use single-state scoring (detected only, no transformation)
_HALF_COMBINATIONS_SCORING = {
    "detected": {
        "1": BASE_SCORES["HALF_COMBINATIONS"]["combined"],
        "2": round(BASE_SCORES["HALF_COMBINATIONS"]["combined"] * DISTANCE_MULTIPLIERS["two_branch"]["2"]),
        "3": round(BASE_SCORES["HALF_COMBINATIONS"]["combined"] * DISTANCE_MULTIPLIERS["two_branch"]["3"]),
        "4": round(BASE_SCORES["HALF_COMBINATIONS"]["combined"] * DISTANCE_MULTIPLIERS["two_branch"]["4"])
    }
}

HALF_COMBINATIONS = {
    "Yin-Wu": {
        "branches": ["Yin", "Wu"], 
        "element": "Fire",
        "scoring": _HALF_COMBINATIONS_SCORING
    },
    "Wu-Xu": {
        "branches": ["Wu", "Xu"], 
        "element": "Fire",
        "scoring": _HALF_COMBINATIONS_SCORING
    },
    "Si-You": {
        "branches": ["Si", "You"], 
        "element": "Metal",
        "scoring": _HALF_COMBINATIONS_SCORING
    },
    "You-Chou": {
        "branches": ["You", "Chou"], 
        "element": "Metal",
        "scoring": _HALF_COMBINATIONS_SCORING
    },
    "Shen-Zi": {
        "branches": ["Shen", "Zi"], 
        "element": "Water",
        "scoring": _HALF_COMBINATIONS_SCORING
    },
    "Zi-Chen": {
        "branches": ["Zi", "Chen"], 
        "element": "Water",
        "scoring": _HALF_COMBINATIONS_SCORING
    },
    "Hai-Mao": {
        "branches": ["Hai", "Mao"], 
        "element": "Wood",
        "scoring": _HALF_COMBINATIONS_SCORING
    },
    "Mao-Wei": {
        "branches": ["Mao", "Wei"], 
        "element": "Wood",
        "scoring": _HALF_COMBINATIONS_SCORING
    }
}

# ARCHED_COMBINATIONS cannot transform (derivative of THREE_COMBINATIONS)
# Use single-state scoring (detected only, no transformation)
_ARCHED_COMBINATIONS_SCORING = {
    "detected": {
        "1": BASE_SCORES["ARCHED_COMBINATIONS"]["combined"],
        "2": round(BASE_SCORES["ARCHED_COMBINATIONS"]["combined"] * DISTANCE_MULTIPLIERS["two_branch"]["2"]),
        "3": round(BASE_SCORES["ARCHED_COMBINATIONS"]["combined"] * DISTANCE_MULTIPLIERS["two_branch"]["3"]),
        "4": round(BASE_SCORES["ARCHED_COMBINATIONS"]["combined"] * DISTANCE_MULTIPLIERS["two_branch"]["4"])
    }
}

ARCHED_COMBINATIONS = {
    "Yin-Xu": {
        "branches": ["Yin", "Xu"], 
        "element": "Fire", 
        "missing": "Wu",
        "scoring": _ARCHED_COMBINATIONS_SCORING
    },
    "Si-Chou": {
        "branches": ["Si", "Chou"], 
        "element": "Metal", 
        "missing": "You",
        "scoring": _ARCHED_COMBINATIONS_SCORING
    },
    "Shen-Chen": {
        "branches": ["Shen", "Chen"], 
        "element": "Water", 
        "missing": "Zi",
        "scoring": _ARCHED_COMBINATIONS_SCORING
    },
    "Hai-Wei": {
        "branches": ["Hai", "Wei"], 
        "element": "Wood", 
        "missing": "Mao",
        "scoring": _ARCHED_COMBINATIONS_SCORING
    }
}

# * -------------------------
# * POSITIVE COMBINATION PATTERNS (Heavenly Stems)
# * -------------------------

_STEM_COMBINATIONS_SCORING = generate_scoring(
    BASE_SCORES["STEM_COMBINATIONS"]["combined"],
    BASE_SCORES["STEM_COMBINATIONS"]["transformed"],
    "two_branch"
)

STEM_COMBINATIONS = {
    "Jia-Ji": {    # 甲己合化土
        "interaction_type": "HS_COMBINATIONS",
        "transform_to": "Wu",
        "transform_element": "Earth",
        "transformation_requirement": {
            "element": "Earth",
            "location": "eb",
        },
        "scoring": _STEM_COMBINATIONS_SCORING,
        "meaning": {} # TODO: Add meaning
    },
    "Yi-Geng": {   # 乙庚合化金
        "interaction_type": "HS_COMBINATIONS",
        "transform_to": "Geng",
        "transform_element": "Metal",
        "transformation_requirement": {
            "element": "Metal",
            "location": "eb",
        },
        "scoring": _STEM_COMBINATIONS_SCORING,
        "meaning": {} # TODO: Add meaning
    },   
    "Bing-Xin": {  # 丙辛合化水
        "interaction_type": "HS_COMBINATIONS",
        "transform_to": "Ren",
        "transform_element": "Water",
        "transformation_requirement": {
            "element": "Water",
            "location": "eb",
        },
        "scoring": _STEM_COMBINATIONS_SCORING,
        "meaning": {} # TODO: Add meaning
    },
    "Ding-Ren": {  # 丁壬合化木
        "interaction_type": "HS_COMBINATIONS",
        "transform_to": "Jia",
        "transform_element": "Wood",
        "transformation_requirement": {
            "element": "Wood",
            "location": "eb",
        },
        "scoring": _STEM_COMBINATIONS_SCORING,
        "meaning": {
            "favorable": {
                "10god_a": "Loyalty and Trust",
                "10god_b": "Charm and Attractiveness",
                "10god_c": "Productivity and Growth",
                "10god_d": "Harmony and Balance",
                "10god_e": "Abundance",
                "10god_f": "",
                "10god_g": "",
                "10god_h": "",
                "10god_i": "",
                "10god_j": "",
            },
            "unfavorable": {
                "10god_a": "Amorous, questionable moral conduct, indulgence in sensual pleasures, and a tendency toward illicit or complicated relationships",
                "10god_b": "Emotional Turmoil",
                "10god_c": "Distraction from Goals",
                "10god_d": "",
                "10god_e": "",
                "10god_f": "",
                "10god_g": "",
                "10god_h": "",
                "10god_i": "",
                "10god_j": "",
            }
        }
    },
    "Wu-Gui": {  # 戊癸合化火
        "interaction_type": "HS_COMBINATIONS",
        "transform_to": "Bing",
        "transform_element": "Fire",
        "transformation_requirement": {
            "element": "Fire",
            "location": "eb",
        },
        "scoring": _STEM_COMBINATIONS_SCORING,
        "meaning": {} # TODO: Add meaning
    }
}

# * -------------------------
# * NEGATIVE INTERACTION PATTERNS
# * -------------------------

# Generate negative scoring using formula
# CLASHES: Two types based on elemental nature
# Opposite elements: Asymmetric (victim 1.0, controller 0.618)
_CLASHES_OPPOSITE_SCORING = generate_asymmetric_scoring(
    BASE_SCORES["CLASHES_OPPOSITE"]["damage"],
    "two_branch",
    ratio=0.618
)

# Same element: Equal mutual damage
_CLASHES_SAME_SCORING = generate_single_scoring(
    BASE_SCORES["CLASHES_SAME"]["damage"],
    "two_branch"
)

# STEM_CONFLICTS: Asymmetric (controller:victim = 0.618:1.0)
_STEM_CONFLICTS_SCORING = generate_asymmetric_scoring(
    BASE_SCORES["STEM_CONFLICTS"]["damage"],
    "two_branch",
    ratio=0.618
)

# PUNISHMENTS: Two separate base scores for different severity levels
# 3-node punishments: ELEVATED (38 damage - same as CLASHES)
_PUNISHMENTS_3NODE_SCORING = generate_single_scoring(
    BASE_SCORES["PUNISHMENTS_3NODE"]["damage"],
    "two_branch"
)

# 2-node punishments: Asymmetric (16 damage - less than HARMS 20)
_PUNISHMENTS_2NODE_SCORING = generate_asymmetric_scoring(
    BASE_SCORES["PUNISHMENTS_2NODE"]["damage"],
    "two_branch",
    ratio=0.618
)

# Self-punishments: Use 2-node scoring (equal mutual, 16 damage)
_PUNISHMENTS_SELF_SCORING = generate_single_scoring(
    BASE_SCORES["PUNISHMENTS_2NODE"]["damage"],
    "two_branch"
)

# HARMS: Asymmetric EB damage (controller:victim = 0.618:1.0)
_HARMS_SCORING = generate_asymmetric_scoring(
    BASE_SCORES["HARMS"]["damage"],
    "two_branch",
    ratio=0.618
)

# DESTRUCTION: Two types based on elemental nature, distance 0 only
# Opposite elements: Asymmetric (victim 1.0, controller 0.618)
_DESTRUCTION_OPPOSITE_SCORING = generate_asymmetric_scoring(
    BASE_SCORES["DESTRUCTION_OPPOSITE"]["damage"],
    "two_branch",
    ratio=0.618
)

# Same element: Equal mutual damage
_DESTRUCTION_SAME_SCORING = generate_single_scoring(
    BASE_SCORES["DESTRUCTION_SAME"]["damage"],
    "two_branch"
)

PUNISHMENTS = {
    # 3-node punishments: ELEVATED damage (38 each - same as CLASHES)
    "Yin-Si-Shen": {
        "branches": ["Yin", "Si", "Shen"], 
        "type": "3-node",
        "scoring": _PUNISHMENTS_3NODE_SCORING
    },
    "Chou-Wei-Xu": {
        "branches": ["Chou", "Wei", "Xu"], 
        "type": "3-node",
        "scoring": _PUNISHMENTS_3NODE_SCORING
    },
    
    # 2-node punishment: Asymmetric (controller:victim = 0.618:1, less than HARMS)
    "Zi-Mao": {
        "branches": ["Zi", "Mao"], 
        "type": "2-node",
        "controller": "Mao",  # Mao punishes Zi
        "controlled": "Zi",
        "scoring": _PUNISHMENTS_2NODE_SCORING
    },
    
    # Self-punishments: Equal mutual damage (16 each)
    "Chen-Chen": {
        "branches": ["Chen", "Chen"], 
        "type": "self",
        "scoring": _PUNISHMENTS_SELF_SCORING
    },
    "Wu-Wu": {
        "branches": ["Wu", "Wu"], 
        "type": "self",
        "scoring": _PUNISHMENTS_SELF_SCORING
    },
    "You-You": {
        "branches": ["You", "You"], 
        "type": "self",
        "scoring": _PUNISHMENTS_SELF_SCORING
    },
    "Hai-Hai": {
        "branches": ["Hai", "Hai"], 
        "type": "self",
        "scoring": _PUNISHMENTS_SELF_SCORING
    }
}

HARMS = {
    "Zi-Wei": {
        "branches": ["Zi", "Wei"],
        "controller": "Wei",
        "controlled": "Zi",
        "scoring": _HARMS_SCORING
    },
    "Chou-Wu": {
        "branches": ["Chou", "Wu"],
        "controller": "Wu",
        "controlled": "Chou",
        "scoring": _HARMS_SCORING
    },
    "Yin-Si": {
        "branches": ["Yin", "Si"],
        "controller": "Si",
        "controlled": "Yin",
        "scoring": _HARMS_SCORING
    },
    "Mao-Chen": {
        "branches": ["Mao", "Chen"],
        "controller": "Chen",
        "controlled": "Mao",
        "scoring": _HARMS_SCORING
    },
    "Shen-Hai": {
        "branches": ["Shen", "Hai"],
        "controller": "Hai",
        "controlled": "Shen",
        "scoring": _HARMS_SCORING
    },
    "You-Xu": {
        "branches": ["You", "Xu"],
        "controller": "Xu",
        "controlled": "You",
        "scoring": _HARMS_SCORING
    }
}

CLASHES = {
    # Opposite element clashes: Asymmetric (controller:victim = 0.618:1)
    "Zi-Wu": {
        "branches": ["Zi", "Wu"],
        "type": "opposite",
        "controller": "Zi",  # Water controls Fire
        "controlled": "Wu",
        "scoring": _CLASHES_OPPOSITE_SCORING
    },
    "Yin-Shen": {
        "branches": ["Yin", "Shen"],
        "type": "opposite",
        "controller": "Shen",  # Metal controls Wood
        "controlled": "Yin",
        "scoring": _CLASHES_OPPOSITE_SCORING
    },
    "Mao-You": {
        "branches": ["Mao", "You"],
        "type": "opposite",
        "controller": "You",  # Metal controls Wood
        "controlled": "Mao",
        "scoring": _CLASHES_OPPOSITE_SCORING
    },
    "Si-Hai": {
        "branches": ["Si", "Hai"],
        "type": "opposite",
        "controller": "Hai",  # Water controls Fire
        "controlled": "Si",
        "scoring": _CLASHES_OPPOSITE_SCORING
    },
    
    # Same element clashes: Equal mutual damage
    "Chou-Wei": {
        "branches": ["Chou", "Wei"],
        "type": "same",
        "scoring": _CLASHES_SAME_SCORING
    },
    "Chen-Xu": {
        "branches": ["Chen", "Xu"],
        "type": "same",
        "scoring": _CLASHES_SAME_SCORING
    }
}

DESTRUCTION = {
    # Distance 0 only (adjacent in natal, or luck↔natal overlays)
    # Opposite element: Asymmetric (controller:victim = 0.618:1)
    "Zi-You": {
        "branches": ["Zi", "You"],
        "type": "opposite",
        "controller": "You",  # Metal (You) generates Water (Zi), expends energy
        "controlled": "Zi",
        "scoring": _DESTRUCTION_OPPOSITE_SCORING
    },
    "Wu-Mao": {
        "branches": ["Wu", "Mao"],
        "type": "opposite",
        "controller": "Mao",  # Wood (Mao) generates Fire (Wu), expends energy
        "controlled": "Wu",
        "scoring": _DESTRUCTION_OPPOSITE_SCORING
    },
    
    # Same element: Equal mutual damage
    "Chen-Chou": {
        "branches": ["Chen", "Chou"],
        "type": "same",
        "scoring": _DESTRUCTION_SAME_SCORING
    },
    "Wei-Xu": {
        "branches": ["Wei", "Xu"],
        "type": "same",
        "scoring": _DESTRUCTION_SAME_SCORING
    }
}

STEM_CONFLICTS = {
    "Jia-Geng": {
        "controller": "Geng",
        "controlled": "Jia",
        "scoring": _STEM_CONFLICTS_SCORING
    },
    "Yi-Xin": {
        "controller": "Xin",
        "controlled": "Yi",
        "scoring": _STEM_CONFLICTS_SCORING
    },
    "Bing-Ren": {
        "controller": "Ren",
        "controlled": "Bing",
        "scoring": _STEM_CONFLICTS_SCORING
    },
    "Ding-Gui": {
        "controller": "Gui",
        "controlled": "Ding",
        "scoring": _STEM_CONFLICTS_SCORING
    },
    "Wu-Jia": {
        "controller": "Jia",
        "controlled": "Wu",
        "scoring": _STEM_CONFLICTS_SCORING
    },
    "Ji-Yi": {
        "controller": "Yi",
        "controlled": "Ji",
        "scoring": _STEM_CONFLICTS_SCORING
    },
    "Geng-Bing": {
        "controller": "Bing",
        "controlled": "Geng",
        "scoring": _STEM_CONFLICTS_SCORING
    },
    "Xin-Ding": {
        "controller": "Ding",
        "controlled": "Xin",
        "scoring": _STEM_CONFLICTS_SCORING
    },
    "Ren-Wu": {
        "controller": "Wu",
        "controlled": "Ren",
        "scoring": _STEM_CONFLICTS_SCORING
    },
    "Gui-Ji": {
        "controller": "Ji",
        "controlled": "Gui",
        "scoring": _STEM_CONFLICTS_SCORING
    }
}

# WuXing Energy Flow (for adjacency)
WUXING_ENERGY_FLOW = {
    "generation": {
        "Wood": "Fire",
        "Fire": "Earth",
        "Earth": "Metal",
        "Metal": "Water",
        "Water": "Wood"
    },
    "control": {
        "Wood": "Earth",
        "Earth": "Water",
        "Water": "Fire",
        "Fire": "Metal",
        "Metal": "Wood"
    },
    "scoring": {
        "generating": {
            "generator_loss": 7,
            "receiver_gain": 10,
            "count_increment": 0.25
        },
        "controlling": {
            "controller_loss": 5,
            "controlled_loss": 10,
            "count_decrement": 0.25
        }
    }
}

# ==================
# TRANSFORMATION STRENGTH TIERS
# ==================
# Defines the relative strength of different transformation types
# Used to determine primary transformation when multiple transformations occur

TRANSFORMATION_STRENGTH = {
    "THREE_MEETINGS": "strong",            # 三會 - Directional/Seasonal combos (strongest)
    "THREE_COMBINATIONS": "normal",        # 三合 - Triangular combos
    "ARCHED_COMBINATIONS": "normal",       # 拱合 - Arched combos
    "SIX_HARMONIES": "weak",               # 六合 - Pair combos  
    "HALF_COMBINATIONS": "weak"            # 半合 - Half combos (weakest)
}

# Strength tier ordering (for sorting)
STRENGTH_ORDER = {
    "ultra_strong": 0,
    "strong": 1,
    "normal": 2,
    "weak": 3
}










# TODO:
# Yin Yin: gila kekuasaan
# Zi Zi: ocd polaris


# TODO: layer 2 combination interaction
# THREE MEETINGS vs THREE MEETINGS


# TODO: shadow HALF MEEETINGS (when one branch is missing) it should become shadow node
# THAT CAN INTERACT