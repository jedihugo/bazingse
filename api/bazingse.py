#!/usr/bin/env python3
"""
BaZingSe - Complete BaZi (四柱八字) Astrology Calculator API
Single-file implementation for simplified development and deployment.

This file contains all modules consolidated into organized sections:
- Libraries & Constants
- BaZi Definitions  
- Chart Constructors
- Pattern Analyzers
- API Endpoints
- Main Application

Run with: python bazingse.py
API will be available at: http://localhost:8008
"""

# * =================
# * IMPORTS
# * =================
import math
import sxtwl
import os
import json
import uvicorn
from datetime import datetime, date
from typing import Literal, Dict, List, Set, Optional, Any
from itertools import permutations

from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel

from library import *

# Create mapping dictionaries for Chinese characters
STEM_CHINESE_MAP = {v["id"]: v["chinese"] for v in HEAVENLY_STEMS.values()}
BRANCH_CHINESE_MAP = {v["id"]: v["chinese"] for v in EARTHLY_BRANCHES.values()}

# * =================
# * HELPER FUNCTIONS
# * =================

def strength_to_badge_size(strength: str) -> str:
    """Map interaction strength to badge size for frontend"""
    size_map = {
        "ultra_strong": "xl",
        "strong": "lg",
        "normal": "md",
        "weak": "sm"
    }
    return size_map.get(strength, "md")

def reduction_to_badge_size(reduction_percent: float) -> str:
    """Map reduction percentage to badge size for negative interactions"""
    if reduction_percent >= 15:
        return "md"
    elif reduction_percent >= 10:
        return "sm"
    else:
        return "xs"

def get_primary_qi_polarity(branch_id: str) -> str:
    """
    Get the polarity of the primary qi (highest score qi) in an Earthly Branch.
    
    CORE BAZI PRINCIPLE:
    When a branch transforms or produces elements, the polarity is determined by 
    its PRIMARY QI (the dominant hidden stem), not the branch's own Yin/Yang nature.
    
    Examples:
    - Si (Yin branch): Primary qi = Bing (Yang Fire) → Returns "Yang"
    - Wu (Yang branch): Primary qi = Ding (Yin Fire) → Returns "Yin"  
    - Shen (Yang branch): Primary qi = Geng (Yang Metal) → Returns "Yang"
    
    This ensures correct element production:
    - Xu (Wu Earth) next to Shen (Geng Metal) → Produces Geng (Yang), not Xin (Yin)
    
    Args:
        branch_id: Branch ID like "Si", "Wu", "Mao", etc.
    
    Returns:
        "Yang" or "Yin" based on the primary qi's polarity
    """
    if branch_id not in EARTHLY_BRANCHES:
        return "Yang"  # Default if branch not found
    
    qi_list = EARTHLY_BRANCHES[branch_id].get("qi", [])
    if not qi_list:
        return "Yang"  # Default if no qi data
    
    # Primary qi is the first one (index 0) with highest score
    primary_qi_stem = qi_list[0]["stem"]
    
    if primary_qi_stem not in HEAVENLY_STEMS:
        return "Yang"  # Default if stem not found
    
    return HEAVENLY_STEMS[primary_qi_stem]["polarity"]

# ========================
# Pydantic Models for Node Structure
# ========================

class InteractionData(BaseModel):
    """Interaction data stored by ID"""
    type: str
    pattern: str
    nodes: List[str]
    effect: Optional[str] = None
    positions: Optional[List[int]] = None
    description: Optional[str] = None

class BadgeData(BaseModel):
    """
    Badge data for frontend display
    
    Badge Types and Their Meanings:
    
    POSITIVE INTERACTIONS (Additive):
    - transformation: Successful EB combination with HS support (e.g., Yin-Hai + Wood HS → gains Wood qi)
    - combination: Partial EB combination without full HS support (e.g., Yin-Hai without Wood HS)
    
    NEGATIVE INTERACTIONS (Reductive):
    - punishment: Xing 刑 - ungrateful/power/rudeness punishment between branches
    - harm: Hai 害 - mutual harm between branches
    - clash: Chong 沖 - direct opposition between branches (strongest negative)
    - destruction: Po 破 - destructive relationship between branches
    
    Badge Stem Logic:
    - For positive (transformation/combination): Shows the NEW element added to this node
      Uses node's OWN polarity to determine stem (Si/Yin → Ding, Wu/Yang → Bing)
    - For negative (punishment/harm/clash/destruction): Shows the ATTACKING element
      Uses the OTHER node's primary qi stem (shows what's damaging this node)
    
    Badge Size:
    - Positive: Based on interaction strength (xl=ultra_strong, lg=strong, md=normal, sm=weak)
    - Negative: Based on reduction severity (md=15%+, sm=10-14%, xs=<10%)
    """
    interaction_id: str  # Full interaction ID (e.g., "SIX_HARMONIES~Yin-Hai~eb_y-eb_m")
    type: str  # transformation, combination, punishment, harm, clash, destruction
    badge: str  # Stem ID showing transformed/attacking element (e.g., Bing, Ren, Ji, Geng)
    size: str  # xl, lg, md, sm, xs

class NodeResponse(BaseModel):
    """Complete node response structure"""
    # Current node ID (post-interaction)
    id: str
    
    # Base qi before interactions
    base_qi: Dict[str, float]
    
    # Post-interaction qi
    post_interaction_qi: Dict[str, float]
    
    # Interactions this node participated in (just IDs)
    interaction_ids: List[str] = []
    
    # Badges for frontend display
    badges: List[BadgeData] = []




# * =================
# * MAIN ANALYSIS FUNCTIONS
# * =================

