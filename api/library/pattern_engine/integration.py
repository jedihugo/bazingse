# * =============================================================================
# * PATTERN ENGINE INTEGRATION
# * =============================================================================
# * Bridges the existing BaZi analysis with the new Pattern Engine.
# * Provides enhanced pattern detection, severity calculation, and predictions.
# * =============================================================================

from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass, field

from .pattern_spec import (
    PatternCategory,
    LifeDomain,
    SeasonalState,
    BadgeType,
)
from .pattern_registry import PatternRegistry, get_global_registry
from .patterns import load_all_patterns, get_special_stars_for_day_master, get_special_stars_for_year_branch
from .life_events import (
    calculate_pattern_severity,
    calculate_compound_severity,
    calculate_health_severity,
    SeverityResult,
    ALL_EVENT_TYPES,
    TCM_ORGANS,
    SEASONAL_STATE_MULTIPLIERS,
)


# =============================================================================
# PATTERN MATCH RESULT
# =============================================================================

@dataclass
class EnhancedPatternMatch:
    """Enhanced pattern match with full metadata."""
    pattern_id: str
    category: str
    chinese_name: str
    english_name: str
    participants: List[str]
    distance: int
    is_transformed: bool
    severity: SeverityResult
    affected_domains: List[str]
    pillar_meaning: str
    event_predictions: List[Dict[str, Any]]


# =============================================================================
# INTERACTION TO PATTERN MAPPING
# =============================================================================

# Map interaction type prefixes to pattern categories
INTERACTION_TYPE_TO_CATEGORY = {
    "THREE_MEETINGS": "three_meetings",
    "THREE_COMBINATIONS": "three_combinations",
    "SIX_HARMONIES": "six_harmonies",
    "HALF_MEETINGS": "half_meetings",
    "HALF_COMBINATIONS": "half_combinations",
    "ARCHED_COMBINATIONS": "arched_combinations",
    "HS_COMBINATIONS": "stem_combination",
    "STEM_COMBINATION": "stem_combination",
    "CLASH": "clash",
    "CLASHES": "clash",
    "PUNISHMENT": "punishment",
    "PUNISHMENTS": "punishment",
    "HARM": "harm",
    "HARMS": "harm",
    "DESTRUCTION": "destruction",
    "STEM_CONFLICT": "stem_conflict",
    "STEM_CONFLICTS": "stem_conflict",
}


def parse_interaction_id(interaction_id: str) -> Tuple[str, List[str], str]:
    """
    Parse interaction ID into components.

    Format: TYPE~PARTICIPANTS~NODES or TYPE~PARTICIPANTS
    Example: "THREE_MEETINGS~Si-Wu-Wei~eb_10yl-eb_ml-eb_m" -> ("THREE_MEETINGS", ["Si", "Wu", "Wei"], "eb_10yl-eb_ml-eb_m")
    """
    parts = interaction_id.split("~")

    if len(parts) >= 3:
        int_type = parts[0]
        participants = parts[1].split("-")
        result = parts[2]  # This is actually node references, not element
    elif len(parts) == 2:
        int_type = parts[0]
        participants = parts[1].split("-")
        result = ""
    else:
        int_type = parts[0]
        participants = []
        result = ""

    return int_type, participants, result


def construct_registry_pattern_id(int_type: str, participants: List[str], element: Optional[str] = None, subtype: Optional[str] = None, trailing_tilde: bool = False) -> str:
    """
    Construct a pattern ID for registry lookup.

    Registry patterns use format: TYPE~PARTICIPANTS~ELEMENT or TYPE~PARTICIPANTS~SUBTYPE
    Example: "THREE_MEETINGS~Yin-Mao-Chen~Wood", "SIX_HARMONIES~Zi-Chou~Earth"

    NOTE: Registry patterns may use directional order, not alphabetical.
    This function tries original order first.

    Some patterns like HARM have empty suffix: "HARM~Zi-Wei~"
    """
    participants_str = "-".join(participants)

    if element:
        return f"{int_type}~{participants_str}~{element}"
    elif subtype:
        return f"{int_type}~{participants_str}~{subtype}"
    elif trailing_tilde:
        return f"{int_type}~{participants_str}~"  # Empty suffix with trailing ~
    else:
        return f"{int_type}~{participants_str}"


