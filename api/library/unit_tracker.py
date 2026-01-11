# * =========================
# * UNIT STORY TRACKER (單位故事追蹤器)
# * =========================
# Tracks every qi unit as a "video game character" throughout BaZi calculation.
# Records all interactions chronologically and maps to Ten God relationships.

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from .core import STEMS


@dataclass
class UnitEvent:
    """A single interaction event for a qi unit."""
    phase: str              # "pillar_unity_day", "combinations", etc.
    phase_step: int         # Order within phase (0, 1, 2...)
    event_type: str         # "controlled", "controlling", "produced", "producing"
    partner_stem: str       # The other stem involved (e.g., "Gui")
    partner_node: str       # Node location (e.g., "eb_d")
    partner_ten_god: str    # Ten God of partner relative to DM (e.g., "七殺")
    partner_ten_god_english: str  # English name (e.g., "Seven Killings")
    qi_before: float        # Qi before this event
    qi_change: float        # Change amount (negative for loss, positive for gain)
    qi_after: float         # Qi after this event
    description: str        # Human-readable: "Controlled by Gui (七殺) -10"
    # Distance penalty fields
    distance: int = 1               # Effective distance (base + hidden penalty)
    distance_multiplier: float = 1.0  # Applied multiplier (1.0, 0.618, 0.5, etc.)
    math_formula: str = ""          # UI display: "min(100,60)×0.5×0.618 = 18.5 → -11.4, -18.5"
    # Extended fields for combinations/conflicts/seasonal
    combination_type: str = ""      # "THREE_MEETINGS", "SIX_HARMONIES", etc.
    conflict_type: str = ""         # "CLASH", "HARM", "PUNISHMENT"
    pattern: str = ""               # "Hai-Zi-Chou", "Zi-Wu"
    seasonal_state: str = ""        # "Prosperous", "Strengthening", "Resting", "Trapped", "Dead"
    boost_amount: float = 0.0       # Combination qi boost
    is_transformed: bool = False    # If combination fully transformed
    severity: str = ""              # For punishments: "severe", "moderate", "light"
    element: str = ""               # Transformed element for combinations
    # Same element relationship fields (rooting/support)
    same_element_type: str = ""     # "rooting" | "support"
    strength: str = ""              # "strong" (Primary Qi) | "normal" (Hidden Stem)
    hidden_position: int = -1       # 0=Primary Qi (本氣), 1+=Hidden Stems (藏干)
    # Detailed calculation breakdown for combinations
    calculation_details: Optional[dict] = None  # Step-by-step formula breakdown

    def to_dict(self) -> dict:
        result = {
            "phase": self.phase,
            "phase_step": self.phase_step,
            "event_type": self.event_type,
            "partner_stem": self.partner_stem,
            "partner_node": self.partner_node,
            "partner_ten_god": self.partner_ten_god,
            "partner_ten_god_english": self.partner_ten_god_english,
            "qi_before": round(self.qi_before, 2),
            "qi_change": round(self.qi_change, 2),
            "qi_after": round(self.qi_after, 2),
            "description": self.description,
            "distance": self.distance,
            "distance_multiplier": self.distance_multiplier,
            "math_formula": self.math_formula,
        }
        # Add optional fields only if they have values
        if self.combination_type:
            result["combination_type"] = self.combination_type
        if self.conflict_type:
            result["conflict_type"] = self.conflict_type
        if self.pattern:
            result["pattern"] = self.pattern
        if self.seasonal_state:
            result["seasonal_state"] = self.seasonal_state
        if self.boost_amount:
            result["boost_amount"] = round(self.boost_amount, 2)
        if self.is_transformed:
            result["is_transformed"] = self.is_transformed
        if self.severity:
            result["severity"] = self.severity
        if self.element:
            result["element"] = self.element
        if self.same_element_type:
            result["same_element_type"] = self.same_element_type
        if self.strength:
            result["strength"] = self.strength
        if self.hidden_position >= 0:
            result["hidden_position"] = self.hidden_position
        if self.calculation_details:
            result["calculation_details"] = self.calculation_details
        return result


