# * =========================
# * NEGATIVE CONFLICT PATTERNS (DERIVED FROM CORE)
# * =========================
# All negative/destructive branch and stem interactions
# Patterns are DERIVED from core.py STEMS and BRANCHES.

from .core import STEMS, BRANCHES
from .derived import ELEMENT_CYCLES
from .scoring import (
    BASE_SCORES,
    generate_single_scoring,
    generate_asymmetric_scoring,
)

# * -------------------------
# * SCORING CONFIGURATIONS
# * -------------------------

_CLASHES_OPPOSITE_SCORING = generate_asymmetric_scoring(
    BASE_SCORES["CLASHES_OPPOSITE"]["damage"],
    "two_branch",
    ratio=0.618
)
_CLASHES_SAME_SCORING = generate_single_scoring(
    BASE_SCORES["CLASHES_SAME"]["damage"],
    "two_branch"
)
_STEM_CONFLICTS_SCORING = generate_asymmetric_scoring(
    BASE_SCORES["STEM_CONFLICTS"]["damage"],
    "two_branch",
    ratio=0.618
)
_PUNISHMENTS_3NODE_SCORING = generate_single_scoring(
    BASE_SCORES["PUNISHMENTS_3NODE"]["damage"],
    "two_branch"
)
_PUNISHMENTS_2NODE_SCORING = generate_asymmetric_scoring(
    BASE_SCORES["PUNISHMENTS_2NODE"]["damage"],
    "two_branch",
    ratio=0.618
)
_PUNISHMENTS_SELF_SCORING = generate_single_scoring(
    BASE_SCORES["PUNISHMENTS_2NODE"]["damage"],
    "two_branch"
)
_HARMS_SCORING = generate_asymmetric_scoring(
    BASE_SCORES["HARMS"]["damage"],
    "two_branch",
    ratio=0.618
)
_DESTRUCTION_OPPOSITE_SCORING = generate_asymmetric_scoring(
    BASE_SCORES["DESTRUCTION_OPPOSITE"]["damage"],
    "two_branch",
    ratio=0.618
)
_DESTRUCTION_SAME_SCORING = generate_single_scoring(
    BASE_SCORES["DESTRUCTION_SAME"]["damage"],
    "two_branch"
)

# * -------------------------
# * PUNISHMENTS (刑)
# * -------------------------

_punishment_groups = {}
_self_punishments = []

for branch_id, branch in BRANCHES.items():
    punishment_group = branch.get("punishment_group")
    if punishment_group:
        group_key = "-".join(punishment_group[:3])
        if group_key not in _punishment_groups:
            _punishment_groups[group_key] = {
                "branches": list(punishment_group[:3]),
                "type": punishment_group[3]
            }

    punishment_pair = branch.get("punishment_pair")
    if punishment_pair:
        partner, pun_type, role = punishment_pair
        pair_key = f"{branch_id}-{partner}" if role == "controller" else f"{partner}-{branch_id}"
        if pair_key not in _punishment_groups:
            _punishment_groups[pair_key] = {
                "branches": [branch_id, partner] if role == "controller" else [partner, branch_id],
                "type": pun_type,
                "controller": branch_id if role == "controller" else partner,
                "controlled": partner if role == "controller" else branch_id,
            }

    if branch.get("self_punishment"):
        _self_punishments.append(branch_id)

PUNISHMENTS = {}

for group_key, group in _punishment_groups.items():
    branches = group["branches"]
    pun_type = group["type"]

    if len(branches) == 3:
        if pun_type == "shi":
            PUNISHMENTS[group_key] = {
                "branches": branches,
                "type": "3-node",
                "category": "shi_xing",
                "chinese_name": "勢刑",
                "english_name": "Bullying Punishment",
                "severity": "severe",
                "element_conflict": True,
                "scoring": _PUNISHMENTS_3NODE_SCORING,
                "description": "Three powerful branches in mutual conflict (恃勢之刑)"
            }
        elif pun_type == "wu_li":
            PUNISHMENTS[group_key] = {
                "branches": branches,
                "type": "3-node",
                "category": "wu_li_xing",
                "chinese_name": "無禮刑",
                "english_name": "Rudeness Punishment",
                "severity": "moderate",
                "element_conflict": False,
                "scoring": _PUNISHMENTS_3NODE_SCORING,
                "description": "Earth branches showing disrespect to each other (無禮之刑)"
            }
    elif len(branches) == 2 and pun_type == "en":
        controller = group.get("controller")
        controlled = group.get("controlled")
        PUNISHMENTS[group_key] = {
            "branches": branches,
            "type": "2-node",
            "category": "en_xing",
            "chinese_name": "恩刑",
            "english_name": "Ungrateful Punishment",
            "severity": "light",
            "controller": controller,
            "controlled": controlled,
            "element_relationship": "productive",
            "scoring": _PUNISHMENTS_2NODE_SCORING,
            "description": "Beneficiary punishes benefactor - betrayal (持恩之刑)"
        }

