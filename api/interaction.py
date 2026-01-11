

from typing import Dict, List, Optional, Set, Any
from library import (
    HEAVENLY_STEMS,
    EARTHLY_BRANCHES,
    SEASONAL_STRENGTH,
    THREE_MEETINGS,
    THREE_COMBINATIONS,
    SIX_HARMONIES,
    HALF_COMBINATIONS,
    ARCHED_COMBINATIONS,
    PUNISHMENTS,
    HARMS
)

def generate_hs_eb_permutations(bazi_chart: Dict) -> Dict:
    """
    Generate all possible permutations of 2 characters in HS and 2/3 characters in EB
    from a Bazi natal chart, including position and distance information.
    
    Args:
        bazi_chart: A dictionary containing the natal chart pillars
        
    Returns:
        A dictionary with permutations of HS and EB characters in string format,
        along with position and distance information
    """
    # Define pillar positions and labels
    pillar_positions = {
        "year_pillar": "y",
        "month_pillar": "m",
        "day_pillar": "d",
        "hour_pillar": "h",
        "luck_10_year": "l10",
        "luck_annual": "la"
    }
    
    hs_pillar_labels = {
        "year_pillar": "y_hs",
        "month_pillar": "m_hs",
        "day_pillar": "d_hs",
        "hour_pillar": "h_hs",
        "luck_10_year": "l10_hs",
        "luck_annual": "la_hs"
    }
    
    eb_pillar_labels = {
        "year_pillar": "y_eb",
        "month_pillar": "m_eb",
        "day_pillar": "d_eb",
        "hour_pillar": "h_eb",
        "luck_10_year": "l10_eb",
        "luck_annual": "la_eb"
    }
    
    # Position mapping for distance calculations
    position_values = {
        "y": 0,
        "m": 1,
        "d": 2,
        "h": 3,
        "l10": 4,
        "la": 5
    }
    
    # Extract HS and EB characters from the chart with their positions and labels
    hs_data = []
    eb_data = []
    
    for pillar_key, pillar_value in bazi_chart.items():
        if pillar_key in pillar_positions:
            if isinstance(pillar_value, str):
                parts = pillar_value.split(" ")
                if len(parts) == 2:
                    hs_char, eb_char = parts
                    
                    # Add HS character with metadata
                    hs_data.append({
                        "char": hs_char,
                        "position": pillar_positions[pillar_key],
                        "label": hs_pillar_labels[pillar_key]
                    })
                    
                    # Add EB character with metadata
                    eb_data.append({
                        "char": eb_char,
                        "position": pillar_positions[pillar_key],
                        "label": eb_pillar_labels[pillar_key]
                    })
    
    # Generate all permutations for HS (2 characters)
    hs_permutations = []
    for perm in permutations(hs_data, 2):
        p1, p2 = perm
        # Calculate distance
        pos1 = position_values[p1["position"]]
        pos2 = position_values[p2["position"]]
        distance = abs(pos1 - pos2)
        
        # Determine adjacency type based on specific positions
        if distance == 1:
            if (p1["position"] in ["y", "m"] and p2["position"] in ["y", "m"]) or \
               (p1["position"] in ["m", "y"] and p2["position"] in ["m", "y"]):
                adjacency = "adjacent_outer"
            elif (p1["position"] in ["d", "h"] and p2["position"] in ["d", "h"]) or \
                 (p1["position"] in ["h", "d"] and p2["position"] in ["h", "d"]):
                adjacency = "adjacent_inner"
            else:
                adjacency = "adjacent"
        else:
            adjacency = "non_adjacent"
        
        hs_permutations.append({
            "combination": f"{p1['char']}-{p2['char']}",
            "elements": [p1, p2],
            "distance": distance,
            "adjacency": adjacency,
            "positions": f"{p1['label']}-{p2['label']}"
        })
    
    # Generate all permutations for EB (2 characters)
    eb_2_permutations = []
    for perm in permutations(eb_data, 2):
        p1, p2 = perm
        # Calculate distance
        pos1 = position_values[p1["position"]]
        pos2 = position_values[p2["position"]]
        distance = abs(pos1 - pos2)
        
        # Determine adjacency type
        if distance == 1:
            if (p1["position"] in ["y", "m"] and p2["position"] in ["y", "m"]) or \
               (p1["position"] in ["m", "y"] and p2["position"] in ["m", "y"]):
                adjacency = "adjacent_outer"
            elif (p1["position"] in ["d", "h"] and p2["position"] in ["d", "h"]) or \
                 (p1["position"] in ["h", "d"] and p2["position"] in ["h", "d"]):
                adjacency = "adjacent_inner"
            else:
                adjacency = "adjacent"
        else:
            adjacency = "non_adjacent"
        
        eb_2_permutations.append({
            "combination": f"{p1['char']}-{p2['char']}",
            "elements": [p1, p2],
            "distance": distance,
            "adjacency": adjacency,
            "positions": f"{p1['label']}-{p2['label']}"
        })
    
    # Generate all permutations for EB (3 characters)
    eb_3_permutations = []
    for perm in permutations(eb_data, 3):
        p1, p2, p3 = perm
        # Calculate average distance
        pos1 = position_values[p1["position"]]
        pos2 = position_values[p2["position"]]
        pos3 = position_values[p3["position"]]
        
        distances = [abs(pos1 - pos2), abs(pos1 - pos3), abs(pos2 - pos3)]
        avg_distance = sum(distances) / len(distances)
        
        # Check if all three are adjacent
        positions_sorted = sorted([pos1, pos2, pos3])
        if positions_sorted[2] - positions_sorted[0] == 2:
            adjacency = "all_adjacent"
        elif 1 in distances:
            adjacency = "partially_adjacent"
        else:
            adjacency = "non_adjacent"
        
        eb_3_permutations.append({
            "combination": f"{p1['char']}-{p2['char']}-{p3['char']}",
            "elements": [p1, p2, p3],
            "avg_distance": avg_distance,
            "adjacency": adjacency,
            "positions": f"{p1['label']}-{p2['label']}-{p3['label']}"
        })
    
    return {
        "hs_2_permutations": hs_permutations,
        "eb_2_permutations": eb_2_permutations,
        "eb_3_permutations": eb_3_permutations
    }


def naive_element_scores(bazi_chart: Dict) -> Dict:
    """
    Calculate naive element scores from a BaZi chart.
    Counts Heavenly Stems at face value (10 points each) and 
    Earthly Branches with their Qi components weighted by strength.
    
    Args:
        bazi_chart: A dictionary containing the natal chart pillars and luck pillars
        
    Returns:
        A dictionary with scores and counts for each of the 10 elements
    """
    
    # Initialize scores for all 10 elements
    elements = ["Wood", "Fire", "Earth", "Metal", "Water"]
    polarities = ["Yang", "Yin"]
    
    element_scores = {}
    
    for element in elements:
        for polarity in polarities:
            key = f"{polarity} {element}"
            element_scores[key] = 0.0
    
    # Process only the four pillars
    pillars_to_process = ["year_pillar", "month_pillar", "day_pillar", "hour_pillar"]
    
    for pillar_key in pillars_to_process:
        if pillar_key in bazi_chart:
            pillar_value = bazi_chart[pillar_key]
            
            if isinstance(pillar_value, str):
                parts = pillar_value.split(" ")
                if len(parts) == 2:
                    hs_char, eb_char = parts
                    
                    # Process Heavenly Stem (100 points each)
                    if hs_char in HEAVENLY_STEMS:
                        hs_info = HEAVENLY_STEMS[hs_char]
                        element_key = f"{hs_info['polarity']} {hs_info['element']}"
                        element_scores[element_key] += hs_info["qi_score"]
                    
                    # Process Earthly Branch Qi (using hardcoded scores)
                    if eb_char in EARTHLY_BRANCHES:
                        eb_info = EARTHLY_BRANCHES[eb_char]
                        for qi_data in eb_info["qi"]:
                            qi_hs = qi_data["stem"]
                            if qi_hs in HEAVENLY_STEMS:
                                qi_info = HEAVENLY_STEMS[qi_hs]
                                element_key = f"{qi_info['polarity']} {qi_info['element']}"
                                # Use the hardcoded score
                                element_scores[element_key] += qi_data["score"]
    
    return {
        "scores": element_scores
    }