@dataclass
class UnitStory:
    """The complete journey of one qi unit (stem) in a specific node."""
    stem: str               # "Ding", "Ji", "Gui"
    stem_chinese: str       # "丁", "己", "癸"
    element: str            # "Fire", "Earth", "Water"
    polarity: str           # "Yin", "Yang"
    ten_god: str            # Ten God relative to Day Master: "比肩", "食神", etc.
    ten_god_id: str         # Short ID: "F", "EG", "7K", etc.
    ten_god_english: str    # "Friend", "Eating God", etc.
    home_node: str          # Primary location: "hs_d", "eb_y", etc.
    initial_qi: float       # Starting qi (naive assignment)
    final_qi: float = 0.0   # After all interactions
    hidden_position: int = -1  # -1=HS, 0=EB Primary Qi (本氣), 1+=Hidden Stem (藏干)
    events: List[UnitEvent] = field(default_factory=list)

    @property
    def total_gained(self) -> float:
        """Total qi gained from all positive events."""
        return sum(e.qi_change for e in self.events if e.qi_change > 0)

    @property
    def total_lost(self) -> float:
        """Total qi lost from all negative events (returned as positive)."""
        return abs(sum(e.qi_change for e in self.events if e.qi_change < 0))

    def get_narrative(self) -> str:
        """Generate human-readable story of this unit's journey."""
        if not self.events:
            return f"{self.stem_chinese} ({self.ten_god}) started at {self.initial_qi:.1f} qi. No interactions. Final: {self.final_qi:.1f} qi."

        parts = [f"{self.stem_chinese} ({self.ten_god}) started at {self.initial_qi:.1f} qi."]

        for event in self.events:
            if event.event_type == "controlling":
                parts.append(f"Controlled {event.partner_stem} ({event.partner_ten_god}), cost {abs(event.qi_change):.1f} qi.")
            elif event.event_type == "controlled":
                parts.append(f"Was controlled by {event.partner_stem} ({event.partner_ten_god}), lost {abs(event.qi_change):.1f} qi.")
            elif event.event_type == "producing":
                parts.append(f"Produced {event.partner_stem} ({event.partner_ten_god}), cost {abs(event.qi_change):.1f} qi.")
            elif event.event_type == "produced":
                parts.append(f"Was produced by {event.partner_stem} ({event.partner_ten_god}), gained {event.qi_change:.1f} qi.")

        parts.append(f"Final: {self.final_qi:.1f} qi.")
        return " ".join(parts)

    def to_dict(self) -> dict:
        result = {
            "stem": self.stem,
            "stem_chinese": self.stem_chinese,
            "element": self.element,
            "polarity": self.polarity,
            "ten_god": self.ten_god,
            "ten_god_id": self.ten_god_id,
            "ten_god_english": self.ten_god_english,
            "home_node": self.home_node,
            "initial_qi": round(self.initial_qi, 2),
            "final_qi": round(self.final_qi, 2),
            "total_gained": round(self.total_gained, 2),
            "total_lost": round(self.total_lost, 2),
            "events": [e.to_dict() for e in self.events],
            "narrative": self.get_narrative(),
        }
        # Include hidden_position for EB nodes (-1 for HS, 0 for Primary Qi, 1+ for Hidden Stems)
        if self.hidden_position >= 0:
            result["hidden_position"] = self.hidden_position
        return result


