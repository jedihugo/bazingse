# * =========================
# * QI PHASE (十二長生 / Twelve Life Stages)
# * =========================
# Classical BaZi concept describing the life cycle of each element
# through 12 phases as it moves through the Earthly Branches.
#
# Principle: 陽順陰逆 (Yang Forward, Yin Reverse)
# - Yang stems progress forward through branches from their birth point
# - Yin stems progress backward through branches from their birth point

# The 12 Qi Phases in lifecycle order
QI_PHASES = [
    {
        "id": "changsheng",
        "chinese": "長生",
        "english": "Birth",
        "description": "Element is born, full of potential",
        "strength": "strong",
        "order": 0
    },
    {
        "id": "muyu",
        "chinese": "沐浴",
        "english": "Bathing",
        "description": "Vulnerable stage, like bathing a newborn",
        "strength": "weak",
        "order": 1
    },
    {
        "id": "guandai",
        "chinese": "冠帶",
        "english": "Capping",
        "description": "Coming of age, putting on the cap",
        "strength": "growing",
        "order": 2
    },
    {
        "id": "linguan",
        "chinese": "臨官",
        "english": "Official",
        "description": "Taking office, career begins",
        "strength": "strong",
        "order": 3
    },
    {
        "id": "diwang",
        "chinese": "帝旺",
        "english": "Peak",
        "description": "Emperor stage, maximum power",
        "strength": "peak",
        "order": 4
    },
    {
        "id": "shuai",
        "chinese": "衰",
        "english": "Decline",
        "description": "Beginning to weaken",
        "strength": "declining",
        "order": 5
    },
    {
        "id": "bing",
        "chinese": "病",
        "english": "Sickness",
        "description": "Getting ill, energy depleted",
        "strength": "weak",
        "order": 6
    },
    {
        "id": "si",
        "chinese": "死",
        "english": "Death",
        "description": "Dying, end of active cycle",
        "strength": "dead",
        "order": 7
    },
    {
        "id": "mu",
        "chinese": "墓",
        "english": "Tomb",
        "description": "Buried, stored away (also: Storage/庫)",
        "strength": "stored",
        "order": 8
    },
    {
        "id": "jue",
        "chinese": "絕",
        "english": "Extinction",
        "description": "Complete ending, void",
        "strength": "dead",
        "order": 9
    },
    {
        "id": "tai",
        "chinese": "胎",
        "english": "Embryo",
        "description": "New conception begins",
        "strength": "nascent",
        "order": 10
    },
    {
        "id": "yang",
        "chinese": "養",
        "english": "Nurturing",
        "description": "Being nurtured in womb",
        "strength": "nascent",
        "order": 11
    }
]

# Create lookup by id
QI_PHASE_BY_ID = {phase["id"]: phase for phase in QI_PHASES}

# Branch order for index calculations
BRANCH_ORDER = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]
BRANCH_INDEX = {branch: i for i, branch in enumerate(BRANCH_ORDER)}

# Birth points (長生 location) for each Heavenly Stem
# Yang stems: forward progression | Yin stems: reverse progression
STEM_BIRTH_POINTS = {
    # Yang stems (forward from birth point)
    "Jia": {"birth_branch": "Hai", "direction": "forward"},   # Yang Wood born at Hai (Water produces Wood)
    "Bing": {"birth_branch": "Yin", "direction": "forward"},  # Yang Fire born at Yin (Wood produces Fire)
    "Wu": {"birth_branch": "Yin", "direction": "forward"},    # Yang Earth born at Yin (same as Fire)
    "Geng": {"birth_branch": "Si", "direction": "forward"},   # Yang Metal born at Si
    "Ren": {"birth_branch": "Shen", "direction": "forward"},  # Yang Water born at Shen (Metal produces Water)

    # Yin stems (reverse from birth point) - 陽順陰逆
    "Yi": {"birth_branch": "Wu", "direction": "reverse"},     # Yin Wood born at Wu
    "Ding": {"birth_branch": "You", "direction": "reverse"},  # Yin Fire born at You
    "Ji": {"birth_branch": "You", "direction": "reverse"},    # Yin Earth born at You (same as Ding)
    "Xin": {"birth_branch": "Zi", "direction": "reverse"},    # Yin Metal born at Zi
    "Gui": {"birth_branch": "Mao", "direction": "reverse"},   # Yin Water born at Mao
}

def get_qi_phase(stem_id: str, branch_id: str) -> dict:
    """
    Get the Qi Phase for a Heavenly Stem in a given Earthly Branch.

    Args:
        stem_id: Heavenly Stem ID (e.g., "Jia", "Yi", "Bing", ...)
        branch_id: Earthly Branch ID (e.g., "Zi", "Chou", "Yin", ...)

    Returns:
        dict with phase info: {id, chinese, english, description, strength, order}
    """
    if stem_id not in STEM_BIRTH_POINTS:
        return None
    if branch_id not in BRANCH_INDEX:
        return None

    birth_info = STEM_BIRTH_POINTS[stem_id]
    birth_branch = birth_info["birth_branch"]
    direction = birth_info["direction"]

    birth_idx = BRANCH_INDEX[birth_branch]
    current_idx = BRANCH_INDEX[branch_id]

    if direction == "forward":
        # Yang stems: count forward from birth point
        # Phase index = (current - birth) mod 12
        phase_idx = (current_idx - birth_idx) % 12
    else:
        # Yin stems: count backward from birth point
        # Phase index = (birth - current) mod 12
        phase_idx = (birth_idx - current_idx) % 12

    return QI_PHASES[phase_idx].copy()


def get_qi_phase_for_pillar(hs_id: str, eb_id: str) -> dict:
    """
    Get Qi Phase for a pillar (HS in context of its EB).
    Returns the phase of the Heavenly Stem relative to the Earthly Branch.

    This answers: "What life stage is this HS experiencing in this EB?"
    """
    phase = get_qi_phase(hs_id, eb_id)
    if phase:
        phase["stem"] = hs_id
        phase["branch"] = eb_id
    return phase


# Pre-computed full lookup table for performance
# Format: QI_PHASE_TABLE[stem_id][branch_id] = phase_id
QI_PHASE_TABLE = {}
for stem_id in STEM_BIRTH_POINTS:
    QI_PHASE_TABLE[stem_id] = {}
    for branch_id in BRANCH_ORDER:
        phase = get_qi_phase(stem_id, branch_id)
        QI_PHASE_TABLE[stem_id][branch_id] = phase["id"] if phase else None


def get_qi_phase_id(stem_id: str, branch_id: str) -> str:
    """Fast lookup returning just the phase ID."""
    return QI_PHASE_TABLE.get(stem_id, {}).get(branch_id)


# Strength categories for UI styling
QI_PHASE_STRENGTH_COLORS = {
    "peak": "#22c55e",      # Green - maximum power
    "strong": "#84cc16",    # Lime - strong
    "growing": "#a3e635",   # Light lime - developing
    "declining": "#fbbf24", # Amber - weakening
    "weak": "#f97316",      # Orange - weak
    "dead": "#ef4444",      # Red - no power
    "stored": "#8b5cf6",    # Purple - stored/hidden
    "nascent": "#06b6d4",   # Cyan - potential/forming
}