def calculate_element_scores_with_interactions(bazi_chart: Dict, month_branch: str = None) -> Dict:
    """
    Calculate element scores with all BaZi interactions applied in priority order.
    
    Priority Order (Highest to Lowest):
    1. Three Meetings (三會) - Seasonal transformations
    2. Punishments (刑) - Negative interactions
    3. Harms (害) - Mutual damage
    4. Clashes (沖) - Direct opposition
    5. Destruction (破) - Breaking relationships
    6. Three Combinations (三合) - Elemental transformations
    7. Six Harmonies (六合) - Harmonious pairs
    8. Half Combinations (半合) - Partial combinations
    9. Arched Combinations (拱合) - Arching patterns
    
    Args:
        bazi_chart: Dictionary containing the four pillars
        month_branch: Month branch for seasonal strength determination
        
    Returns:
        Dictionary with naive scores, interactions log, and final scores
    """
    from copy import deepcopy
    
    # Get naive element scores first
    naive_scores = naive_element_scores(bazi_chart)
    element_scores = deepcopy(naive_scores["scores"])
    
    # Extract branches and their positions
    branches_data = []
    pillar_order = ["year_pillar", "month_pillar", "day_pillar", "hour_pillar"]
    
    for idx, pillar_key in enumerate(pillar_order):
        if pillar_key in bazi_chart:
            pillar = bazi_chart[pillar_key]
            if isinstance(pillar, str) and " " in pillar:
                hs, eb = pillar.split(" ")
                branches_data.append({
                    "branch": eb,
                    "position": idx,
                    "pillar": pillar_key,
                    "marked": False  # Track if branch is already used
                })
    
    # Interaction log to track all changes
    interaction_log = []
    
    def mark_branches(branch_indices):
        """Mark branches as used in interaction."""
        for idx in branch_indices:
            branches_data[idx]["marked"] = True
    
    def are_adjacent(indices):
        """Check if branch indices are adjacent."""
        sorted_indices = sorted(indices)
        for i in range(len(sorted_indices) - 1):
            if sorted_indices[i+1] - sorted_indices[i] == 1:
                return True
        return False
    
    def get_season_strength(element):
        """Get seasonal strength multiplier based on month branch."""
        if not month_branch:
            return 1.0
        
        states = ELEMENT_SEASONAL_STATES.get(element, {})
        if month_branch in states.get("Prosperous", []):
            return 1.5  # 50% boost when prosperous
        elif month_branch in states.get("Strengthening", []):
            return 1.2  # 20% boost when strengthening
        elif month_branch in states.get("Resting", []):
            return 1.0  # Normal strength
        elif month_branch in states.get("Trapped", []):
            return 0.8  # 20% reduction when trapped
        elif month_branch in states.get("Dead", []):
            return 0.5  # 50% reduction when dead
        return 1.0
    
    def apply_element_change(element, polarity, amount, reason):
        """Apply element score change and log it."""
        key = f"{polarity} {element}"
        old_score = element_scores.get(key, 0)
        element_scores[key] = max(0, old_score + amount)  # Don't go below 0
        
        interaction_log.append({
            "element": key,
            "change": amount,
            "old_score": old_score,
            "new_score": element_scores[key],
            "reason": reason
        })
    
    # 1. THREE MEETINGS (三會) - Highest Priority
    for direction, required in THREE_MEETINGS.items():
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 3:
            # Check if we have all three branches
            found_branches = [branches_data[i]["branch"] for i in indices[:3]]
            if set(found_branches) == set(required):
                mark_branches(indices[:3])
                
                # Determine element and strength
                if "Wood" in direction:
                    element = "Wood"
                elif "Fire" in direction:
                    element = "Fire"
                elif "Metal" in direction:
                    element = "Metal"
                elif "Water" in direction:
                    element = "Water"
                else:
                    continue
                
                adjacent = are_adjacent(indices[:3])
                seasonal = get_season_strength(element)
                base_boost = 30  # Base transformation strength
                
                # Calculate total boost
                total_boost = base_boost * seasonal
                if adjacent:
                    total_boost *= 1.3  # 30% bonus for adjacent
                
                # Apply to both polarities of the element
                apply_element_change(element, "Yang", total_boost * 0.6,
                    f"Three Meetings ({direction}) - {'Adjacent' if adjacent else 'Separated'}, Season x{seasonal:.1f}")
                apply_element_change(element, "Yin", total_boost * 0.4,
                    f"Three Meetings ({direction}) - {'Adjacent' if adjacent else 'Separated'}, Season x{seasonal:.1f}")
                
                interaction_log.append({
                    "type": "THREE_MEETINGS",
                    "pattern": direction,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "seasonal_strength": seasonal
                })
    
    # 2. PUNISHMENTS (刑) - Negative
    for punishment, info in PUNISHMENTS.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= len(required):
            # Check for self-punishment (needs 2 of same)
            if len(set(required)) == 1:
                if len([i for i in indices if branches_data[i]["branch"] == required[0]]) >= 2:
                    mark_branches(indices[:2])
                    adjacent = are_adjacent(indices[:2])
                    
                    # Self-punishment reduces the element
                    branch = required[0]
                    element = EARTHLY_BRANCHES[branch]["element"]
                    polarity = EARTHLY_BRANCHES[branch]["polarity"]
                    
                    reduction = -15 if info["effect"] == "Medium" else -20
                    if adjacent:
                        reduction *= 1.5  # Stronger when adjacent
                    
                    apply_element_change(element, polarity, reduction,
                        f"Self-Punishment ({punishment}) - {'Adjacent' if adjacent else 'Separated'}")
                    
                    interaction_log.append({
                        "type": "PUNISHMENT",
                        "pattern": punishment,
                        "branches": [branches_data[i]["branch"] for i in indices[:2]],
                        "adjacent": adjacent,
                        "base_reduction": info.get("base_reduction", 10)
                    })
            else:
                # Regular punishment
                found_branches = [branches_data[i]["branch"] for i in indices]
                if set(found_branches[:len(required)]) == set(required):
                    mark_branches(indices[:len(required)])
                    adjacent = are_adjacent(indices[:len(required)])
                    
                    # Punishment weakens involved elements
                    effect_multiplier = info.get("base_reduction", 10) / 10  # Convert base_reduction to multiplier
                    base_reduction = -10 * effect_multiplier
                    
                    if adjacent:
                        base_reduction *= 1.5
                    
                    for branch in required:
                        element = EARTHLY_BRANCHES[branch]["element"]
                        polarity = EARTHLY_BRANCHES[branch]["polarity"]
                        apply_element_change(element, polarity, base_reduction,
                            f"Punishment ({punishment}) - {'Adjacent' if adjacent else 'Separated'}")
                    
                    interaction_log.append({
                        "type": "PUNISHMENT",
                        "pattern": punishment,
                        "branches": found_branches[:len(required)],
                        "adjacent": adjacent,
                        "base_reduction": info.get("base_reduction", 10)
                    })
    
    # 3. HARMS (害) - Negative
    for harm, info in HARMS.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                adjacent = are_adjacent(indices[:2])
                
                effect_multiplier = info.get("base_reduction", 10) / 10  # Convert base_reduction to multiplier
                base_reduction = -8 * effect_multiplier
                
                if adjacent:
                    base_reduction *= 1.5
                
                for branch in required:
                    element = EARTHLY_BRANCHES[branch]["element"]
                    polarity = EARTHLY_BRANCHES[branch]["polarity"]
                    apply_element_change(element, polarity, base_reduction,
                        f"Harm ({harm}) - {'Adjacent' if adjacent else 'Separated'}")
                
                interaction_log.append({
                    "type": "HARM",
                    "pattern": harm,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "base_reduction": info.get("base_reduction", 10)
                })
    
    # 4. CLASHES (沖) - Negative
    for clash, info in CLASHES.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                adjacent = are_adjacent(indices[:2])
                
                effect_multiplier = info.get("base_reduction", 15) / 10  # Convert base_reduction to multiplier
                base_reduction = -12 * effect_multiplier
                
                if adjacent:
                    base_reduction *= 1.5
                
                # Clashes weaken both elements involved
                for branch in required:
                    element = EARTHLY_BRANCHES[branch]["element"]
                    polarity = EARTHLY_BRANCHES[branch]["polarity"]
                    apply_element_change(element, polarity, base_reduction,
                        f"Clash ({clash}) - {'Adjacent' if adjacent else 'Separated'}")
                
                interaction_log.append({
                    "type": "CLASH",
                    "pattern": clash,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "base_reduction": info.get("base_reduction", 10)
                })
    
    # 5. DESTRUCTION (破) - Negative
    for destruction, info in DESTRUCTION.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                adjacent = are_adjacent(indices[:2])
                
                effect_multiplier = info.get("base_reduction", 10) / 10  # Convert base_reduction to multiplier
                base_reduction = -6 * effect_multiplier
                
                if adjacent:
                    base_reduction *= 1.5
                
                for branch in required:
                    element = EARTHLY_BRANCHES[branch]["element"]
                    polarity = EARTHLY_BRANCHES[branch]["polarity"]
                    apply_element_change(element, polarity, base_reduction,
                        f"Destruction ({destruction}) - {'Adjacent' if adjacent else 'Separated'}")
                
                interaction_log.append({
                    "type": "DESTRUCTION",
                    "pattern": destruction,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "base_reduction": info.get("base_reduction", 10)
                })
    
    # 6. THREE COMBINATIONS (三合) - Positive
    for element, required in THREE_COMBINATIONS.items():
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 3:
            found_branches = [branches_data[i]["branch"] for i in indices[:3]]
            if set(found_branches) == set(required):
                mark_branches(indices[:3])
                adjacent = are_adjacent(indices[:3])
                seasonal = get_season_strength(element)
                
                base_boost = 25
                total_boost = base_boost * seasonal
                if adjacent:
                    total_boost *= 1.3
                
                # Determine polarity distribution
                apply_element_change(element, "Yang", total_boost * 0.6,
                    f"Three Combinations ({element}) - {'Adjacent' if adjacent else 'Separated'}, Season x{seasonal:.1f}")
                apply_element_change(element, "Yin", total_boost * 0.4,
                    f"Three Combinations ({element}) - {'Adjacent' if adjacent else 'Separated'}, Season x{seasonal:.1f}")
                
                interaction_log.append({
                    "type": "THREE_COMBINATIONS",
                    "element": element,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "seasonal_strength": seasonal
                })
    
    # 7. SIX HARMONIES (六合) - Positive
    for harmony, info in SIX_HARMONIES.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                adjacent = are_adjacent(indices[:2])
                
                element = info["element"]
                seasonal = get_season_strength(element)
                base_boost = 15
                total_boost = base_boost * seasonal
                
                if adjacent:
                    total_boost *= 1.3
                
                apply_element_change(element, "Yang", total_boost * 0.6,
                    f"Six Harmonies ({harmony}) - {'Adjacent' if adjacent else 'Separated'}, Season x{seasonal:.1f}")
                apply_element_change(element, "Yin", total_boost * 0.4,
                    f"Six Harmonies ({harmony}) - {'Adjacent' if adjacent else 'Separated'}, Season x{seasonal:.1f}")
                
                interaction_log.append({
                    "type": "SIX_HARMONIES",
                    "pattern": harmony,
                    "element": element,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "seasonal_strength": seasonal
                })
    
    # 8. HALF COMBINATIONS (半合) - Positive
    for combo, info in HALF_COMBINATIONS.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                adjacent = are_adjacent(indices[:2])
                
                element = info["element"]
                seasonal = get_season_strength(element)
                base_boost = 10
                total_boost = base_boost * seasonal
                
                if adjacent:
                    total_boost *= 1.3
                
                apply_element_change(element, "Yang", total_boost * 0.6,
                    f"Half Combination ({combo}) - {'Adjacent' if adjacent else 'Separated'}, Season x{seasonal:.1f}")
                apply_element_change(element, "Yin", total_boost * 0.4,
                    f"Half Combination ({combo}) - {'Adjacent' if adjacent else 'Separated'}, Season x{seasonal:.1f}")
                
                interaction_log.append({
                    "type": "HALF_COMBINATION",
                    "pattern": combo,
                    "element": element,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "seasonal_strength": seasonal
                })
    
    # 9. ARCHED COMBINATIONS (拱合) - Positive (weakest)
    for combo, info in ARCHED_COMBINATIONS.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                
                element = info["element"]
                seasonal = get_season_strength(element)
                base_boost = 8
                total_boost = base_boost * seasonal
                
                # Arched combinations don't get adjacent bonus (they're missing middle)
                
                apply_element_change(element, "Yang", total_boost * 0.6,
                    f"Arched Combination ({combo}) - Missing {info['missing']}, Season x{seasonal:.1f}")
                apply_element_change(element, "Yin", total_boost * 0.4,
                    f"Arched Combination ({combo}) - Missing {info['missing']}, Season x{seasonal:.1f}")
                
                interaction_log.append({
                    "type": "ARCHED_COMBINATION",
                    "pattern": combo,
                    "element": element,
                    "branches": found_branches,
                    "missing": info["missing"],
                    "seasonal_strength": seasonal
                })
    
    # Calculate summary statistics
    total_positive_changes = sum(log["change"] for log in interaction_log 
                                 if isinstance(log, dict) and "change" in log and log["change"] > 0)
    total_negative_changes = sum(log["change"] for log in interaction_log 
                                 if isinstance(log, dict) and "change" in log and log["change"] < 0)
    
    return {
        "naive_scores": naive_scores,
        "interaction_log": interaction_log,
        "element_changes": [log for log in interaction_log if "change" in log],
        "final_scores": {
            "scores": element_scores,
            "counts": naive_scores["counts"]  # Counts don't change
        },
        "summary": {
            "total_interactions": len([log for log in interaction_log if "type" in log]),
            "total_positive_changes": round(total_positive_changes, 1),
            "total_negative_changes": round(total_negative_changes, 1),
            "net_change": round(total_positive_changes + total_negative_changes, 1)
        }
    }