# Note: The FastAPI app initialization is in run_bazingse.py to avoid circular imports
def analyze_8_node_interactions(
    bazi_chart: Dict, 
    month_branch: str = None,
    talisman_year_hs: str = None,
    talisman_year_eb: str = None,
    talisman_month_hs: str = None,
    talisman_month_eb: str = None,
    talisman_day_hs: str = None,
    talisman_day_eb: str = None,
    talisman_hour_hs: str = None,
    talisman_hour_eb: str = None,
    location: str = None
) -> Dict:
    """
    BaZi interaction calculator V7 - Extensible architecture with talisman support.
    
    Core Concept:
    - 8-26 nodes: 8 natal + up to 10 luck + up to 8 talisman nodes
    - Each node has its own element inventory
    - Interactions ONLY affect the specific nodes involved
    - Talismans: User-added nodes for creating harmony/balance
    
    Node Types:
    - Natal (8): hs_y, hs_m, hs_d, hs_h, eb_y, eb_m, eb_d, eb_h
    - Luck (10): hs_10yl, eb_10yl, hs_yl, eb_yl, hs_ml, eb_ml, hs_dl, eb_dl, hs_hl, eb_hl
    - Talisman (8): hs_ty, eb_ty, hs_tm, eb_tm, hs_td, eb_td, hs_th, eb_th
    
    Example: Yin-Hai combination only affects eb_y and eb_d nodes
    """
    from copy import deepcopy
    
    class ElementNode:
        """
        A single node representing either a Heavenly Stem or Earthly Branch.
        Each node maintains its own element inventory.
        """
        def __init__(self, node_id, value, node_type):
            self.node_id = node_id  # e.g., "hs_y", "eb_m"
            self.value = value  # e.g., "Bing", "Yin"
            self.node_type = node_type  # "stem" or "branch"
            self.elements = {}  # {element_key: {"score": x}}
            
            # Transformation state (legacy - for backward compat)
            self.transformation_element = None
            self.transformation_pattern = None
            
            # Badge tracking (unified for EB and HS interactions)
            self.badges = []  # List of badge dicts with interaction_id, badge, size
            
            # Interaction tracking
            self.interactions = []
            self.marked = False  # Used in interaction
            
            # Initialize elements based on type
            self._initialize_elements()
        
        def _initialize_elements(self):
            """Initialize element scores and counts based on node type"""
            if self.node_type == "stem" and self.value in HEAVENLY_STEMS:
                # Heavenly Stem - base score from HS definition
                elem = HEAVENLY_STEMS[self.value]["element"]
                pol = HEAVENLY_STEMS[self.value]["polarity"]
                self.elements[f"{pol} {elem}"] = {
                    "score": HEAVENLY_STEMS[self.value]["qi_score"]
                }
                
            elif self.node_type == "branch" and self.value in EARTHLY_BRANCHES:
                # Earthly Branch - Hidden Qi with hardcoded scores and counts
                for qi_info in EARTHLY_BRANCHES[self.value]["qi"]:
                    hs_hidden = qi_info["stem"]
                    if hs_hidden in HEAVENLY_STEMS:
                        elem = HEAVENLY_STEMS[hs_hidden]["element"]
                        pol = HEAVENLY_STEMS[hs_hidden]["polarity"]
                        key = f"{pol} {elem}"
                        
                        if key not in self.elements:
                            self.elements[key] = {
                                "score": 0
                            }
                        
                        self.elements[key]["score"] += qi_info["score"]
        
        def get_total_score(self):
            """Total element score in this node"""
            return int(sum(e["score"] for e in self.elements.values()))
        
        def get_dominant_element(self):
            """Get the dominant base element (Wood/Fire/Earth/Metal/Water) in this node"""
            # Aggregate scores by base element
            base_elements = {}
            for elem_key, elem_data in self.elements.items():
                base_elem = elem_key.replace("Yang ", "").replace("Yin ", "")
                if base_elem not in base_elements:
                    base_elements[base_elem] = 0
                base_elements[base_elem] += elem_data["score"]
            
            # Find the dominant element
            if base_elements:
                dominant = max(base_elements.items(), key=lambda x: x[1])
                if dominant[1] > 0:
                    return dominant[0]
            return None
        
        def add_element(self, element, amount, polarity=None):
            """Add specific amount to an element
            
            Args:
                element: Base element name (Wood, Fire, Earth, Metal, Water)
                amount: Amount to add
                polarity: Optional polarity ("Yang" or "Yin")
                         - If specified: Add to only that polarity
                         - If None: Split 50/50 between Yang and Yin (backward compatible)
                         - For BRANCH nodes: Should use primary qi's polarity
            """
            if polarity:
                # Add to specific polarity only (e.g., Geng Metal, not Xin Metal)
                key = f"{polarity} {element}"
                if key not in self.elements:
                    self.elements[key] = {"score": 0}
                self.elements[key]["score"] += amount
            else:
                # Split between both polarities (backward compatible default)
                for pol in ["Yang", "Yin"]:
                    key = f"{pol} {element}"
                    if key not in self.elements:
                        self.elements[key] = {"score": 0}
                    self.elements[key]["score"] += amount / 2
        
        def boost_element_by_percentage(self, element, percentage):
            """Boost element by percentage of node's total"""
            boost_amount = self.get_total_score() * percentage
            self.add_element(element, boost_amount)
        
        def reduce_all_by_percentage(self, percentage):
            """Reduce all elements by percentage"""
            for key in self.elements:
                self.elements[key]["score"] *= (1 - percentage)
                self.elements[key]["score"] = max(0, self.elements[key]["score"])
        
        def reduce_by_amount_with_minimum(self, damage_amount, minimum_qi=1.0):
            """
            Reduce qi by absolute amount while enforcing minimum total qi threshold.
            Returns the actual damage applied (which may be less than requested).
            
            Args:
                damage_amount (float): Intended damage amount
                minimum_qi (float): Minimum total qi threshold (default: 1.0)
            
            Returns:
                float: Actual damage applied (capped if node can't take full damage)
            
            Example:
                Node has 20 qi total, damage_amount=35, minimum_qi=1
                → Can only take 19 damage (leaving 1 qi)
                → Returns 19 (actual damage applied)
            
            Use case: STEM_CONFLICTS where controller damage is proportional to victim's actual damage
            """
            current_qi = self.get_total_score()
            max_damage = max(0, current_qi - minimum_qi)
            actual_damage = min(damage_amount, max_damage)
            
            if actual_damage <= 0:
                return 0
            
            # Apply proportional reduction to all elements
            reduction_ratio = actual_damage / current_qi
            for key in self.elements:
                self.elements[key]["score"] *= (1 - reduction_ratio)
                self.elements[key]["score"] = max(0, self.elements[key]["score"])
            
            return actual_damage
        
        def transform_to_element(self, element, amount, is_transformed=True, transformation_type=None, pattern=None, interaction_id=None):
            """Additive transformation - adds transformed element and tracks transformation
            
            Args:
                element: Target element (Fire, Water, etc.)
                amount: Amount to add (from library scoring dictionaries)
                is_transformed: Whether transformation is successful (True) or partial/detected (False)
                transformation_type: Type of interaction (THREE_MEETINGS, SIX_HARMONIES, etc.)
                pattern: Pattern name (Si-Wu-Wei, Si-Shen, etc.)
                interaction_id: Full interaction ID for reference
            
            In WuXing theory (this school), transformations are additive/dilutive.
            Original elements are preserved, and the transformed element is added
            based on the node's Yin/Yang polarity:
            - For HS: Uses the stem's own polarity
            - For EB: Uses the BRANCH's own polarity (not the primary qi's polarity)
            
            Example: Si (Yin branch) → Fire transformation uses Ding (Yin Fire)
                     Wu (Yang branch) → Fire transformation uses Bing (Yang Fire)
            """
            # Use the amount from library scoring
            transformation_score = amount
            
            # Determine node's polarity
            node_polarity = None
            if self.node_type == "stem" and self.value in HEAVENLY_STEMS:
                node_polarity = HEAVENLY_STEMS[self.value]["polarity"]
            elif self.node_type == "branch" and self.value in EARTHLY_BRANCHES:
                # Use the branch's own polarity for transformations
                node_polarity = EARTHLY_BRANCHES[self.value]["polarity"]
            
            if not node_polarity:
                return
            
            # Get the appropriate stem based on node's polarity using ELEMENT_POLARITY_STEMS
            stem_to_add = ELEMENT_POLARITY_STEMS.get((element, node_polarity))
            
            if stem_to_add and stem_to_add in HEAVENLY_STEMS:
                stem_element = HEAVENLY_STEMS[stem_to_add]["element"]
                stem_polarity = HEAVENLY_STEMS[stem_to_add]["polarity"]
                element_key = f"{stem_polarity} {stem_element}"
                
                # Initialize if not present
                if element_key not in self.elements:
                    self.elements[element_key] = {"score": 0}
                
                # Add transformation score (additive, preserves existing)
                self.elements[element_key]["score"] += transformation_score
                
                # Track this as a badge
                # Badge type: "transformation" if fully transformed, "combination" if partial/detected
                badge_type = "transformation" if is_transformed else "combination"
                
                from library import TRANSFORMATION_STRENGTH
                strength = TRANSFORMATION_STRENGTH.get(transformation_type, "normal") if transformation_type else "normal"
                badge_size = strength_to_badge_size(strength)
                
                badge_data = {
                    "interaction_id": interaction_id or "",
                    "type": badge_type,
                    "badge": stem_to_add,
                    "size": badge_size
                }
                self.badges.append(badge_data)
                
                # Update legacy transformation fields (for backward compatibility)
                # Use the first/primary transformation if not already set
                if not self.transformation_element and is_transformed:
                    self.transformation_element = element
                    self.transformation_pattern = pattern
        
        def apply_hidden_qi_damage(self, other_node, damage_factor=None):
            """
            Apply hidden Qi interactions between branch nodes.
            Only Primary (index 0) and Secondary (index 1) Qi interact.
            """
            if self.node_type != "branch" or other_node.node_type != "branch":
                return
            
            if self.value not in EARTHLY_BRANCHES or other_node.value not in EARTHLY_BRANCHES:
                return
            
            qi_self = EARTHLY_BRANCHES[self.value]["qi"]
            qi_other = EARTHLY_BRANCHES[other_node.value]["qi"]
            
            # Use damage factor from constants if not provided
            if damage_factor is None:
                damage_factor = HIDDEN_QI_INTERACTIONS["damage"]["damage_factor"]
            
            # Destructive cycle
            destructive = {
                ("Water", "Fire"): damage_factor,
                ("Fire", "Metal"): damage_factor,
                ("Metal", "Wood"): damage_factor,
                ("Wood", "Earth"): damage_factor,
                ("Earth", "Water"): damage_factor,
            }
            
            # Check Primary and Secondary Qi only
            for qi_index in [0, 1]:
                if qi_index < len(qi_self) and qi_index < len(qi_other):
                    hs_self = qi_self[qi_index]["stem"]
                    strength_self = qi_self[qi_index]["score"] / 100.0
                    hs_other = qi_other[qi_index]["stem"]
                    strength_other = qi_other[qi_index]["score"] / 100.0
                    
                    if hs_self in HEAVENLY_STEMS and hs_other in HEAVENLY_STEMS:
                        elem_self = HEAVENLY_STEMS[hs_self]["element"]
                        elem_other = HEAVENLY_STEMS[hs_other]["element"]
                        
                        # Apply damage
                        damage = destructive.get((elem_self, elem_other), 0)
                        if damage > 0:
                            # Damage other node's element
                            for pol in ["Yang", "Yin"]:
                                key = f"{pol} {elem_other}"
                                if key in other_node.elements:
                                    reduction = damage * strength_other
                                    other_node.elements[key]["score"] *= (1 - reduction)
                                    # Fixed count reduction for hidden qi damage
                        
                        # Check reverse damage
                        damage_rev = destructive.get((elem_other, elem_self), 0)
                        if damage_rev > 0:
                            for pol in ["Yang", "Yin"]:
                                key = f"{pol} {elem_self}"
                                if key in self.elements:
                                    reduction = damage_rev * strength_self
                                    self.elements[key]["score"] *= (1 - reduction)
                                    # Fixed count reduction for hidden qi damage
    
    # ============= CREATE NODES =============
    nodes = {}
    
    # Define pillar mappings (extensible for luck pillars and talismans)
    pillar_mappings = [
        ("year_pillar", "y"),
        ("month_pillar", "m"),
        ("day_pillar", "d"),
        ("hour_pillar", "h"),
        ("luck_10_year", "10yl"),  # 10-year luck pillar (Da Yun)
        ("yearly_luck", "yl"),    # Yearly luck
        ("monthly_luck", "ml"),   # Monthly luck
        ("daily_luck", "dl"),     # Daily luck
        ("hourly_luck", "hl")     # Hourly luck
    ]
    
    # Track which positions we actually have
    active_positions = []
    
    for pillar_key, position_code in pillar_mappings:
        if pillar_key in bazi_chart and isinstance(bazi_chart[pillar_key], str):
            if " " in bazi_chart[pillar_key]:
                hs, eb = bazi_chart[pillar_key].split(" ")
                
                # Create Heavenly Stem node
                hs_id = f"hs_{position_code}"
                nodes[hs_id] = ElementNode(hs_id, hs, "stem")
                
                # Create Earthly Branch node
                eb_id = f"eb_{position_code}"
                nodes[eb_id] = ElementNode(eb_id, eb, "branch")
                
                active_positions.append(position_code)
    
    # Create talisman nodes (optional user-provided nodes for harmony/balance)
    talisman_mappings = [
        (talisman_year_hs, talisman_year_eb, "ty"),
        (talisman_month_hs, talisman_month_eb, "tm"),
        (talisman_day_hs, talisman_day_eb, "td"),
        (talisman_hour_hs, talisman_hour_eb, "th")
    ]
    
    for hs_value, eb_value, position_code in talisman_mappings:
        # Create HS talisman node if provided
        if hs_value and hs_value in HEAVENLY_STEMS:
            hs_id = f"hs_{position_code}"
            nodes[hs_id] = ElementNode(hs_id, hs_value, "stem")
            if position_code not in active_positions:
                active_positions.append(position_code)
        
        # Create EB talisman node if provided
        if eb_value and eb_value in EARTHLY_BRANCHES:
            eb_id = f"eb_{position_code}"
            nodes[eb_id] = ElementNode(eb_id, eb_value, "branch")
            if position_code not in active_positions:
                active_positions.append(position_code)
    
    # Extract heavenly stems for transformation checks (including talismans)
    heavenly_stems = [nodes[f"hs_{pos}"].value for pos in active_positions if f"hs_{pos}" in nodes]
    heavenly_stems_elements = [HEAVENLY_STEMS[stem]["element"] for stem in heavenly_stems if stem in HEAVENLY_STEMS]
    
    # Build dynamic position codes including luck pillars if present
    # Standard natal chart positions with their numeric indices
    base_position_map = {"y": 0, "m": 1, "d": 2, "h": 3}
    
    # Position codes for interaction processing - include luck pillars if present
    position_codes = ["y", "m", "d", "h"]  # Core natal chart positions
    position_to_index = base_position_map.copy()
    
    # Add 10-year luck if present (treated as position 4, adjacent to hour)
    if "10yl" in active_positions:
        position_codes.append("10yl")
        position_to_index["10yl"] = 4  # Position 4, adjacent to hour (position 3)
    
    # Add yearly luck pillar if present (treated as position 5, adjacent to 10-year luck)
    if "yl" in active_positions:
        position_codes.append("yl")
        position_to_index["yl"] = 5  # Position 5, adjacent to 10-year luck (position 4)
    
    # Add monthly luck pillar if present (position 6)
    if "ml" in active_positions:
        position_codes.append("ml")
        position_to_index["ml"] = 6
    
    # Add daily luck pillar if present (position 7)
    if "dl" in active_positions:
        position_codes.append("dl")
        position_to_index["dl"] = 7
    
    # Add hourly luck pillar if present (position 8)
    if "hl" in active_positions:
        position_codes.append("hl")
        position_to_index["hl"] = 8
    
    # Add talisman positions (positions 9-12) - treated like luck pillars (temporal/external overlays)
    if "ty" in active_positions:
        position_codes.append("ty")
        position_to_index["ty"] = 9  # Talisman year
    
    if "tm" in active_positions:
        position_codes.append("tm")
        position_to_index["tm"] = 10  # Talisman month
    
    if "td" in active_positions:
        position_codes.append("td")
        position_to_index["td"] = 11  # Talisman day
    
    if "th" in active_positions:
        position_codes.append("th")
        position_to_index["th"] = 12  # Talisman hour
    
    # Helper functions
    def get_transformation_badge(branch_id: str, target_element: str) -> str:
        """
        Get correct transformation badge stem based on BRANCH polarity.
        
        CORE BAZI PRINCIPLE:
        When a branch transforms to an element through combinations (THREE_MEETINGS,
        THREE_COMBINATIONS, SIX_HARMONIES, etc.), the badge stem must match
        the BRANCH's own polarity, not the primary qi's polarity.
        
        Examples:
        - Si (Yin branch): Transforms to Fire → Ding (Yin Fire)
        - Wu (Yang branch): Transforms to Fire → Bing (Yang Fire)
        - Wei (Yin branch): Transforms to Fire → Ding (Yin Fire)
        
        Args:
            branch_id: Branch ID like "Si", "Wu", "Mao", etc.
            target_element: Target element like "Fire", "Wood", etc.
        
        Returns:
            Stem ID matching both element and branch polarity (e.g., "Bing", "Ding")
        """
        # Use the branch's own polarity for transformations
        if branch_id not in EARTHLY_BRANCHES:
            return target_element
        
        branch_polarity = EARTHLY_BRANCHES[branch_id]["polarity"]
        
        # Use ELEMENT_POLARITY_STEMS mapping
        return ELEMENT_POLARITY_STEMS.get((target_element, branch_polarity), target_element)
    
    def get_branch_nodes():
        """Get all branch nodes with their positions"""
        branch_nodes = []
        for pos in position_codes:
            eb_id = f"eb_{pos}"
            if eb_id in nodes:
                idx = position_to_index.get(pos, 0)
                branch_nodes.append((idx, eb_id, nodes[eb_id]))
        return branch_nodes
    
    def calculate_interaction_distance(pos1, pos2):
        """
        Calculate distance between positions with special handling for luck pillars and talismans.
        
        **CRITICAL BAZI METAPHYSICS:**
        
        1. **Luck pillars** (4-8): TEMPORAL OVERLAYS representing time periods that affect
           the ENTIRE natal chart equally. Distance = 0 to ANY natal position.
        
        2. **Talisman nodes** (9-12): EXTERNAL HARMONY TOOLS user-placed to create balance.
           Like luck pillars, they're conceptual overlays. Distance = 0 to ANY natal position.
        
        3. **Natal positions** (0-3): Spatial pillars using normal Manhattan distance.
        
        Distance Logic:
        - Luck/Talisman ↔ Natal: distance = 0 (full strength interaction)
        - Luck ↔ Luck: normal distance (both temporal)
        - Talisman ↔ Talisman: normal distance (both external)
        - Luck ↔ Talisman: normal distance (different overlay types)
        - Natal ↔ Natal: normal spatial distance
        
        Position Map:
        - 0-3 = Natal (Year, Month, Day, Hour)
        - 4-8 = Luck (10-Year, Annual, Monthly, Daily, Hourly)
        - 9-12 = Talisman (Year, Month, Day, Hour)
        
        Args:
            pos1: First position index
            pos2: Second position index
            
        Returns:
            int: Distance (0=adjacent/conceptually_adjacent, 1=one_away, 2+=far)
        """
        NATAL_POSITIONS = [0, 1, 2, 3]  # Year, Month, Day, Hour
        LUCK_POSITIONS = [4, 5, 6, 7, 8]  # 10-Year, Annual, Monthly, Daily, Hourly (temporal overlays)
        TALISMAN_POSITIONS = [9, 10, 11, 12]  # Year, Month, Day, Hour talismans (external harmony tools)
        
        # Special case: If one is luck/talisman and other is natal
        # They are conceptually adjacent (distance = 0) for full interaction strength
        if (pos1 in LUCK_POSITIONS and pos2 in NATAL_POSITIONS) or \
           (pos2 in LUCK_POSITIONS and pos1 in NATAL_POSITIONS):
            return 0  # Temporal overlay → full adjacency to all natal pillars
        
        if (pos1 in TALISMAN_POSITIONS and pos2 in NATAL_POSITIONS) or \
           (pos2 in TALISMAN_POSITIONS and pos1 in NATAL_POSITIONS):
            return 0  # External harmony tool → full adjacency to all natal pillars
        
        # All other combinations: use normal spatial distance
        return abs(pos1 - pos2)
    
    def are_adjacent(positions):
        """Check if any positions are adjacent (for interaction bonuses)"""
        if len(positions) < 2:
            return False
        # Check each pair using the new distance calculation
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                if calculate_interaction_distance(positions[i], positions[j]) <= 1:
                    return True
        return False
    
    # Track interactions
    interaction_log = []
    
    # ============= PROCESS INTERACTIONS BY PRIORITY =============
    
    # Get branch nodes for interaction processing
    branch_data = get_branch_nodes()
    
    # ========================================================================
    # CORE WUXING INTERACTION LOGIC - The Fundamental Flow:
    # 
    # 1. DETECTION: Does a combination of nodes exist?
    #    - Check if required stems/branches are present in the chart
    #    
    # 2. DISTANCE: Is position far? nearby? adjacent?
    #    - Adjacent (distance 0): Strongest interaction
    #    - Distance 1: Moderate interaction  
    #    - Distance 2+: Weak or no interaction
    #    
    # 3. TRANSFORMATION: Does it transform?
    #    - For HS combinations: Check if transforming element exists in EB
    #    - For EB combinations: Check if transforming element exists in HS
    #    - Successful transformation significantly boosts the interaction
    #
    # This three-step evaluation applies to ALL interactions and determines
    # their strength and effects on the chart.
    # ========================================================================
    
    # 1. THREE MEETINGS (三會) - Highest Priority
    for direction, config in THREE_MEETINGS.items():
        required_branches = config["branches"]
        element = config["element"]
        
        # Find matching branch nodes
        matching = [(pos, nid, node) for pos, nid, node in branch_data 
                   if node.value in required_branches]
        
        if len(matching) >= 3:
            # Check all combinations of 3 branches
            found_branches = [node.value for _, _, node in matching]
            if set(found_branches) >= set(required_branches):  # Has all required branches
                # Select exactly the branches we need
                # PRIORITY: Day > Hour > Month > Year (Day pillar is most important in BaZi!)
                pillar_priority = {2: 0, 3: 1, 1: 2, 0: 3}  # d=0, h=1, m=2, y=3 (lower = higher priority)
                
                selected = []
                for req_branch in required_branches:
                    # Find all nodes matching this branch
                    candidates = [(pos, nid, node) for pos, nid, node in matching 
                                 if node.value == req_branch and not any(s[1] == nid for s in selected)]
                    
                    if candidates:
                        # Sort by pillar priority (Day > Hour > Month > Year)
                        candidates.sort(key=lambda x: pillar_priority.get(x[0], 99))
                        # Pick the highest priority candidate
                        selected.append(candidates[0])
                
                if len(selected) == 3:
                    # Sort selected to match library definition order
                    branch_to_data = {node.value: (pos, nid, node) for pos, nid, node in selected}
                    ordered_selected = []
                    for req_branch in required_branches:
                        if req_branch in branch_to_data:
                            ordered_selected.append(branch_to_data[req_branch])
                    
                    positions = [pos for pos, _, _ in ordered_selected]
                    affected_nodes = [node for _, _, node in ordered_selected]
                    affected_ids = [nid for _, nid, _ in ordered_selected]
                    
                    # Calculate score using tuple-based scoring
                    scoring_dict = config.get("scoring", {})
                    
                    # Get distance key for 3-node interactions
                    distance_key = get_distance_key_3nodes(affected_ids[0], affected_ids[1], affected_ids[2])
                    
                    # Check transformation
                    can_transform = element in heavenly_stems_elements
                    
                    if can_transform:
                        # TRANSFORMATION - nodes become pure element
                        transformation_key = "transformed"
                        total_score = scoring_dict.get(transformation_key, {}).get(distance_key, 70)
                        
                        # Use branch combination as pattern (in library order)
                        pattern_key = "-".join(required_branches)
                        interaction_id = f"THREE_MEETINGS~{pattern_key}~{'-'.join(affected_ids)}"
                        
                        for node in affected_nodes:
                            node.transform_to_element(
                                element=element,
                                amount=total_score,
                                is_transformed=True,
                                transformation_type="THREE_MEETINGS",
                                pattern=pattern_key,
                                interaction_id=interaction_id
                            )
                            node.marked = True
                            node.interactions.append(f"Three Meetings → {element}")
                        
                        # Use branch combination as pattern (in library order)
                        pattern_key = "-".join(required_branches)
                        interaction_log.append({
                            "type": "THREE_MEETINGS",
                            "pattern": pattern_key,
                            "nodes": affected_ids,
                            "positions": positions,
                            "branches": [node.value for node in affected_nodes],
                            "transformed": True,
                            "element": element,
                            "points": f"+{total_score} points",
                            "distance": distance_key
                        })
                    else:
                        # PARTIAL - combined but not fully transformed
                        transformation_key = "combined"
                        total_score = scoring_dict.get(transformation_key, {}).get(distance_key, 25)
                        
                        pattern_key = "-".join(required_branches)
                        interaction_id = f"THREE_MEETINGS~{pattern_key}~{'-'.join(affected_ids)}"
                        
                        for node in affected_nodes:
                            node.transform_to_element(
                                element=element,
                                amount=total_score,
                                is_transformed=False,
                                transformation_type="THREE_MEETINGS",
                                pattern=pattern_key,
                                interaction_id=interaction_id
                            )
                            node.marked = True
                            node.interactions.append(f"Three Meetings +{total_score}pts {element}")
                        
                        # Use branch combination as pattern (in library order)
                        pattern_key = "-".join(required_branches)
                        interaction_log.append({
                            "type": "THREE_MEETINGS",
                            "pattern": pattern_key,
                            "nodes": affected_ids,
                            "positions": positions,
                            "branches": [node.value for node in affected_nodes],
                            "transformed": False,
                            "element": element,
                            "points": f"+{total_score} points",
                            "distance": distance_key,
                            "reason": f"No {element} in Heavenly Stems"
                        })
    
    # 3. THREE COMBINATIONS (三合) - Positive (High Priority for Transformation)
    for pattern_key, config in THREE_COMBINATIONS.items():
        required_branches = config["branches"]
        element = config["element"]
        
        # NOTE: Allow multiple THREE_COMBINATIONS (e.g., if two Yin nodes, both can form combos)
        matching = [(pos, nid, node) for pos, nid, node in branch_data 
                   if node.value in required_branches]
        
        if len(matching) >= 3:
            # Group nodes by their branch value
            import itertools
            branches_map = {}
            for pos, nid, node in matching:
                if node.value not in branches_map:
                    branches_map[node.value] = []
                branches_map[node.value].append((pos, nid, node))
            
            # Check if we have all required branches
            if set(branches_map.keys()) >= set(required_branches):
                # Get nodes for each required branch
                branch1_nodes = branches_map.get(required_branches[0], [])
                branch2_nodes = branches_map.get(required_branches[1], [])
                branch3_nodes = branches_map.get(required_branches[2], [])
                
                # Generate ALL possible triplets (Cartesian product)
                for combo in itertools.product(branch1_nodes, branch2_nodes, branch3_nodes):
                    # Check that all three nodes are distinct
                    node_ids = [nid for _, nid, _ in combo]
                    if len(set(node_ids)) != 3:
                        continue  # Skip if any nodes are the same
                    
                    selected = list(combo)
                    # Sort selected to match library definition order
                    branch_to_data = {node.value: (pos, nid, node) for pos, nid, node in selected}
                    ordered_selected = []
                    for req_branch in required_branches:
                        if req_branch in branch_to_data:
                            ordered_selected.append(branch_to_data[req_branch])
                    
                    positions = [pos for pos, _, _ in ordered_selected]
                    nodes_affected = [node for _, _, node in ordered_selected]
                    affected_ids = [nid for _, nid, _ in ordered_selected]
                    
                    # Calculate score using tuple-based scoring
                    scoring_dict = config.get("scoring", {})
                    
                    # Get distance key for 3-node interactions
                    distance_key = get_distance_key_3nodes(affected_ids[0], affected_ids[1], affected_ids[2])
                    
                    can_transform = element in heavenly_stems_elements
                    
                    if can_transform:
                        transformation_key = "transformed"
                        total_score = scoring_dict.get(transformation_key, {}).get(distance_key, 60)
                        
                        interaction_id = f"THREE_COMBINATIONS~{pattern_key}~{'-'.join(affected_ids)}"
                        
                        for node in nodes_affected:
                            node.transform_to_element(
                                element=element,
                                amount=total_score,
                                is_transformed=True,
                                transformation_type="THREE_COMBINATIONS",
                                pattern=pattern_key,
                                interaction_id=interaction_id
                            )
                            node.marked = True
                            node.interactions.append(f"Three Combinations → {element}")
                        
                        interaction_log.append({
                            "type": "THREE_COMBINATIONS",
                            "pattern": pattern_key,
                            "element": element,
                            "nodes": affected_ids,
                            "positions": positions,
                            "branches": [node.value for node in nodes_affected],
                            "transformed": True,
                            "boost": f"+{total_score:.0f} points",
                            "distance": distance_key
                        })
                    else:
                        transformation_key = "combined"
                        total_score = scoring_dict.get(transformation_key, {}).get(distance_key, 22)
                        
                        interaction_id = f"THREE_COMBINATIONS~{pattern_key}~{'-'.join(affected_ids)}"
                        
                        for node in nodes_affected:
                            node.transform_to_element(
                                element=element,
                                amount=total_score,
                                is_transformed=False,
                                transformation_type="THREE_COMBINATIONS",
                                pattern=pattern_key,
                                interaction_id=interaction_id
                            )
                            node.marked = True
                            node.interactions.append(f"Three Combinations +{total_score:.0f}pts {element}")
                        
                        interaction_log.append({
                            "type": "THREE_COMBINATIONS",
                            "pattern": pattern_key,
                            "element": element,
                            "nodes": affected_ids,
                            "positions": positions,
                            "branches": [node.value for node in nodes_affected],
                            "transformed": False,
                            "boost": f"+{total_score:.0f} points",
                            "distance": distance_key
                        })
    
    # 7. HALF MEETINGS (半會) - Positive (2/3 of THREE_MEETINGS, higher priority than SIX_HARMONIES)
    # Child of THREE_MEETINGS: blocked ONLY by THREE_MEETINGS, allowed with everything else
    for pattern_key, info in HALF_MEETINGS.items():
        required_branches = info["branches"]
        element = info["element"]
        missing = info["missing"]
        
        # Check if nodes have THREE_MEETINGS interaction (blocks HALF_MEETINGS)
        matching = [(pos, nid, node) for pos, nid, node in branch_data 
                   if node.value in required_branches 
                   and not any("THREE_MEETING" in badge.get("interaction_id", "") for badge in node.badges)]
        
        if len(matching) >= 2:
            found_branches = [node.value for _, _, node in matching[:2]]
            if set(found_branches) == set(required_branches):
                positions = [pos for pos, _, _ in matching[:2]]
                nodes_affected = [node for _, _, node in matching[:2]]
                ids_affected = [nid for _, nid, _ in matching[:2]]
                
                # Calculate score using nested dict scoring
                scoring_dict = info.get("scoring", {})
                
                # Calculate distance for logging and scoring
                from library import get_distance_key
                distance_key = get_distance_key(ids_affected[0], ids_affected[1])
                
                # Check if can transform (element exists in Heavenly Stems)
                can_transform = element in heavenly_stems_elements
                
                if can_transform:
                    transformation_key = "transformed"
                    total_score = scoring_dict.get(transformation_key, {}).get(distance_key, 50)
                    
                    interaction_id = f"HALF_MEETING~{pattern_key}~{'-'.join(ids_affected)}"
                    
                    for node in nodes_affected:
                        node.transform_to_element(
                            element=element,
                            amount=total_score,
                            is_transformed=True,
                            transformation_type="HALF_MEETING",
                            pattern=pattern_key,
                            interaction_id=interaction_id
                        )
                        node.marked = True
                        node.interactions.append(f"Half Meeting → {element}")
                    
                    interaction_log.append({
                        "type": "HALF_MEETING",
                        "pattern": pattern_key,
                        "nodes": ids_affected,
                        "positions": positions,
                        "branches": found_branches,
                        "transformed": True,
                        "element": element,
                        "missing": missing,
                        "boost": f"+{total_score:.0f} points",
                        "distance": distance_key
                    })
                else:
                    transformation_key = "combined"
                    total_score = scoring_dict.get(transformation_key, {}).get(distance_key, 20)
                    
                    interaction_id = f"HALF_MEETING~{pattern_key}~{'-'.join(ids_affected)}"
                    
                    for node in nodes_affected:
                        node.transform_to_element(
                            element=element,
                            amount=total_score,
                            is_transformed=False,
                            transformation_type="HALF_MEETING",
                            pattern=pattern_key,
                            interaction_id=interaction_id
                        )
                        node.marked = True
                        node.interactions.append(f"Half Meeting +{total_score:.0f}pts {element}")
                    
                    interaction_log.append({
                        "type": "HALF_MEETING",
                        "pattern": pattern_key,
                        "nodes": ids_affected,
                        "positions": positions,
                        "branches": found_branches,
                        "transformed": False,
                        "element": element,
                        "missing": missing,
                        "boost": f"+{total_score:.0f} points",
                        "distance": distance_key
                    })
    
    # 8. SIX HARMONIES (六合) - Positive
    for pattern_key, info in SIX_HARMONIES.items():
        required_branches = info["branches"]
        element = info["element"]
        
        # NOTE: Allow multiple Six Harmonies interactions (e.g., Month Chen + You, Day Chen + You)
        matching = [(pos, nid, node) for pos, nid, node in branch_data 
                   if node.value in required_branches]
        
        if len(matching) >= 2:
            # Find ALL possible pairs (every combination can happen!)
            # Example: Month Chen + Day Chen + Hour You → Two interactions:
            #   1. Month Chen + Hour You
            #   2. Day Chen + Hour You
            
            # Group nodes by their branch value
            branches_map = {}
            for pos, nid, node in matching:
                if node.value not in branches_map:
                    branches_map[node.value] = []
                branches_map[node.value].append((pos, nid, node))
            
            # Check if we have all required branches
            if set(branches_map.keys()) >= set(required_branches):
                # Get nodes for each required branch
                branch1_nodes = branches_map.get(required_branches[0], [])
                branch2_nodes = branches_map.get(required_branches[1], [])
                
                # Generate ALL possible pairs (Cartesian product)
                for node1 in branch1_nodes:
                    for node2 in branch2_nodes:
                        selected = [node1, node2]
                        
                        positions = [pos for pos, _, _ in selected]
                        nodes_affected = [node for _, _, node in selected]
                        ids_affected = [nid for _, nid, _ in selected]
                        selected_branches = [node.value for node in nodes_affected]
                        
                        # Calculate score using tuple-based scoring
                        scoring_dict = info.get("scoring", {})
                    
                        # Get distance key using node IDs (not position indices!)
                        from library import get_distance_key
                        distance_key = get_distance_key(ids_affected[0], ids_affected[1])
                
                        can_transform = element in heavenly_stems_elements
                
                        if can_transform:
                            transformation_key = "transformed"
                            total_score = scoring_dict.get(transformation_key, {}).get(distance_key, 55)
                    
                            interaction_id = f"SIX_HARMONIES~{pattern_key}~{'-'.join(ids_affected)}"
                            
                            for node in nodes_affected:
                                node.transform_to_element(
                                    element=element,
                                    amount=total_score,
                                    is_transformed=True,
                                    transformation_type="SIX_HARMONIES",
                                    pattern=pattern_key,
                                    interaction_id=interaction_id
                                )
                                node.marked = True
                                node.interactions.append(f"Six Harmonies → {element}")
                    
                            interaction_log.append({
                                "type": "SIX_HARMONIES",
                                "pattern": pattern_key,
                                "nodes": ids_affected,
                                "positions": positions,
                                "branches": selected_branches,
                                "transformed": True,
                                "element": element,
                                "boost": f"+{total_score:.0f} points",
                                "distance": distance_key
                            })
                        else:
                            transformation_key = "combined"
                            total_score = scoring_dict.get(transformation_key, {}).get(distance_key, 14)
                    
                            interaction_id = f"SIX_HARMONIES~{pattern_key}~{'-'.join(ids_affected)}"
                            
                            for node in nodes_affected:
                                node.transform_to_element(
                                    element=element,
                                    amount=total_score,
                                    is_transformed=False,
                                    transformation_type="SIX_HARMONIES",
                                    pattern=pattern_key,
                                    interaction_id=interaction_id
                                )
                                node.marked = True
                                node.interactions.append(f"Six Harmonies +{total_score:.0f}pts {element}")
                    
                            interaction_log.append({
                                "type": "SIX_HARMONIES",
                                "pattern": pattern_key,
                                "nodes": ids_affected,
                                "positions": positions,
                                "branches": selected_branches,
                                "transformed": False,
                                "element": element,
                                "boost": f"+{total_score:.0f} points",
                                "distance": distance_key,
                                "reason": f"No {element} in Heavenly Stems"
                        })
    
    # 2. PUNISHMENTS (刑) - Three types with different logic
    # Type 1: 3-node punishments (equal 1:1:1 damage)
    # Type 2: 2-node punishments (asymmetric 0.618:1, less than HARMS)
    # Type 3: Self-punishments (equal mutual damage)
    for punishment, info in PUNISHMENTS.items():
        required_branches = info["branches"]
        punishment_type = info["type"]
        scoring = info["scoring"]
        
        # NOTE: Removed 'not node.marked' - negative interactions apply regardless of positive combinations
        matching = [(pos, nid, node) for pos, nid, node in branch_data 
                   if node.value in required_branches]
        
        # Handle self-punishment (same branch appearing twice)
        if punishment_type == "self":
            same_branch = [m for m in matching if m[2].value == required_branches[0]]
            if len(same_branch) >= 2:
                affected = same_branch[:2]
                positions = [pos for pos, _, _ in affected]
                nodes_affected = [node for _, _, node in affected]
                ids_affected = [nid for _, nid, _ in affected]
                
                # Calculate distance and get appropriate scoring (equal damage for self-punishment)
                distance = abs(positions[0] - positions[1])
                distance_key = f"distance_{min(distance, 3)}" if distance > 0 else "adjacent"
                damage = scoring.get(distance_key, 16)  # Flat structure for equal damage
                
                # Create interaction ID for badges
                interaction_id = f"PUNISHMENT~{punishment}~{'-'.join(ids_affected)}"
                badge_size = reduction_to_badge_size(damage)
                
                # Apply damage with minimum qi protection to both nodes
                actual_damages = []
                for i, node in enumerate(nodes_affected):
                    actual_damage = node.reduce_by_amount_with_minimum(damage, minimum_qi=1.0)
                    actual_damages.append(actual_damage)
                    node.marked = True
                    node.interactions.append(f"Self-Punishment -{actual_damage:.1f} damage")
                    
                    # Add negation badge with neutral icon (same for both nodes)
                    badge_data = {
                        "interaction_id": interaction_id,
                        "type": "punishment",
                        "badge": "XING",  # Icon identifier, not elemental character
                        "size": badge_size
                    }
                    node.badges.append(badge_data)
                
                # Hidden Qi damage
                nodes_affected[0].apply_hidden_qi_damage(nodes_affected[1])
                
                interaction_log.append({
                    "type": "PUNISHMENT",
                    "pattern": punishment,
                    "nodes": ids_affected,
                    "positions": positions,
                    "damage": [round(d, 1) for d in actual_damages],
                    "distance": distance_key
                })
        elif punishment_type == "3-node":
            # 3-node punishment: ELEVATED equal 1:1:1 damage across all 3 nodes (38 each)
            if len(matching) >= 3:
                found_branches = [node.value for _, _, node in matching[:3]]
                if set(found_branches) == set(required_branches):
                    affected = matching[:3]
                    positions = [pos for pos, _, _ in affected]
                    nodes_affected = [node for _, _, node in affected]
                    ids_affected = [nid for _, nid, _ in affected]
                    
                    # Use minimum distance for strongest effect in 3-node setup
                    distances = [abs(positions[i] - positions[j]) for i in range(len(positions)) for j in range(i+1, len(positions))]
                    distance = min(distances)
                    distance_key = f"distance_{min(distance, 3)}" if distance > 0 else "adjacent"
                    damage = scoring.get(distance_key, 38)  # Flat structure for equal elevated damage
                    
                    # Create interaction ID for badges
                    interaction_id = f"PUNISHMENT~{punishment}~{'-'.join(ids_affected)}"
                    badge_size = reduction_to_badge_size(damage)
                    
                    # Apply equal damage to all 3 nodes with minimum qi protection
                    actual_damages = []
                    for node in nodes_affected:
                        actual_damage = node.reduce_by_amount_with_minimum(damage, minimum_qi=1.0)
                        actual_damages.append(actual_damage)
                        node.marked = True
                        node.interactions.append(f"Punishment (3-node) -{actual_damage:.1f} damage")
                        
                        # Add negation badge with neutral icon (same for all 3 nodes)
                        badge_data = {
                            "interaction_id": interaction_id,
                            "type": "punishment",
                            "badge": "XING",  # Icon identifier, not elemental character
                            "size": badge_size
                        }
                        node.badges.append(badge_data)
                    
                    # Hidden Qi damage between pairs (apply to all pairs)
                    for i in range(len(nodes_affected)):
                        for j in range(i+1, len(nodes_affected)):
                            nodes_affected[i].apply_hidden_qi_damage(nodes_affected[j])
                    
                    interaction_log.append({
                        "type": "PUNISHMENT",
                        "pattern": punishment,
                        "nodes": ids_affected,
                        "positions": positions,
                        "branches": found_branches,
                        "damage": [round(d, 1) for d in actual_damages],
                        "distance": distance_key,
                        "punishment_type": "3-node"
                    })
        
        elif punishment_type == "2-node":
            # 2-node punishment: Asymmetric (controller:victim = 0.618:1, less severe than HARMS)
            if len(matching) >= 2:
                found_branches = [node.value for _, _, node in matching[:2]]
                if set(found_branches) == set(required_branches):
                    # Identify controller and victim nodes
                    controller_branch = info["controller"]
                    controlled_branch = info["controlled"]
                    
                    controller_node = None
                    victim_node = None
                    for pos, nid, node in matching[:2]:
                        if node.value == controller_branch:
                            controller_node = (pos, nid, node)
                        elif node.value == controlled_branch:
                            victim_node = (pos, nid, node)
                    
                    if not controller_node or not victim_node:
                        continue
                    
                    positions = [controller_node[0], victim_node[0]]
                    distance = abs(positions[0] - positions[1])
                    distance_key = f"distance_{min(distance, 3)}" if distance > 0 else "adjacent"
                    
                    # Use asymmetric scoring
                    victim_damage = scoring.get("victim", {}).get(distance_key, 16)
                    controller_damage = scoring.get("controller", {}).get(distance_key, 10)
                    
                    # Apply victim damage first with minimum qi protection
                    actual_victim_damage = victim_node[2].reduce_by_amount_with_minimum(victim_damage, minimum_qi=1.0)
                    victim_node[2].interactions.append(f"Punishment (victim) -{actual_victim_damage:.1f} damage")
                    victim_node[2].marked = True
                    
                    # Scale controller damage proportionally if victim couldn't take full damage
                    if actual_victim_damage < victim_damage:
                        controller_damage = controller_damage * (actual_victim_damage / victim_damage)
                    
                    # Apply controller damage
                    actual_controller_damage = controller_node[2].reduce_by_amount_with_minimum(controller_damage, minimum_qi=1.0)
                    controller_node[2].interactions.append(f"Punishment (controller) -{actual_controller_damage:.1f} energy spent")
                    controller_node[2].marked = True
                    
                    # Create interaction ID for badges
                    interaction_id = f"PUNISHMENT~{punishment}~{controller_node[1]}-{victim_node[1]}"
                    badge_size = reduction_to_badge_size(actual_victim_damage)
                    
                    # Add negation badge to BOTH nodes with neutral icon
                    badge_data_victim = {
                        "interaction_id": interaction_id,
                        "type": "punishment",
                        "badge": "XING",  # Icon identifier, not elemental character
                        "size": badge_size
                    }
                    victim_node[2].badges.append(badge_data_victim)
                    
                    badge_data_controller = {
                        "interaction_id": interaction_id,
                        "type": "punishment",
                        "badge": "XING",  # Icon identifier, not elemental character
                        "size": badge_size
                    }
                    controller_node[2].badges.append(badge_data_controller)
                    
                    # Hidden Qi damage
                    controller_node[2].apply_hidden_qi_damage(victim_node[2])
                    
                    interaction_log.append({
                        "type": "PUNISHMENT",
                        "pattern": punishment,
                        "nodes": [controller_node[1], victim_node[1]],
                        "controller": {"node": controller_node[1], "branch": controller_branch, "damage": round(actual_controller_damage, 1)},
                        "victim": {"node": victim_node[1], "branch": controlled_branch, "damage": round(actual_victim_damage, 1)},
                        "positions": positions,
                        "branches": found_branches,
                        "distance": distance_key,
                        "punishment_type": "2-node",
                        "proportional_scaling": actual_victim_damage < victim_damage
                    })
    
    # 4. HARMS (害) - Asymmetric EB damage (controller:victim = 0.618:1.0)
    for harm, info in HARMS.items():
        required_branches = info["branches"]
        controller_branch = info["controller"]
        controlled_branch = info["controlled"]
        scoring = info["scoring"]
        
        # NOTE: Removed 'not node.marked' - negative interactions apply regardless of positive combinations
        matching = [(pos, nid, node) for pos, nid, node in branch_data 
                   if node.value in required_branches]
        
        if len(matching) >= 2:
            found_branches = [node.value for _, _, node in matching[:2]]
            if set(found_branches) == set(required_branches):
                # Identify controller and victim nodes
                controller_node = None
                victim_node = None
                for pos, nid, node in matching[:2]:
                    if node.value == controller_branch:
                        controller_node = (pos, nid, node)
                    elif node.value == controlled_branch:
                        victim_node = (pos, nid, node)
                
                if not controller_node or not victim_node:
                    continue
                
                positions = [controller_node[0], victim_node[0]]
                is_adjacent = are_adjacent(positions)
                
                # Get appropriate scoring based on distance
                distance = abs(positions[0] - positions[1])
                distance_key = f"distance_{min(distance, 3)}" if distance > 0 else "adjacent"
                
                victim_damage = scoring.get("victim", {}).get(distance_key, 20)
                controller_damage = scoring.get("controller", {}).get(distance_key, 12)
                
                # Apply victim damage first with minimum qi protection
                actual_victim_damage = victim_node[2].reduce_by_amount_with_minimum(victim_damage, minimum_qi=1.0)
                victim_node[2].interactions.append(f"Harm (victim) -{actual_victim_damage:.1f} damage")
                victim_node[2].marked = True
                
                # Scale controller damage proportionally if victim couldn't take full damage
                if actual_victim_damage < victim_damage:
                    controller_damage = controller_damage * (actual_victim_damage / victim_damage)
                
                # Apply controller damage
                actual_controller_damage = controller_node[2].reduce_by_amount_with_minimum(controller_damage, minimum_qi=1.0)
                controller_node[2].interactions.append(f"Harm (controller) -{actual_controller_damage:.1f} energy spent")
                controller_node[2].marked = True
                
                # Create interaction ID for badges
                interaction_id = f"HARM~{harm}~{controller_node[1]}-{victim_node[1]}"
                badge_size = reduction_to_badge_size(actual_victim_damage)
                
                # Add negation badge to BOTH nodes with neutral icon
                badge_data_victim = {
                    "interaction_id": interaction_id,
                    "type": "harm",
                    "badge": "HAI",  # Icon identifier, not elemental character
                    "size": badge_size
                }
                victim_node[2].badges.append(badge_data_victim)
                
                badge_data_controller = {
                    "interaction_id": interaction_id,
                    "type": "harm",
                    "badge": "HAI",  # Icon identifier, not elemental character
                    "size": badge_size
                }
                controller_node[2].badges.append(badge_data_controller)
                
                # Hidden Qi damage
                controller_node[2].apply_hidden_qi_damage(victim_node[2])
                
                interaction_log.append({
                    "type": "HARM",
                    "pattern": harm,
                    "nodes": [controller_node[1], victim_node[1]],  # Controller first, victim second
                    "controller": {"node": controller_node[1], "branch": controller_branch, "damage": round(actual_controller_damage, 1)},
                    "victim": {"node": victim_node[1], "branch": controlled_branch, "damage": round(actual_victim_damage, 1)},
                    "positions": positions,
                    "branches": found_branches,
                    "distance": distance_key,
                    "proportional_scaling": actual_victim_damage < victim_damage
                })
    
    # 4. CLASHES (沖) - Two types: opposite (asymmetric) vs same element (equal)
    for clash, info in CLASHES.items():
        required_branches = info["branches"]
        clash_type = info["type"]
        scoring = info["scoring"]
        
        # NOTE: Removed 'not node.marked' - negative interactions apply regardless of positive combinations
        matching = [(pos, nid, node) for pos, nid, node in branch_data 
                   if node.value in required_branches]
        
        if len(matching) >= 2:
            # Group nodes by their branch value (same approach as SIX_HARMONIES)
            branches_map = {}
            for pos, nid, node in matching:
                if node.value not in branches_map:
                    branches_map[node.value] = []
                branches_map[node.value].append((pos, nid, node))
            
            # Check if we have all required branches
            if set(branches_map.keys()) >= set(required_branches):
                # Get nodes for each required branch
                branch1_nodes = branches_map.get(required_branches[0], [])
                branch2_nodes = branches_map.get(required_branches[1], [])
                
                # Generate ALL possible pairs (Cartesian product)
                for node1 in branch1_nodes:
                    for node2 in branch2_nodes:
                        affected = [node1, node2]
                        positions = [pos for pos, _, _ in affected]
                        
                        # Calculate distance
                        distance = abs(positions[0] - positions[1])
                        distance_key = f"distance_{min(distance, 3)}" if distance > 0 else "adjacent"
                        found_branches = [node.value for _, _, node in affected]
                        
                        if clash_type == "opposite":
                            # Opposite elements: Asymmetric (controller:victim = 0.618:1)
                            controller_branch = info["controller"]
                            controlled_branch = info["controlled"]
                            
                            controller_node = None
                            victim_node = None
                            for pos, nid, node in affected:
                                if node.value == controller_branch:
                                    controller_node = (pos, nid, node)
                                elif node.value == controlled_branch:
                                    victim_node = (pos, nid, node)
                            
                            if not controller_node or not victim_node:
                                continue
                    
                            # Use asymmetric scoring
                            victim_damage = scoring.get("victim", {}).get(distance_key, 38)
                            controller_damage = scoring.get("controller", {}).get(distance_key, 24)
                            
                            # Apply victim damage first with minimum qi protection
                            actual_victim_damage = victim_node[2].reduce_by_amount_with_minimum(victim_damage, minimum_qi=1.0)
                            victim_node[2].interactions.append(f"Clash (victim) -{actual_victim_damage:.1f} damage")
                            victim_node[2].marked = True
                            
                            # Scale controller damage proportionally if victim couldn't take full damage
                            if actual_victim_damage < victim_damage:
                                controller_damage = controller_damage * (actual_victim_damage / victim_damage)
                            
                            # Apply controller damage
                            actual_controller_damage = controller_node[2].reduce_by_amount_with_minimum(controller_damage, minimum_qi=1.0)
                            controller_node[2].interactions.append(f"Clash (controller) -{actual_controller_damage:.1f} energy spent")
                            controller_node[2].marked = True
                            
                            # Create interaction ID for badges
                            interaction_id = f"CLASH~{clash}~{controller_node[1]}-{victim_node[1]}"
                            badge_size = reduction_to_badge_size(actual_victim_damage)
                            
                            # Add negation badge to BOTH nodes with neutral icon
                            badge_data_victim = {
                                "interaction_id": interaction_id,
                                "type": "clash",
                                "badge": "CHONG",  # Icon identifier, not elemental character
                                "size": badge_size
                            }
                            victim_node[2].badges.append(badge_data_victim)
                            
                            badge_data_controller = {
                                "interaction_id": interaction_id,
                                "type": "clash",
                                "badge": "CHONG",  # Icon identifier, not elemental character
                                "size": badge_size
                            }
                            controller_node[2].badges.append(badge_data_controller)
                            
                            # Hidden Qi damage
                            controller_node[2].apply_hidden_qi_damage(victim_node[2])
                            
                            interaction_log.append({
                                "type": "CLASH",
                                "pattern": clash,
                                "nodes": [controller_node[1], victim_node[1]],
                                "controller": {"node": controller_node[1], "branch": controller_branch, "damage": round(actual_controller_damage, 1)},
                                "victim": {"node": victim_node[1], "branch": controlled_branch, "damage": round(actual_victim_damage, 1)},
                                "positions": positions,
                                "branches": found_branches,
                                "distance": distance_key,
                                "clash_type": "opposite",
                                "proportional_scaling": actual_victim_damage < victim_damage
                            })
                        
                        elif clash_type == "same":
                            # Same element: Equal mutual damage
                            nodes_affected = [node for _, _, node in affected]
                            ids_affected = [nid for _, nid, _ in affected]
                            
                            damage = scoring.get(distance_key, 38)  # Flat structure for equal damage
                            
                            # Create interaction ID for badges
                            interaction_id = f"CLASH~{clash}~{'-'.join(ids_affected)}"
                            badge_size = reduction_to_badge_size(damage)
                            
                            # Apply equal damage to both nodes with minimum qi protection
                            actual_damages = []
                            for i, node in enumerate(nodes_affected):
                                actual_damage = node.reduce_by_amount_with_minimum(damage, minimum_qi=1.0)
                                actual_damages.append(actual_damage)
                                node.marked = True
                                node.interactions.append(f"Clash (equal) -{actual_damage:.1f} damage")
                                
                                # Add negation badge with neutral icon (same for both nodes)
                                badge_data = {
                                    "interaction_id": interaction_id,
                                    "type": "clash",
                                    "badge": "CHONG",  # Icon identifier, not elemental character
                                    "size": badge_size
                                }
                                node.badges.append(badge_data)
                            
                            # Hidden Qi damage
                            nodes_affected[0].apply_hidden_qi_damage(nodes_affected[1])
                            
                            interaction_log.append({
                                "type": "CLASH",
                                "pattern": clash,
                                "nodes": ids_affected,
                                "positions": positions,
                                "branches": found_branches,
                                "damage": [round(d, 1) for d in actual_damages],
                                "distance": distance_key,
                                "clash_type": "same"
                            })
    
    # 5. DESTRUCTION (破) - Distance 0 only, two types: opposite (asymmetric) vs same (equal)
    for destruction, info in DESTRUCTION.items():
        required_branches = info["branches"]
        destruction_type = info["type"]
        scoring = info["scoring"]
        
        # NOTE: Removed 'not node.marked' - negative interactions apply regardless of positive combinations
        matching = [(pos, nid, node) for pos, nid, node in branch_data 
                   if node.value in required_branches]
        
        if len(matching) >= 2:
            found_branches = [node.value for _, _, node in matching[:2]]
            if set(found_branches) == set(required_branches):
                affected = matching[:2]
                positions = [pos for pos, _, _ in affected]
                
                # Calculate distance using proper function
                distance = calculate_interaction_distance(positions[0], positions[1])
                
                # DESTRUCTION only valid when adjacent (distance 1)
                # Distance 1 includes: y-m, m-d, d-h, and luck↔natal
                if distance > 1:
                    continue  # Skip: DESTRUCTION only valid at distance 1
                
                # Get distance key for logging (always "1" for DESTRUCTION)
                ids_affected = [nid for _, nid, _ in affected]
                from library import get_distance_key
                distance_key = get_distance_key(ids_affected[0], ids_affected[1])
                
                if destruction_type == "opposite":
                    # Opposite elements: Asymmetric (controller:victim = 0.618:1)
                    controller_branch = info["controller"]
                    controlled_branch = info["controlled"]
                    
                    controller_node = None
                    victim_node = None
                    for pos, nid, node in affected:
                        if node.value == controller_branch:
                            controller_node = (pos, nid, node)
                        elif node.value == controlled_branch:
                            victim_node = (pos, nid, node)
                    
                    if not controller_node or not victim_node:
                        continue
                    
                    # Use asymmetric scoring
                    victim_damage = scoring.get("victim", {}).get(distance_key, 20)
                    controller_damage = scoring.get("controller", {}).get(distance_key, 12)
                    
                    # Apply victim damage first with minimum qi protection
                    actual_victim_damage = victim_node[2].reduce_by_amount_with_minimum(victim_damage, minimum_qi=1.0)
                    victim_node[2].interactions.append(f"Destruction (victim) -{actual_victim_damage:.1f} damage")
                    victim_node[2].marked = True
                    
                    # Scale controller damage proportionally if victim couldn't take full damage
                    if actual_victim_damage < victim_damage:
                        controller_damage = controller_damage * (actual_victim_damage / victim_damage)
                    
                    # Apply controller damage
                    actual_controller_damage = controller_node[2].reduce_by_amount_with_minimum(controller_damage, minimum_qi=1.0)
                    controller_node[2].interactions.append(f"Destruction (controller) -{actual_controller_damage:.1f} energy spent")
                    controller_node[2].marked = True
                    
                    # Create interaction ID for badges
                    interaction_id = f"DESTRUCTION~{destruction}~{controller_node[1]}-{victim_node[1]}"
                    badge_size = reduction_to_badge_size(actual_victim_damage)
                    
                    # Add negation badge to BOTH nodes with neutral icon
                    badge_data_victim = {
                        "interaction_id": interaction_id,
                        "type": "destruction",
                        "badge": "PO",  # Icon identifier, not elemental character
                        "size": badge_size
                    }
                    victim_node[2].badges.append(badge_data_victim)
                    
                    badge_data_controller = {
                        "interaction_id": interaction_id,
                        "type": "destruction",
                        "badge": "PO",  # Icon identifier, not elemental character
                        "size": badge_size
                    }
                    controller_node[2].badges.append(badge_data_controller)
                    
                    # Hidden Qi damage
                    controller_node[2].apply_hidden_qi_damage(victim_node[2])
                    
                    interaction_log.append({
                        "type": "DESTRUCTION",
                        "pattern": destruction,
                        "nodes": [controller_node[1], victim_node[1]],
                        "controller": {"node": controller_node[1], "branch": controller_branch, "damage": round(actual_controller_damage, 1)},
                        "victim": {"node": victim_node[1], "branch": controlled_branch, "damage": round(actual_victim_damage, 1)},
                        "positions": positions,
                        "branches": found_branches,
                        "distance": distance_key,
                        "destruction_type": "opposite",
                        "proportional_scaling": actual_victim_damage < victim_damage
                    })
                
                elif destruction_type == "same":
                    # Same element: Equal mutual damage
                    nodes_affected = [node for _, _, node in affected]
                    ids_affected = [nid for _, nid, _ in affected]
                    
                    damage = scoring.get(distance_key, 20)  # Flat structure for equal damage
                    
                    # Create interaction ID for badges
                    interaction_id = f"DESTRUCTION~{destruction}~{'-'.join(ids_affected)}"
                    badge_size = reduction_to_badge_size(damage)
                    
                    # Apply equal damage to both nodes with minimum qi protection
                    actual_damages = []
                    for i, node in enumerate(nodes_affected):
                        actual_damage = node.reduce_by_amount_with_minimum(damage, minimum_qi=1.0)
                        actual_damages.append(actual_damage)
                        node.marked = True
                        node.interactions.append(f"Destruction (equal) -{actual_damage:.1f} damage")
                        
                        # Add negation badge with neutral icon (same for both nodes)
                        badge_data = {
                            "interaction_id": interaction_id,
                            "type": "destruction",
                            "badge": "PO",  # Icon identifier, not elemental character
                            "size": badge_size
                        }
                        node.badges.append(badge_data)
                    
                    # Hidden Qi damage
                    nodes_affected[0].apply_hidden_qi_damage(nodes_affected[1])
                    
                    interaction_log.append({
                        "type": "DESTRUCTION",
                        "pattern": destruction,
                        "nodes": ids_affected,
                        "positions": positions,
                        "branches": found_branches,
                        "damage": [round(d, 1) for d in actual_damages],
                        "distance": distance_key,
                        "destruction_type": "same"
                    })
    
    # 8. HALF COMBINATIONS (半合) - Positive (partial combination, never transforms)
    # Child of THREE_COMBINATIONS: blocked ONLY by THREE_COMBINATIONS, allowed with everything else
    for pattern_key, info in HALF_COMBINATIONS.items():
        required_branches = info["branches"]
        element = info["element"]
        
        # Check if nodes have THREE_COMBINATIONS interaction (blocks HALF_COMBINATIONS)
        matching = [(pos, nid, node) for pos, nid, node in branch_data 
                   if node.value in required_branches
                   and not any("THREE_COMBINATION" in badge.get("interaction_id", "") for badge in node.badges)]
        
        if len(matching) >= 2:
            # Group nodes by their branch value (same approach as SIX_HARMONIES)
            branches_map = {}
            for pos, nid, node in matching:
                if node.value not in branches_map:
                    branches_map[node.value] = []
                branches_map[node.value].append((pos, nid, node))
            
            # Check if we have all required branches
            if set(branches_map.keys()) >= set(required_branches):
                # Get nodes for each required branch
                branch1_nodes = branches_map.get(required_branches[0], [])
                branch2_nodes = branches_map.get(required_branches[1], [])
                
                # Generate ALL possible pairs (Cartesian product)
                for node1 in branch1_nodes:
                    for node2 in branch2_nodes:
                        selected = [node1, node2]
                        
                        positions = [pos for pos, _, _ in selected]
                        nodes_affected = [node for _, _, node in selected]
                        ids_affected = [nid for _, nid, _ in selected]
                        found_branches = [node.value for node in nodes_affected]
                        
                        # Calculate score using detected (never transforms - derivative of THREE_COMBINATIONS)
                        scoring_dict = info.get("scoring", {})
                        
                        # Calculate distance for logging and scoring
                        from library import get_distance_key
                        distance_key = get_distance_key(ids_affected[0], ids_affected[1])
                        
                        # Always use "detected" scoring - derivative patterns never transform
                        transformation_key = "detected"
                        total_score = scoring_dict.get(transformation_key, {}).get(distance_key, 15)
                        
                        interaction_id = f"HALF_COMBINATION~{pattern_key}~{'-'.join(ids_affected)}"
                        
                        for node in nodes_affected:
                            node.transform_to_element(
                                element=element,
                                amount=total_score,
                                is_transformed=False,  # Derivative patterns never transform
                                transformation_type="HALF_COMBINATION",
                                pattern=pattern_key,
                                interaction_id=interaction_id
                            )
                            node.marked = True
                            node.interactions.append(f"Half Combination +{total_score:.0f}pts {element}")
                        
                        interaction_log.append({
                            "type": "HALF_COMBINATION",
                            "pattern": pattern_key,
                            "nodes": ids_affected,
                            "positions": positions,
                            "branches": found_branches,
                            "element": element,
                            "boost": f"+{total_score:.0f} points",
                            "distance": distance_key
                        })
    
    # 9. ARCHED COMBINATIONS (拱合) - Positive (partial combination, never transforms)
    # Child of THREE_COMBINATIONS: blocked ONLY by THREE_COMBINATIONS, allowed with everything else
    for pattern_key, info in ARCHED_COMBINATIONS.items():
        required_branches = info["branches"]
        element = info["element"]
        missing = info["missing"]
        
        # Check if nodes have THREE_COMBINATIONS interaction (blocks ARCHED_COMBINATIONS)
        matching = [(pos, nid, node) for pos, nid, node in branch_data 
                   if node.value in required_branches
                   and not any("THREE_COMBINATION" in badge.get("interaction_id", "") for badge in node.badges)]
        
        if len(matching) >= 2:
            # Group nodes by their branch value (same approach as SIX_HARMONIES)
            branches_map = {}
            for pos, nid, node in matching:
                if node.value not in branches_map:
                    branches_map[node.value] = []
                branches_map[node.value].append((pos, nid, node))
            
            # Check if we have all required branches
            if set(branches_map.keys()) >= set(required_branches):
                # Get nodes for each required branch
                branch1_nodes = branches_map.get(required_branches[0], [])
                branch2_nodes = branches_map.get(required_branches[1], [])
                
                # Generate ALL possible pairs (Cartesian product)
                for node1 in branch1_nodes:
                    for node2 in branch2_nodes:
                        selected = [node1, node2]
                        
                        positions = [pos for pos, _, _ in selected]
                        nodes_affected = [node for _, _, node in selected]
                        ids_affected = [nid for _, nid, _ in selected]
                        found_branches = [node.value for node in nodes_affected]
                        
                        # Calculate score using detected (never transforms - derivative of THREE_COMBINATIONS)
                        scoring_dict = info.get("scoring", {})
                        
                        # Calculate distance for logging and scoring
                        from library import get_distance_key
                        distance_key = get_distance_key(ids_affected[0], ids_affected[1])
                        
                        # Always use "detected" scoring - derivative patterns never transform
                        transformation_key = "detected"
                        total_score = scoring_dict.get(transformation_key, {}).get(distance_key, 12)
                        
                        interaction_id = f"ARCHED_COMBINATION~{pattern_key}~{'-'.join(ids_affected)}"
                        
                        for node in nodes_affected:
                            node.transform_to_element(
                                element=element,
                                amount=total_score,
                                is_transformed=False,  # Derivative patterns never transform
                                transformation_type="ARCHED_COMBINATION",
                                pattern=pattern_key,
                                interaction_id=interaction_id
                            )
                            node.marked = True
                            node.interactions.append(f"Arched Combination +{total_score:.0f}pts {element}")
                        
                        interaction_log.append({
                            "type": "ARCHED_COMBINATION",
                            "pattern": pattern_key,
                            "nodes": ids_affected,
                            "positions": positions,
                            "branches": found_branches,
                            "element": element,
                            "missing": missing,
                            "boost": f"+{total_score:.0f} points",
                            "distance": distance_key
                        })
    
    # ============= HEAVENLY STEM INTERACTIONS =============
    
    # Get stem nodes for interaction processing
    def get_stem_nodes():
        """Get all stem nodes with their positions"""
        stem_nodes = []
        for pos in position_codes:
            hs_id = f"hs_{pos}"
            if hs_id in nodes:
                idx = position_to_index.get(pos, 0)
                stem_nodes.append((idx, hs_id, nodes[hs_id]))
        return stem_nodes
    
    stem_data = get_stem_nodes()
    
    # Process HS interactions with proper priority and queueing
    # Priority: adjacent combinations -> adjacent conflicts -> non-adjacent (queued)
    
    # Collect all potential interactions first
    hs_combinations_queue = []  # Will hold (is_adjacent, data_dict)
    hs_conflicts_queue = []     # Will hold (is_adjacent, data_dict)
    
    # 9. STEM COMBINATIONS (天干五合) - Collect first
    for stem_pair, config in STEM_COMBINATIONS.items():
        required_stems = stem_pair.split("-")  # Split hyphenated string
        
        matching = [(pos, nid, node) for pos, nid, node in stem_data 
                   if node.value in required_stems]
        
        if len(matching) >= 2:
            found_stems = [node.value for _, _, node in matching]
            if set(found_stems) >= set(required_stems):
                # Find ALL possible pairs when there are multiple instances
                stem1_nodes = [(pos, nid, node) for pos, nid, node in matching 
                              if node.value == required_stems[0]]
                stem2_nodes = [(pos, nid, node) for pos, nid, node in matching 
                              if node.value == required_stems[1]]
                
                # Create all possible combinations between stem1 and stem2 nodes
                for s1_pos, s1_id, s1_node in stem1_nodes:
                    for s2_pos, s2_id, s2_node in stem2_nodes:
                        if s1_id != s2_id:  # Don't pair a node with itself
                            positions = [s1_pos, s2_pos]
                            is_adjacent = are_adjacent(positions)
                            
                            # Queue the combination with adjacency info
                            hs_combinations_queue.append((is_adjacent, {
                                "positions": positions,
                                "nodes": [s1_node, s2_node],
                                "node_ids": [s1_id, s2_id],
                                "stems": [s1_node.value, s2_node.value],
                                "config": config,  # Pass the entire config dictionary
                                "required_stems": required_stems
                            }))
    
    # 10. STEM CONFLICTS (天干沖) - Collect first
    for stem_pair, config in STEM_CONFLICTS.items():
        required_stems = stem_pair.split("-")  # Split hyphenated string
        conflictor_stem = config["controller"]
        conflicted_stem = config["controlled"]
        
        matching = [(pos, nid, node) for pos, nid, node in stem_data 
                   if node.value in required_stems]
        
        if len(matching) >= 2:
            found_stems = [node.value for _, _, node in matching]
            if set(found_stems) >= set(required_stems):
                # Find ALL possible conflict pairs when there are multiple instances
                conflictor_nodes = [(pos, nid, node) for pos, nid, node in matching 
                                   if node.value == conflictor_stem]
                conflicted_nodes = [(pos, nid, node) for pos, nid, node in matching 
                                   if node.value == conflicted_stem]
                
                # Create all possible conflicts between conflictor and conflicted nodes
                for conf_node in conflictor_nodes:
                    for confd_node in conflicted_nodes:
                        if conf_node[1] != confd_node[1]:  # Don't conflict with itself
                            positions = [conf_node[0], confd_node[0]]
                            is_adjacent = are_adjacent(positions)
                            
                            # Queue the conflict with adjacency info
                            hs_conflicts_queue.append((is_adjacent, {
                                "positions": positions,
                                "conflictor": conf_node,
                                "conflicted": confd_node,
                                "conflictor_stem": conflictor_stem,
                                "conflicted_stem": conflicted_stem,
                                "required_stems": required_stems
                            }))
    
    # Process in priority order:
    # 1. Adjacent HS Combinations
    for is_adjacent, combo_data in hs_combinations_queue:
        if is_adjacent:
            nodes_affected = combo_data["nodes"]
            
            # Process the adjacent combination
            affected_ids = combo_data["node_ids"]
            stems_involved = combo_data["stems"]
            config = combo_data["config"]  # Full configuration dictionary
            required_stems = combo_data["required_stems"]
            positions = combo_data["positions"]
            
            # Create structured interaction_id
            stems_str = "-".join(sorted(stems_involved))
            nodes_str = "~".join(sorted(affected_ids))
            interaction_id = f"HS_COMBINATION~{stems_str}~{nodes_str}"
            
            # Get transformation requirements from config
            transform_to_stem = config.get("transform_to", "")
            transform_requirement = config.get("transformation_requirement", {})
            required_element = transform_requirement.get("element", "")
            
            # Check if transformation is supported by any earthly branch (including luck pillars and talismans)
            earthly_branch_elements = set()
            for pos in position_codes:
                eb_id = f"eb_{pos}"
                if eb_id in nodes:
                    eb_value = nodes[eb_id].value
                    if eb_value in EARTHLY_BRANCHES:
                        earthly_branch_elements.add(EARTHLY_BRANCHES[eb_value]["element"])
            
            transforming_element_exists = required_element in earthly_branch_elements
            
            # Use tuple-based scoring from config
            scoring_dict = config.get("scoring", {})
            
            # Determine the scoring key based on transformation and distance
            # Calculate distance for logging
            from library import get_distance_key
            distance_key = get_distance_key(affected_ids[0], affected_ids[1])
            transformation_key = "transformed" if transforming_element_exists else "combined"
            
            # Get score from the scoring dictionary
            total_score = scoring_dict.get(transformation_key, {}).get(distance_key, 20)  # Default to 20 if not found
            
            for node in nodes_affected:
                # For HS Combinations: Add qi of the transformed element
                if transform_to_stem and transform_to_stem in HEAVENLY_STEMS:
                    trans_element = HEAVENLY_STEMS[transform_to_stem]["element"]
                    
                    # Find both Yang and Yin stems for this element
                    yang_stem = None
                    yin_stem = None
                    for stem_name, stem_data in HEAVENLY_STEMS.items():
                        if stem_data["element"] == trans_element:
                            if stem_data["polarity"] == "Yang":
                                yang_stem = stem_name
                            else:
                                yin_stem = stem_name
                    
                    # Add qi for the polarity matching the node's original stem
                    node_polarity = HEAVENLY_STEMS[node.value]["polarity"] if node.value in HEAVENLY_STEMS else "Yang"
                    
                    # Determine which stem to use based on node's polarity
                    if node_polarity == "Yang" and yang_stem:
                        trans_stem = yang_stem
                    elif node_polarity == "Yin" and yin_stem:
                        trans_stem = yin_stem
                    else:
                        trans_stem = transform_to_stem  # Fallback to config stem
                    
                    trans_polarity = HEAVENLY_STEMS[trans_stem]["polarity"]
                    trans_element_key = f"{trans_polarity} {trans_element}"
                    
                    # Add transformed element qi WITHOUT clearing existing qi
                    if trans_element_key not in node.elements:
                        node.elements[trans_element_key] = {"score": 0}
                    node.elements[trans_element_key]["score"] += total_score
                    
                    # Track this combination as a badge
                    # HS combinations: "transformation" if transformed, "combination" if not
                    badge_type = "transformation" if transforming_element_exists else "combination"
                    badge_size = "lg" if transforming_element_exists else "xs"
                    badge_data = {
                        "interaction_id": interaction_id,
                        "type": badge_type,
                        "badge": trans_stem,
                        "size": badge_size
                    }
                    node.badges.append(badge_data)
                
                node.marked = True
                
                interaction_desc = f"HS Combination → {required_element} (score: {total_score})"
                if not transforming_element_exists:
                    interaction_desc += " [No transformation]"
                node.interactions.append(interaction_desc)
            
            # Log the interaction
            interaction_log.append({
                "interaction_id": interaction_id,
                "type": "STEM_COMBINATION",
                "element": required_element,
                "transform_to": transform_to_stem,
                "nodes": affected_ids,
                "positions": positions,
                "stems": stems_involved,
                "transformation": transforming_element_exists,
                "transforming_element_exists": transforming_element_exists,
                "score": total_score,
                "distance": distance_key,
                "boost": f"+{total_score:.0f} points",
                "description": f"{' + '.join(required_stems)} → {required_element}" + (" [Transformed]" if transforming_element_exists else " [Boost only]")
            })
            
    
    # 2. Adjacent HS Conflicts
    for is_adjacent, conflict_data in hs_conflicts_queue:
        if is_adjacent:
            conflictor_node = conflict_data["conflictor"]
            conflicted_node = conflict_data["conflicted"]
            
            # Extract node IDs from the tuples
            conflictor_id = conflictor_node[1]
            conflicted_id = conflicted_node[1]
            
            positions = conflict_data["positions"]
            conflictor_stem = conflict_data["conflictor_stem"]
            conflicted_stem = conflict_data["conflicted_stem"]
            required_stems = conflict_data["required_stems"]
            
            # Find the conflict pattern to get scoring
            conflict_key = None
            for key, cfg in STEM_CONFLICTS.items():
                if set(key.split("-")) == set(required_stems):
                    conflict_key = key
                    break
            
            scoring = STEM_CONFLICTS[conflict_key]["scoring"] if conflict_key else {}
            
            # Calculate distance for logging and scoring
            from library import get_distance_key
            distance_key = get_distance_key(conflictor_id, conflicted_id)
            
            # Use new asymmetric scoring structure (victim/controller with distance decay)
            victim_damage = scoring.get("victim", {}).get(distance_key, scoring.get("victim", {}).get("1", 35))  # Fallback to "1" then 35
            controller_damage = scoring.get("controller", {}).get(distance_key, scoring.get("controller", {}).get("1", 22))  # Fallback to "1" then 22
            
            # Apply victim damage first with minimum qi protection
            actual_victim_damage = conflicted_node[2].reduce_by_amount_with_minimum(victim_damage, minimum_qi=1.0)
            conflicted_node[2].interactions.append(f"HS Conflict (victim) -{actual_victim_damage:.1f} damage")
            conflicted_node[2].marked = True
            
            # Scale controller damage proportionally if victim couldn't take full damage
            if actual_victim_damage < victim_damage:
                # Victim was capped - controller only spends proportional energy
                controller_damage = controller_damage * (actual_victim_damage / victim_damage)
            
            # Apply controller damage
            actual_controller_damage = conflictor_node[2].reduce_by_amount_with_minimum(controller_damage, minimum_qi=1.0)
            conflictor_node[2].interactions.append(f"HS Conflict (controller) -{actual_controller_damage:.1f} energy spent")
            conflictor_node[2].marked = True
            
            # Create interaction ID and badges
            interaction_id = f"STEM_CONFLICT~{conflictor_stem}-{conflicted_stem}~{conflictor_id}-{conflicted_id}"
            badge_size = reduction_to_badge_size(actual_victim_damage)
            
            # Add negation badge to BOTH nodes with neutral icon
            badge_data_victim = {
                "interaction_id": interaction_id,
                "type": "stem_conflict",
                "badge": "KE",  # Icon identifier (剋/克 = control/restrain)
                "size": badge_size
            }
            conflicted_node[2].badges.append(badge_data_victim)
            
            badge_data_controller = {
                "interaction_id": interaction_id,
                "type": "stem_conflict",
                "badge": "KE",  # Icon identifier (剋/克 = control/restrain)
                "size": badge_size
            }
            conflictor_node[2].badges.append(badge_data_controller)
            
            # Reduce count for conflicted element only
            conflicted_count_reduction = scoring.get("conflicted_count_reduction", 0.5)
            for elem_type in conflicted_node[2].elements:
                for elem_name in conflicted_node[2].elements[elem_type]:
                    elem_data = conflicted_node[2].elements[elem_type][elem_name]
            
            # Find the original stem_pair key from the conflict
            conflict_key = None
            for key, cfg in STEM_CONFLICTS.items():
                if set(key.split("-")) == set(required_stems):
                    conflict_key = key
                    break
            
            # Order nodes to match the pattern order
            if conflict_key:
                pattern_stems = conflict_key.split("-")
                if pattern_stems[0] == conflictor_stem:
                    ordered_nodes = [conflictor_node[1], conflicted_node[1]]
                elif pattern_stems[0] == conflicted_stem:
                    ordered_nodes = [conflicted_node[1], conflictor_node[1]]
                else:
                    # Fallback to original order
                    ordered_nodes = [conflictor_node[1], conflicted_node[1]]
            else:
                ordered_nodes = [conflictor_node[1], conflicted_node[1]]
            
            interaction_log.append({
                "type": "STEM_CONFLICT",
                "pattern": conflict_key or "-".join(sorted(required_stems)),
                "nodes": ordered_nodes,  # Nodes ordered to match pattern
                "controller": {"node": conflictor_node[1], "stem": conflictor_stem, "damage": round(actual_controller_damage, 1)},
                "victim": {"node": conflicted_node[1], "stem": conflicted_stem, "damage": round(actual_victim_damage, 1)},
                "positions": positions,
                "distance": distance_key,
                "proportional_scaling": actual_victim_damage < victim_damage  # Flag if victim was capped
            })
    
    # 3. Non-adjacent HS Combinations (only if nodes not yet marked)
    for is_adjacent, combo_data in hs_combinations_queue:
        if not is_adjacent:  # Non-adjacent
            nodes_affected = combo_data["nodes"]
            
            # Process the non-adjacent combination
            affected_ids = combo_data["node_ids"]
            stems_involved = combo_data["stems"]
            config = combo_data["config"]  # Full configuration dictionary
            required_stems = combo_data["required_stems"]
            positions = combo_data["positions"]
            
            # Create structured interaction_id
            stems_str = "-".join(sorted(stems_involved))
            nodes_str = "-".join(sorted(affected_ids))
            interaction_id = f"HS_COMBINATION_{stems_str}_{nodes_str}"
            
            # Get transformation requirements from config
            transform_to_stem = config.get("transform_to", "")
            transform_requirement = config.get("transformation_requirement", {})
            required_element = transform_requirement.get("element", "")
            
            # Check if transformation is supported by any earthly branch (including luck pillars and talismans)
            earthly_branch_elements = set()
            for pos in position_codes:
                eb_id = f"eb_{pos}"
                if eb_id in nodes:
                    eb_value = nodes[eb_id].value
                    if eb_value in EARTHLY_BRANCHES:
                        earthly_branch_elements.add(EARTHLY_BRANCHES[eb_value]["element"])
            
            transforming_element_exists = required_element in earthly_branch_elements
            
            # Use tuple-based scoring from config
            scoring_dict = config.get("scoring", {})
            
            # Calculate distance for logging and scoring
            from library import get_distance_key
            distance_key = get_distance_key(affected_ids[0], affected_ids[1])
            
            # Determine transformation key
            transformation_key = "transformed" if transforming_element_exists else "combined"
            
            # Get score from the scoring dictionary
            total_score = scoring_dict.get(transformation_key, {}).get(distance_key, 15)  # Default to 15 if not found
            
            for node in nodes_affected:
                # For HS Combinations: Add qi of the transformed element (same logic as adjacent)
                if transform_to_stem and transform_to_stem in HEAVENLY_STEMS:
                    trans_element = HEAVENLY_STEMS[transform_to_stem]["element"]
                    
                    # Find both Yang and Yin stems for this element
                    yang_stem = None
                    yin_stem = None
                    for stem_name, stem_data in HEAVENLY_STEMS.items():
                        if stem_data["element"] == trans_element:
                            if stem_data["polarity"] == "Yang":
                                yang_stem = stem_name
                            else:
                                yin_stem = stem_name
                    
                    # Add qi for the polarity matching the node's original stem
                    node_polarity = HEAVENLY_STEMS[node.value]["polarity"] if node.value in HEAVENLY_STEMS else "Yang"
                    
                    # Determine which stem to use based on node's polarity
                    if node_polarity == "Yang" and yang_stem:
                        trans_stem = yang_stem
                    elif node_polarity == "Yin" and yin_stem:
                        trans_stem = yin_stem
                    else:
                        trans_stem = transform_to_stem  # Fallback to config stem
                    
                    trans_polarity = HEAVENLY_STEMS[trans_stem]["polarity"]
                    trans_element_key = f"{trans_polarity} {trans_element}"
                    
                    # Add transformed element qi WITHOUT clearing existing qi
                    if trans_element_key not in node.elements:
                        node.elements[trans_element_key] = {"score": 0}
                    node.elements[trans_element_key]["score"] += total_score
                    
                    # Track this combination as a badge
                    # HS combinations: "transformation" if transformed, "combination" if not
                    badge_type = "transformation" if transforming_element_exists else "combination"
                    badge_size = "lg" if transforming_element_exists else "xs"
                    badge_data = {
                        "interaction_id": interaction_id,
                        "type": badge_type,
                        "badge": trans_stem,
                        "size": badge_size
                    }
                    node.badges.append(badge_data)
                
                node.marked = True
                
                interaction_desc = f"HS Combination → {required_element} (score: {total_score})"
                if not transforming_element_exists:
                    interaction_desc += " [No transformation]"
                node.interactions.append(interaction_desc)
            
            # Log the interaction
            interaction_log.append({
                "interaction_id": interaction_id,
                "type": "STEM_COMBINATION",
                "element": required_element,
                "transform_to": transform_to_stem,
                "nodes": affected_ids,
                "positions": positions,
                "stems": stems_involved,
                "transformation": transforming_element_exists,
                "transforming_element_exists": transforming_element_exists,
                "score": total_score,
                "distance": distance_key,
                "boost": f"+{total_score:.0f} points",
                "description": f"{' + '.join(required_stems)} → {required_element}" + (" [Transformed]" if transforming_element_exists else " [Boost only]")
            })
            
    
    # 4. Non-adjacent HS Conflicts (only if nodes not yet marked)
    for is_adjacent, conflict_data in hs_conflicts_queue:
        if not is_adjacent:  # Non-adjacent
            conflictor_node = conflict_data["conflictor"]
            conflicted_node = conflict_data["conflicted"]
            
            conflictor_id = conflictor_node[2].node_id
            conflicted_id = conflicted_node[2].node_id
            
            positions = conflict_data["positions"]
            conflictor_stem = conflict_data["conflictor_stem"]
            conflicted_stem = conflict_data["conflicted_stem"]
            required_stems = conflict_data["required_stems"]
            
            # Find the conflict pattern to get scoring
            conflict_key = None
            for key, cfg in STEM_CONFLICTS.items():
                if set(key.split("-")) == set(required_stems):
                    conflict_key = key
                    break
            
            scoring = STEM_CONFLICTS[conflict_key]["scoring"] if conflict_key else {}
            
            # Calculate distance for logging and scoring
            from library import get_distance_key
            distance_key = get_distance_key(conflictor_id, conflicted_id)
            
            # Use new asymmetric scoring structure with distance decay
            victim_damage = scoring.get("victim", {}).get(distance_key, scoring.get("victim", {}).get("1", 22))  # Fallback to "1" then 22
            controller_damage = scoring.get("controller", {}).get(distance_key, scoring.get("controller", {}).get("1", 13))  # Fallback to "1" then 13
            
            # Apply victim damage first with minimum qi protection
            actual_victim_damage = conflicted_node[2].reduce_by_amount_with_minimum(victim_damage, minimum_qi=1.0)
            conflicted_node[2].interactions.append(f"HS Conflict (victim) -{actual_victim_damage:.1f} damage")
            conflicted_node[2].marked = True
            
            # Scale controller damage proportionally if victim couldn't take full damage
            if actual_victim_damage < victim_damage:
                # Victim was capped - controller only spends proportional energy
                controller_damage = controller_damage * (actual_victim_damage / victim_damage)
            
            # Apply controller damage
            actual_controller_damage = conflictor_node[2].reduce_by_amount_with_minimum(controller_damage, minimum_qi=1.0)
            conflictor_node[2].interactions.append(f"HS Conflict (controller) -{actual_controller_damage:.1f} energy spent")
            conflictor_node[2].marked = True
            
            # Create interaction ID and badges
            interaction_id = f"STEM_CONFLICT~{conflictor_stem}-{conflicted_stem}~{conflictor_id}-{conflicted_id}"
            badge_size = reduction_to_badge_size(actual_victim_damage)
            
            # Add negation badge to BOTH nodes with neutral icon
            badge_data_victim = {
                "interaction_id": interaction_id,
                "type": "stem_conflict",
                "badge": "KE",  # Icon identifier (剋/克 = control/restrain)
                "size": badge_size
            }
            conflicted_node[2].badges.append(badge_data_victim)
            
            badge_data_controller = {
                "interaction_id": interaction_id,
                "type": "stem_conflict",
                "badge": "KE",  # Icon identifier (剋/克 = control/restrain)
                "size": badge_size
            }
            conflictor_node[2].badges.append(badge_data_controller)
            
            # Reduce count for conflicted element
            conflicted_count_reduction = scoring.get("conflicted_count_reduction", 0.5)
            for elem_type in conflicted_node[2].elements:
                for elem_name in conflicted_node[2].elements[elem_type]:
                    elem_data = conflicted_node[2].elements[elem_type][elem_name]
            
            # Find the original stem_pair key from the conflict
            conflict_key = None
            for key, cfg in STEM_CONFLICTS.items():
                if set(key.split("-")) == set(required_stems):
                    conflict_key = key
                    break
            
            # Order nodes to match the pattern order
            if conflict_key:
                pattern_stems = conflict_key.split("-")
                if pattern_stems[0] == conflictor_stem:
                    ordered_nodes = [conflictor_node[1], conflicted_node[1]]
                elif pattern_stems[0] == conflicted_stem:
                    ordered_nodes = [conflicted_node[1], conflictor_node[1]]
                else:
                    # Fallback to original order
                    ordered_nodes = [conflictor_node[1], conflicted_node[1]]
            else:
                ordered_nodes = [conflictor_node[1], conflicted_node[1]]
            
            interaction_log.append({
                "type": "STEM_CONFLICT",
                "pattern": conflict_key or "-".join(sorted(required_stems)),
                "nodes": ordered_nodes,  # Nodes ordered to match pattern
                "controller": {"node": conflictor_node[1], "stem": conflictor_stem, "damage": round(actual_controller_damage, 1)},
                "victim": {"node": conflicted_node[1], "stem": conflicted_stem, "damage": round(actual_victim_damage, 1)},
                "positions": positions,
                "distance": distance_key,
                "proportional_scaling": actual_victim_damage < victim_damage  # Flag if victim was capped
            })
    
    # ============= CASCADING TRANSFORMATION RE-CHECK =============
    #
    # CRITICAL: Combinations can enable other combinations in cascading fashion:
    # Example: Ding-Ren (HS) transforms to Wood → enables Yin-Hai (EB) to transform
    # 
    # Solution: Re-check combinations until stable (2 consecutive passes with 0 new transformations)
    # 
    # Strategy: Track which interactions were TRANSFORMED (not just detected). Re-check
    # interactions that were only "detected" to see if they can NOW transform.
    # ========================================================================
    
    # Track which interaction IDs were already TRANSFORMED (not just detected)
    transformed_interaction_ids = {
        entry.get("interaction_id") 
        for entry in interaction_log 
        if entry.get("transformation") == True
    }
    
    consecutive_zero_passes = 0
    pass_num = 0
    
    while consecutive_zero_passes < 2:
        pass_num += 1
        new_transformations_count = 0
        pass_interaction_ids = set()  # Track new interactions this pass
        
        # Re-check EB combinations against current HS elements
        # (Similar logic to original processing, but checking transformation eligibility)
        
        # Get current HS elements (for EB transformation checks)
        # CRITICAL: Check ACTUAL elements in the node (including transformed qi), not just base value
        heavenly_stems_elements = set()
        # Check ALL HS nodes including talismans
        for pos in position_codes:
            hs_id = f"hs_{pos}"
            if hs_id in nodes:
                node = nodes[hs_id]
                # Check all elements in the node's qi (including transformed elements)
                for elem_key in node.elements.keys():
                    if node.elements[elem_key]["score"] > 0:
                        # Extract base element (remove Yang/Yin polarity)
                        base_elem = elem_key.replace("Yang ", "").replace("Yin ", "")
                        heavenly_stems_elements.add(base_elem)
        
        print(f"[CASCADING PASS {pass_num}] Current HS elements detected: {heavenly_stems_elements}")
        
        # Get current EB elements (for HS transformation checks)
        earthly_branch_elements = set()
        # Check ALL EB nodes including talismans
        for pos in position_codes:
            eb_id = f"eb_{pos}"
            if eb_id in nodes:
                eb_value = nodes[eb_id].value
                if eb_value in EARTHLY_BRANCHES:
                    earthly_branch_elements.add(EARTHLY_BRANCHES[eb_value]["element"])
        
        # Re-check THREE_MEETINGS for transformation eligibility
        branch_data = get_branch_nodes()
        
        for direction, config in THREE_MEETINGS.items():
            required_branches = config["branches"]
            element = config["element"]
            
            matching = [(pos, nid, node) for pos, nid, node in branch_data 
                       if node.value in required_branches]
            
            if len(matching) >= 3:
                found_branches = [node.value for _, _, node in matching]
                if set(found_branches) >= set(required_branches):
                    # Build mapping from branch value to node data
                    branch_to_data = {}
                    for pos, nid, node in matching:
                        if node.value not in branch_to_data:
                            branch_to_data[node.value] = (pos, nid, node)
                    
                    # Order nodes to match library order
                    ordered_selected = []
                    for req_branch in required_branches:
                        if req_branch in branch_to_data:
                            ordered_selected.append(branch_to_data[req_branch])
                    
                    if len(ordered_selected) >= 3:
                        positions = [pos for pos, _, _ in ordered_selected]
                        affected_nodes = [node for _, _, node in ordered_selected]
                        affected_ids = [nid for _, nid, _ in ordered_selected]
                        
                        # Create interaction ID using library order pattern
                        pattern_key = "-".join(required_branches)
                        interaction_id = f"THREE_MEETINGS~{pattern_key}~{'-'.join(affected_ids)}"
                        
                        # Skip if already TRANSFORMED in initial pass or previous re-check pass
                        if interaction_id in transformed_interaction_ids or interaction_id in pass_interaction_ids:
                            continue
                        
                        # Check if transformation requirement is NOW met
                        can_transform_now = element in heavenly_stems_elements
                        
                        # Only process if it can transform NOW (cascading transformation)
                        if can_transform_now:
                            # Find existing interaction in log (should exist from initial pass)
                            existing_interaction = None
                            for entry in interaction_log:
                                if (entry.get("type") == "THREE_MEETINGS" and 
                                    entry.get("pattern") == pattern_key and 
                                    set(entry.get("nodes", [])) == set(affected_ids)):
                                    existing_interaction = entry
                                    break
                            
                            # If exists and was NOT transformed, upgrade it
                            if existing_interaction and not existing_interaction.get("transformed", False):
                                # Calculate new scoring for transformed state
                                scoring_dict = config.get("scoring", {})
                                distance_key = get_distance_key_3nodes(affected_ids[0], affected_ids[1], affected_ids[2])
                                
                                transformation_key = "transformed"
                                combined_key = "combined"
                                transformed_score = scoring_dict.get(transformation_key, {}).get(distance_key, 70)
                                combined_score = scoring_dict.get(combined_key, {}).get(distance_key, 25)
                                
                                # Calculate additional score (transformed_score - combined_score)
                                additional_score = transformed_score - combined_score
                                
                                # Apply ADDITIONAL transformation to nodes (without adding duplicate badges)
                                for node in affected_nodes:
                                    node.transformed = True
                                    
                                    # Add the additional element qi directly (without calling transform_to_element)
                                    node_polarity = None
                                    if node.node_type == "branch" and node.value in EARTHLY_BRANCHES:
                                        node_polarity = EARTHLY_BRANCHES[node.value]["polarity"]
                                    
                                    if node_polarity:
                                        stem_to_add = ELEMENT_POLARITY_STEMS.get((element, node_polarity))
                                        if stem_to_add and stem_to_add in HEAVENLY_STEMS:
                                            stem_element = HEAVENLY_STEMS[stem_to_add]["element"]
                                            stem_polarity = HEAVENLY_STEMS[stem_to_add]["polarity"]
                                            element_key = f"{stem_polarity} {stem_element}"
                                            
                                            if element_key not in node.elements:
                                                node.elements[element_key] = {"score": 0}
                                            node.elements[element_key]["score"] += additional_score
                                    
                                    # Update existing badges from "combination" to "transformation"
                                    for badge in node.badges:
                                        if badge.get("interaction_id") == interaction_id and badge.get("type") == "combination":
                                            badge["type"] = "transformation"
                                            # Upgrade badge size from weak to normal strength
                                            badge["size"] = "lg"  # THREE_MEETINGS is strong
                                    
                                    # Update interactions list
                                    node.interactions = [
                                        i for i in node.interactions 
                                        if not (f"Three Meetings" in i and element in i and pattern_key in str(i))
                                    ]
                                    node.interactions.append(f"Three Meetings → {element} (cascading)")
                                
                                # UPGRADE existing interaction (no duplicate!)
                                existing_interaction["transformed"] = True
                                existing_interaction["points"] = f"+{transformed_score} points"
                                existing_interaction["distance"] = distance_key
                                existing_interaction["cascading"] = True
                                if "reason" in existing_interaction:
                                    del existing_interaction["reason"]
                                
                                pass_interaction_ids.add(interaction_id)
                                new_transformations_count += 1
        
        # Re-check SIX_HARMONIES for transformation eligibility
        # (This is the specific case mentioned: Yin-Hai needs Wood in HS)
        branch_data = get_branch_nodes()
        
        for pair, config in SIX_HARMONIES.items():
            required_branches = pair.split("-")
            element = config["element"]
            
            matching = [(pos, nid, node) for pos, nid, node in branch_data 
                       if node.value in required_branches]
            
            if len(matching) >= 2:
                found_branches = [node.value for _, _, node in matching]
                if set(found_branches) >= set(required_branches):
                    # Find all possible pairs
                    branch1_nodes = [(pos, nid, node) for pos, nid, node in matching 
                                    if node.value == required_branches[0]]
                    branch2_nodes = [(pos, nid, node) for pos, nid, node in matching 
                                    if node.value == required_branches[1]]
                    
                    for b1 in branch1_nodes:
                        for b2 in branch2_nodes:
                            if b1[1] != b2[1]:
                                positions = [b1[0], b2[0]]
                                affected_nodes = [b1[2], b2[2]]
                                affected_ids = [b1[1], b2[1]]
                                
                                # Create interaction ID (MUST match initial pass format - NO sorting!)
                                interaction_id = f"SIX_HARMONIES~{pair}~{'-'.join(affected_ids)}"
                                
                                # Skip if already TRANSFORMED in initial pass or previous re-check pass
                                if interaction_id in transformed_interaction_ids or interaction_id in pass_interaction_ids:
                                    continue
                                
                                # Check if transformation requirement is NOW met
                                can_transform_now = element in heavenly_stems_elements
                                
                                # Only process if it can transform NOW (cascading transformation)
                                if can_transform_now:
                                    # Find existing interaction in log (should exist from initial pass)
                                    existing_interaction = None
                                    for entry in interaction_log:
                                        if (entry.get("type") == "SIX_HARMONIES" and 
                                            entry.get("pattern") == pair and 
                                            set(entry.get("nodes", [])) == set(affected_ids)):
                                            existing_interaction = entry
                                            break
                                    
                                    # If exists and was NOT transformed, upgrade it
                                    if existing_interaction and not existing_interaction.get("transformed", False):
                                        # Calculate new scoring for transformed state
                                        scoring_dict = config.get("scoring", {})
                                        from library import get_distance_key
                                        distance_key = get_distance_key(affected_ids[0], affected_ids[1])
                                        
                                        transformation_key = "transformed"
                                        combined_key = "combined"
                                        transformed_score = scoring_dict.get(transformation_key, {}).get(distance_key, 50)
                                        combined_score = scoring_dict.get(combined_key, {}).get(distance_key, 14)
                                        
                                        # Calculate additional score (transformed_score - combined_score)
                                        additional_score = transformed_score - combined_score
                                        
                                        # Apply ADDITIONAL transformation to nodes
                                        for node in affected_nodes:
                                            # Add the additional score (not full transformed score)
                                            node.add_element(element, additional_score)
                                            node.transformed = True
                                            
                                            # Update existing badge from "combination" to "transformation"
                                            for badge in node.badges:
                                                if badge.get("interaction_id") == interaction_id and badge.get("type") == "combination":
                                                    badge["type"] = "transformation"
                                            
                                            # Update interactions list (remove old, add new)
                                            node.interactions = [
                                                i for i in node.interactions 
                                                if not (f"Six Harmonies" in i and element in i and pair in str(node.value))
                                            ]
                                            node.interactions.append(f"Six Harmonies → {element} (cascading)")
                                        
                                        # UPGRADE existing interaction (no duplicate!)
                                        existing_interaction["transformed"] = True
                                        existing_interaction["boost"] = f"+{transformed_score:.0f} points"
                                        existing_interaction["distance"] = distance_key
                                        existing_interaction["cascading"] = True
                                        if "reason" in existing_interaction:
                                            del existing_interaction["reason"]
                                        
                                        pass_interaction_ids.add(interaction_id)
                                        new_transformations_count += 1
        
        # Update transformed IDs
        transformed_interaction_ids.update(pass_interaction_ids)
        
        # Update consecutive zero counter
        if new_transformations_count == 0:
            consecutive_zero_passes += 1
        else:
            consecutive_zero_passes = 0
    
    # ============= ELEMENT CALCULATION HELPER FUNCTIONS =============
    
    def calculate_five_element_totals(nodes_dict):
        """Calculate combined Yin+Yang totals for 5 elements"""
        five_elements = ["Wood", "Fire", "Earth", "Metal", "Water"]
        element_totals = {elem: {"score": 0} for elem in five_elements}
        
        for node in nodes_dict.values():
            for elem_key, elem_data in node.elements.items():
                # Extract base element (remove polarity)
                base_elem = elem_key.replace("Yang ", "").replace("Yin ", "")
                if base_elem in five_elements:
                    element_totals[base_elem]["score"] += elem_data["score"]
        
        # Convert to integers and round counts
        for elem in element_totals:
            element_totals[elem]["score"] = int(element_totals[elem]["score"])
        
        return element_totals
    
    def calculate_ten_element_totals(nodes_dict):
        """Calculate totals for all 10 Heavenly Stems"""
        # Map from element+polarity to Heavenly Stem ID
        element_to_stem = {
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
        
        # Initialize all 10 stems with 0
        ten_elements = {stem: 0 for stem in element_to_stem.values()}
        
        # Sum up from all nodes
        for node in nodes_dict.values():
            for elem_key, elem_data in node.elements.items():
                if elem_key in element_to_stem:
                    stem_id = element_to_stem[elem_key]
                    ten_elements[stem_id] += elem_data["score"]
        
        # Convert to integers
        for stem_id in ten_elements:
            ten_elements[stem_id] = int(ten_elements[stem_id])
        
        return ten_elements
    
    # ============= CAPTURE POST-INTERACTION SCORES =============
    
    # Get element totals after interactions but before seasonal adjustment
    post_interaction_five_elements = calculate_five_element_totals(nodes)
    post_interaction_ten_elements = calculate_ten_element_totals(nodes)
    
    # ============= APPLY SEASONAL ADJUSTMENT TO ALL NODES =============
    
    def apply_seasonal_adjustment(nodes_dict, month_branch):
        """
        Apply seasonal adjustment to all nodes based on month branch.
        Uses 旺相休囚死 (Wàng Xiāng Xiū Qiú Sǐ) five-phase cycle.
        """
        if not month_branch or month_branch not in BRANCH_TO_SEASON:
            return  # No adjustment if no valid month branch
        
        # Track adjustment details for logging
        adjustment_details = []
        
        for node_id, node in nodes_dict.items():
            node_adjustments = {}
            
            # Apply adjustment to each element in the node
            for elem_key, elem_data in node.elements.items():
                if elem_data["score"] > 0:
                    # Extract base element (remove polarity)
                    base_elem = elem_key.replace("Yang ", "").replace("Yin ", "")
                    
                    # Find the seasonal state for this element based on month branch
                    if base_elem in SEASONAL_STRENGTH:
                        multiplier = 1.0  # Default no adjustment
                        for state, branches in SEASONAL_STRENGTH[base_elem].items():
                            if month_branch in branches:
                                state_key = state.lower()
                                multiplier = SEASONAL_ADJUSTMENT.get(state_key, 1.0)
                                break
                        
                        old_score = elem_data["score"]
                        new_score = old_score * multiplier
                        elem_data["score"] = new_score
                        
                        # Track significant adjustments
                        if multiplier != 1.0:
                            node_adjustments[elem_key] = {
                                "old": int(old_score),
                                "new": int(new_score),
                                "multiplier": multiplier
                            }
            
            if node_adjustments:
                adjustment_details.append({
                    "node": node_id,
                    "value": node.value,
                    "adjustments": node_adjustments
                })
        
        # Add seasonal adjustment to interaction log
        if adjustment_details:
            season = BRANCH_TO_SEASON.get(month_branch, "Unknown")
            interaction_log.append({
                "type": "SEASONAL_ADJUSTMENT",
                "season": season,
                "month_branch": month_branch,
                "adjustments": adjustment_details,
                "description": f"Applied {season} seasonal modifiers (旺相休囚死)"
            })
    
    # Apply seasonal adjustment after all interactions
    apply_seasonal_adjustment(nodes, month_branch)
    
    # ============= NATURAL WUXING INTERACTIONS (自然五行相生相剋) =============
    # Apply natural element interactions within pillars (vertical HS-EB relationships)
    # Energy transfer model: generating source loses energy, controlling both lose energy
    
    def apply_natural_interactions():
        """Apply WuXing energy transfer relationships between adjacent nodes"""
        natural_log = []
        interaction_pairs = set()  # Track which pairs have already interacted
        
        # Define adjacency relationships for each node
        adjacencies = {
            "hs_y": ["hs_m", "eb_y"],        # HS Year can interact with HS Month and EB Year
            "hs_m": ["hs_y", "hs_d", "eb_m"], # HS Month can interact with HS Year, HS Day, EB Month
            "hs_d": ["hs_m", "hs_h", "eb_d"], # HS Day can interact with HS Month, HS Hour, EB Day
            "hs_h": ["hs_d", "eb_h"],        # HS Hour can interact with HS Day and EB Hour
            "eb_y": ["eb_m", "hs_y"],        # EB Year can interact with EB Month and HS Year
            "eb_m": ["eb_y", "eb_d", "hs_m"], # EB Month can interact with EB Year, EB Day, HS Month
            "eb_d": ["eb_m", "eb_h", "hs_d"], # EB Day can interact with EB Month, EB Hour, HS Day
            "eb_h": ["eb_d", "hs_h"],        # EB Hour can interact with EB Day and HS Hour
        }
        
        # Process nodes in order, each can interact multiple times (once per adjacent node)
        node_order = ["hs_y", "hs_m", "hs_d", "hs_h", "eb_y", "eb_m", "eb_d", "eb_h"]
        
        for source_id in node_order:
            if source_id not in nodes:
                continue  # Skip if doesn't exist
                
            source_node = nodes[source_id]
            source_element = source_node.get_dominant_element()
            
            if not source_element:
                continue
            
            # Try to interact with each adjacent node
            for target_id in adjacencies.get(source_id, []):
                if target_id not in nodes:
                    continue  # Skip if doesn't exist
                
                # Create a normalized pair key to avoid duplicate interactions
                pair_key = tuple(sorted([source_id, target_id]))
                if pair_key in interaction_pairs:
                    continue  # This pair has already interacted
                    
                target_node = nodes[target_id]
                target_element = target_node.get_dominant_element()
                
                if not target_element:
                    continue
                
                # Check for WuXing relationships between these elements
                interaction_found = False
                
                # GENERATING RELATIONSHIP: Source generates target
                if WUXING_ENERGY_FLOW["generation"].get(source_element) == target_element:
                    generator_loss = WUXING_ENERGY_FLOW["scoring"]["generating"]["generator_loss"]
                    target_gain = WUXING_ENERGY_FLOW["scoring"]["generating"]["receiver_gain"]
                    
                    # Source loses energy by generating
                    reduce_element_score(source_node, source_element, generator_loss)
                    source_node.interactions.append(f"Natural Gen: -{generator_loss}pts generating {target_element}")
                    
                    # Target gains energy - use PRIMARY QI polarity for branches
                    target_polarity = None
                    if target_node.node_type == "branch":
                        target_polarity = get_primary_qi_polarity(target_node.value)
                    target_node.add_element(target_element, target_gain, polarity=target_polarity)
                    target_node.interactions.append(f"Natural Gen: +{target_gain}pts from {source_element}")
                    
                    natural_log.append({
                        "type": "ENERGY_FLOW_GENERATING",
                        "pattern": f"{source_element}→{target_element}",
                        "source": source_id,
                        "target": target_id,
                        "source_element": source_element,
                        "target_element": target_element,
                        "effect": f"{source_element} -{generator_loss}, {target_element} +{target_gain}",
                        "relationship": f"{source_element} generates {target_element}",
                        "description": f"{source_id} exhausts itself generating energy for {target_id}"
                    })
                    interaction_found = True
                
                # Target generates source
                elif WUXING_ENERGY_FLOW["generation"].get(target_element) == source_element:
                    generator_loss = WUXING_ENERGY_FLOW["scoring"]["generating"]["generator_loss"]
                    target_gain = WUXING_ENERGY_FLOW["scoring"]["generating"]["receiver_gain"]
                    
                    # Target loses energy by generating
                    reduce_element_score(target_node, target_element, generator_loss)
                    target_node.interactions.append(f"Natural Gen: -{generator_loss}pts generating {source_element}")
                    
                    # Source gains energy - use PRIMARY QI polarity for branches
                    source_polarity = None
                    if source_node.node_type == "branch":
                        source_polarity = get_primary_qi_polarity(source_node.value)
                    source_node.add_element(source_element, target_gain, polarity=source_polarity)
                    source_node.interactions.append(f"Natural Gen: +{target_gain}pts from {target_element}")
                    
                    natural_log.append({
                        "type": "ENERGY_FLOW_GENERATING",
                        "pattern": f"{target_element}→{source_element}",
                        "source": target_id,
                        "target": source_id,
                        "source_element": target_element,
                        "target_element": source_element,
                        "effect": f"{target_element} -{generator_loss}, {source_element} +{target_gain}",
                        "relationship": f"{target_element} generates {source_element}",
                        "description": f"{target_id} exhausts itself generating energy for {source_id}"
                    })
                    interaction_found = True
                
                # CONTROLLING RELATIONSHIP: Source controls target
                elif WUXING_ENERGY_FLOW["control"].get(source_element) == target_element:
                    controller_loss = WUXING_ENERGY_FLOW["scoring"]["controlling"]["controller_loss"]
                    controlled_loss = WUXING_ENERGY_FLOW["scoring"]["controlling"]["controlled_loss"]
                    
                    # Source (controller) loses some energy
                    reduce_element_score(source_node, source_element, controller_loss)
                    source_node.interactions.append(f"Natural Control: -{controller_loss}pts controlling {target_element}")
                    
                    # Target (controlled) loses more energy
                    reduce_element_score(target_node, target_element, controlled_loss)
                    target_node.interactions.append(f"Natural Control: -{controlled_loss}pts controlled by {source_element}")
                    
                    natural_log.append({
                        "type": "ENERGY_FLOW_CONTROLLING",
                        "pattern": f"{source_element}⊗{target_element}",
                        "source": source_id,
                        "target": target_id,
                        "source_element": source_element,
                        "target_element": target_element,
                        "effect": f"{source_element} -{controller_loss}, {target_element} -{controlled_loss}",
                        "relationship": f"{source_element} controls {target_element}",
                        "description": f"{source_id} uses energy (-{controller_loss}) to control {target_id} (-{controlled_loss})"
                    })
                    interaction_found = True
                
                # Target controls source
                elif WUXING_ENERGY_FLOW["control"].get(target_element) == source_element:
                    controller_loss = WUXING_ENERGY_FLOW["scoring"]["controlling"]["controller_loss"]
                    controlled_loss = WUXING_ENERGY_FLOW["scoring"]["controlling"]["controlled_loss"]
                    
                    # Target (controller) loses less energy
                    reduce_element_score(target_node, target_element, controller_loss)
                    target_node.interactions.append(f"Natural Control: -{controller_loss}pts controlling {source_element}")
                    
                    # Source (controlled) loses more energy
                    reduce_element_score(source_node, source_element, controlled_loss)
                    source_node.interactions.append(f"Natural Control: -{controlled_loss}pts controlled by {target_element}")
                    
                    natural_log.append({
                        "type": "ENERGY_FLOW_CONTROLLING",
                        "pattern": f"{target_element}⊗{source_element}",
                        "source": target_id,
                        "target": source_id,
                        "source_element": target_element,
                        "target_element": source_element,
                        "effect": f"{target_element} -{controller_loss}, {source_element} -{controlled_loss}",
                        "relationship": f"{target_element} controls {source_element}",
                        "description": f"{target_id} uses energy (-{controller_loss}) to control {source_id} (-{controlled_loss})"
                    })
                    interaction_found = True
                
                # If interaction found, mark this pair as processed
                if interaction_found:
                    interaction_pairs.add(pair_key)
        
        return natural_log
    
    def reduce_element_score(node, element, amount):
        """Helper function to reduce element score in a node"""
        # Reduce both Yin and Yang variants of the element
        for polarity in ["Yang", "Yin"]:
            elem_key = f"{polarity} {element}"
            if elem_key in node.elements:
                node.elements[elem_key]["score"] = max(0, node.elements[elem_key]["score"] - amount/2)
    
    # Apply natural interactions and log them
    natural_interaction_log = apply_natural_interactions()
    interaction_log.extend(natural_interaction_log)
    
    # Add summary entry for natural interactions
    if natural_interaction_log:
        interaction_log.append({
            "type": "ENERGY_FLOW",
            "summary": f"Applied {len(natural_interaction_log)} natural WuXing interactions",
            "details": {
                "generating": len([x for x in natural_interaction_log if "GENERATING" in x["type"]]),
                "controlling": len([x for x in natural_interaction_log if "CONTROLLING" in x["type"]]),
                "exhausting": len([x for x in natural_interaction_log if "EXHAUSTING" in x["type"]])
            }
        })
    
    # ============= DETAILED ELEMENT BREAKDOWN BY NODE =============
    
    # Build element contribution table showing each node's contribution
    element_breakdown = {}
    all_elements = ["Yang Wood", "Yin Wood", "Yang Fire", "Yin Fire", 
                   "Yang Earth", "Yin Earth", "Yang Metal", "Yin Metal",
                   "Yang Water", "Yin Water"]
    
    # Initialize structure
    for elem in all_elements:
        element_breakdown[elem] = {
            "nodes": {},  # Contribution from each node
            "total": 0    # Sum of all nodes
        }
    
    # Fill in contributions from each node
    for node_id, node in nodes.items():
        for elem_key, elem_data in node.elements.items():
            if elem_key in element_breakdown and elem_data["score"] > 0:
                element_breakdown[elem_key]["nodes"][node_id] = int(elem_data["score"])
                element_breakdown[elem_key]["total"] += elem_data["score"]
    
    # Convert totals to integers
    for elem in element_breakdown:
        element_breakdown[elem]["total"] = int(element_breakdown[elem]["total"])
    
    pillar_structure = {}
    
    # Map position codes back to pillar keys for reconstruction
    pos_to_pillar = {
        "y": "year_pillar",
        "m": "month_pillar", 
        "d": "day_pillar",
        "h": "hour_pillar",
        "10yl": "luck_10_year_pillar",
        "yl": "yearly_luck_pillar"
    }
    
    for pos in position_codes:
        pillar_key = pos_to_pillar.get(pos)
        if not pillar_key:
            continue
        idx = position_to_index.get(pos, 0)
        hs_id = f"hs_{pos}"
        eb_id = f"eb_{pos}"
        
        # Create pillar structure showing both stem and branch
        pillar_structure[pillar_key] = {
            "stem": {},
            "branch": {}
        }
        
        # Add stem info to pillar structure
        if hs_id in nodes:
            hs_node = nodes[hs_id]
            pillar_structure[pillar_key]["stem"] = {
                "value": hs_node.value,
                "elements": {k: {"score": int(v["score"])} for k, v in hs_node.elements.items() if v["score"] > 0}
            }
        
        # Add branch info to pillar structure
        if eb_id in nodes:
            eb_node = nodes[eb_id]
            pillar_structure[pillar_key]["branch"] = {
                "value": eb_node.value,
                "elements": {k: {"score": int(v["score"])} for k, v in eb_node.elements.items() if v["score"] > 0},
                "transformed": bool(eb_node.badges),
                "transformation_element": eb_node.transformation_element if eb_node.badges else None
            }
    
    
    # ============= CALCULATE 2-TIER ELEMENT SCORES =============
    # Purpose: Separate natal destiny (birth chart only) vs. full chart (everything)
    
    # Define natal node IDs (core birth chart - 6 or 8 nodes depending on birth_time)
    natal_node_ids = {'hs_y', 'eb_y', 'hs_m', 'eb_m', 'hs_d', 'eb_d', 'hs_h', 'eb_h'}
    
    # 1. BASE: Only natal nodes, before interactions (pure birth destiny)
    base_nodes = {}
    for node_id in natal_node_ids:
        if node_id in nodes:
            node = nodes[node_id]
            base_nodes[node_id] = ElementNode(node_id, node.value, node.node_type)
    
    base_five_elements = calculate_five_element_totals(base_nodes)
    base_ten_elements = calculate_ten_element_totals(base_nodes)
    
    # 2. POST: All nodes (natal + luck + talisman + location), after interactions (current situation)
    post_five_elements = calculate_five_element_totals(nodes)
    post_ten_elements = calculate_ten_element_totals(nodes)
    
    # ============= APPLY LOCATION BOOST (ONLY TO POST SCORES) =============
    def apply_location_boost(ten_elements_dict, location_type):
        """
        Add location-based element boosts (non-interactive, no node creation).
        
        Overseas (2 Water pillars: Ren-Zi + Gui-Hai):
            hs_ren: 100 Yang Water (Ren)
            eb_zi: 80 Yang Water (Ren) + 40 Yin Water (Gui) = 120 Water
            hs_gui: 100 Yin Water (Gui)
            eb_hai: 70 Yin Water (Gui) + 30 Yang Water (Ren) + 10 Yang Wood (Jia) + 10 Yang Earth (Wu)
            Total: 420 Water (210 Ren + 210 Gui), 10 Wood (Jia), 10 Earth (Wu)
        
        Birthplace (4 Earth pillars at 50%: Ji-Wei + Ji-Chou + Wu-Xu + Wu-Chen):
            hs_ji: 100 Yin Earth (Ji) * 0.5 = 50
            eb_wei: (95 Ji + 20 Ding + 10 Yi) * 0.5 = 47.5 Ji, 10 Ding, 5 Yi
            hs_ji: 100 Yin Earth (Ji) * 0.5 = 50
            eb_chou: (95 Ji + 15 Gui + 10 Xin) * 0.5 = 47.5 Ji, 7.5 Gui, 5 Xin
            hs_wu: 100 Yang Earth (Wu) * 0.5 = 50
            eb_xu: (95 Wu + 20 Xin + 10 Ding) * 0.5 = 47.5 Wu, 10 Xin, 5 Ding
            hs_wu: 100 Yang Earth (Wu) * 0.5 = 50
            eb_chen: (95 Wu + 15 Yi + 10 Gui) * 0.5 = 47.5 Wu, 7.5 Yi, 5 Gui
            Total: 390 Earth (195 Ji + 195 Wu), 15 Fire (Ding), 12.5 Wood (Yi), 12.5 Water (Gui), 15 Metal (Xin)
        """
        if location_type == "overseas":
            ten_elements_dict["Ren"] += 210  # Yang Water
            ten_elements_dict["Gui"] += 210  # Yin Water
            ten_elements_dict["Jia"] += 10   # Yang Wood (from Hai)
            ten_elements_dict["Wu"] += 10    # Yang Earth (from Hai)
        elif location_type == "birthplace":
            ten_elements_dict["Ji"] += 195    # Yin Earth
            ten_elements_dict["Wu"] += 195    # Yang Earth
            ten_elements_dict["Ding"] += 15   # Yin Fire
            ten_elements_dict["Yi"] += 12.5   # Yin Wood (will be int-converted later)
            ten_elements_dict["Gui"] += 12.5  # Yin Water (will be int-converted later)
            ten_elements_dict["Xin"] += 15    # Yin Metal
    
    # Apply location boost ONLY to post scores (current situation, not birth destiny)
    if location:
        apply_location_boost(post_ten_elements, location)
    
    # Enhanced Daymaster Analysis System
    def analyze_daymaster_strength(bazi_chart, five_elements):
        """
        Advanced Daymaster strength analysis with multi-factor assessment.
        Based on traditional BaZi principles: Resource, Companion, Output, Wealth, Officer.
        """
        
        # Get Day Master element
        day_hs = bazi_chart.get("day_pillar", "").split()[0] if "day_pillar" in bazi_chart else ""
        if day_hs not in HEAVENLY_STEMS:
            return {
                "daymaster": "Unknown",
                "strength_category": "Cannot determine",
                "chart_type": "Unknown",
                "favorable_elements": [],
                "unfavorable_elements": [],
                "useful_god": None,
                "explanation": "Day Master not found"
            }
        
        dm_element = HEAVENLY_STEMS[day_hs]["element"]
        dm_polarity = HEAVENLY_STEMS[day_hs]["polarity"]
        
        # Define Wu Xing element relationships
        element_relationships = {
            "Wood": {
                "resource": "Water",      # Water produces Wood
                "companion": "Wood",       # Same element
                "output": "Fire",          # Wood produces Fire
                "wealth": "Earth",         # Wood controls Earth
                "officer": "Metal"         # Metal controls Wood
            },
            "Fire": {
                "resource": "Wood",
                "companion": "Fire",
                "output": "Earth",
                "wealth": "Metal",
                "officer": "Water"
            },
            "Earth": {
                "resource": "Fire",
                "companion": "Earth", 
                "output": "Metal",
                "wealth": "Water",
                "officer": "Wood"
            },
            "Metal": {
                "resource": "Earth",
                "companion": "Metal",
                "output": "Water",
                "wealth": "Wood",
                "officer": "Fire"
            },
            "Water": {
                "resource": "Metal",
                "companion": "Water",
                "output": "Wood",
                "wealth": "Fire",
                "officer": "Earth"
            }
        }
        
        relationships = element_relationships[dm_element]
        
        # Calculate element scores
        dm_score = five_elements.get(dm_element, {}).get("score", 0)
        total_score = sum(e["score"] for e in five_elements.values())
        
        if total_score == 0:
            return {
                "daymaster": f"{dm_polarity} {dm_element}",
                "strength_category": "Cannot determine",
                "chart_type": "Invalid",
                "favorable_elements": [],
                "unfavorable_elements": [],
                "useful_god": None,
                "explanation": "No element scores found"
            }
        
        # Calculate scores for each element relationship
        resource_score = five_elements.get(relationships["resource"], {}).get("score", 0)
        output_score = five_elements.get(relationships["output"], {}).get("score", 0)
        wealth_score = five_elements.get(relationships["wealth"], {}).get("score", 0)
        officer_score = five_elements.get(relationships["officer"], {}).get("score", 0)
        
        # Support vs Drain calculation
        support_score = resource_score + dm_score  # Resource + Companion
        drain_score = output_score + wealth_score + officer_score
        
        support_percentage = (support_score / total_score * 100)
        drain_percentage = (drain_score / total_score * 100)
        dm_percentage = (dm_score / total_score * 100)
        
        # Check for special chart patterns
        chart_type = "Normal"
        
        # Follower Chart detection (从格) - Day Master < 10%, Support < 20%
        if dm_percentage < 10 and support_percentage < 20:
            dominant_elem = max(five_elements.items(), key=lambda x: x[1]["score"])
            if dominant_elem[1]["score"] / total_score > 0.4:
                chart_type = "Follower"
        
        # Vibrant Chart detection (旺格) - Support > 70%
        elif support_percentage > 70:
            chart_type = "Vibrant"
        
        # Determine favorable elements based on chart type
        if chart_type == "Follower":
            # Follower: Support the dominant element
            dominant = max([(relationships["output"], output_score, "Output"),
                          (relationships["wealth"], wealth_score, "Wealth"),
                          (relationships["officer"], officer_score, "Officer")],
                         key=lambda x: x[1])
            
            strength_category = "Follower (从格)"
            useful_god = dominant[0]
            favorable = [dominant[0]]
            if dominant[0] in element_relationships:
                favorable.append(element_relationships[dominant[0]]["resource"])
            unfavorable = [dm_element, relationships["resource"]]
            explanation = f"Follower Chart: Day Master surrenders to {dominant[0]} ({dominant[2]}). Support {dominant[0]}, avoid strengthening Day Master."
            
        elif chart_type == "Vibrant":
            # Vibrant: Channel excess energy
            strength_category = "Vibrant (旺格)"
            useful_god = relationships["output"]
            favorable = [relationships["output"], relationships["wealth"]]
            unfavorable = [relationships["officer"]]
            explanation = f"Vibrant Chart: Day Master self-sufficient at {support_percentage:.1f}%. Channel through Output ({relationships['output']}), avoid suppression."
            
        else:
            # Normal chart analysis
            if support_percentage >= 60:
                strength_category = "Very Strong"
                useful_god = relationships["output"]
                favorable = [relationships["output"], relationships["wealth"]]
                unfavorable = [relationships["resource"], dm_element]
                explanation = f"Day Master very strong ({support_percentage:.1f}% support). Release excess through Output ({relationships['output']}) and Wealth ({relationships['wealth']})."
                
            elif support_percentage >= 45:
                strength_category = "Strong"
                useful_god = relationships["wealth"]
                favorable = [relationships["wealth"], relationships["officer"], relationships["output"]]
                unfavorable = [relationships["resource"]]
                explanation = f"Day Master strong ({support_percentage:.1f}% support). Channel strength through Wealth ({relationships['wealth']}) and Officer ({relationships['officer']})."
                
            elif support_percentage >= 35:
                strength_category = "Balanced"
                
                # Smart analysis: Consider generation chain effects
                element_scores = {elem: data["score"] for elem, data in five_elements.items()}
                
                # Define WuXing generation relationships
                generates = {
                    "Wood": "Fire", "Fire": "Earth", "Earth": "Metal", 
                    "Metal": "Water", "Water": "Wood"
                }
                controls = {
                    "Wood": "Earth", "Earth": "Water", "Water": "Fire",
                    "Fire": "Metal", "Metal": "Wood"
                }
                
                # Find problematic elements (too strong and harmful to DM)
                problematic_elements = []
                for elem, score in element_scores.items():
                    if score > total_score * 0.3:  # More than 30% of total
                        # Check if this element harms the Day Master
                        if (elem == relationships["officer"] and score > dm_score * 1.5) or \
                           (elem == relationships["wealth"] and score > dm_score * 2.0) or \
                           (score > total_score * 0.4):  # Or simply too dominant (>40%)
                            problematic_elements.append(elem)
                
                # Smart favorable element selection
                if problematic_elements:
                    # Strategy: Control the problematic element or strengthen DM
                    primary_problem = max(problematic_elements, key=lambda x: element_scores[x])
                    
                    # Option 1: Use element that controls the problematic element
                    controller = None
                    for elem, controlled in controls.items():
                        if controlled == primary_problem and elem != primary_problem:
                            controller = elem
                            break
                    
                    # Option 2: Strengthen Day Master support (Resource)
                    resource_elem = relationships["resource"]
                    
                    # Special case: When Day Master itself is too strong
                    if primary_problem == dm_element:
                        # Use Output to drain, Officer to control, or Wealth to consume
                        useful_god = relationships["output"]  # Primary: drain excess energy
                        favorable = [relationships["output"], relationships["wealth"]]
                        unfavorable = [resource_elem]  # Avoid what feeds the Day Master
                        
                        # Also mark element that generates the Day Master as unfavorable
                        for elem, generated in generates.items():
                            if generated == dm_element and elem not in unfavorable:
                                unfavorable.append(elem)
                        
                        explanation = f"Day Master excessively strong ({dm_percentage:.1f}%). Use Output ({relationships['output']}) to drain excess energy and Wealth ({relationships['wealth']}) to consume it."
                        explanation += f" Avoid {resource_elem} which would strengthen it further."
                    
                    # Choose the better strategy for other problematic elements
                    elif controller and element_scores.get(controller, 0) < element_scores[primary_problem] * 0.3:
                        # Controller is weak enough to be effective
                        useful_god = controller
                        favorable = [controller]
                        
                        # Build comprehensive strategy based on element relationships
                        
                        # 1. Always strengthen daymaster when under attack (officer or wealth overwhelming)
                        if primary_problem == relationships["officer"] or primary_problem == relationships["wealth"]:
                            if dm_element not in favorable:
                                favorable.append(dm_element)  # Strengthen daymaster to resist
                        
                        # 2. Check what element the problem generates (that element drains the problem!)
                        drainer = generates.get(primary_problem)
                        if drainer and drainer not in favorable:
                            # Check if drainer is beneficial to daymaster
                            if drainer == resource_elem or drainer == dm_element:
                                favorable.append(drainer)
                                drain_benefit = f" {drainer} drains {primary_problem} while supporting {dm_element}."
                            elif drainer != relationships["officer"] and drainer != relationships["wealth"]:
                                # Only add if it's not harmful to daymaster
                                favorable.append(drainer)
                                drain_benefit = f" {drainer} drains {primary_problem} energy."
                            else:
                                drain_benefit = ""
                        else:
                            drain_benefit = ""
                        
                        # 3. Check for generation chains and synergies
                        synergies = []
                        for i, elem1 in enumerate(favorable):
                            for elem2 in favorable[i+1:]:
                                if generates.get(elem1) == elem2:
                                    synergies.append(f"{elem1}→{elem2}")
                                elif generates.get(elem2) == elem1:
                                    synergies.append(f"{elem2}→{elem1}")
                        
                        # Build explanation
                        explanation = f"Day Master balanced ({support_percentage:.1f}% support). {primary_problem} ({element_scores[primary_problem]}pts) is overwhelming."
                        explanation += f" Strategy: {controller} controls {primary_problem}"
                        
                        if dm_element in favorable:
                            explanation += f", {dm_element} strengthens self"
                        
                        if drain_benefit:
                            explanation += drain_benefit
                        
                        if synergies:
                            explanation += f" Synergies: {', '.join(synergies)}."
                        
                        # Only add resource if Day Master itself is NOT the problem
                        if primary_problem != dm_element and element_scores.get(resource_elem, 0) < dm_score * 0.5:
                            favorable.append(resource_elem)  # Strengthen if resource is weak
                            explanation += f" {resource_elem} can provide modest support."
                    else:
                        # Strengthen Day Master instead
                        useful_god = resource_elem
                        favorable = [resource_elem, dm_element]
                        explanation = f"Day Master balanced ({support_percentage:.1f}% support). {primary_problem} ({element_scores[primary_problem]}pts) is too strong. Strengthen Day Master with {resource_elem}."
                    
                    unfavorable = [primary_problem]
                    
                    # Check if any element feeds the problematic element
                    for elem, generated in generates.items():
                        if generated == primary_problem and elem not in favorable:
                            unfavorable.append(elem)
                            if elem not in explanation:
                                explanation += f" Avoid {elem} (feeds {primary_problem})."
                else:
                    # No major problems, traditional weakest element approach
                    weakest = min(five_elements.items(), key=lambda x: x[1]["score"])
                    useful_god = weakest[0]
                    favorable = [weakest[0]]
                    strongest = max(five_elements.items(), key=lambda x: x[1]["score"])
                    unfavorable = [strongest[0]] if strongest[0] != dm_element else []
                    explanation = f"Day Master balanced ({support_percentage:.1f}% support). Enhance {weakest[0]} (weakest element) for equilibrium."
                
            elif support_percentage >= 20:
                strength_category = "Weak"
                useful_god = relationships["resource"]
                favorable = [relationships["resource"], dm_element]
                unfavorable = [relationships["officer"], relationships["wealth"]]
                explanation = f"Day Master weak ({support_percentage:.1f}% support). Strengthen with Resource ({relationships['resource']}) and Companion ({dm_element})."
                
            else:
                strength_category = "Very Weak"
                useful_god = relationships["resource"]
                favorable = [relationships["resource"], dm_element]
                unfavorable = [relationships["officer"], relationships["wealth"], relationships["output"]]
                explanation = f"Day Master very weak ({support_percentage:.1f}% support). Urgently needs Resource ({relationships['resource']}) and Companion support."
        
        # Add seasonal context
        month_eb = bazi_chart.get("month_pillar", "").split()[1] if " " in bazi_chart.get("month_pillar", "") else ""
        
        # Find element's seasonal state based on month branch
        seasonal_state = None
        seasonal_factor = 1.0
        if month_eb and dm_element in SEASONAL_STRENGTH:
            for state, branches in SEASONAL_STRENGTH[dm_element].items():
                if month_eb in branches:
                    seasonal_state = state.lower()
                    seasonal_factor = SEASONAL_ADJUSTMENT.get(seasonal_state, 1.0)
                    break
        
        if seasonal_state:
            season = BRANCH_TO_SEASON.get(month_eb, "Unknown")
            if seasonal_factor > 1.0:
                explanation += f" Born in favorable {season} ({seasonal_state}, ×{seasonal_factor:.2f})."
            elif seasonal_factor < 1.0:
                explanation += f" Born in challenging {season} ({seasonal_state}, ×{seasonal_factor:.2f})."
        
        return {
            "daymaster": f"{dm_polarity} {dm_element}",
            "daymaster_strength": strength_category,
            "daymaster_percentage": round(dm_percentage, 1),
            "support_percentage": round(support_percentage, 1),
            "drain_percentage": round(drain_percentage, 1),
            "chart_type": chart_type,
            "element_relationships": {
                "resource": f"{relationships['resource']} ({resource_score}pts)",
                "companion": f"{dm_element} ({dm_score}pts)",
                "output": f"{relationships['output']} ({output_score}pts)",
                "wealth": f"{relationships['wealth']} ({wealth_score}pts)",
                "officer": f"{relationships['officer']} ({officer_score}pts)"
            },
            "favorable_elements": favorable,
            "unfavorable_elements": unfavorable,
            "useful_god": useful_god,
            "explanation": explanation
        }
    
    # Perform Daymaster analysis (use post for full chart strength)
    daymaster_analysis = analyze_daymaster_strength(bazi_chart, post_five_elements)
    
    # Convert nodes to Pydantic structure
    def node_to_pydantic(node, node_id, position=None, day_master_hs=None):
        """Convert ElementNode to Pydantic NodeResponse structure"""
        
        # Extract position from node_id if not provided
        if position is None:
            position = node_id.split("_")[1] if "_" in node_id else None
        
        # Determine position index
        position_idx_map = {"y": 0, "m": 1, "d": 2, "h": 3}
        position_idx = position_idx_map.get(position)
        
        # Build base state (initial values)
        base_qi = {}
        post_qi = {}
        
        if node.node_type == "stem":
            # Heavenly Stem
            stem_name = node.value
            if stem_name in HEAVENLY_STEMS:
                stem_info = HEAVENLY_STEMS[stem_name]
                
                # Base qi for stem (single entry)
                base_qi[stem_name] = stem_info["qi_score"]
                
                # Post-interaction qi - include ALL stems with scores in node.elements
                for elem_key, elem_data in node.elements.items():
                    if elem_data["score"] > 0:
                        # Find corresponding stem for this element
                        parts = elem_key.split(" ")
                        if len(parts) == 2:
                            pol, elem = parts
                            # Find the stem that matches this polarity and element
                            for hs_name, hs_info in HEAVENLY_STEMS.items():
                                if hs_info["polarity"] == pol and hs_info["element"] == elem:
                                    post_qi[hs_name] = round(elem_data["score"], 1)
                                    break
                
                # ID is always the original stem name
                post_id = stem_name
                
        else:
            # Earthly Branch
            branch_name = node.value
            if branch_name in EARTHLY_BRANCHES:
                branch_info = EARTHLY_BRANCHES[branch_name]
                
                # Base qi for branch (hidden stems)
                for qi_info in branch_info["qi"]:
                    stem = qi_info["stem"]
                    base_qi[stem] = qi_info["score"]
                
                # Base qi collected above
                
                # Post-interaction qi - ALWAYS build from actual node.elements
                # This preserves original elements + adds transformed elements
                for elem_key, elem_data in node.elements.items():
                    if elem_data["score"] > 0:
                        # Parse element key to find matching stem
                        parts = elem_key.split(" ")
                        if len(parts) == 2:
                            pol, elem = parts
                            # Find the stem that matches this polarity and element
                            for hs_name, hs_info in HEAVENLY_STEMS.items():
                                if hs_info["polarity"] == pol and hs_info["element"] == elem:
                                    post_qi[hs_name] = round(elem_data["score"], 1)
                                    break
                
                # ID is always the original branch name
                post_id = branch_name
        
        # Collect interaction IDs - will be populated from interaction_log later
        interaction_ids = []
        
        # Build NodeResponse with flat structure
        return NodeResponse(
            id=post_id,
            base_qi=base_qi,
            post_interaction_qi=post_qi,
            interaction_ids=interaction_ids,  # Will be populated from interaction_log
            badges=[BadgeData(**b) for b in getattr(node, 'badges', [])]
        )
    
    # Create visualization of transformations
    transformed_chart = {}
    transformations = []
    
    # Reconstruct pillars from nodes
    # Map position codes back to pillar keys for reconstruction
    pos_to_pillar = {
        "y": "year_pillar",
        "m": "month_pillar", 
        "d": "day_pillar",
        "h": "hour_pillar",
        "10yl": "luck_10_year_pillar",
        "yl": "yearly_luck_pillar"
    }
    
    for pos in position_codes:
        pillar_key = pos_to_pillar.get(pos)
        if not pillar_key:
            continue
        idx = position_to_index.get(pos, 0)
        hs_id = f"hs_{pos}"
        eb_id = f"eb_{pos}"
        
        if hs_id in nodes and eb_id in nodes:
            hs_node = nodes[hs_id]
            eb_node = nodes[eb_id]
            
            # Check if branch has badges (transformations)
            if eb_node.badges:
                # Show transformation (use legacy transformation_element field)
                trans_element = eb_node.transformation_element or ""
                trans_pattern = eb_node.transformation_pattern or ""
                transformed_chart[pillar_key] = f"{hs_node.value} {trans_element}"
                transformations.append({
                    "node": eb_id,
                    "original": eb_node.value,
                    "transformed": trans_element,
                    "pattern": trans_pattern
                })
            else:
                transformed_chart[pillar_key] = f"{hs_node.value} {eb_node.value}"
    
    # Determine if seasonal adjustment was applied
    seasonal_adjustment_applied = month_branch and month_branch in BRANCH_TO_SEASON
    
    # Extract day master stem for Ten Gods calculation
    day_master_hs = None
    if "hs_d" in nodes:
        day_master_hs = nodes["hs_d"].value
    
    # Format node states for API response
    def format_node_state(node):
        """Format an ElementNode for API response"""
        # Extract position from node_id (e.g., "hs_y" -> "y")
        position = node.node_id.split("_")[1] if "_" in node.node_id else None
        
        # Get additional attributes based on node type
        additional_attrs = {}
        if node.node_type == "stem" and node.value in HEAVENLY_STEMS:
            additional_attrs["element"] = HEAVENLY_STEMS[node.value]["element"]
            additional_attrs["polarity"] = HEAVENLY_STEMS[node.value]["polarity"]
            # Add hex color for frontend - use HEAVENLY_STEM colors for stems
            if node.value in HEAVENLY_STEMS:
                additional_attrs["hex_color"] = HEAVENLY_STEMS[node.value]["hex_color"]
        elif node.node_type == "branch" and node.value in EARTHLY_BRANCHES:
            additional_attrs["element"] = EARTHLY_BRANCHES[node.value]["element"]
            additional_attrs["animal"] = EARTHLY_BRANCHES[node.value]["animal"]
            # Add hex color for frontend - use EARTHLY_BRANCH colors for branches
            if node.value in EARTHLY_BRANCHES:
                additional_attrs["hex_color"] = EARTHLY_BRANCHES[node.value]["hex_color"]
        
        # Format qi (unified structure with stem IDs, elements, and values)
        total_score = node.get_total_score()
        qi = []
        post_qi = []
        
        # Get the original qi values (before any interactions/transformations)
        if node.node_type == "stem" and node.value in HEAVENLY_STEMS:
            # For Heavenly Stems, create a single qi entry
            stem_data = HEAVENLY_STEMS[node.value]
            qi.append({
                "stem": node.value,
                "element": stem_data["element"],
                "polarity": stem_data["polarity"],
                "score": stem_data["qi_score"],
                "hex_color": stem_data["hex_color"]
            })
        elif node.node_type == "branch" and node.value in EARTHLY_BRANCHES:
            # For Earthly Branches, add each hidden stem
            for qi_info in EARTHLY_BRANCHES[node.value]["qi"]:
                hs_hidden = qi_info["stem"]
                if hs_hidden in HEAVENLY_STEMS:
                    stem_data = HEAVENLY_STEMS[hs_hidden]
                    qi_entry = {
                        "stem": hs_hidden,
                        "element": stem_data["element"],
                        "polarity": stem_data["polarity"],
                        "score": qi_info["score"],
                        "hex_color": stem_data["hex_color"]
                    }
                    qi.append(qi_entry)
        
        # Post-qi shows the current state after all interactions
        # For transformed branches, build from node.elements using polarity-based stems
        if node.badges and node.transformation_element:
            trans_element = node.transformation_element.split()[1] if " " in node.transformation_element else node.transformation_element
            
            # Build qi dynamically from ELEMENT_POLARITY_STEMS for both polarities
            for polarity in ["Yang", "Yin"]:
                stem_id = ELEMENT_POLARITY_STEMS.get((trans_element, polarity))
                if stem_id and stem_id in HEAVENLY_STEMS:
                    stem_data = HEAVENLY_STEMS[stem_id]
                    elem_key = f"{polarity} {trans_element}"
                    elem_score = node.elements.get(elem_key, {}).get("score", 0)
                    if elem_score > 0:  # Only add if element actually exists
                        qi_entry = {
                            "stem": stem_id,
                            "element": trans_element,
                            "polarity": polarity,
                            "score": round(elem_score, 1),
                            "hex_color": stem_data["hex_color"]
                        }
                        post_qi.append(qi_entry)
        else:
            # Not transformed - build post_qi from current node.elements
            # Map back to stems based on element+polarity
            elem_to_stems = {}  # Track which elements we've already added
            
            for elem_key, elem_data in node.elements.items():
                if elem_data["score"] > 0:
                    # Parse polarity and element from key
                    parts = elem_key.split(" ")
                    if len(parts) == 2:
                        polarity, element = parts
                        # Find corresponding stem(s)
                        for stem, stem_info in HEAVENLY_STEMS.items():
                            if stem_info["element"] == element and stem_info["polarity"] == polarity:
                                # Check if this stem was in the original qi
                                if node.node_type == "stem" and stem == node.value:
                                    # For stems, only include the stem itself
                                    post_qi.append({
                                        "stem": stem,
                                        "element": element,
                                        "polarity": polarity,
                                        "score": round(elem_data["score"], 1),
                                        "hex_color": stem_info["hex_color"]
                                    })
                                    break
                                elif node.node_type == "branch":
                                    # For branches, check if this stem was in original hidden qi
                                    original_stems = [q["stem"] for q in EARTHLY_BRANCHES.get(node.value, {}).get("qi", [])]
                                    if stem in original_stems:
                                        qi_entry = {
                                            "stem": stem,
                                            "element": element,
                                            "polarity": polarity,
                                            "score": round(elem_data["score"], 1),
                                            "hex_color": stem_info["hex_color"]
                                        }
                                        post_qi.append(qi_entry)
                                        break
        
        # Add post-transformation properties if node has badges
        post_transformation_attrs = {}
        if node.badges and node.transformation_element:
            # Parse transformation element (e.g., "Yang Metal")
            trans_parts = node.transformation_element.split()
            if len(trans_parts) == 2:
                trans_polarity = trans_parts[0]
                trans_element = trans_parts[1]
                
                # Find corresponding stem for the transformed element
                trans_stem = None
                for stem, stem_info in HEAVENLY_STEMS.items():
                    if stem_info["element"] == trans_element and stem_info["polarity"] == trans_polarity:
                        trans_stem = stem
                        break
                
                if trans_stem:
                    post_transformation_attrs["post_name"] = trans_stem
                    post_transformation_attrs["post_element"] = trans_element
                    post_transformation_attrs["post_polarity"] = trans_polarity
                    
                    # Add post-transformation hex color
                    if trans_stem in HEAVENLY_STEMS:
                        post_transformation_attrs["post_hex_color"] = HEAVENLY_STEMS[trans_stem]["hex_color"]
        
        return {
            "node": node.node_id,
            "type": node.node_type,
            "position": position,
            "name": node.value,
            "qi": qi,  # Original qi with stem IDs
            "post_qi": post_qi,  # Post-interaction qi with stem IDs
            "transformation_element": node.transformation_element,
            "transformation_pattern": node.transformation_pattern,
            "interactions": node.interactions,
            "total_score": total_score,
            **additional_attrs,
            **post_transformation_attrs
        }
    
    # Format all nodes using Pydantic structure
    # Get day master for ten gods calculation
    day_master_hs = bazi_chart.get("day_pillar", "").split()[0] if "day_pillar" in bazi_chart else None
    
    nodes_state = {}
    for node_id, node in nodes.items():
        # Use the node_to_pydantic function defined above
        pydantic_node = node_to_pydantic(node, node_id, node_id.split("_")[1] if "_" in node_id else None, day_master_hs)
        # Convert to dict for JSON response
        nodes_state[node_id] = pydantic_node.dict()
    
    # Build interaction dictionary with IDs and update node interaction_ids
    interactions_dict = {}
    node_interaction_map = {}  # Maps node_id to list of interaction IDs
    
    for interaction in interaction_log:
        # Generate interaction ID based on type, pattern, and nodes
        int_type = interaction.get("type", "UNKNOWN")
        pattern = interaction.get("pattern", "")
        nodes_list = interaction.get("nodes", [])
        
        # For interactions with pattern field, use it directly
        # Otherwise, build from branches/stems
        if pattern:
            # Pattern is already in library order (e.g., "Si-Wu-Wei" or "Chou-Wu")
            base_str = pattern
            
            # Map nodes to match the pattern order
            if "branches" in interaction and len(interaction["branches"]) == len(nodes_list):
                # Create mapping of branch value to node_id
                branch_to_node = {}
                for i, node_id in enumerate(nodes_list):
                    branch_to_node[interaction["branches"][i]] = node_id
                
                # Order nodes to match pattern order
                pattern_branches = pattern.split("-")
                ordered_nodes = []
                for branch in pattern_branches:
                    if branch in branch_to_node:
                        ordered_nodes.append(branch_to_node[branch])
                
                nodes_str = "-".join(ordered_nodes) if ordered_nodes else "-".join(sorted(nodes_list))
            else:
                nodes_str = "-".join(sorted(nodes_list))
        else:
            # No pattern, extract from nodes
            node_base_pairs = []
            for node_id in nodes_list:
                if node_id in nodes:
                    node_base_pairs.append((node_id, nodes[node_id].value))
                else:
                    node_base_pairs.append((node_id, "?"))
            
            # Sort pairs by node_id
            node_base_pairs.sort(key=lambda x: x[0])
            base_str = "-".join([pair[1] for pair in node_base_pairs])
            nodes_str = "-".join([pair[0] for pair in node_base_pairs])
        
        # Create standardized ID format: TYPE~PATTERN~NODE_IDS
        interaction_id = f"{int_type}~{base_str}~{nodes_str}"
        
        # Store interaction data (convert to dict for JSON serialization)
        # Include ALL fields from the interaction_log entry
        interactions_dict[interaction_id] = {
            "type": int_type,
            "pattern": pattern,
            "nodes": nodes_list,
            "effect": interaction.get("effect"),
            "positions": interaction.get("positions"),
            "description": interaction.get("description"),
            # Preserve additional fields for positive interactions
            "transformed": interaction.get("transformed"),  # Fixed: was "transformation"
            "cascading": interaction.get("cascading"),  # Flag for upgraded interactions
            "element": interaction.get("element"),
            "boost": interaction.get("boost"),
            "distance": interaction.get("distance"),  # Distance key for scoring transparency
            "branches": interaction.get("branches"),
            "reason": interaction.get("reason"),
            "reduction": interaction.get("reduction")
        }
        
        # Remove None values to keep response clean
        interactions_dict[interaction_id] = {k: v for k, v in interactions_dict[interaction_id].items() if v is not None}
        
        # Track which nodes are involved in this interaction
        for node_id in nodes_list:
            if node_id not in node_interaction_map:
                node_interaction_map[node_id] = []
            node_interaction_map[node_id].append(interaction_id)
    
    # Update nodes_state with interaction IDs
    for node_id in nodes_state:
        if node_id in node_interaction_map:
            nodes_state[node_id]["interaction_ids"] = node_interaction_map[node_id]
    
    return {
        "nodes": nodes_state,
        # 2-tier element scoring (Nov 2025): base=natal only, post=everything
        "base_element_score": base_ten_elements,   # Natal chart only, before interactions
        "post_element_score": post_ten_elements,   # All nodes + location, after interactions
        "interactions": interactions_dict,
        "daymaster_analysis": daymaster_analysis,
        "transformed_chart": transformed_chart,
        "transformations": transformations,
        "summary": {
            "total_interactions": len(interaction_log),
            "total_transformations": len(transformations),
            "nodes_affected": sum(1 for n in nodes.values() if n.marked),
            "branch_nodes_transformed": sum(1 for n in nodes.values() if n.badges),
            "seasonal_adjustment_applied": seasonal_adjustment_applied
        }
    }