class UnitTracker:
    """
    Main tracker for all qi units throughout BaZi calculation.
    Tracks phases chronologically and records all interactions.
    """

    # Ten God English translations
    TEN_GOD_ENGLISH = {
        "比肩": "Friend",
        "劫財": "Rob Wealth",
        "食神": "Eating God",
        "傷官": "Hurting Officer",
        "偏財": "Indirect Wealth",
        "正財": "Direct Wealth",
        "七殺": "Seven Killings",
        "正官": "Direct Officer",
        "偏印": "Indirect Resource",
        "正印": "Direct Resource",
        "日主": "Day Master",
    }

    # Phase labels for display
    PHASE_LABELS = {
        "naive_assignment": "Initial Qi Assignment",
        "pillar_unity_d": "Day Pillar Unity",
        "pillar_unity_y": "Year Pillar Unity",
        "pillar_unity_m": "Month Pillar Unity",
        "pillar_unity_h": "Hour Pillar Unity",
        "seasonal": "Seasonal Adjustments (旺相休囚死)",
        "three_meetings": "Three Meetings (三會)",
        "three_combinations": "Three Combinations (三合)",
        "half_meetings": "Half Meetings (半會)",
        "six_harmonies": "Six Harmonies (六合)",
        "conflicts": "Conflicts (沖害刑)",
        "arched_combinations": "Arched Combinations (拱合)",
        "hs_combinations": "Heavenly Stem Combinations (天干五合)",
        "hs_conflicts": "Heavenly Stem Conflicts (天干相剋)",
        "cross_pillar": "Cross-Pillar Wuxing",
    }

    def __init__(self, day_master: str):
        """
        Initialize tracker with Day Master stem.

        Args:
            day_master: The Day Master stem (e.g., "Ding")
        """
        self.day_master = day_master
        self.day_master_chinese = STEMS[day_master]["chinese"]
        # {node_id: {stem: UnitStory}}
        self.units: Dict[str, Dict[str, UnitStory]] = {}
        # Timeline of phases with their events
        self.timeline: List[dict] = []
        # Current phase info
        self.current_phase: Optional[str] = None
        self.current_phase_label: Optional[str] = None
        self.current_phase_events: List[dict] = []
        self.phase_step: int = 0

    def get_ten_god(self, stem: str) -> Tuple[str, str, str]:
        """
        Get Ten God relationship between Day Master and a stem.

        Returns:
            Tuple of (id, english, chinese)
        """
        if stem == self.day_master:
            return ("DM", "Day Master", "日主")

        ten_gods = STEMS[self.day_master].get("ten_gods", {})
        if stem in ten_gods:
            return ten_gods[stem]

        # Fallback - should not happen if data is correct
        return ("?", "Unknown", "未知")

    def register_unit(
        self,
        node_id: str,
        stem: str,
        element: str,
        polarity: str,
        initial_qi: float,
        hidden_position: int = -1
    ):
        """
        Register a qi unit (stem) in a specific node.

        Args:
            node_id: Node identifier (e.g., "hs_d", "eb_y")
            stem: Stem name (e.g., "Ding", "Ji")
            element: Element name (e.g., "Fire", "Earth")
            polarity: "Yin" or "Yang"
            initial_qi: Starting qi value
            hidden_position: Position in EB qi list (-1=HS, 0=Primary Qi 本氣, 1+=Hidden Stem 藏干)
        """
        if node_id not in self.units:
            self.units[node_id] = {}

        ten_god_info = self.get_ten_god(stem)
        ten_god_id, ten_god_english, ten_god_chinese = ten_god_info

        self.units[node_id][stem] = UnitStory(
            stem=stem,
            stem_chinese=STEMS[stem]["chinese"],
            element=element,
            polarity=polarity,
            ten_god=ten_god_chinese,
            ten_god_id=ten_god_id,
            ten_god_english=ten_god_english,
            home_node=node_id,
            initial_qi=initial_qi,
            final_qi=initial_qi,  # Start with initial value
            hidden_position=hidden_position,
        )

        # Add to current phase events if in a phase
        if self.current_phase:
            self.current_phase_events.append({
                "type": "registration",
                "node": node_id,
                "stem": stem,
                "stem_chinese": STEMS[stem]["chinese"],
                "ten_god": ten_god_chinese,
                "ten_god_english": ten_god_english,
                "qi": initial_qi,
                "description": f"{stem} ({ten_god_chinese}) assigned {initial_qi} qi",
            })

    def start_phase(self, phase_name: str, phase_label: Optional[str] = None):
        """
        Start a new calculation phase.

        Args:
            phase_name: Internal phase identifier
            phase_label: Human-readable label (optional, will use default)
        """
        self.current_phase = phase_name
        self.current_phase_label = phase_label or self.PHASE_LABELS.get(phase_name, phase_name)
        self.current_phase_events = []
        self.phase_step = 0

    def record_interaction(
        self,
        source_node: str,
        source_stem: str,
        target_node: str,
        target_stem: str,
        interaction_type: str,  # "control", "generation"
        source_qi_before: float,
        source_qi_after: float,
        target_qi_before: float,
        target_qi_after: float,
        distance: int = 1,
        distance_multiplier: float = 1.0,
        math_formula: str = "",
    ):
        """
        Record an interaction between two qi units.

        Args:
            source_node: Node of the source/actor
            source_stem: Stem of the source
            target_node: Node of the target
            target_stem: Stem of the target
            interaction_type: "control" or "generation"
            source_qi_before: Source qi before interaction
            source_qi_after: Source qi after interaction
            target_qi_before: Target qi before interaction
            target_qi_after: Target qi after interaction
            distance: Effective distance (base + hidden penalty)
            distance_multiplier: Applied multiplier (1.0, 0.618, etc.)
            math_formula: UI display formula string
        """
        source_change = source_qi_after - source_qi_before
        target_change = target_qi_after - target_qi_before

        # Get Ten God info for both stems
        source_ten_god = self.get_ten_god(source_stem)
        target_ten_god = self.get_ten_god(target_stem)

        # Determine event types based on interaction
        if interaction_type == "control":
            source_event_type = "controlling"
            target_event_type = "controlled"
            source_desc = f"Controlled {target_stem} ({target_ten_god[2]}), cost {abs(source_change):.1f}"
            target_desc = f"Controlled by {source_stem} ({source_ten_god[2]}), lost {abs(target_change):.1f}"
        else:  # generation
            source_event_type = "producing"
            target_event_type = "produced"
            source_desc = f"Produced {target_stem} ({target_ten_god[2]}), cost {abs(source_change):.1f}"
            target_desc = f"Produced by {source_stem} ({source_ten_god[2]}), gained {target_change:.1f}"

        # Record event for source unit
        if source_node in self.units and source_stem in self.units[source_node]:
            source_unit = self.units[source_node][source_stem]
            source_unit.events.append(UnitEvent(
                phase=self.current_phase,
                phase_step=self.phase_step,
                event_type=source_event_type,
                partner_stem=target_stem,
                partner_node=target_node,
                partner_ten_god=target_ten_god[2],
                partner_ten_god_english=target_ten_god[1],
                qi_before=source_qi_before,
                qi_change=source_change,
                qi_after=source_qi_after,
                description=source_desc,
                distance=distance,
                distance_multiplier=distance_multiplier,
                math_formula=math_formula,
            ))
            source_unit.final_qi = source_qi_after

        # Record event for target unit
        if target_node in self.units and target_stem in self.units[target_node]:
            target_unit = self.units[target_node][target_stem]
            target_unit.events.append(UnitEvent(
                phase=self.current_phase,
                phase_step=self.phase_step,
                event_type=target_event_type,
                partner_stem=source_stem,
                partner_node=source_node,
                partner_ten_god=source_ten_god[2],
                partner_ten_god_english=source_ten_god[1],
                qi_before=target_qi_before,
                qi_change=target_change,
                qi_after=target_qi_after,
                description=target_desc,
                distance=distance,
                distance_multiplier=distance_multiplier,
                math_formula=math_formula,
            ))
            target_unit.final_qi = target_qi_after

        # Add to phase events for timeline
        self.current_phase_events.append({
            "type": "interaction",
            "step": self.phase_step,
            "interaction_type": interaction_type,
            "distance": distance,
            "distance_multiplier": distance_multiplier,
            "math_formula": math_formula,
            "source": {
                "node": source_node,
                "stem": source_stem,
                "stem_chinese": STEMS[source_stem]["chinese"],
                "ten_god": source_ten_god[2],
                "ten_god_english": source_ten_god[1],
                "qi_before": round(source_qi_before, 2),
                "qi_change": round(source_change, 2),
                "qi_after": round(source_qi_after, 2),
            },
            "target": {
                "node": target_node,
                "stem": target_stem,
                "stem_chinese": STEMS[target_stem]["chinese"],
                "ten_god": target_ten_god[2],
                "ten_god_english": target_ten_god[1],
                "qi_before": round(target_qi_before, 2),
                "qi_change": round(target_change, 2),
                "qi_after": round(target_qi_after, 2),
            },
            "description": f"{source_stem} ({source_ten_god[2]}) {'controls' if interaction_type == 'control' else 'produces'} {target_stem} ({target_ten_god[2]})",
        })

        self.phase_step += 1

    def update_unit_qi(self, node_id: str, stem: str, new_qi: float, reason: str = ""):
        """
        Update a unit's qi directly (for adjustments without partner interaction).

        Args:
            node_id: Node identifier
            stem: Stem name
            new_qi: New qi value
            reason: Optional reason for the adjustment
        """
        if node_id in self.units and stem in self.units[node_id]:
            unit = self.units[node_id][stem]
            qi_before = unit.final_qi
            qi_change = new_qi - qi_before
            unit.final_qi = new_qi

            if self.current_phase and abs(qi_change) > 0.01:
                self.current_phase_events.append({
                    "type": "adjustment",
                    "step": self.phase_step,
                    "node": node_id,
                    "stem": stem,
                    "stem_chinese": STEMS[stem]["chinese"],
                    "ten_god": unit.ten_god,
                    "qi_before": round(qi_before, 2),
                    "qi_change": round(qi_change, 2),
                    "qi_after": round(new_qi, 2),
                    "reason": reason,
                    "description": f"{stem} ({unit.ten_god}) adjusted by {qi_change:+.1f}: {reason}" if reason else f"{stem} adjusted by {qi_change:+.1f}",
                })
                self.phase_step += 1

    def record_seasonal_adjustment(
        self,
        node_id: str,
        stem: str,
        element: str,
        qi_before: float,
        qi_after: float,
        seasonal_state: str,
        multiplier: float,
        month_branch: str,
        hidden_position: int = -1  # -1=unknown, 0=Primary Qi (本氣), 1+=Hidden Stem (藏干)
    ):
        """
        Record a seasonal multiplier adjustment for a stem.

        Args:
            node_id: Node identifier
            stem: Stem name
            element: Element of the stem
            qi_before: Qi before adjustment
            qi_after: Qi after adjustment
            seasonal_state: "Prosperous", "Strengthening", "Resting", "Trapped", "Dead"
            multiplier: Applied multiplier (0.618-1.382, Fibonacci-based)
            month_branch: The month branch determining season
            hidden_position: Position in qi list. 0=Primary Qi (本氣), 1+=Hidden Stem (藏干)
        """
        qi_change = qi_after - qi_before
        ten_god_info = self.get_ten_god(stem)

        # Update unit's final_qi and add event to unit story
        if node_id in self.units and stem in self.units[node_id]:
            unit = self.units[node_id][stem]
            unit.final_qi = qi_after
            # Add seasonal event to unit's events for Unit Narratives
            unit.events.append(UnitEvent(
                phase=self.current_phase or "seasonal",
                phase_step=self.phase_step,
                event_type="seasonal",
                partner_stem="",  # No partner for seasonal
                partner_node="",
                partner_ten_god="",
                partner_ten_god_english="",
                qi_before=qi_before,
                qi_change=qi_change,
                qi_after=qi_after,
                description=f"Seasonal {seasonal_state} ×{multiplier:.3f}",
                seasonal_state=seasonal_state,
            ))

        # Parse node_id to get readable location
        # e.g., "hs_y" -> "Year HS", "eb_d" -> "Day EB hidden"
        node_type = "HS" if node_id.startswith("hs_") else "EB"
        pillar_map = {"y": "Year", "m": "Month", "d": "Day", "h": "Hour"}
        pillar_suffix = node_id.split("_")[1] if "_" in node_id else ""
        pillar_name = pillar_map.get(pillar_suffix, pillar_suffix.upper())

        # Get polarity from stem info
        polarity = STEMS[stem]["polarity"]  # "Yang" or "Yin"
        polarity_sign = "+" if polarity == "Yang" else "-"

        # Build location description
        # For EB nodes, distinguish Primary Qi (index 0) from Hidden Stems (index 1+)
        if node_type == "HS":
            location = f"{pillar_name} HS"
        else:
            # Use hidden_position to determine if Primary Qi or Hidden Stem
            # 0 = Primary Qi (本氣, NOT hidden), 1+ = Hidden Stem (藏干, actually hidden)
            if hidden_position == 0:
                location = f"{pillar_name} EB"  # Primary Qi - not hidden
            elif hidden_position > 0:
                location = f"{pillar_name} EB hidden stem"  # Hidden Stem (藏干)
            else:
                # hidden_position not provided (-1), default to "EB" (assume Primary Qi)
                location = f"{pillar_name} EB"

        # Build descriptive text: "丙 Bing (Fire Yang) in Year EB hidden"
        stem_chinese = STEMS[stem]["chinese"]
        stem_desc = f"{stem_chinese} {stem} ({element} {polarity})"

        # Add to phase events
        self.current_phase_events.append({
            "type": "seasonal",
            "step": self.phase_step,
            "node": node_id,
            "stem": stem,
            "stem_chinese": STEMS[stem]["chinese"],
            "element": element,
            "polarity": polarity,
            "ten_god": ten_god_info[2],
            "ten_god_english": ten_god_info[1],
            "qi_before": round(qi_before, 2),
            "qi_change": round(qi_change, 2),
            "qi_after": round(qi_after, 2),
            "seasonal_state": seasonal_state,
            "multiplier": multiplier,
            "month_branch": month_branch,
            "location": location,
            "pillar": pillar_name,
            "node_type": node_type,
            "description": f"{stem_desc} in {location}: {seasonal_state} ×{multiplier:.3f} ({qi_before:.1f} → {qi_after:.1f})",
        })
        self.phase_step += 1

    def record_combination(
        self,
        nodes: List[str],
        stems: List[str],
        combination_type: str,
        pattern: str,
        element: str,
        boost_amount: float,
        is_transformed: bool,
        math_formula: str = "",
        calculation_details: Optional[dict] = None
    ):
        """
        Record a combination detection and qi boost.

        Args:
            nodes: List of node IDs involved (e.g., ["eb_y", "eb_m", "eb_d"])
            stems: List of stems affected (primary hidden stems of participating nodes)
            combination_type: "THREE_MEETINGS", "SIX_HARMONIES", etc.
            pattern: Pattern string (e.g., "Hai-Zi-Chou")
            element: Transformed element (e.g., "Water")
            boost_amount: Total qi boost from combination (dynamically calculated)
            is_transformed: Whether combination fully transformed
            math_formula: Display formula for timeline (e.g., "avg(72.5, 85.2) x 0.382 x 1.618 = 48.7")
            calculation_details: Detailed step-by-step breakdown dict
        """
        # Each participating unit gets the FULL boost amount to match transform_to_element behavior
        # (transform_to_element is called for EACH node with the same amount)
        boost_per_unit = boost_amount

        combo_label = combination_type.replace('_', ' ')
        status = "Transformed" if is_transformed else "Combined"

        for i, (node_id, stem) in enumerate(zip(nodes, stems)):
            if stem is None:
                # Skip if stem couldn't be determined (shouldn't happen)
                continue

            # If the transformed stem doesn't exist yet for this node, create it
            if node_id not in self.units:
                self.units[node_id] = {}

            if stem not in self.units[node_id]:
                # Register new unit for the transformed stem
                stem_data = STEMS.get(stem, {})
                stem_element = stem_data.get("element", element)
                stem_polarity = stem_data.get("polarity", "Yang")

                ten_god_info = self.get_ten_god(stem)
                ten_god_id, ten_god_english, ten_god_chinese = ten_god_info

                self.units[node_id][stem] = UnitStory(
                    stem=stem,
                    stem_chinese=stem_data.get("chinese", "?"),
                    element=stem_element,
                    polarity=stem_polarity,
                    ten_god=ten_god_chinese,  # Chinese name
                    ten_god_id=ten_god_id,
                    ten_god_english=ten_god_english,
                    home_node=node_id,
                    initial_qi=0.0,  # Transformation creates new qi from 0
                    final_qi=0.0,
                    hidden_position=-2,  # -2 = transformation-created unit
                    events=[]
                )

            unit = self.units[node_id][stem]
            qi_before = unit.final_qi
            qi_after = qi_before + boost_per_unit
            unit.final_qi = qi_after

            # Add combination event to unit's events for Unit Narratives
            unit.events.append(UnitEvent(
                phase=self.current_phase or "combinations",
                phase_step=self.phase_step,
                event_type="combination",
                partner_stem=pattern,  # Use pattern as partner info
                partner_node=", ".join(n for n in nodes if n != node_id),
                partner_ten_god="",
                partner_ten_god_english="",
                qi_before=qi_before,
                qi_change=boost_per_unit,
                qi_after=qi_after,
                description=f"{combo_label}: {pattern} → {element} ({status})",
                combination_type=combination_type,
                pattern=pattern,
                element=element,
                boost_amount=boost_per_unit,
                is_transformed=is_transformed,
                calculation_details=calculation_details,
            ))

        event_data = {
            "type": "combination",
            "step": self.phase_step,
            "combination_type": combination_type,
            "pattern": pattern,
            "element": element,
            "nodes": nodes,
            "stems": stems,
            "boost_amount": round(boost_amount, 2),
            "is_transformed": is_transformed,
            "math_formula": math_formula,
            "description": f"{combo_label}: {pattern} → {element}" + (" (Transformed)" if is_transformed else " (Combined)"),
        }
        if calculation_details:
            event_data["calculation_details"] = calculation_details
        self.current_phase_events.append(event_data)
        self.phase_step += 1

    def record_conflict(
        self,
        aggressor_node: str,
        aggressor_stem: str,
        victim_node: str,
        victim_stem: str,
        conflict_type: str,
        pattern: str,
        aggressor_damage: float,
        victim_damage: float,
        severity: str = "",
        math_formula: str = ""
    ):
        """
        Record conflict damage (clash/harm/punishment).

        Args:
            aggressor_node: Node of the aggressor/controller
            aggressor_stem: Stem of the aggressor
            victim_node: Node of the victim
            victim_stem: Stem of the victim
            conflict_type: "CLASH", "HARM", "PUNISHMENT"
            pattern: Pattern string (e.g., "Zi-Wu")
            aggressor_damage: Damage taken by aggressor (dynamically calculated)
            victim_damage: Damage taken by victim (dynamically calculated)
            severity: For punishments: "severe", "moderate", "light", "self"
            math_formula: Display formula for timeline
        """
        aggressor_ten_god = self.get_ten_god(aggressor_stem)
        victim_ten_god = self.get_ten_god(victim_stem)

        severity_label = f" ({severity})" if severity else ""
        conflict_desc = f"{conflict_type}: {pattern}{severity_label}"

        # Update units' final_qi and add events to their stories
        if aggressor_node in self.units and aggressor_stem in self.units[aggressor_node]:
            unit = self.units[aggressor_node][aggressor_stem]
            qi_before = unit.final_qi
            qi_after = max(1.0, qi_before - aggressor_damage)
            unit.final_qi = qi_after

            # Add conflict event to aggressor's unit events
            unit.events.append(UnitEvent(
                phase=self.current_phase or "conflicts",
                phase_step=self.phase_step,
                event_type="conflict_aggressor",
                partner_stem=victim_stem,
                partner_node=victim_node,
                partner_ten_god=victim_ten_god[2],
                partner_ten_god_english=victim_ten_god[1],
                qi_before=qi_before,
                qi_change=-aggressor_damage,
                qi_after=qi_after,
                description=f"{conflict_desc}, lost {aggressor_damage:.1f}",
                conflict_type=conflict_type,
                pattern=pattern,
                severity=severity,
            ))

        if victim_node in self.units and victim_stem in self.units[victim_node]:
            unit = self.units[victim_node][victim_stem]
            qi_before = unit.final_qi
            qi_after = max(1.0, qi_before - victim_damage)
            unit.final_qi = qi_after

            # Add conflict event to victim's unit events
            unit.events.append(UnitEvent(
                phase=self.current_phase or "conflicts",
                phase_step=self.phase_step,
                event_type="conflict_victim",
                partner_stem=aggressor_stem,
                partner_node=aggressor_node,
                partner_ten_god=aggressor_ten_god[2],
                partner_ten_god_english=aggressor_ten_god[1],
                qi_before=qi_before,
                qi_change=-victim_damage,
                qi_after=qi_after,
                description=f"{conflict_desc}, lost {victim_damage:.1f}",
                conflict_type=conflict_type,
                pattern=pattern,
                severity=severity,
            ))

        self.current_phase_events.append({
            "type": "conflict",
            "step": self.phase_step,
            "conflict_type": conflict_type,
            "pattern": pattern,
            "severity": severity,
            "math_formula": math_formula,
            "aggressor": {
                "node": aggressor_node,
                "stem": aggressor_stem,
                "stem_chinese": STEMS[aggressor_stem]["chinese"],
                "ten_god": aggressor_ten_god[2],
                "ten_god_english": aggressor_ten_god[1],
                "damage": round(aggressor_damage, 2),
            },
            "victim": {
                "node": victim_node,
                "stem": victim_stem,
                "stem_chinese": STEMS[victim_stem]["chinese"],
                "ten_god": victim_ten_god[2],
                "ten_god_english": victim_ten_god[1],
                "damage": round(victim_damage, 2),
            },
            "description": f"{conflict_type}: {pattern}" + (f" ({severity})" if severity else "") + f" → -{victim_damage:.1f}",
        })
        self.phase_step += 1

    def record_same_element(
        self,
        hs_node: str,
        hs_stem: str,
        eb_node: str,
        eb_stem: str,
        relationship: str,  # "rooting" or "support"
        strength: str,      # "strong" or "normal"
        hidden_position: int = 0
    ):
        """
        Record same-element relationship (rooting/support) - no qi change.

        BaZi Concepts:
        - Rooting (通根): HS element finds same element in EB qi values
          - Strong (強根): Matches Primary Qi (本氣, hidden_position=0)
          - Normal (弱根): Matches Hidden Stem (藏干, hidden_position>0)
        - Support (透出): EB qi element is "expressed" by matching HS
          - Strong: EB qi is Primary Qi (main energy)
          - Normal: EB qi is Hidden Stem (secondary/tertiary)

        BaZi Terminology:
        - Primary Qi (本氣): Index 0 - main energy, NOT hidden
        - Hidden Stems (藏干): Index 1+ - secondary/tertiary, actually hidden

        Args:
            hs_node: HS node ID (e.g., "hs_d")
            hs_stem: HS stem name (e.g., "Ding")
            eb_node: EB node ID (e.g., "eb_d")
            eb_stem: EB qi stem name (e.g., "Ding")
            relationship: "rooting" (HS←EB) or "support" (EB→HS)
            strength: "strong" (Primary Qi) or "normal" (Hidden Stem)
            hidden_position: 0=Primary Qi, 1+=Hidden Stem
        """
        hs_ten_god = self.get_ten_god(hs_stem)
        eb_ten_god = self.get_ten_god(eb_stem)
        hs_element = STEMS[hs_stem]["element"]

        # Build description based on relationship type
        position_label = ["primary", "secondary", "tertiary"][min(hidden_position, 2)]
        if relationship == "rooting":
            if strength == "strong":
                desc = f"{hs_stem} ({hs_ten_god[2]}) has strong rooting in {eb_stem} ({position_label} qi)"
            else:
                desc = f"{hs_stem} ({hs_ten_god[2]}) has rooting in {eb_stem} ({position_label} qi)"
        else:  # support
            if strength == "strong":
                desc = f"{eb_stem} ({eb_ten_god[2]}) has strong support from {hs_stem} ({hs_ten_god[2]})"
            else:
                desc = f"{eb_stem} ({eb_ten_god[2]}) has support from {hs_stem} ({hs_ten_god[2]})"

        self.current_phase_events.append({
            "type": "same_element",
            "step": self.phase_step,
            "same_element_type": relationship,
            "strength": strength,
            "hidden_position": hidden_position,
            "element": hs_element,
            "hs": {
                "node": hs_node,
                "stem": hs_stem,
                "stem_chinese": STEMS[hs_stem]["chinese"],
                "ten_god": hs_ten_god[2],
                "ten_god_english": hs_ten_god[1],
            },
            "eb": {
                "node": eb_node,
                "stem": eb_stem,
                "stem_chinese": STEMS[eb_stem]["chinese"],
                "ten_god": eb_ten_god[2],
                "ten_god_english": eb_ten_god[1],
            },
            "description": desc,
        })
        self.phase_step += 1

    def end_phase(self):
        """End the current phase and add it to the timeline."""
        if self.current_phase:
            # Calculate running totals at end of phase
            running_total = sum(
                unit.final_qi
                for node_units in self.units.values()
                for unit in node_units.values()
            )

            # Calculate element totals (Wood, Fire, Earth, Metal, Water)
            element_totals = {"Wood": 0, "Fire": 0, "Earth": 0, "Metal": 0, "Water": 0}
            for node_units in self.units.values():
                for unit in node_units.values():
                    if unit.element in element_totals:
                        element_totals[unit.element] += unit.final_qi

            # Round element totals
            element_totals = {k: round(v, 1) for k, v in element_totals.items()}

            # Count events - include all types (interaction, seasonal, combination, conflict)
            event_count = len(self.current_phase_events)

            self.timeline.append({
                "phase": self.current_phase,
                "phase_label": self.current_phase_label,
                "events": self.current_phase_events,
                "event_count": event_count,
                "running_total": round(running_total, 2),
                "element_totals": element_totals,  # NEW: Element breakdown at end of phase
            })

            self.current_phase = None
            self.current_phase_label = None
            self.current_phase_events = []
            self.phase_step = 0

    def get_unit_stories(self) -> Dict[str, List[dict]]:
        """Get all unit stories organized by node."""
        return {
            node_id: [unit.to_dict() for unit in units.values()]
            for node_id, units in self.units.items()
        }

    def get_all_narratives(self) -> Dict[str, Dict[str, str]]:
        """Get narrative for every unit, organized by node."""
        return {
            node_id: {stem: unit.get_narrative() for stem, unit in units.items()}
            for node_id, units in self.units.items()
        }

    def get_five_element_totals(self, node_ids: Optional[set] = None) -> Dict[str, float]:
        """
        Calculate combined Yin+Yang totals for 5 elements from unit_tracker.

        Args:
            node_ids: Optional set of node IDs to filter. If None, includes all nodes.

        Returns:
            Dict with Wood, Fire, Earth, Metal, Water totals
        """
        element_totals = {"Wood": 0.0, "Fire": 0.0, "Earth": 0.0, "Metal": 0.0, "Water": 0.0}

        for node_id, node_units in self.units.items():
            # Filter by node_ids if specified
            if node_ids is not None and node_id not in node_ids:
                continue

            for unit in node_units.values():
                if unit.element in element_totals:
                    element_totals[unit.element] += unit.final_qi

        # Round to 1 decimal
        return {k: round(v, 1) for k, v in element_totals.items()}

    def get_ten_element_totals(self, node_ids: Optional[set] = None) -> Dict[str, int]:
        """
        Calculate totals for all 10 Heavenly Stems from unit_tracker.

        Args:
            node_ids: Optional set of node IDs to filter. If None, includes all nodes.

        Returns:
            Dict with stem totals: {"Jia": X, "Yi": Y, ...}
        """
        # All 10 Heavenly Stems
        ten_elements = {
            "Jia": 0, "Yi": 0, "Bing": 0, "Ding": 0, "Wu": 0,
            "Ji": 0, "Geng": 0, "Xin": 0, "Ren": 0, "Gui": 0
        }

        for node_id, node_units in self.units.items():
            # Filter by node_ids if specified
            if node_ids is not None and node_id not in node_ids:
                continue

            for stem, unit in node_units.items():
                if stem in ten_elements:
                    ten_elements[stem] += unit.final_qi

        # Round to integers (not truncate)
        return {k: round(v) for k, v in ten_elements.items()}

    def get_element_totals_at_phase(self, phase_name: str) -> Optional[Dict[str, float]]:
        """
        Get element totals (5 elements) at the end of a specific phase from timeline.

        Args:
            phase_name: The phase ID (e.g., "stem_branch_unity", "seasonal")

        Returns:
            Dict with element totals, or None if phase not found
        """
        for phase_data in self.timeline:
            if phase_data.get("phase") == phase_name:
                return phase_data.get("element_totals")
        return None

    def get_ten_element_totals_at_phase(self, phase_name: str, node_ids: Optional[set] = None) -> Optional[Dict[str, int]]:
        """
        Calculate 10 Heavenly Stem totals at the end of a specific phase.
        Uses the qi values that were current at that phase.

        Args:
            phase_name: The phase ID (e.g., "stem_branch_unity", "seasonal")
            node_ids: Optional set of node IDs to filter. If None, includes all nodes.

        Returns:
            Dict with stem totals: {"Jia": X, "Yi": Y, ...}, or None if phase not found
        """
        # Find the phase index
        phase_index = None
        for i, phase_data in enumerate(self.timeline):
            if phase_data.get("phase") == phase_name:
                phase_index = i
                break

        if phase_index is None:
            return None

        # Calculate qi at end of that phase by replaying events
        # Start from initial_qi and apply events up to (and including) that phase
        ten_elements = {
            "Jia": 0, "Yi": 0, "Bing": 0, "Ding": 0, "Wu": 0,
            "Ji": 0, "Geng": 0, "Xin": 0, "Ren": 0, "Gui": 0
        }

        # Get list of phases up to and including target phase
        phases_to_include = set()
        for i in range(phase_index + 1):
            phases_to_include.add(self.timeline[i].get("phase"))

        for node_id, node_units in self.units.items():
            # Filter by node_ids if specified
            if node_ids is not None and node_id not in node_ids:
                continue

            for stem, unit in node_units.items():
                if stem not in ten_elements:
                    continue

                # Start from initial qi
                qi = unit.initial_qi

                # Apply events from phases up to target phase
                for event in unit.events:
                    if event.phase in phases_to_include:
                        qi += event.qi_change

                ten_elements[stem] += qi

        return {k: round(v) for k, v in ten_elements.items()}

    def to_dict(self) -> dict:
        """Convert tracker to dictionary for API response."""
        return {
            "day_master": self.day_master,
            "day_master_chinese": self.day_master_chinese,
            "timeline": self.timeline,
            "unit_stories": self.get_unit_stories(),
            "summary": {
                "total_units": sum(len(units) for units in self.units.values()),
                "total_phases": len(self.timeline),
                "total_interactions": sum(
                    phase.get("event_count", 0) for phase in self.timeline
                ),
                "final_total_qi": round(sum(
                    unit.final_qi
                    for node_units in self.units.values()
                    for unit in node_units.values()
                ), 2),
            },
        }