def calculate_element_scores_with_interactions_v3(bazi_chart: Dict, month_branch: str = None) -> Dict:
    """
    Enhanced BaZi interaction calculator V3 with:
    - Index-based Hidden Qi interactions (only Primary & Secondary)
    - Updates both scores AND counts
    - Tracks transformations and creates transformed chart
    """
    from copy import deepcopy
    
    # Get naive element scores first
    naive_scores = naive_element_scores(bazi_chart)
    element_scores = deepcopy(naive_scores["scores"])
    element_counts = deepcopy(naive_scores["counts"])
    
    # Create a transformed chart copy
    transformed_chart = deepcopy(bazi_chart)
    
    # Extract branches and their positions
    branches_data = []
    pillar_order = ["year_pillar", "month_pillar", "day_pillar", "hour_pillar"]
    
    for idx, pillar_key in enumerate(pillar_order):
        if pillar_key in bazi_chart:
            pillar = bazi_chart[pillar_key]
            if isinstance(pillar, str) and " " in pillar:
                hs, eb = pillar.split(" ")
                branches_data.append({
                    "branch": eb,
                    "stem": hs,
                    "position": idx,
                    "pillar": pillar_key,
                    "marked": False,
                    "transformed": None  # Track if this pillar is transformed
                })
    
    # Track all transformations
    transformations = []
    interaction_log = []
    
    def mark_branches(branch_indices, transformation=None):
        """Mark branches as used and optionally record transformation."""
        for idx in branch_indices:
            branches_data[idx]["marked"] = True
            if transformation:
                branches_data[idx]["transformed"] = transformation
    
    def are_adjacent(indices):
        """Check if branch indices are adjacent."""
        sorted_indices = sorted(indices)
        for i in range(len(sorted_indices) - 1):
            if sorted_indices[i+1] - sorted_indices[i] == 1:
                return True
        return False
    
    def get_season_strength(element):
        """Get seasonal strength multiplier based on month branch."""
        if not month_branch:
            return 1.0
        
        states = ELEMENT_SEASONAL_STATES.get(element, {})
        if month_branch in states.get("Prosperous", []):
            return 1.5
        elif month_branch in states.get("Growing", []):
            return 1.2
        elif month_branch in states.get("Resting", []):
            return 1.0
        elif month_branch in states.get("Imprisoned", []):
            return 0.8
        elif month_branch in states.get("Dead", []):
            return 0.5
        return 1.0
    
    def apply_element_change(element, polarity, score_change, count_change, reason):
        """Apply element score AND count change and log it."""
        key = f"{polarity} {element}"
        old_score = element_scores.get(key, 0)
        old_count = element_counts.get(key, 0)
        
        element_scores[key] = max(0, old_score + score_change)
        element_counts[key] = max(0, old_count + count_change)
        
        interaction_log.append({
            "element": key,
            "score_change": score_change,
            "count_change": count_change,
            "old_score": old_score,
            "new_score": element_scores[key],
            "old_count": old_count,
            "new_count": element_counts[key],
            "reason": reason
        })
    
    def apply_hidden_qi_interactions_v2(branch1, branch2, interaction_type, adjacent):
        """
        Apply interactions between hidden Qi using index-based matching.
        Only Primary (index 0) and Secondary (index 1) Qi interact.
        """
        qi1 = EARTHLY_BRANCHES[branch1]["qi"]
        qi2 = EARTHLY_BRANCHES[branch2]["qi"]
        
        destructive_cycle = HIDDEN_QI_INTERACTIONS["destructive_cycle"]
        interaction_strength = HIDDEN_QI_INTERACTIONS["interaction_strength"].get(interaction_type, 0.3)
        
        # Only interact Primary and Secondary Qi (indices 0 and 1)
        for qi_index in HIDDEN_QI_INTERACTIONS["qi_indices_to_interact"]:
            # Make sure both branches have Qi at this index
            if qi_index < len(qi1) and qi_index < len(qi2):
                hs1 = qi1[qi_index]["stem"]
                strength1 = qi1[qi_index]["score"] / 100.0  # Convert score back to strength percentage
                hs2 = qi2[qi_index]["stem"]
                strength2 = qi2[qi_index]["score"] / 100.0
                
                elem1 = HEAVENLY_STEMS[hs1]["element"]
                pol1 = HEAVENLY_STEMS[hs1]["polarity"]
                elem2 = HEAVENLY_STEMS[hs2]["element"]
                pol2 = HEAVENLY_STEMS[hs2]["polarity"]
                
                # Check if elem1 destroys elem2
                if destructive_cycle.get(elem1) == elem2:
                    # Score reduction based on Qi strengths
                    base_score_reduction = -10 * strength1 * strength2 * interaction_strength
                    # Count reduction (smaller than score)
                    base_count_reduction = -strength1 * strength2 * interaction_strength * 0.5
                    
                    if adjacent:
                        base_score_reduction *= 1.3
                        base_count_reduction *= 1.3
                    
                    apply_element_change(elem2, pol2, base_score_reduction, base_count_reduction,
                        f"Hidden Qi[{qi_index}]: {hs1}({elem1}) {interaction_type.lower()}s {hs2}({elem2}) in {branch1}-{branch2}")
                
                # Check if elem2 destroys elem1
                elif destructive_cycle.get(elem2) == elem1:
                    base_score_reduction = -10 * strength2 * strength1 * interaction_strength
                    base_count_reduction = -strength2 * strength1 * interaction_strength * 0.5
                    
                    if adjacent:
                        base_score_reduction *= 1.3
                        base_count_reduction *= 1.3
                    
                    apply_element_change(elem1, pol1, base_score_reduction, base_count_reduction,
                        f"Hidden Qi[{qi_index}]: {hs2}({elem2}) {interaction_type.lower()}s {hs1}({elem1}) in {branch2}-{branch1}")
    
    def apply_transformation(branch_indices, element, pattern_name, is_complete=True):
        """
        Apply a transformation to branches, updating the transformed chart.
        For complete transformations, the pillar becomes pure element.
        """
        for idx in branch_indices:
            branch_data = branches_data[idx]
            pillar_key = branch_data["pillar"]
            
            if is_complete:
                # Complete transformation - pillar becomes pure element
                # "Wood Wood" means pure Wood, distributing equally to Yang and Yin
                transformed_chart[pillar_key] = f"{element} {element}"
                branch_data["transformed"] = element
                
                transformations.append({
                    "pillar": pillar_key,
                    "original": bazi_chart[pillar_key],
                    "transformed": f"{element} {element}",
                    "pattern": pattern_name,
                    "element": element
                })
    
    # Process interactions in priority order...
    
    # 1. THREE MEETINGS (三會) - Highest Priority
    for direction, required in THREE_MEETINGS.items():
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 3:
            found_branches = [branches_data[i]["branch"] for i in indices[:3]]
            if set(found_branches) == set(required):
                # Determine element
                if "Wood" in direction:
                    element = "Wood"
                elif "Fire" in direction:
                    element = "Fire"
                elif "Metal" in direction:
                    element = "Metal"
                elif "Water" in direction:
                    element = "Water"
                else:
                    continue
                
                adjacent = are_adjacent(indices[:3])
                seasonal = get_season_strength(element)
                
                # Mark and transform
                mark_branches(indices[:3])
                apply_transformation(indices[:3], element, f"Three Meetings ({direction})")
                
                # Base transformation: 40% boost to the meeting element
                base_boost = 40
                total_boost = base_boost * seasonal
                if adjacent:
                    total_boost *= 1.3
                
                # Apply boost equally to Yang and Yin (pure element)
                score_boost = total_boost * 0.5
                count_boost = 1.5  # Add 1.5 to each polarity count
                
                apply_element_change(element, "Yang", score_boost, count_boost,
                    f"Three Meetings ({direction}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'} [TRANSFORMED]")
                apply_element_change(element, "Yin", score_boost, count_boost,
                    f"Three Meetings ({direction}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'} [TRANSFORMED]")
                
                # Note: Transformations are additive - original elements are preserved
                
                interaction_log.append({
                    "type": "THREE_MEETINGS",
                    "pattern": direction,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "seasonal_strength": seasonal,
                    "transformation": element,
                    "calculation": f"+{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'}"
                })
    
    # 2. PUNISHMENTS (刑) - Negative
    for punishment, info in PUNISHMENTS.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= len(required):
            # Self-punishment
            if len(set(required)) == 1:
                if len([i for i in indices if branches_data[i]["branch"] == required[0]]) >= 2:
                    mark_branches(indices[:2])
                    adjacent = are_adjacent(indices[:2])
                    
                    branch = required[0]
                    element = EARTHLY_BRANCHES[branch]["element"]
                    polarity = EARTHLY_BRANCHES[branch]["polarity"]
                    
                    current_score = element_scores.get(f"{polarity} {element}", 0)
                    current_count = element_counts.get(f"{polarity} {element}", 0)
                    reduction_pct = 0.25 if info["effect"] == "Medium" else 0.35
                    if adjacent:
                        reduction_pct *= 1.3
                    
                    score_reduction = -current_score * reduction_pct
                    count_reduction = -current_count * reduction_pct * 0.5  # Counts reduce less
                    
                    apply_element_change(element, polarity, score_reduction, count_reduction,
                        f"Self-Punishment ({punishment}): -{reduction_pct*100:.0f}% {'(adjacent)' if adjacent else ''}")
                    
                    interaction_log.append({
                        "type": "PUNISHMENT",
                        "pattern": punishment,
                        "branches": [branches_data[i]["branch"] for i in indices[:2]],
                        "adjacent": adjacent,
                        "base_reduction": info.get("base_reduction", 10),
                        "calculation": f"-{reduction_pct*100:.0f}% of {element}"
                    })
            else:
                # Regular punishment
                found_branches = [branches_data[i]["branch"] for i in indices]
                if set(found_branches[:len(required)]) == set(required):
                    mark_branches(indices[:len(required)])
                    adjacent = are_adjacent(indices[:len(required)])
                    
                    effect_pct = {
                        "Low": 0.15, "Medium": 0.20, 
                        "High": 0.30, "Very High": 0.40
                    }.get(info["effect"], 0.20)
                    
                    if adjacent:
                        effect_pct *= 1.3
                    
                    for branch in required:
                        element = EARTHLY_BRANCHES[branch]["element"]
                        polarity = EARTHLY_BRANCHES[branch]["polarity"]
                        current_score = element_scores.get(f"{polarity} {element}", 0)
                        current_count = element_counts.get(f"{polarity} {element}", 0)
                        score_reduction = -current_score * effect_pct
                        count_reduction = -current_count * effect_pct * 0.5
                        
                        apply_element_change(element, polarity, score_reduction, count_reduction,
                            f"Punishment ({punishment}): -{effect_pct*100:.0f}% {'(adjacent)' if adjacent else ''}")
                    
                    # Apply hidden Qi interactions
                    if len(required) == 2:
                        apply_hidden_qi_interactions_v2(required[0], required[1], "PUNISHMENT", adjacent)
                    
                    interaction_log.append({
                        "type": "PUNISHMENT",
                        "pattern": punishment,
                        "branches": found_branches[:len(required)],
                        "adjacent": adjacent,
                        "base_reduction": info.get("base_reduction", 10),
                        "calculation": f"-{effect_pct*100:.0f}% of each element"
                    })
    
    # 3. HARMS (害) - Negative
    for harm, info in HARMS.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                adjacent = are_adjacent(indices[:2])
                
                effect_pct = {"Low": 0.10, "Medium": 0.15, "High": 0.20}.get(info["effect"], 0.15)
                if adjacent:
                    effect_pct *= 1.3
                
                for branch in required:
                    element = EARTHLY_BRANCHES[branch]["element"]
                    polarity = EARTHLY_BRANCHES[branch]["polarity"]
                    current_score = element_scores.get(f"{polarity} {element}", 0)
                    current_count = element_counts.get(f"{polarity} {element}", 0)
                    score_reduction = -current_score * effect_pct
                    count_reduction = -current_count * effect_pct * 0.5
                    
                    apply_element_change(element, polarity, score_reduction, count_reduction,
                        f"Harm ({harm}): -{effect_pct*100:.0f}% {'(adjacent)' if adjacent else ''}")
                
                # Apply hidden Qi interactions
                apply_hidden_qi_interactions_v2(required[0], required[1], "HARM", adjacent)
                
                interaction_log.append({
                    "type": "HARM",
                    "pattern": harm,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "base_reduction": info.get("base_reduction", 10),
                    "calculation": f"-{effect_pct*100:.0f}% + hidden Qi"
                })
    
    # 4. CLASHES (沖) - Negative
    for clash, info in CLASHES.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                adjacent = are_adjacent(indices[:2])
                
                branch1, branch2 = required
                elem1 = EARTHLY_BRANCHES[branch1]["element"]
                pol1 = EARTHLY_BRANCHES[branch1]["polarity"]
                elem2 = EARTHLY_BRANCHES[branch2]["element"]
                pol2 = EARTHLY_BRANCHES[branch2]["polarity"]
                
                # Same element clash (e.g., Chou-Wei both Earth)
                if elem1 == elem2:
                    reduction_pct = 0.25
                    if adjacent:
                        reduction_pct *= 1.3
                    
                    for branch in required:
                        element = EARTHLY_BRANCHES[branch]["element"]
                        polarity = EARTHLY_BRANCHES[branch]["polarity"]
                        current_score = element_scores.get(f"{polarity} {element}", 0)
                        current_count = element_counts.get(f"{polarity} {element}", 0)
                        score_reduction = -current_score * reduction_pct
                        count_reduction = -current_count * reduction_pct * 0.5
                        
                        apply_element_change(element, polarity, score_reduction, count_reduction,
                            f"Clash ({clash}): Same element -{reduction_pct*100:.0f}% {'(adjacent)' if adjacent else ''}")
                
                # Opposing element clash
                else:
                    effect_multiplier = {
                        "Medium": 0.30, "High": 0.35, "Very High": 0.45
                    }.get(info["effect"], 0.35)
                    
                    if adjacent:
                        effect_multiplier *= 1.3
                    
                    score1 = element_scores.get(f"{pol1} {elem1}", 0)
                    count1 = element_counts.get(f"{pol1} {elem1}", 0)
                    score2 = element_scores.get(f"{pol2} {elem2}", 0)
                    count2 = element_counts.get(f"{pol2} {elem2}", 0)
                    
                    apply_element_change(elem1, pol1, -score1 * effect_multiplier, -count1 * effect_multiplier * 0.5,
                        f"Clash ({clash}): Opposing -{effect_multiplier*100:.0f}% {'(adjacent)' if adjacent else ''}")
                    apply_element_change(elem2, pol2, -score2 * effect_multiplier, -count2 * effect_multiplier * 0.5,
                        f"Clash ({clash}): Opposing -{effect_multiplier*100:.0f}% {'(adjacent)' if adjacent else ''}")
                
                # Apply hidden Qi interactions (index-based)
                apply_hidden_qi_interactions_v2(branch1, branch2, "CLASH", adjacent)
                
                interaction_log.append({
                    "type": "CLASH",
                    "pattern": clash,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "base_reduction": info.get("base_reduction", 10),
                    "same_element": elem1 == elem2,
                    "calculation": f"Main: -{25 if elem1==elem2 else 35-45}% + Hidden Qi[0,1]"
                })
    
    # 5. DESTRUCTION (破) - Negative
    for destruction, info in DESTRUCTION.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                adjacent = are_adjacent(indices[:2])
                
                effect_pct = {"Low": 0.08, "Medium": 0.12, "High": 0.15}.get(info["effect"], 0.10)
                if adjacent:
                    effect_pct *= 1.3
                
                for branch in required:
                    element = EARTHLY_BRANCHES[branch]["element"]
                    polarity = EARTHLY_BRANCHES[branch]["polarity"]
                    current_score = element_scores.get(f"{polarity} {element}", 0)
                    current_count = element_counts.get(f"{polarity} {element}", 0)
                    score_reduction = -current_score * effect_pct
                    count_reduction = -current_count * effect_pct * 0.5
                    
                    apply_element_change(element, polarity, score_reduction, count_reduction,
                        f"Destruction ({destruction}): -{effect_pct*100:.0f}% {'(adjacent)' if adjacent else ''}")
                
                apply_hidden_qi_interactions_v2(required[0], required[1], "DESTRUCTION", adjacent)
                
                interaction_log.append({
                    "type": "DESTRUCTION",
                    "pattern": destruction,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "base_reduction": info.get("base_reduction", 10),
                    "calculation": f"-{effect_pct*100:.0f}% + hidden Qi[0,1]"
                })
    
    # 6. THREE COMBINATIONS (三合) - Positive
    for element, required in THREE_COMBINATIONS.items():
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 3:
            found_branches = [branches_data[i]["branch"] for i in indices[:3]]
            if set(found_branches) == set(required):
                # Check if transformation element exists in Heavenly Stems
                heavenly_stems = []
                for pillar_name, pillar_str in bazi_chart.items():
                    if pillar_name.endswith("_pillar"):
                        hs = pillar_str.split(" ")[0]
                        heavenly_stems.append(HEAVENLY_STEMS[hs]["element"])
                
                has_element_in_hs = element in heavenly_stems
                
                mark_branches(indices[:3])
                adjacent = are_adjacent(indices[:3])
                seasonal = get_season_strength(element)
                
                if has_element_in_hs:
                    # Successful transformation - full effect
                    apply_transformation(indices[:3], element, f"Three Combinations ({element})")
                    
                    base_boost = 35
                    total_boost = base_boost * seasonal
                    if adjacent:
                        total_boost *= 1.3
                    
                    # Pure element boost (equal to Yang and Yin)
                    score_boost = total_boost * 0.5
                    count_boost = 1.2
                    
                    apply_element_change(element, "Yang", score_boost, count_boost,
                        f"Three Combinations ({element}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'} [TRANSFORMED]")
                    apply_element_change(element, "Yin", score_boost, count_boost,
                        f"Three Combinations ({element}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'} [TRANSFORMED]")
                    
                    # Note: Transformations are additive - original elements are preserved
                    
                    transformation_status = "SUCCESSFUL"
                else:
                    # Failed transformation - partial effect only
                    base_boost = 12  # Much weaker boost
                    total_boost = base_boost * seasonal
                    if adjacent:
                        total_boost *= 1.3
                    
                    score_boost = total_boost * 0.5
                    count_boost = 0.4
                    
                    apply_element_change(element, "Yang", score_boost, count_boost,
                        f"Three Combinations ({element}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'} [PARTIAL - no {element} in HS]")
                    apply_element_change(element, "Yin", score_boost, count_boost,
                        f"Three Combinations ({element}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'} [PARTIAL - no {element} in HS]")
                    
                    transformation_status = "PARTIAL"
                
                interaction_log.append({
                    "type": "THREE_COMBINATIONS",
                    "element": element,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "seasonal_strength": seasonal,
                    "transformation": transformation_status,
                    "has_element_in_hs": has_element_in_hs,
                    "calculation": f"+{base_boost}% {'transform' if has_element_in_hs else 'partial'}"
                })
    
    # 7. SIX HARMONIES (六合) - Positive (Transformation)
    for harmony, info in SIX_HARMONIES.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                element = info["element"]
                
                # Check if transformation element exists in Heavenly Stems
                heavenly_stems = []
                for pillar_name, pillar_str in bazi_chart.items():
                    if pillar_name.endswith("_pillar"):
                        hs = pillar_str.split(" ")[0]
                        heavenly_stems.append(HEAVENLY_STEMS[hs]["element"])
                
                has_element_in_hs = element in heavenly_stems
                
                mark_branches(indices[:2])
                adjacent = are_adjacent(indices[:2])
                seasonal = get_season_strength(element)
                
                if has_element_in_hs:
                    # Successful transformation - full effect
                    apply_transformation(indices[:2], element, f"Six Harmonies ({harmony})")
                    
                    base_boost = 20
                    total_boost = base_boost * seasonal
                    if adjacent:
                        total_boost *= 1.3
                    
                    # Pure element transformation
                    score_boost = total_boost * 0.5
                    count_boost = 0.8
                    
                    apply_element_change(element, "Yang", score_boost, count_boost,
                        f"Six Harmonies ({harmony}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'} [TRANSFORMED]")
                    apply_element_change(element, "Yin", score_boost, count_boost,
                        f"Six Harmonies ({harmony}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'} [TRANSFORMED]")
                    
                    # Note: Transformations are additive - original elements are preserved
                    
                    transformation_status = "SUCCESSFUL"
                else:
                    # Failed transformation - partial effect only
                    base_boost = 8  # Much weaker boost
                    total_boost = base_boost * seasonal
                    if adjacent:
                        total_boost *= 1.3
                    
                    score_boost = total_boost * 0.5
                    count_boost = 0.3
                    
                    apply_element_change(element, "Yang", score_boost, count_boost,
                        f"Six Harmonies ({harmony}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'} [PARTIAL - no {element} in HS]")
                    apply_element_change(element, "Yin", score_boost, count_boost,
                        f"Six Harmonies ({harmony}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'} [PARTIAL - no {element} in HS]")
                    
                    transformation_status = "PARTIAL"
                
                interaction_log.append({
                    "type": "SIX_HARMONIES",
                    "pattern": harmony,
                    "element": element,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "seasonal_strength": seasonal,
                    "transformation": transformation_status,
                    "has_element_in_hs": has_element_in_hs,
                    "calculation": f"+{base_boost}% {'transform' if has_element_in_hs else 'partial'}"
                })
    
    # 8. HALF COMBINATIONS (半合) - Positive (Partial Transformation)
    for combo, info in HALF_COMBINATIONS.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                
                element = info["element"]
                adjacent = are_adjacent(indices[:2])
                seasonal = get_season_strength(element)
                
                base_boost = 12
                total_boost = base_boost * seasonal
                if adjacent:
                    total_boost *= 1.3
                
                score_boost = total_boost * 0.5
                count_boost = 0.4
                
                apply_element_change(element, "Yang", score_boost, count_boost,
                    f"Half Combination ({combo}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'}")
                apply_element_change(element, "Yin", score_boost, count_boost,
                    f"Half Combination ({combo}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'}")
                
                interaction_log.append({
                    "type": "HALF_COMBINATION",
                    "pattern": combo,
                    "element": element,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "seasonal_strength": seasonal,
                    "calculation": f"+{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'}"
                })
    
    # 9. ARCHED COMBINATIONS (拱合) - Positive (Weakest)
    for combo, info in ARCHED_COMBINATIONS.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                
                element = info["element"]
                seasonal = get_season_strength(element)
                
                base_boost = 8
                total_boost = base_boost * seasonal
                
                score_boost = total_boost * 0.5
                count_boost = 0.3
                
                apply_element_change(element, "Yang", score_boost, count_boost,
                    f"Arched Combination ({combo}): +{base_boost}% × {seasonal:.1f} (missing {info['missing']})")
                apply_element_change(element, "Yin", score_boost, count_boost,
                    f"Arched Combination ({combo}): +{base_boost}% × {seasonal:.1f} (missing {info['missing']})")
                
                interaction_log.append({
                    "type": "ARCHED_COMBINATION",
                    "pattern": combo,
                    "element": element,
                    "branches": found_branches,
                    "missing": info["missing"],
                    "seasonal_strength": seasonal,
                    "calculation": f"+{base_boost}% × {seasonal:.1f}"
                })
    
    # Calculate summary statistics
    total_positive_changes = sum(log["score_change"] for log in interaction_log 
                                 if isinstance(log, dict) and "score_change" in log and log["score_change"] > 0)
    total_negative_changes = sum(log["score_change"] for log in interaction_log 
                                 if isinstance(log, dict) and "score_change" in log and log["score_change"] < 0)
    
    return {
        "naive_scores": naive_scores,
        "interaction_log": interaction_log,
        "element_changes": [log for log in interaction_log if "score_change" in log],
        "final_scores": {
            "scores": element_scores,
            "counts": element_counts
        },
        "transformed_chart": transformed_chart,
        "transformations": transformations,
        "summary": {
            "total_interactions": len([log for log in interaction_log if "type" in log]),
            "total_positive_changes": round(total_positive_changes, 1),
            "total_negative_changes": round(total_negative_changes, 1),
            "net_change": round(total_positive_changes + total_negative_changes, 1),
            "total_transformations": len(transformations)
        }
    }