def find_pattern_in_registry(registry, int_type: str, participants: List[str], element: Optional[str] = None, subtype: Optional[str] = None):
    """
    Find a pattern in the registry, trying multiple participant orderings.

    Registry patterns may use directional order (not alphabetical), so we try:
    1. Original order from interaction
    2. Reversed order (for 2-participant patterns like SIX_HARMONIES)
    3. Search by matching participant set (for any order)
    4. All orderings with trailing tilde (for HARM patterns etc.)
    """
    from itertools import permutations

    # Build candidate IDs to try
    candidates = []

    # 1. Original order (without and with trailing tilde)
    orig_id = construct_registry_pattern_id(int_type, participants, element, subtype)
    candidates.append(orig_id)
    orig_id_tilde = construct_registry_pattern_id(int_type, participants, element, subtype, trailing_tilde=True)
    if orig_id_tilde not in candidates:
        candidates.append(orig_id_tilde)

    # 2. For 2-participant patterns, try reversed (with and without trailing tilde)
    if len(participants) == 2:
        rev_participants = list(reversed(participants))
        rev_id = construct_registry_pattern_id(int_type, rev_participants, element, subtype)
        if rev_id not in candidates:
            candidates.append(rev_id)
        rev_id_tilde = construct_registry_pattern_id(int_type, rev_participants, element, subtype, trailing_tilde=True)
        if rev_id_tilde not in candidates:
            candidates.append(rev_id_tilde)

    # 3. Try all permutations for 3-participant patterns (with and without trailing tilde)
    if len(participants) == 3:
        for perm in permutations(participants):
            perm_list = list(perm)
            perm_id = construct_registry_pattern_id(int_type, perm_list, element, subtype)
            if perm_id not in candidates:
                candidates.append(perm_id)
            perm_id_tilde = construct_registry_pattern_id(int_type, perm_list, element, subtype, trailing_tilde=True)
            if perm_id_tilde not in candidates:
                candidates.append(perm_id_tilde)

    # Try each candidate
    for candidate_id in candidates:
        pattern = registry.get(candidate_id)
        if pattern:
            return pattern

    return None


def get_pillar_name_from_position(position: int) -> str:
    """Convert position code to pillar name."""
    POSITION_NAMES = {
        0: "hour",
        1: "day",
        2: "month",
        3: "year",
        4: "10yl",
        5: "annual",
        6: "monthly",
        7: "daily",
        8: "hourly",
    }
    return POSITION_NAMES.get(position, "unknown")


# =============================================================================
# PATTERN ENGINE ANALYZER
# =============================================================================