# Self-punishment data now embedded in BRANCHES as self_punishment_nature
for branch_id in _self_punishments:
    branch = BRANCHES[branch_id]
    nature = branch.get("self_punishment_nature", "Self-conflict")
    key = f"{branch_id}-{branch_id}"
    PUNISHMENTS[key] = {
        "branches": [branch_id, branch_id],
        "type": "self",
        "category": "zi_xing",
        "chinese_name": "自刑",
        "english_name": f"Self-Punishment ({branch['animal']})",
        "severity": "self",
        "element": branch["element"],
        "nature": nature,
        "scoring": _PUNISHMENTS_SELF_SCORING,
        "description": f"{branch['animal']}'s nature punishes itself ({branch_id}自刑)"
    }

PUNISHMENT_SEVERITY = {
    "severe": 1.0,
    "moderate": 0.85,
    "light": 0.70,
    "self": 0.60
}

# * -------------------------
# * HARMS (害)
# * -------------------------

_harms_seen = set()
HARMS = {}
for branch_id, branch in BRANCHES.items():
    partner = branch.get("harms")
    role = branch.get("harm_role")
    if partner and role:
        pair = tuple(sorted([branch_id, partner]))
        if pair not in _harms_seen:
            _harms_seen.add(pair)
            if role == "controller":
                controller, controlled = branch_id, partner
            else:
                controller, controlled = partner, branch_id
            key = f"{pair[0]}-{pair[1]}"
            HARMS[key] = {
                "branches": list(pair),
                "controller": controller,
                "controlled": controlled,
                "scoring": _HARMS_SCORING
            }

# * -------------------------
# * CLASHES (沖)
# * -------------------------

_clashes_seen = set()
CLASHES = {}
for branch_id, branch in BRANCHES.items():
    partner = branch.get("clashes")
    if partner:
        pair = tuple(sorted([branch_id, partner]))
        if pair not in _clashes_seen:
            _clashes_seen.add(pair)
            b1_elem = branch["element"]
            b2_elem = BRANCHES[partner]["element"]

            if b1_elem == b2_elem:
                clash_type = "same"
                scoring = _CLASHES_SAME_SCORING
                key = f"{pair[0]}-{pair[1]}"
                CLASHES[key] = {
                    "branches": list(pair),
                    "type": clash_type,
                    "scoring": scoring
                }
            else:
                clash_type = "opposite"
                scoring = _CLASHES_OPPOSITE_SCORING
                if ELEMENT_CYCLES["controlling"].get(b1_elem) == b2_elem:
                    controller, controlled = branch_id, partner
                else:
                    controller, controlled = partner, branch_id
                key = f"{pair[0]}-{pair[1]}"
                CLASHES[key] = {
                    "branches": list(pair),
                    "type": clash_type,
                    "controller": controller,
                    "controlled": controlled,
                    "scoring": scoring
                }

# * -------------------------
# * DESTRUCTION (破)
# * -------------------------

_destruction_seen = set()
DESTRUCTION = {}
for branch_id, branch in BRANCHES.items():
    partner = branch.get("destroys")
    if partner:
        pair = tuple(sorted([branch_id, partner]))
        if pair not in _destruction_seen:
            _destruction_seen.add(pair)
            b1_elem = branch["element"]
            b2_elem = BRANCHES[partner]["element"]

            if b1_elem == b2_elem:
                dest_type = "same"
                scoring = _DESTRUCTION_SAME_SCORING
                key = f"{pair[0]}-{pair[1]}"
                DESTRUCTION[key] = {
                    "branches": list(pair),
                    "type": dest_type,
                    "scoring": scoring
                }
            else:
                dest_type = "opposite"
                scoring = _DESTRUCTION_OPPOSITE_SCORING
                if ELEMENT_CYCLES["generating"].get(b1_elem) == b2_elem:
                    controller, controlled = branch_id, partner
                else:
                    controller, controlled = partner, branch_id
                key = f"{pair[0]}-{pair[1]}"
                DESTRUCTION[key] = {
                    "branches": list(pair),
                    "type": dest_type,
                    "controller": controller,
                    "controlled": controlled,
                    "scoring": scoring
                }

# * -------------------------
# * STEM CONFLICTS (天干相剋)
# * -------------------------

_stem_conflicts_seen = set()
STEM_CONFLICTS = {}
for stem_id, stem in STEMS.items():
    controlled = stem.get("controls")
    if controlled:
        pair = tuple(sorted([stem_id, controlled]))
        if pair not in _stem_conflicts_seen:
            _stem_conflicts_seen.add(pair)
            key = f"{pair[0]}-{pair[1]}"
            STEM_CONFLICTS[key] = {
                "controller": stem_id,
                "controlled": controlled,
                "scoring": _STEM_CONFLICTS_SCORING
            }

# * -------------------------
# * WUXING ENERGY FLOW (五行流動)
# * -------------------------

WUXING_ENERGY_FLOW = {
    "generation": ELEMENT_CYCLES["generating"],
    "control": ELEMENT_CYCLES["controlling"],
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