def calculate_element_scores_with_interactions_v2(bazi_chart: Dict, month_branch: str = None) -> Dict:
    """
    Enhanced BaZi interaction calculator with explicit percentage-based calculations
    and hidden Qi interactions.
    
    Key Improvements:
    - Explicit percentage reductions/boosts with clear reasoning
    - Hidden Qi interactions for clashes and other patterns
    - Proper handling of same-element vs opposing-element interactions
    - Detailed documentation of each calculation
    """
    from copy import deepcopy
    
    # Get naive element scores first
    naive_scores = naive_element_scores(bazi_chart)
    element_scores = deepcopy(naive_scores["scores"])
    
    # Extract branches and their positions
    branches_data = []
    pillar_order = ["year_pillar", "month_pillar", "day_pillar", "hour_pillar"]
    
    for idx, pillar_key in enumerate(pillar_order):
        if pillar_key in bazi_chart:
            pillar = bazi_chart[pillar_key]
            if isinstance(pillar, str) and " " in pillar:
                hs, eb = pillar.split(" ")
                branches_data.append({
                    "branch": eb,
                    "position": idx,
                    "pillar": pillar_key,
                    "marked": False
                })
    
    # Interaction log to track all changes
    interaction_log = []
    
    def mark_branches(branch_indices):
        """Mark branches as used in interaction."""
        for idx in branch_indices:
            branches_data[idx]["marked"] = True
    
    def are_adjacent(indices):
        """Check if branch indices are adjacent."""
        sorted_indices = sorted(indices)
        for i in range(len(sorted_indices) - 1):
            if sorted_indices[i+1] - sorted_indices[i] == 1:
                return True
        return False
    
    def get_season_strength(element):
        """Get seasonal strength multiplier based on month branch."""
        if not month_branch:
            return 1.0
        
        states = ELEMENT_SEASONAL_STATES.get(element, {})
        if month_branch in states.get("Prosperous", []):
            return 1.5  # 50% boost when prosperous
        elif month_branch in states.get("Strengthening", []):
            return 1.2  # 20% boost when strengthening
        elif month_branch in states.get("Resting", []):
            return 1.0  # Normal strength
        elif month_branch in states.get("Trapped", []):
            return 0.8  # 20% reduction when trapped
        elif month_branch in states.get("Dead", []):
            return 0.5  # 50% reduction when dead
        return 1.0
    
    def apply_element_change(element, polarity, amount, reason):
        """Apply element score change and log it."""
        key = f"{polarity} {element}"
        old_score = element_scores.get(key, 0)
        element_scores[key] = max(0, old_score + amount)
        
        interaction_log.append({
            "element": key,
            "change": amount,
            "old_score": old_score,
            "new_score": element_scores[key],
            "reason": reason
        })
    
    def apply_hidden_qi_interactions(branch1, branch2, interaction_type, adjacent):
        """
        Apply interactions between hidden Qi of two branches.
        This is crucial for clashes and other interactions.
        """
        qi1 = EARTHLY_BRANCHES[branch1]["qi"]
        qi2 = EARTHLY_BRANCHES[branch2]["qi"]
        
        # Elemental interaction rules
        destructive_cycle = {
            "Water": "Fire",    # Water extinguishes Fire
            "Fire": "Metal",    # Fire melts Metal
            "Metal": "Wood",    # Metal cuts Wood
            "Wood": "Earth",    # Wood breaks Earth
            "Earth": "Water"    # Earth absorbs Water
        }
        
        for qi1_info in qi1:
            hs1 = qi1_info["stem"]
            strength1 = qi1_info["score"] / 100.0
            elem1 = HEAVENLY_STEMS[hs1]["element"]
            pol1 = HEAVENLY_STEMS[hs1]["polarity"]
            
            for qi2_info in qi2:
                hs2 = qi2_info["stem"]
                strength2 = qi2_info["score"] / 100.0
                elem2 = HEAVENLY_STEMS[hs2]["element"]
                pol2 = HEAVENLY_STEMS[hs2]["polarity"]
                
                # Check if elem1 destroys elem2
                if destructive_cycle.get(elem1) == elem2:
                    # Calculate reduction based on Qi strengths
                    base_reduction = -10 * strength1 * strength2
                    if interaction_type == "CLASH":
                        base_reduction *= 0.5  # 50% of Qi strength for clashes
                    elif interaction_type == "HARM":
                        base_reduction *= 0.3  # 30% for harms
                    elif interaction_type == "DESTRUCTION":
                        base_reduction *= 0.2  # 20% for destructions
                    
                    if adjacent:
                        base_reduction *= 1.3  # 30% stronger when adjacent
                    
                    apply_element_change(elem2, pol2, base_reduction,
                        f"Hidden Qi: {hs1}({elem1}) {interaction_type.lower()}s {hs2}({elem2}) in {branch1}-{branch2}")
                
                # Check if elem2 destroys elem1
                elif destructive_cycle.get(elem2) == elem1:
                    base_reduction = -10 * strength2 * strength1
                    if interaction_type == "CLASH":
                        base_reduction *= 0.5
                    elif interaction_type == "HARM":
                        base_reduction *= 0.3
                    elif interaction_type == "DESTRUCTION":
                        base_reduction *= 0.2
                    
                    if adjacent:
                        base_reduction *= 1.3
                    
                    apply_element_change(elem1, pol1, base_reduction,
                        f"Hidden Qi: {hs2}({elem2}) {interaction_type.lower()}s {hs1}({elem1}) in {branch2}-{branch1}")
    
    # 1. THREE MEETINGS (三會) - Highest Priority
    for direction, required in THREE_MEETINGS.items():
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 3:
            found_branches = [branches_data[i]["branch"] for i in indices[:3]]
            if set(found_branches) == set(required):
                mark_branches(indices[:3])
                
                # Determine element
                if "Wood" in direction:
                    element = "Wood"
                elif "Fire" in direction:
                    element = "Fire"
                elif "Metal" in direction:
                    element = "Metal"
                elif "Water" in direction:
                    element = "Water"
                else:
                    continue
                
                adjacent = are_adjacent(indices[:3])
                seasonal = get_season_strength(element)
                
                # Base transformation: 40% boost to the meeting element
                base_boost = 40
                total_boost = base_boost * seasonal
                
                if adjacent:
                    total_boost *= 1.3  # 30% bonus for adjacent
                
                # Apply boost (60% Yang, 40% Yin distribution)
                apply_element_change(element, "Yang", total_boost * 0.6,
                    f"Three Meetings ({direction}): +{base_boost}% base × {seasonal:.1f} season × {'1.3 adjacent' if adjacent else '1.0'}")
                apply_element_change(element, "Yin", total_boost * 0.4,
                    f"Three Meetings ({direction}): +{base_boost}% base × {seasonal:.1f} season × {'1.3 adjacent' if adjacent else '1.0'}")
                
                # Note: Transformations are additive - original elements are preserved
                
                interaction_log.append({
                    "type": "THREE_MEETINGS",
                    "pattern": direction,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "seasonal_strength": seasonal,
                    "calculation": f"+{base_boost}% × {seasonal:.1f} season × {'1.3 adj' if adjacent else '1.0'}"
                })
    
    # 2. PUNISHMENTS (刑) - Negative
    for punishment, info in PUNISHMENTS.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= len(required):
            # Self-punishment
            if len(set(required)) == 1:
                if len([i for i in indices if branches_data[i]["branch"] == required[0]]) >= 2:
                    mark_branches(indices[:2])
                    adjacent = are_adjacent(indices[:2])
                    
                    branch = required[0]
                    element = EARTHLY_BRANCHES[branch]["element"]
                    polarity = EARTHLY_BRANCHES[branch]["polarity"]
                    
                    # Self-punishment: -25% of element
                    current_score = element_scores.get(f"{polarity} {element}", 0)
                    reduction_pct = 0.25 if info["effect"] == "Medium" else 0.35
                    if adjacent:
                        reduction_pct *= 1.3
                    
                    reduction = -current_score * reduction_pct
                    apply_element_change(element, polarity, reduction,
                        f"Self-Punishment ({punishment}): -{reduction_pct*100:.0f}% {'(adjacent)' if adjacent else ''}")
                    
                    interaction_log.append({
                        "type": "PUNISHMENT",
                        "pattern": punishment,
                        "branches": [branches_data[i]["branch"] for i in indices[:2]],
                        "adjacent": adjacent,
                        "base_reduction": info.get("base_reduction", 10),
                        "calculation": f"-{reduction_pct*100:.0f}% of {element}"
                    })
            else:
                # Regular punishment
                found_branches = [branches_data[i]["branch"] for i in indices]
                if set(found_branches[:len(required)]) == set(required):
                    mark_branches(indices[:len(required)])
                    adjacent = are_adjacent(indices[:len(required)])
                    
                    # Effect percentages based on base reduction
                    effect_pct = {
                        "Low": 0.15, "Medium": 0.20, 
                        "High": 0.30, "Very High": 0.40
                    }.get(info["effect"], 0.20)
                    
                    if adjacent:
                        effect_pct *= 1.3
                    
                    for branch in required:
                        element = EARTHLY_BRANCHES[branch]["element"]
                        polarity = EARTHLY_BRANCHES[branch]["polarity"]
                        current_score = element_scores.get(f"{polarity} {element}", 0)
                        reduction = -current_score * effect_pct
                        
                        apply_element_change(element, polarity, reduction,
                            f"Punishment ({punishment}): -{effect_pct*100:.0f}% {'(adjacent)' if adjacent else ''}")
                    
                    # Apply hidden Qi interactions
                    if len(required) == 2:
                        apply_hidden_qi_interactions(required[0], required[1], "PUNISHMENT", adjacent)
                    
                    interaction_log.append({
                        "type": "PUNISHMENT",
                        "pattern": punishment,
                        "branches": found_branches[:len(required)],
                        "adjacent": adjacent,
                        "base_reduction": info.get("base_reduction", 10),
                        "calculation": f"-{effect_pct*100:.0f}% of each element"
                    })
    
    # 3. HARMS (害) - Negative
    for harm, info in HARMS.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                adjacent = are_adjacent(indices[:2])
                
                # Harm percentages
                effect_pct = {"Low": 0.10, "Medium": 0.15, "High": 0.20}.get(info["effect"], 0.15)
                if adjacent:
                    effect_pct *= 1.3
                
                for branch in required:
                    element = EARTHLY_BRANCHES[branch]["element"]
                    polarity = EARTHLY_BRANCHES[branch]["polarity"]
                    current_score = element_scores.get(f"{polarity} {element}", 0)
                    reduction = -current_score * effect_pct
                    
                    apply_element_change(element, polarity, reduction,
                        f"Harm ({harm}): -{effect_pct*100:.0f}% {'(adjacent)' if adjacent else ''}")
                
                # Apply hidden Qi interactions
                apply_hidden_qi_interactions(required[0], required[1], "HARM", adjacent)
                
                interaction_log.append({
                    "type": "HARM",
                    "pattern": harm,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "base_reduction": info.get("base_reduction", 10),
                    "calculation": f"-{effect_pct*100:.0f}% of each element + hidden Qi"
                })
    
    # 4. CLASHES (沖) - Negative (Most Complex)
    for clash, info in CLASHES.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                adjacent = are_adjacent(indices[:2])
                
                branch1, branch2 = required
                elem1 = EARTHLY_BRANCHES[branch1]["element"]
                pol1 = EARTHLY_BRANCHES[branch1]["polarity"]
                elem2 = EARTHLY_BRANCHES[branch2]["element"]
                pol2 = EARTHLY_BRANCHES[branch2]["polarity"]
                
                # Same element clash (e.g., Earth vs Earth)
                if elem1 == elem2:
                    # Both reduce by 25%
                    reduction_pct = 0.25
                    if adjacent:
                        reduction_pct *= 1.3
                    
                    for branch in required:
                        element = EARTHLY_BRANCHES[branch]["element"]
                        polarity = EARTHLY_BRANCHES[branch]["polarity"]
                        current_score = element_scores.get(f"{polarity} {element}", 0)
                        reduction = -current_score * reduction_pct
                        
                        apply_element_change(element, polarity, reduction,
                            f"Clash ({clash}): Same element -{reduction_pct*100:.0f}% {'(adjacent)' if adjacent else ''}")
                
                # Opposing element clash (Water-Fire, Wood-Metal)
                else:
                    # Stronger reduction: 40-50%
                    effect_multiplier = {
                        "Medium": 0.30, "High": 0.35, "Very High": 0.45
                    }.get(info["effect"], 0.35)
                    
                    if adjacent:
                        effect_multiplier *= 1.3
                    
                    score1 = element_scores.get(f"{pol1} {elem1}", 0)
                    score2 = element_scores.get(f"{pol2} {elem2}", 0)
                    
                    reduction1 = -score1 * effect_multiplier
                    reduction2 = -score2 * effect_multiplier
                    
                    apply_element_change(elem1, pol1, reduction1,
                        f"Clash ({clash}): Opposing -{effect_multiplier*100:.0f}% {'(adjacent)' if adjacent else ''}")
                    apply_element_change(elem2, pol2, reduction2,
                        f"Clash ({clash}): Opposing -{effect_multiplier*100:.0f}% {'(adjacent)' if adjacent else ''}")
                
                # Always apply hidden Qi interactions for clashes
                apply_hidden_qi_interactions(branch1, branch2, "CLASH", adjacent)
                
                interaction_log.append({
                    "type": "CLASH",
                    "pattern": clash,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "base_reduction": info.get("base_reduction", 10),
                    "same_element": elem1 == elem2,
                    "calculation": f"Main: -{25 if elem1==elem2 else 35-45}% + Hidden Qi interactions"
                })
    
    # 5. DESTRUCTION (破) - Negative
    for destruction, info in DESTRUCTION.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                adjacent = are_adjacent(indices[:2])
                
                # Destruction percentages
                effect_pct = {"Low": 0.08, "Medium": 0.12, "High": 0.15}.get(info["effect"], 0.10)
                if adjacent:
                    effect_pct *= 1.3
                
                for branch in required:
                    element = EARTHLY_BRANCHES[branch]["element"]
                    polarity = EARTHLY_BRANCHES[branch]["polarity"]
                    current_score = element_scores.get(f"{polarity} {element}", 0)
                    reduction = -current_score * effect_pct
                    
                    apply_element_change(element, polarity, reduction,
                        f"Destruction ({destruction}): -{effect_pct*100:.0f}% {'(adjacent)' if adjacent else ''}")
                
                # Apply hidden Qi interactions
                apply_hidden_qi_interactions(required[0], required[1], "DESTRUCTION", adjacent)
                
                interaction_log.append({
                    "type": "DESTRUCTION",
                    "pattern": destruction,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "base_reduction": info.get("base_reduction", 10),
                    "calculation": f"-{effect_pct*100:.0f}% + hidden Qi"
                })
    
    # 6. THREE COMBINATIONS (三合) - Positive
    for element, required in THREE_COMBINATIONS.items():
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 3:
            found_branches = [branches_data[i]["branch"] for i in indices[:3]]
            if set(found_branches) == set(required):
                mark_branches(indices[:3])
                adjacent = are_adjacent(indices[:3])
                seasonal = get_season_strength(element)
                
                # Base boost: 35%
                base_boost = 35
                total_boost = base_boost * seasonal
                if adjacent:
                    total_boost *= 1.3
                
                # Boost the combination element
                apply_element_change(element, "Yang", total_boost * 0.6,
                    f"Three Combinations ({element}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'}")
                apply_element_change(element, "Yin", total_boost * 0.4,
                    f"Three Combinations ({element}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'}")
                
                # Note: Transformations are additive - original elements are preserved
                
                interaction_log.append({
                    "type": "THREE_COMBINATIONS",
                    "element": element,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "seasonal_strength": seasonal,
                    "calculation": f"+{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'}"
                })
    
    # 7. SIX HARMONIES (六合) - Positive (With Transformation)
    for harmony, info in SIX_HARMONIES.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                adjacent = are_adjacent(indices[:2])
                
                element = info["element"]
                seasonal = get_season_strength(element)
                
                # Base boost: 20%
                base_boost = 20
                total_boost = base_boost * seasonal
                if adjacent:
                    total_boost *= 1.3
                
                # Boost transformation element
                apply_element_change(element, "Yang", total_boost * 0.6,
                    f"Six Harmonies ({harmony}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'}")
                apply_element_change(element, "Yin", total_boost * 0.4,
                    f"Six Harmonies ({harmony}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'}")
                
                # Note: Transformations are additive - original elements are preserved
                
                interaction_log.append({
                    "type": "SIX_HARMONIES",
                    "pattern": harmony,
                    "element": element,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "seasonal_strength": seasonal,
                    "calculation": f"+{base_boost}% transform (additive)"
                })
    
    # 8. HALF COMBINATIONS (半合) - Positive
    for combo, info in HALF_COMBINATIONS.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                adjacent = are_adjacent(indices[:2])
                
                element = info["element"]
                seasonal = get_season_strength(element)
                
                # Base boost: 12% (weaker than full combinations)
                base_boost = 12
                total_boost = base_boost * seasonal
                if adjacent:
                    total_boost *= 1.3
                
                apply_element_change(element, "Yang", total_boost * 0.6,
                    f"Half Combination ({combo}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'}")
                apply_element_change(element, "Yin", total_boost * 0.4,
                    f"Half Combination ({combo}): +{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'}")
                
                interaction_log.append({
                    "type": "HALF_COMBINATION",
                    "pattern": combo,
                    "element": element,
                    "branches": found_branches,
                    "adjacent": adjacent,
                    "seasonal_strength": seasonal,
                    "calculation": f"+{base_boost}% × {seasonal:.1f} × {'1.3 adj' if adjacent else '1.0'}"
                })
    
    # 9. ARCHED COMBINATIONS (拱合) - Positive (Weakest)
    for combo, info in ARCHED_COMBINATIONS.items():
        required = info["branches"]
        indices = [i for i, b in enumerate(branches_data) 
                  if b["branch"] in required and not b["marked"]]
        
        if len(indices) >= 2:
            found_branches = [branches_data[i]["branch"] for i in indices[:2]]
            if set(found_branches) == set(required):
                mark_branches(indices[:2])
                
                element = info["element"]
                seasonal = get_season_strength(element)
                
                # Base boost: 8% (weakest, no adjacent bonus)
                base_boost = 8
                total_boost = base_boost * seasonal
                
                apply_element_change(element, "Yang", total_boost * 0.6,
                    f"Arched Combination ({combo}): +{base_boost}% × {seasonal:.1f} (missing {info['missing']})")
                apply_element_change(element, "Yin", total_boost * 0.4,
                    f"Arched Combination ({combo}): +{base_boost}% × {seasonal:.1f} (missing {info['missing']})")
                
                interaction_log.append({
                    "type": "ARCHED_COMBINATION",
                    "pattern": combo,
                    "element": element,
                    "branches": found_branches,
                    "missing": info["missing"],
                    "seasonal_strength": seasonal,
                    "calculation": f"+{base_boost}% × {seasonal:.1f}"
                })
    
    # Calculate summary statistics
    total_positive_changes = sum(log["change"] for log in interaction_log 
                                 if isinstance(log, dict) and "change" in log and log["change"] > 0)
    total_negative_changes = sum(log["change"] for log in interaction_log 
                                 if isinstance(log, dict) and "change" in log and log["change"] < 0)
    
    return {
        "naive_scores": naive_scores,
        "interaction_log": interaction_log,
        "element_changes": [log for log in interaction_log if "change" in log],
        "final_scores": {
            "scores": element_scores,
            "counts": naive_scores["counts"]
        },
        "summary": {
            "total_interactions": len([log for log in interaction_log if "type" in log]),
            "total_positive_changes": round(total_positive_changes, 1),
            "total_negative_changes": round(total_negative_changes, 1),
            "net_change": round(total_positive_changes + total_negative_changes, 1)
        }
    }