class PatternEngineAnalyzer:
    """
    Integrates Pattern Engine with existing BaZi analysis.

    Provides:
    - Enhanced pattern detection with registry lookup
    - Severity calculation using multiple factors
    - Life event predictions based on patterns
    - Special star detection for Day Master
    """

    def __init__(self):
        """Initialize with loaded pattern registry."""
        self.registry = load_all_patterns()

    def analyze_interactions(
        self,
        interactions: Dict[str, Any],
        seasonal_states: Dict[str, str],
        daymaster_stem: str,
        daymaster_element: str,
        post_element_score: Dict[str, float],
        year_branch: str = "",
    ) -> Dict[str, Any]:
        """
        Analyze existing interactions through Pattern Engine.

        Args:
            interactions: Raw interaction dict from bazingse.py
            seasonal_states: Element -> Seasonal state mapping
            daymaster_stem: Day Master heavenly stem (e.g., "Gui")
            daymaster_element: Day Master element (e.g., "Water")
            post_element_score: Post-interaction element scores
            year_branch: Year Earthly Branch (e.g., "Yin") for Year Branch-dependent stars

        Returns:
            Enhanced analysis with severity, predictions, and recommendations
        """
        enhanced_patterns: List[EnhancedPatternMatch] = []
        domain_risks: Dict[str, List[Dict]] = {domain.value: [] for domain in LifeDomain}
        affected_elements: Set[str] = set()

        # Process each interaction
        for int_id, int_data in interactions.items():
            if isinstance(int_data, str):
                continue  # Skip metadata entries

            # Parse interaction
            int_type, participants, _ = parse_interaction_id(int_id)

            # Get category
            category = INTERACTION_TYPE_TO_CATEGORY.get(int_type, "unknown")
            if category == "unknown":
                continue

            # Get element from interaction data (for combinations)
            pattern_element = int_data.get("element")

            # If no element in data, try to infer from participants
            if not pattern_element and participants:
                from ..core import STEMS, BRANCHES
                for p in participants:
                    if p in STEMS:
                        pattern_element = STEMS[p].get("element")
                        break
                    elif p in BRANCHES:
                        pattern_element = BRANCHES[p].get("element")
                        break

            # Look up pattern in registry (tries multiple orderings)
            pattern = find_pattern_in_registry(self.registry, int_type, participants, pattern_element)

            # Try alternate lookups if not found
            if not pattern:
                # CLASH patterns use "opposite" or "same" instead of element
                if int_type == "CLASH":
                    for subtype in ["opposite", "same"]:
                        pattern = find_pattern_in_registry(self.registry, int_type, participants, subtype=subtype)
                        if pattern:
                            break

            # Try without element suffix for STEM_CONFLICT
            if not pattern and int_type == "STEM_CONFLICT":
                pattern = find_pattern_in_registry(self.registry, int_type, participants)

            # Try HARM patterns - they have empty suffix
            if not pattern and int_type == "HARM":
                pattern = find_pattern_in_registry(self.registry, int_type, participants)

            # Get interaction metadata
            distance_raw = int_data.get("distance", 1)
            # Handle string distance formats like "distance_1" or "1"
            if isinstance(distance_raw, str):
                if distance_raw.startswith("distance_"):
                    distance = int(distance_raw.split("_")[1])
                else:
                    try:
                        distance = int(distance_raw)
                    except ValueError:
                        distance = 1
            else:
                distance = int(distance_raw) if distance_raw else 1

            is_transformed = int_data.get("transformed", False)

            if pattern_element:
                affected_elements.add(pattern_element)

            # Get seasonal state for pattern element
            seasonal_state = seasonal_states.get(pattern_element, "Resting") if pattern_element else "Resting"

            # Extract primary pillar position
            positions = int_data.get("positions", [])
            primary_position = min(positions) if positions else 1

            # Calculate severity
            severity = calculate_pattern_severity(
                pattern_id=int_id,
                pattern_category=category,
                distance=distance,
                seasonal_state=seasonal_state,
                pillar_position=primary_position,
                daymaster_element=daymaster_element,
                pattern_element=pattern_element,
                is_transformed=is_transformed,
            )

            # Get pattern metadata from registry or defaults
            chinese_name = pattern.chinese_name if pattern else int_type
            english_name = pattern.english_name if pattern else int_type
            affected_domains = [d.value for d in pattern.life_domains] if pattern else []
            pillar_meaning = ""

            if pattern and pattern.pillar_meanings:
                pillar_name = get_pillar_name_from_position(primary_position)
                pillar_meaning = getattr(pattern.pillar_meanings, pillar_name, "")

            # Generate event predictions
            event_predictions = self._generate_event_predictions(
                pattern=pattern,
                category=category,
                severity=severity,
                is_positive=category in ["stem_combination", "three_meetings", "three_combinations", "six_harmonies"],
            )

            # Create enhanced match
            match = EnhancedPatternMatch(
                pattern_id=int_id,
                category=category,
                chinese_name=chinese_name,
                english_name=english_name,
                participants=participants,
                distance=distance,
                is_transformed=is_transformed,
                severity=severity,
                affected_domains=affected_domains,
                pillar_meaning=pillar_meaning,
                event_predictions=event_predictions,
            )

            enhanced_patterns.append(match)

            # Aggregate by domain
            for domain in affected_domains:
                domain_risks[domain].append({
                    "pattern_id": int_id,
                    "severity": severity.normalized_score,
                    "level": severity.severity_level.value,
                })

        # Get special stars for Day Master and Year Branch
        special_stars = self._detect_special_stars(daymaster_stem, interactions, year_branch)

        # Calculate compound severity by domain
        domain_analysis = {}
        for domain, risks in domain_risks.items():
            if risks:
                severities = [SeverityResult(
                    raw_score=r["severity"] * 0.3,
                    normalized_score=r["severity"],
                    severity_level=r["level"],
                    contributing_factors={},
                    explanation=""
                ) for r in risks]

                # Use actual SeverityResult objects
                compound = calculate_compound_severity(
                    [SeverityResult(
                        raw_score=r["severity"] * 0.3,
                        normalized_score=r["severity"],
                        severity_level=self._str_to_severity(r["level"]),
                        contributing_factors={},
                        explanation=""
                    ) for r in risks],
                    self._str_to_domain(domain)
                )

                domain_analysis[domain] = {
                    "pattern_count": len(risks),
                    "compound_severity": compound.normalized_score,
                    "severity_level": compound.severity_level.value,
                    "top_patterns": sorted(risks, key=lambda x: x["severity"], reverse=True)[:3],
                }

        # Generate health-specific analysis
        health_enhanced = None
        if "health" in domain_analysis and affected_elements:
            health_severities = [
                SeverityResult(
                    raw_score=r["severity"] * 0.3,
                    normalized_score=r["severity"],
                    severity_level=self._str_to_severity(r["level"]),
                    contributing_factors={},
                    explanation=""
                )
                for r in domain_risks["health"]
            ]

            if health_severities:
                health_enhanced = calculate_health_severity(
                    pattern_results=health_severities,
                    affected_elements=affected_elements,
                    seasonal_states=seasonal_states,
                    daymaster_element=daymaster_element,
                )

        return {
            "enhanced_patterns": [self._match_to_dict(m) for m in enhanced_patterns],
            "pattern_count": len(enhanced_patterns),
            "domain_analysis": domain_analysis,
            "affected_elements": list(affected_elements),
            "special_stars": special_stars,
            "health_enhanced": health_enhanced,
            "recommendations": self._generate_recommendations(domain_analysis, daymaster_element, seasonal_states),
        }

    def _detect_special_stars(
        self,
        daymaster_stem: str,
        interactions: Dict[str, Any],
        year_branch: str = "",
    ) -> List[Dict[str, Any]]:
        """
        Detect special stars applicable to Day Master and Year Branch.

        Args:
            daymaster_stem: Day Master heavenly stem
            interactions: Raw interactions dict
            year_branch: Year Earthly Branch for context-dependent stars
        """
        stars = []

        # Get Day Master-dependent patterns (Kong Wang, Gui Ren, Yang Ren, Lu Shen)
        applicable_patterns = get_special_stars_for_day_master(daymaster_stem)

        # Get Year Branch-dependent patterns (Gu Chen, Gua Su, Hua Gai, Tao Hua, Yi Ma)
        if year_branch:
            year_patterns = get_special_stars_for_year_branch(year_branch)
            applicable_patterns.extend(year_patterns)

        # Get all branches present in the chart (from interactions)
        present_branches = set()
        for int_id in interactions.keys():
            if isinstance(int_id, str) and "~" in int_id:
                _, participants, _ = parse_interaction_id(int_id)
                for p in participants:
                    if len(p) <= 4:  # Branch names are short
                        present_branches.add(p)

        # Also add Year Branch itself as present
        if year_branch:
            present_branches.add(year_branch)

        # Check each pattern for triggers
        for pattern in applicable_patterns:
            # Check if the star's target branch is present in the chart
            for nf in pattern.node_filters:
                if nf.branches:
                    for target_branch in nf.branches:
                        if target_branch in present_branches:
                            # Find which nodes have this branch
                            triggers = self._find_branch_triggers(target_branch, interactions)

                            stars.append({
                                "pattern_id": pattern.id,
                                "chinese_name": pattern.chinese_name,
                                "english_name": pattern.english_name,
                                "category": pattern.category.value,
                                "target_branch": target_branch,
                                "description": pattern.description,
                                "pillar_meanings": {
                                    "year": pattern.pillar_meanings.year if pattern.pillar_meanings else "",
                                    "month": pattern.pillar_meanings.month if pattern.pillar_meanings else "",
                                    "day": pattern.pillar_meanings.day if pattern.pillar_meanings else "",
                                    "hour": pattern.pillar_meanings.hour if pattern.pillar_meanings else "",
                                } if pattern.pillar_meanings else {},
                                "triggers": triggers,
                            })

        return stars

    def _find_branch_triggers(
        self,
        target_branch: str,
        interactions: Dict[str, Any],
    ) -> List[Dict[str, str]]:
        """
        Find which nodes (pillars) contain a specific branch.

        Returns list of {node_id, pillar_type} for each trigger.
        """
        triggers = []

        # Map of branch to common node patterns
        # We need to check which interactions involve this branch
        for int_id in interactions.keys():
            if isinstance(int_id, str) and "~" in int_id:
                _, participants, nodes_str = parse_interaction_id(int_id)

                # Check if target_branch is in participants
                if target_branch in participants:
                    # Parse nodes to find which pillar has this branch
                    if nodes_str:
                        node_ids = nodes_str.split("-")
                        for i, branch in enumerate(participants):
                            if branch == target_branch and i < len(node_ids):
                                node_id = node_ids[i]
                                pillar_type = get_pillar_name_from_position(
                                    self._node_id_to_position(node_id)
                                )
                                trigger = {"node_id": node_id, "pillar_type": pillar_type}
                                if trigger not in triggers:
                                    triggers.append(trigger)

        return triggers

    def _node_id_to_position(self, node_id: str) -> int:
        """Convert node ID to position code."""
        NODE_TO_POSITION = {
            "hs_h": 0, "eb_h": 0,
            "hs_d": 1, "eb_d": 1,
            "hs_m": 2, "eb_m": 2,
            "hs_y": 3, "eb_y": 3,
            "hs_10yl": 4, "eb_10yl": 4,
            "hs_yl": 5, "eb_yl": 5,
            "hs_ml": 6, "eb_ml": 6,
            "hs_dl": 7, "eb_dl": 7,
            "hs_hl": 8, "eb_hl": 8,
        }
        return NODE_TO_POSITION.get(node_id, 1)

    def _generate_event_predictions(
        self,
        pattern: Any,
        category: str,
        severity: SeverityResult,
        is_positive: bool,
    ) -> List[Dict[str, Any]]:
        """Generate life event predictions from pattern."""
        predictions = []

        if not pattern or not pattern.event_mapping:
            # Generate generic predictions based on category
            if is_positive:
                predictions.append({
                    "domain": "career",
                    "event_type": "opportunity",
                    "sentiment": "positive",
                    "probability": min(0.8, severity.normalized_score / 100),
                })
            else:
                predictions.append({
                    "domain": "health",
                    "event_type": "attention_needed",
                    "sentiment": "negative",
                    "probability": min(0.7, severity.normalized_score / 100),
                })
            return predictions

        # Use pattern's event mapping
        mapping = pattern.event_mapping

        # Add positive event predictions
        for domain, event_type in mapping.positive_events:
            predictions.append({
                "domain": domain,
                "event_type": event_type,
                "sentiment": "positive",
                "probability": min(0.9, 0.5 + severity.normalized_score / 200),
            })

        # Add negative event predictions
        for domain, event_type in mapping.negative_events:
            predictions.append({
                "domain": domain,
                "event_type": event_type,
                "sentiment": "negative",
                "probability": min(0.8, 0.4 + severity.normalized_score / 200),
            })

        return predictions[:5]  # Limit to top 5

    def _generate_recommendations(
        self,
        domain_analysis: Dict[str, Dict],
        daymaster_element: str,
        seasonal_states: Dict[str, str],
    ) -> List[Dict[str, str]]:
        """Generate recommendations based on analysis."""
        recommendations = []

        # Health recommendations
        if "health" in domain_analysis:
            health = domain_analysis["health"]
            if health.get("compound_severity", 0) > 50:
                # Find most vulnerable element
                vulnerable = None
                max_vuln = 0
                for elem, state in seasonal_states.items():
                    vuln = SEASONAL_STATE_MULTIPLIERS.get(state, 1.0)
                    if vuln > max_vuln:
                        max_vuln = vuln
                        vulnerable = elem

                if vulnerable and vulnerable in TCM_ORGANS:
                    organ = TCM_ORGANS[vulnerable]
                    recommendations.append({
                        "domain": "health",
                        "priority": "high" if health["compound_severity"] > 70 else "medium",
                        "title": f"Support {organ.zang_organ} Function",
                        "description": f"Your {organ.zang_organ} ({organ.chinese_zang}) may need attention. "
                                      f"Associated body parts: {', '.join(organ.body_parts)}. "
                                      f"Manage {organ.emotion} for better balance.",
                    })

        # Wealth recommendations
        if "wealth" in domain_analysis:
            wealth = domain_analysis["wealth"]
            if wealth.get("compound_severity", 0) > 40:
                recommendations.append({
                    "domain": "wealth",
                    "priority": "medium",
                    "title": "Financial Caution Advised",
                    "description": "Multiple patterns indicate financial fluctuations. "
                                  "Consider conservative investments and avoid major financial commitments.",
                })

        # Career recommendations
        if "career" in domain_analysis:
            career = domain_analysis["career"]
            if career.get("compound_severity", 0) > 50:
                recommendations.append({
                    "domain": "career",
                    "priority": "medium",
                    "title": "Career Dynamics Active",
                    "description": "Significant career energy detected. "
                                  "Be prepared for changes and opportunities in your professional life.",
                })

        # Relationship recommendations
        if "relationship" in domain_analysis:
            rel = domain_analysis["relationship"]
            if rel.get("compound_severity", 0) > 40:
                recommendations.append({
                    "domain": "relationship",
                    "priority": "medium",
                    "title": "Relationship Attention Needed",
                    "description": "Relationship patterns are active. "
                                  "Focus on communication and understanding in close relationships.",
                })

        return recommendations

    def _match_to_dict(self, match: EnhancedPatternMatch) -> Dict[str, Any]:
        """Convert EnhancedPatternMatch to dictionary."""
        return {
            "pattern_id": match.pattern_id,
            "category": match.category,
            "chinese_name": match.chinese_name,
            "english_name": match.english_name,
            "participants": match.participants,
            "distance": match.distance,
            "is_transformed": match.is_transformed,
            "severity": {
                "raw_score": match.severity.raw_score,
                "normalized_score": match.severity.normalized_score,
                "level": match.severity.severity_level.value,
                "explanation": match.severity.explanation,
            },
            "affected_domains": match.affected_domains,
            "pillar_meaning": match.pillar_meaning,
            "event_predictions": match.event_predictions,
        }

    def _str_to_severity(self, level_str: str):
        """Convert severity level string to enum."""
        from .life_events.taxonomy import Severity
        mapping = {
            "minor": Severity.MINOR,
            "moderate": Severity.MODERATE,
            "major": Severity.MAJOR,
            "critical": Severity.CRITICAL,
        }
        return mapping.get(level_str, Severity.MINOR)

    def _str_to_domain(self, domain_str: str):
        """Convert domain string to enum."""
        mapping = {
            "health": LifeDomain.HEALTH,
            "wealth": LifeDomain.WEALTH,
            "career": LifeDomain.CAREER,
            "relationship": LifeDomain.RELATIONSHIP,
            "education": LifeDomain.EDUCATION,
            "family": LifeDomain.FAMILY,
            "legal": LifeDomain.LEGAL,
            "travel": LifeDomain.TRAVEL,
        }
        return mapping.get(domain_str, LifeDomain.HEALTH)


