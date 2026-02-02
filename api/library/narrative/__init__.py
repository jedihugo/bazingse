# * =========================
# * BAZI NARRATIVE INTERPRETATION SYSTEM
# * =========================
# Generates human-readable narrative text (no AI) about WuXing interactions,
# element balance, Shen Sha, wealth storage, and remedies.
#
# Core Principle: All BaZi logic lives in the backend. Frontend only displays.
#
# Usage: from library.narrative import generate_narrative

from .interpreter import generate_narrative
from .templates import NARRATIVE_TEMPLATES
from .priority import calculate_priority_score, prioritize_narratives
from .modifiers import (
    apply_element_modifiers,
    apply_shen_sha_modifiers,
    get_element_balance_context,
)
from .remedies import (
    generate_remedies,
    REMEDY_TEMPLATES,
    ELEMENT_REMEDIES,
)
from .localization import (
    build_narrative_text,
    get_localized_template,
    SUPPORTED_LOCALES,
)
from .chain_engine import (
    analyze_node_chain,
    enrich_clash_with_chain_analysis,
    SHEN_SHA_MEANINGS,
    QI_PHASE_MEANINGS,
    STORAGE_BRANCHES,
)
from .qi_phase import (
    get_qi_phase,
    get_qi_phase_for_stem,
    get_storage_info,
    get_qi_phase_narrative_context,
    QI_PHASE_INFO,
    QI_PHASE_ORDER,
)
from .pillar_story import generate_pillar_stories

__all__ = [
    # Main entry point
    "generate_narrative",
    # Templates
    "NARRATIVE_TEMPLATES",
    # Priority
    "calculate_priority_score",
    "prioritize_narratives",
    # Modifiers
    "apply_element_modifiers",
    "apply_shen_sha_modifiers",
    "get_element_balance_context",
    # Remedies
    "generate_remedies",
    "REMEDY_TEMPLATES",
    "ELEMENT_REMEDIES",
    # Localization
    "build_narrative_text",
    "get_localized_template",
    "SUPPORTED_LOCALES",
    # Pillar-based stories
    "generate_pillar_stories",
]