# * =================
# * PATTERN ANALYZERS (interaction.py)
# * =================

def count_element_in_heavenly_stems(chart: Dict[str, str], element: str) -> int:
    """Count occurrences of an element in chart's Heavenly Stems."""
    count = 0
    for pillar_value in chart.values():
        if isinstance(pillar_value, str):
            hs = pillar_value.split(" ")[0]
            if hs in HEAVENLY_STEMS and HEAVENLY_STEMS[hs]["element"] == element:
                count += 1
    return count


def get_seasonal_state(branches: List[str], element: str) -> Optional[str]:
    """Determine the seasonal state of an element based on branches present."""
    if element not in ELEMENT_SEASONAL_STATES:
        return None
    
    states = ELEMENT_SEASONAL_STATES[element]
    
    # Check each state category
    for state, state_branches in states.items():
        if any(branch in state_branches for branch in branches):
            return state
    
    return None


def analyze_seasonal_directions(bazi_chart: Dict) -> Dict:
    """Analyze a BaZi chart for three seasonal direction patterns."""
    results = {
        "found": False,
        "patterns": [],
        "transformations": {},
        "analysis": ""
    }
    
    # Get earthly branches from the chart
    branches = []
    pillar_keys = ["year_pillar", "month_pillar", "day_pillar", "hour_pillar", 
                   "luck_10_year", "luck_annual"]
    
    for key in pillar_keys:
        if key in bazi_chart and bazi_chart[key]:
            if isinstance(bazi_chart[key], str):
                parts = bazi_chart[key].split(" ")
                if len(parts) == 2:
                    branches.append(parts[1])
    
    # Check for each seasonal direction pattern
    for direction, required_branches in THREE_MEETINGS.items():
        if all(branch in branches for branch in required_branches):
            results["found"] = True
            
            # Determine the transformation element
            if direction == "Eastern Wood":
                element = "Wood"
            elif direction == "Southern Fire":
                element = "Fire"
            elif direction == "Western Metal":
                element = "Metal"
            else:  # Northern Water
                element = "Water"
            
            # Count existing element strength
            hs_count = count_element_in_heavenly_stems(bazi_chart, element)
            
            # Get seasonal state
            seasonal_state = get_seasonal_state(branches, element)
            
            pattern_info = {
                "type": direction,
                "branches": required_branches,
                "transformation_element": element,
                "heavenly_stem_support": hs_count,
                "seasonal_state": seasonal_state,
                "strength": "Very Strong" if hs_count >= 2 else "Strong" if hs_count == 1 else "Moderate"
            }
            
            results["patterns"].append(pattern_info)
            
            # Record transformation
            for branch in required_branches:
                results["transformations"][branch] = {
                    "original": EARTHLY_BRANCHES[branch]["element"],
                    "transformed": element,
                    "pattern": direction
                }
    
    # Generate analysis
    if results["found"]:
        for pattern in results["patterns"]:
            results["analysis"] += f"Found {pattern['type']} pattern with branches "
            results["analysis"] += f"{', '.join(pattern['branches'])}. "
            results["analysis"] += f"Transforms to {pattern['transformation_element']} element. "
            results["analysis"] += f"Strength: {pattern['strength']} "
            results["analysis"] += f"(HS support: {pattern['heavenly_stem_support']}, "
            results["analysis"] += f"Seasonal: {pattern['seasonal_state'] or 'Neutral'}). "
    else:
        results["analysis"] = "No complete Three Seasonal Direction patterns found."
    
    # Generate permutations for detailed pattern matching
    permutations = generate_hs_eb_permutations(bazi_chart)
    
    # Find all partial patterns (2 out of 3 branches)
    partial_patterns = []
    for direction, required_branches in THREE_MEETINGS.items():
        branches_found = [b for b in required_branches if b in branches]
        if len(branches_found) == 2:
            missing = [b for b in required_branches if b not in branches_found][0]
            partial_patterns.append({
                "type": f"Partial {direction}",
                "branches_found": branches_found,
                "missing_branch": missing,
                "completion": "66.7%"
            })
    
    if partial_patterns:
        results["partial_patterns"] = partial_patterns
        results["analysis"] += f"\n\nPartial patterns detected: "
        for partial in partial_patterns:
            results["analysis"] += f"\n- {partial['type']}: has {', '.join(partial['branches_found'])}, "
            results["analysis"] += f"missing {partial['missing_branch']}"
    
    return results