# =============================================================================
# GLOBAL ANALYZER INSTANCE
# =============================================================================

_global_analyzer: Optional[PatternEngineAnalyzer] = None


def get_pattern_analyzer() -> PatternEngineAnalyzer:
    """Get global pattern analyzer instance."""
    global _global_analyzer
    if _global_analyzer is None:
        _global_analyzer = PatternEngineAnalyzer()
    return _global_analyzer


def analyze_with_pattern_engine(
    interactions: Dict[str, Any],
    seasonal_states: Dict[str, str],
    daymaster_stem: str,
    daymaster_element: str,
    post_element_score: Dict[str, float],
    year_branch: str = "",
) -> Dict[str, Any]:
    """
    Convenience function to analyze with Pattern Engine.

    Use this function in routes.py to integrate Pattern Engine analysis.

    Args:
        year_branch: Year Earthly Branch (e.g., "Yin") for Year Branch-dependent
                    special stars like Gu Chen (孤辰) and Gua Su (寡宿).
    """
    analyzer = get_pattern_analyzer()
    return analyzer.analyze_interactions(
        interactions=interactions,
        seasonal_states=seasonal_states,
        daymaster_stem=daymaster_stem,
        daymaster_element=daymaster_element,
        post_element_score=post_element_score,
        year_branch=year_branch,
    )


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "EnhancedPatternMatch",
    "PatternEngineAnalyzer",
    "get_pattern_analyzer",
    "analyze_with_pattern_engine",
]