def analyze_three_combinations(bazi_chart: Dict) -> Dict:
    """Analyze a BaZi chart for three combination patterns."""
    results = {
        "found": False,
        "patterns": [],
        "transformations": {},
        "analysis": ""
    }
    
    # Get earthly branches from the chart
    branches = []
    pillar_keys = ["year_pillar", "month_pillar", "day_pillar", "hour_pillar", 
                   "luck_10_year", "luck_annual"]
    
    for key in pillar_keys:
        if key in bazi_chart and bazi_chart[key]:
            if isinstance(bazi_chart[key], str):
                parts = bazi_chart[key].split(" ")
                if len(parts) == 2:
                    branches.append(parts[1])
    
    # Check for each three combination pattern
    for element, required_branches in THREE_COMBINATIONS.items():
        if all(branch in branches for branch in required_branches):
            results["found"] = True
            
            # Count existing element strength in Heavenly Stems
            hs_count = count_element_in_heavenly_stems(bazi_chart, element)
            
            # Get seasonal state
            seasonal_state = get_seasonal_state(branches, element)
            
            pattern_info = {
                "type": f"{element} Combination",
                "branches": required_branches,
                "transformation_element": element,
                "heavenly_stem_support": hs_count,
                "seasonal_state": seasonal_state,
                "strength": "Very Strong" if hs_count >= 2 else "Strong" if hs_count == 1 else "Moderate"
            }
            
            results["patterns"].append(pattern_info)
            
            # Record transformation
            for branch in required_branches:
                results["transformations"][branch] = {
                    "original": EARTHLY_BRANCHES[branch]["element"],
                    "transformed": element,
                    "pattern": f"{element} Combination"
                }
    
    # Generate analysis
    if results["found"]:
        for pattern in results["patterns"]:
            results["analysis"] += f"Found {pattern['type']} with branches "
            results["analysis"] += f"{', '.join(pattern['branches'])}. "
            results["analysis"] += f"Transforms to {pattern['transformation_element']} element. "
            results["analysis"] += f"Strength: {pattern['strength']} "
            results["analysis"] += f"(HS support: {pattern['heavenly_stem_support']}, "
            results["analysis"] += f"Seasonal: {pattern['seasonal_state'] or 'Neutral'}). "
    else:
        results["analysis"] = "No complete Three Combination patterns found."
    
    # Generate permutations for detailed pattern matching
    permutations = generate_hs_eb_permutations(bazi_chart)
    
    # Find all partial patterns (2 out of 3 branches)
    partial_patterns = []
    for element, required_branches in THREE_COMBINATIONS.items():
        branches_found = [b for b in required_branches if b in branches]
        if len(branches_found) == 2:
            missing = [b for b in required_branches if b not in branches_found][0]
            partial_patterns.append({
                "type": f"Partial {element} Combination",
                "branches_found": branches_found,
                "missing_branch": missing,
                "completion": "66.7%"
            })
    
    if partial_patterns:
        results["partial_patterns"] = partial_patterns
        results["analysis"] += f"\n\nPartial patterns detected: "
        for partial in partial_patterns:
            results["analysis"] += f"\n- {partial['type']}: has {', '.join(partial['branches_found'])}, "
            results["analysis"] += f"missing {partial['missing_branch']}"
    
    return results


def analyze_six_harmonies(bazi_chart: Dict) -> Dict:
    """Analyze a BaZi chart for six harmony patterns."""
    results = {
        "found": False,
        "patterns": [],
        "transformations": {},
        "analysis": ""
    }
    
    # Get earthly branches from the chart
    branches = []
    branch_positions = {}  # Track which pillar each branch comes from
    pillar_keys = ["year_pillar", "month_pillar", "day_pillar", "hour_pillar", 
                   "luck_10_year", "luck_annual"]
    
    for key in pillar_keys:
        if key in bazi_chart and bazi_chart[key]:
            if isinstance(bazi_chart[key], str):
                parts = bazi_chart[key].split(" ")
                if len(parts) == 2:
                    branch = parts[1]
                    branches.append(branch)
                    branch_positions[branch] = key
    
    # Check for each six harmony pattern
    for harmony_name, harmony_info in SIX_HARMONIES.items():
        required_branches = harmony_info["branches"]
        if all(branch in branches for branch in required_branches):
            results["found"] = True
            
            # Determine transformation element
            element = harmony_info["element"]
            
            # For Wu-Wei, it can transform to either Fire or Earth
            if element == "Fire/Earth":
                # Check which element has more support
                fire_count = count_element_in_heavenly_stems(bazi_chart, "Fire")
                earth_count = count_element_in_heavenly_stems(bazi_chart, "Earth")
                element = "Fire" if fire_count >= earth_count else "Earth"
            
            # Count existing element strength in Heavenly Stems
            hs_count = count_element_in_heavenly_stems(bazi_chart, element)
            
            # Get seasonal state
            seasonal_state = get_seasonal_state(branches, element)
            
            # Determine positions of the harmonizing branches
            positions = [branch_positions.get(b, "unknown") for b in required_branches]
            
            pattern_info = {
                "type": f"{harmony_name} Harmony",
                "branches": required_branches,
                "transformation_element": element,
                "heavenly_stem_support": hs_count,
                "seasonal_state": seasonal_state,
                "positions": positions,
                "strength": "Very Strong" if hs_count >= 2 else "Strong" if hs_count == 1 else "Moderate"
            }
            
            results["patterns"].append(pattern_info)
            
            # Record transformation
            for branch in required_branches:
                results["transformations"][branch] = {
                    "original": EARTHLY_BRANCHES[branch]["element"],
                    "transformed": element,
                    "pattern": harmony_name
                }
    
    # Generate analysis
    if results["found"]:
        for pattern in results["patterns"]:
            results["analysis"] += f"Found {pattern['type']} with branches "
            results["analysis"] += f"{', '.join(pattern['branches'])} at positions "
            results["analysis"] += f"{', '.join(pattern['positions'])}. "
            results["analysis"] += f"Transforms to {pattern['transformation_element']} element. "
            results["analysis"] += f"Strength: {pattern['strength']} "
            results["analysis"] += f"(HS support: {pattern['heavenly_stem_support']}, "
            results["analysis"] += f"Seasonal: {pattern['seasonal_state'] or 'Neutral'}). "
    else:
        results["analysis"] = "No Six Harmony patterns found."
    
    # Generate permutations for detailed pattern matching
    permutations = generate_hs_eb_permutations(bazi_chart)
    
    # Check for potential harmonies if missing branches were added
    potential_patterns = []
    for harmony_name, harmony_info in SIX_HARMONIES.items():
        required_branches = harmony_info["branches"]
        branches_found = [b for b in required_branches if b in branches]
        if len(branches_found) == 1:
            missing = [b for b in required_branches if b not in branches_found][0]
            potential_patterns.append({
                "type": f"Potential {harmony_name}",
                "has_branch": branches_found[0],
                "needs_branch": missing,
                "would_transform_to": harmony_info["element"]
            })
    
    if potential_patterns:
        results["potential_patterns"] = potential_patterns
        results["analysis"] += f"\n\nPotential harmonies if branches added: "
        for potential in potential_patterns:
            results["analysis"] += f"\n- {potential['type']}: has {potential['has_branch']}, "
            results["analysis"] += f"needs {potential['needs_branch']} to transform to {potential['would_transform_to']}"
    
    return results


def analyze_half_combinations(bazi_chart: Dict) -> Dict:
    """Analyze a BaZi chart for half combination patterns."""
    results = {
        "found": False,
        "patterns": [],
        "transformations": {},
        "analysis": ""
    }
    
    # Get earthly branches from the chart
    branches = []
    branch_positions = {}
    pillar_keys = ["year_pillar", "month_pillar", "day_pillar", "hour_pillar", 
                   "luck_10_year", "luck_annual"]
    
    for key in pillar_keys:
        if key in bazi_chart and bazi_chart[key]:
            if isinstance(bazi_chart[key], str):
                parts = bazi_chart[key].split(" ")
                if len(parts) == 2:
                    branch = parts[1]
                    branches.append(branch)
                    branch_positions[branch] = key
    
    # Check for each half combination pattern
    for combo_name, combo_info in HALF_COMBINATIONS.items():
        required_branches = combo_info["branches"]
        if all(branch in branches for branch in required_branches):
            results["found"] = True
            
            element = combo_info["element"]
            full_combo = combo_info["full_combo"]
            
            # Find the missing branch for the full combination
            full_branches = full_combo.split("-")
            missing_branch = [b for b in full_branches if b not in required_branches][0]
            
            # Count existing element strength
            hs_count = count_element_in_heavenly_stems(bazi_chart, element)
            
            # Get seasonal state
            seasonal_state = get_seasonal_state(branches, element)
            
            # Determine positions
            positions = [branch_positions.get(b, "unknown") for b in required_branches]
            
            pattern_info = {
                "type": f"{combo_name} Half Combination",
                "branches": required_branches,
                "transformation_element": element,
                "missing_for_full": missing_branch,
                "full_combination": full_combo,
                "heavenly_stem_support": hs_count,
                "seasonal_state": seasonal_state,
                "positions": positions,
                "strength": "Strong" if hs_count >= 2 else "Moderate" if hs_count == 1 else "Weak"
            }
            
            results["patterns"].append(pattern_info)
            
            # Record partial transformation (50% strength)
            for branch in required_branches:
                results["transformations"][branch] = {
                    "original": EARTHLY_BRANCHES[branch]["element"],
                    "transformed": element,
                    "pattern": combo_name,
                    "transformation_strength": "50%"
                }
    
    # Generate analysis
    if results["found"]:
        for pattern in results["patterns"]:
            results["analysis"] += f"Found {pattern['type']} with branches "
            results["analysis"] += f"{', '.join(pattern['branches'])} at positions "
            results["analysis"] += f"{', '.join(pattern['positions'])}. "
            results["analysis"] += f"Partially transforms to {pattern['transformation_element']} element. "
            results["analysis"] += f"Missing {pattern['missing_for_full']} for full {pattern['full_combination']} combination. "
            results["analysis"] += f"Strength: {pattern['strength']} "
            results["analysis"] += f"(HS support: {pattern['heavenly_stem_support']}, "
            results["analysis"] += f"Seasonal: {pattern['seasonal_state'] or 'Neutral'}). "
    else:
        results["analysis"] = "No Half Combination patterns found."
    
    # Generate permutations for detailed pattern matching
    permutations = generate_hs_eb_permutations(bazi_chart)
    
    # Check if adding the missing branch would complete any half combinations
    enhancement_opportunities = []
    for pattern in results.get("patterns", []):
        enhancement_opportunities.append({
            "current_pattern": pattern["type"],
            "add_branch": pattern["missing_for_full"],
            "result": f"Complete {pattern['full_combination']} combination",
            "element_boost": pattern["transformation_element"]
        })
    
    if enhancement_opportunities:
        results["enhancement_opportunities"] = enhancement_opportunities
        results["analysis"] += f"\n\nEnhancement opportunities: "
        for opp in enhancement_opportunities:
            results["analysis"] += f"\n- Adding {opp['add_branch']} would complete "
            results["analysis"] += f"{opp['result']} (boosting {opp['element_boost']})"
    
    return results


def analyze_arched_combinations(bazi_chart: Dict) -> Dict:
    """Analyze a BaZi chart for arched combination patterns."""
    results = {
        "found": False,
        "patterns": [],
        "transformations": {},
        "analysis": ""
    }
    
    # Get earthly branches from the chart
    branches = []
    branch_positions = {}
    pillar_keys = ["year_pillar", "month_pillar", "day_pillar", "hour_pillar", 
                   "luck_10_year", "luck_annual"]
    
    for key in pillar_keys:
        if key in bazi_chart and bazi_chart[key]:
            if isinstance(bazi_chart[key], str):
                parts = bazi_chart[key].split(" ")
                if len(parts) == 2:
                    branch = parts[1]
                    branches.append(branch)
                    branch_positions[branch] = key
    
    # Check for each arched combination pattern
    for combo_name, combo_info in ARCHED_COMBINATIONS.items():
        required_branches = combo_info["branches"]
        if all(branch in branches for branch in required_branches):
            results["found"] = True
            
            element = combo_info["element"]
            missing_branch = combo_info["missing"]
            
            # Count existing element strength
            hs_count = count_element_in_heavenly_stems(bazi_chart, element)
            
            # Get seasonal state
            seasonal_state = get_seasonal_state(branches, element)
            
            # Determine positions
            positions = [branch_positions.get(b, "unknown") for b in required_branches]
            
            # Calculate distance between branches
            pillar_order = ["year_pillar", "month_pillar", "day_pillar", "hour_pillar", 
                           "luck_10_year", "luck_annual"]
            pos_indices = [pillar_order.index(branch_positions.get(b, "unknown")) 
                          for b in required_branches if branch_positions.get(b) in pillar_order]
            
            if len(pos_indices) == 2:
                distance = abs(pos_indices[0] - pos_indices[1])
            else:
                distance = "unknown"
            
            pattern_info = {
                "type": f"{combo_name} Arched Combination",
                "branches": required_branches,
                "transformation_element": element,
                "missing_middle": missing_branch,
                "heavenly_stem_support": hs_count,
                "seasonal_state": seasonal_state,
                "positions": positions,
                "distance": distance,
                "strength": "Moderate" if hs_count >= 2 else "Weak" if hs_count == 1 else "Very Weak"
            }
            
            results["patterns"].append(pattern_info)
            
            # Record weak transformation (30% strength due to missing middle)
            for branch in required_branches:
                results["transformations"][branch] = {
                    "original": EARTHLY_BRANCHES[branch]["element"],
                    "transformed": element,
                    "pattern": combo_name,
                    "transformation_strength": "30%",
                    "note": f"Missing {missing_branch} in middle"
                }
    
    # Generate analysis
    if results["found"]:
        for pattern in results["patterns"]:
            results["analysis"] += f"Found {pattern['type']} with branches "
            results["analysis"] += f"{', '.join(pattern['branches'])} at positions "
            results["analysis"] += f"{', '.join(pattern['positions'])}. "
            results["analysis"] += f"Weakly transforms to {pattern['transformation_element']} element. "
            results["analysis"] += f"Missing middle branch {pattern['missing_middle']} for full combination. "
            if pattern['distance'] != "unknown":
                results["analysis"] += f"Distance between branches: {pattern['distance']} pillars. "
            results["analysis"] += f"Strength: {pattern['strength']} "
            results["analysis"] += f"(HS support: {pattern['heavenly_stem_support']}, "
            results["analysis"] += f"Seasonal: {pattern['seasonal_state'] or 'Neutral'}). "
    else:
        results["analysis"] = "No Arched Combination patterns found."
    
    # Generate permutations for detailed pattern matching
    permutations = generate_hs_eb_permutations(bazi_chart)
    
    # Check for completion opportunities
    completion_opportunities = []
    for pattern in results.get("patterns", []):
        # Determine what would happen if the missing middle was added
        full_branches = pattern["branches"] + [pattern["missing_middle"]]
        full_combo_name = "-".join(sorted(full_branches))
        
        # Check which full combination this would create
        for element, combo_branches in THREE_COMBINATIONS.items():
            if set(full_branches) == set(combo_branches):
                completion_opportunities.append({
                    "current_pattern": pattern["type"],
                    "add_branch": pattern["missing_middle"],
                    "result": f"Complete {element} Three Combination",
                    "transformation_boost": f"30% to 100% {element}"
                })
                break
    
    if completion_opportunities:
        results["completion_opportunities"] = completion_opportunities
        results["analysis"] += f"\n\nCompletion opportunities: "
        for opp in completion_opportunities:
            results["analysis"] += f"\n- Adding {opp['add_branch']} would {opp['result']} "
            results["analysis"] += f"({opp['transformation_boost']})"
    
    return results


def find_punishment_matches(permutations: List[Dict], chart: Dict[str, str]) -> List[Dict]:
    """Find all punishment pattern matches in the permutations."""
    matches = []
    
    for perm_data in permutations:
        branches_in_perm = [elem["char"] for elem in perm_data["elements"]]
        
        for punishment_name, punishment_info in PUNISHMENTS.items():
            required_branches = punishment_info["branches"]
            
            # Check if all required branches are in this permutation
            if set(required_branches) == set(branches_in_perm):
                # Found a match
                match_info = {
                    "pattern_name": punishment_name,
                    "branches": branches_in_perm,
                    "positions": perm_data["positions"],
                    "type": punishment_info["type"],
                    "base_reduction": punishment_info.get("base_reduction", 10),
                    "description": punishment_info["description"],
                    "distance": perm_data.get("distance") or perm_data.get("avg_distance"),
                    "adjacency": perm_data["adjacency"]
                }
                
                # Check for additional context
                # Count how many of same element in Heavenly Stems
                elements_affected = set()
                for branch in branches_in_perm:
                    elements_affected.add(EARTHLY_BRANCHES[branch]["element"])
                
                match_info["elements_affected"] = list(elements_affected)
                
                # Determine severity based on distance and adjacency
                base_reduction = punishment_info.get("base_reduction", 10)
                if perm_data["adjacency"] in ["adjacent", "adjacent_inner", "adjacent_outer", "all_adjacent"]:
                    match_info["severity"] = "High" if base_reduction >= 15 else "Moderate"
                else:
                    match_info["severity"] = "Moderate" if base_reduction >= 12 else "Low"
                
                matches.append(match_info)
    
    return matches


def analyze_punishments(bazi_chart: Dict) -> Dict:
    """Analyze a BaZi chart for punishment patterns."""
    results = {
        "found": False,
        "patterns": [],
        "analysis": ""
    }
    
    # Generate permutations for pattern matching
    permutations = generate_hs_eb_permutations(bazi_chart)
    
    # Check 2-branch punishments
    two_branch_matches = find_punishment_matches(
        permutations["eb_2_permutations"], 
        bazi_chart
    )
    
    # Check 3-branch punishments
    three_branch_matches = find_punishment_matches(
        permutations["eb_3_permutations"], 
        bazi_chart
    )
    
    # Combine all matches
    all_matches = two_branch_matches + three_branch_matches
    
    if all_matches:
        results["found"] = True
        results["patterns"] = all_matches
        
        # Generate analysis
        results["analysis"] = f"Found {len(all_matches)} punishment pattern(s):\n\n"
        
        for i, pattern in enumerate(all_matches, 1):
            results["analysis"] += f"{i}. {pattern['pattern_name']} ({pattern['type']})\n"
            results["analysis"] += f"   Branches: {', '.join(pattern['branches'])} at {pattern['positions']}\n"
            results["analysis"] += f"   Base Reduction: {pattern.get('base_reduction', 10)}%\n"
            results["analysis"] += f"   Severity: {pattern['severity']} (based on {pattern['adjacency']} positioning)\n"
            results["analysis"] += f"   Description: {pattern['description']}\n"
            results["analysis"] += f"   Elements Affected: {', '.join(pattern['elements_affected'])}\n\n"
        
        # Add summary
        high_severity = [p for p in all_matches if p["severity"] == "High"]
        if high_severity:
            results["analysis"] += f"⚠️ Warning: {len(high_severity)} high-severity punishment(s) detected.\n"
            results["analysis"] += "These may indicate significant challenges or conflicts in the chart."
    else:
        results["analysis"] = "No punishment patterns found in the chart."
    
    # Check for near-miss patterns (missing one branch)
    near_misses = []
    branches = []
    for key in ["year_pillar", "month_pillar", "day_pillar", "hour_pillar", 
                "luck_10_year", "luck_annual"]:
        if key in bazi_chart and bazi_chart[key]:
            if isinstance(bazi_chart[key], str):
                parts = bazi_chart[key].split(" ")
                if len(parts) == 2:
                    branches.append(parts[1])
    
    for punishment_name, punishment_info in PUNISHMENTS.items():
        required = punishment_info["branches"]
        found = [b for b in required if b in branches]
        
        if len(required) == 2 and len(found) == 1:
            missing = [b for b in required if b not in found][0]
            near_misses.append({
                "pattern": punishment_name,
                "has": found[0],
                "needs": missing,
                "type": punishment_info["type"]
            })
        elif len(required) == 3 and len(found) == 2:
            missing = [b for b in required if b not in found][0]
            near_misses.append({
                "pattern": punishment_name,
                "has": ", ".join(found),
                "needs": missing,
                "type": punishment_info["type"]
            })
    
    if near_misses:
        results["near_misses"] = near_misses
        results["analysis"] += "\n\nNear-miss patterns (caution if missing branch appears):\n"
        for nm in near_misses:
            results["analysis"] += f"- {nm['pattern']}: has {nm['has']}, needs {nm['needs']}\n"
    
    return results


def find_harm_matches(permutations: List[Dict], chart: Dict[str, str]) -> List[Dict]:
    """Find all harm pattern matches in the permutations."""
    
    matches = []
    
    for perm_data in permutations:
        branches_in_perm = [elem["char"] for elem in perm_data["elements"]]
        
        for harm_name, harm_info in HARMS.items():
            required_branches = harm_info["branches"]
            
            # Check if both required branches are in this permutation
            if set(required_branches) == set(branches_in_perm):
                # Found a match
                match_info = {
                    "pattern_name": harm_name,
                    "branches": branches_in_perm,
                    "positions": perm_data["positions"],
                    "base_reduction": harm_info.get("base_reduction", 10),
                    "description": harm_info["description"],
                    "distance": perm_data["distance"],
                    "adjacency": perm_data["adjacency"]
                }
                
                # Determine impact based on adjacency
                if perm_data["adjacency"] in ["adjacent", "adjacent_inner", "adjacent_outer"]:
                    match_info["impact"] = "Strong"
                else:
                    match_info["impact"] = "Moderate"
                
                matches.append(match_info)
    
    return matches


def analyze_harm_combinations(bazi_chart: Dict) -> Dict:
    """Analyze a BaZi chart for harm combination patterns."""
    results = {
        "found": False,
        "patterns": [],
        "analysis": ""
    }
    
    # Generate permutations for pattern matching
    permutations = generate_hs_eb_permutations(bazi_chart)
    
    # Find all harm matches
    harm_matches = find_harm_matches(
        permutations["eb_2_permutations"], 
        bazi_chart
    )
    
    if harm_matches:
        results["found"] = True
        results["patterns"] = harm_matches
        
        # Generate analysis
        results["analysis"] = f"Found {len(harm_matches)} harm pattern(s):\n\n"
        
        for i, pattern in enumerate(harm_matches, 1):
            results["analysis"] += f"{i}. {pattern['pattern_name']} Harm\n"
            results["analysis"] += f"   Branches: {', '.join(pattern['branches'])} at {pattern['positions']}\n"
            results["analysis"] += f"   Base Reduction: {pattern.get('base_reduction', 10)}%\n"
            results["analysis"] += f"   Impact: {pattern['impact']} (based on {pattern['adjacency']} positioning)\n"
            results["analysis"] += f"   Description: {pattern['description']}\n\n"
        
        # Add summary
        strong_impact = [p for p in harm_matches if p["impact"] == "Strong"]
        if strong_impact:
            results["analysis"] += f"Note: {len(strong_impact)} harm pattern(s) with strong impact detected.\n"
            results["analysis"] += "These may indicate minor obstacles or irritations."
    else:
        results["analysis"] = "No harm patterns found in the chart."
    
    # Check for potential harm patterns
    branches = []
    for key in ["year_pillar", "month_pillar", "day_pillar", "hour_pillar", 
                "luck_10_year", "luck_annual"]:
        if key in bazi_chart and bazi_chart[key]:
            if isinstance(bazi_chart[key], str):
                parts = bazi_chart[key].split(" ")
                if len(parts) == 2:
                    branches.append(parts[1])
    
    potential_harms = []
    for harm_name, harm_info in HARMS.items():
        required = harm_info["branches"]
        found = [b for b in required if b in branches]
        
        if len(found) == 1:
            missing = [b for b in required if b not in found][0]
            potential_harms.append({
                "pattern": harm_name,
                "has": found[0],
                "needs": missing,
                "base_reduction": harm_info.get("base_reduction", 10)
            })
    
    if potential_harms:
        results["potential_patterns"] = potential_harms
        results["analysis"] += "\n\nPotential harm patterns (if missing branch appears):\n"
        for ph in potential_harms:
            results["analysis"] += f"- {ph['pattern']}: has {ph['has']}, needs {ph['needs']} (Effect: {ph['effect']})\n"
    
    return results
