# AGENTS.md

Guidance for AI agents working on **Bazingse** - a BaZi (四柱八字) Calculator with backend API.

**Status**: Production-ready API with 8-26 node extensible architecture, comprehensive test suite.

---

## 🚨 CRITICAL: Pattern-Based Thinking (READ THIS FIRST!)

**When given an example, NEVER hardcode for just that one case. Always identify the pattern and apply it universally.**

### ❌ WRONG Approach:
```
User: "Add distance field to SIX_HARMONIES interactions"
Agent: *Only adds distance to SIX_HARMONIES*
Result: 23 other interaction types still missing distance field!
```

### ✅ CORRECT Approach:
```
User: "Add distance field to SIX_HARMONIES interactions"  
Agent: 
  1. Understands: User wants distance for scoring transparency
  2. Searches: How many interaction types exist? (grep for interaction_log.append)
  3. Discovers: 14 interaction types, 24 locations total
  4. Applies: Adds distance to ALL interaction types (THREE_MEETINGS, STEM_COMBINATIONS, CLASHES, etc.)
  5. Verifies: Checks that ALL interactions now have distance field
Result: Complete fix, no follow-up needed!
```

### Pattern Recognition Examples:

**Example 1: Field Additions**
- Given: "Add X field to Y"
- Think: Where else does Y pattern appear? Apply to ALL instances.

**Example 2: Bug Fixes**  
- Given: "Fix distance calculation for eb_y-eb_m"
- Think: Is this a systemic issue? Check ALL node pairs, not just this one.

**Example 3: Refactoring**
- Given: "Use node IDs instead of positions in get_distance_key()"
- Think: How many places call get_distance_key()? Fix ALL of them.

### Key Questions to Ask:
1. **"Is this a single instance or a pattern?"** (Usually a pattern!)
2. **"Where else does this pattern occur?"** (Search with grep/Glob)
3. **"What's the root cause?"** (Fix the source, not symptoms)
4. **"Are there similar cases?"** (Apply fix universally)

### Tools for Pattern Discovery:
```bash
# Find all similar patterns
grep -n "pattern" file.py
rg "pattern" --type py

# Count occurrences
grep -c "pattern" file.py

# Find all interaction types
grep "interaction_log.append" | wc -l
```

**REMEMBER: Examples are teaching tools, not literal instructions. Think systematically, act comprehensively.**

---

## Critical BaZi Principles

### 1. Earthly Branch Polarity Rules (MOST IMPORTANT)

**CRITICAL: Different rules for transformations vs. energy flow!**

#### A. EB Transformations (Combinations)
**When Earthly Branches transform through combinations, use BRANCH polarity for the badge.**

Applies to: THREE_MEETINGS, THREE_COMBINATIONS, SIX_HARMONIES, HALF_COMBINATIONS, ARCHED_COMBINATIONS

**Examples:**
- Si 巳 (Yin branch) → Fire transformation uses **Ding** 丁 (Yin Fire badge)
- Wu 午 (Yang branch) → Fire transformation uses **Bing** 丙 (Yang Fire badge)
- Wei 未 (Yin branch) → Fire transformation uses **Ding** 丁 (Yin Fire badge)

**Implementation:** In `transform_to_element()`, use `EARTHLY_BRANCHES[branch_id]["polarity"]`

#### B. Energy Flow (Natural Production)
**When Earthly Branches generate elements through WuXing cycle, use PRIMARY QI polarity.**

Applies to: Natural element generation, receiver nodes in energy flow

**Examples:**
- Si 巳 (Yin branch) has Bing 丙 (Yang) primary → Produces **Geng** 庚 (Yang Metal)
- Wu 午 (Yang branch) has Ding 丁 (Yin) primary → Produces **Xin** 辛 (Yin Metal)
- Chou 丑 (Yin branch) has Ji 己 (Yin) primary → Produces **Xin** 辛 (Yin Metal)

**Implementation:** Use `get_primary_qi_polarity(branch_id)` helper in `add_element()` calls

#### Summary Table

| Context | Use | Example |
|---------|-----|---------|
| EB Transformation Badge | Branch Polarity | Si (Yin) → Fire = Ding badge |
| Energy Generation/Flow | Primary Qi Polarity | Si (Bing Yang primary) → Metal = Geng |

### 2. BaZi Is Deterministic
**Use constants, never dynamic functions.** All mappings are fixed forever.

```python
# ✅ CORRECT: Deterministic constants
ELEMENT_CHARACTERS = {"Wood": "木", "Fire": "火", ...}
ELEMENT_POLARITY_TO_STEM = {"Yang Wood": "Jia", "Yin Wood": "Yi", ...}
ELEMENT_POLARITY_STEMS = {("Wood", "Yang"): "Jia", ...}  # Tuple keys

# ❌ WRONG: Dynamic lookup functions
def get_element_character(name): ...  # Don't do this!
```

### 3. Interaction Logic Flow
All interactions follow this sequence:

1. **DETECTION**: Required stems/branches present?
2. **DISTANCE**: Adjacent (0), nearby (1), or far (2+)?
3. **TRANSFORMATION**: Transforming element exists?
   - HS combinations: Check if target element exists in **ANY EB** (including luck pillars!)
   - EB combinations: Check if target element exists in **ANY HS**

### 4. Transformation Tracking
- **EB Transformations**: `node.transformed = True`, ID changes (Si → Fire element)
- **HS Combinations**: `node.transformed = True`, ID stays same but gets `transformation_badge` (Bing stays Bing, gains Water qi, badge shows Ren)
- **Response builder**: Use `node.transformed` flag directly, NOT ID comparison

## Architecture

### File Structure
```
app/
├── library.py (2,380 lines)   # All BaZi constants (deterministic!)
├── bazingse.py (3,671 lines)  # Core interaction engine (8-26 nodes)
├── chart_constructor.py (241 lines) # Pillar generation (uses sxtwl)
├── routes.py (313 lines)      # FastAPI endpoint /analyze_bazi
└── interaction.py (2,750 lines) # Legacy/reference (not used)

run_bazingse.py                # Entry point (uvicorn on port 8008)
test_analyze_bazi.py           # Python test suite
test_analyze_bazi.sh           # Bash test suite
```

### Node System (8-26 nodes)
**Natal (8)**: `hs_y`, `hs_m`, `hs_d`, `hs_h`, `eb_y`, `eb_m`, `eb_d`, `eb_h`  
**10-Year Luck (2)**: `hs_10yl`, `eb_10yl` (when `analysis_year` provided)  
**Annual (2)**: `hs_yl`, `eb_yl`  
**Monthly (2)**: `hs_ml`, `eb_ml` (when `analysis_month` provided)  
**Daily (2)**: `hs_dl`, `eb_dl` (when `analysis_day` provided)  
**Hourly (2)**: `hs_hl`, `eb_hl` (when `analysis_time` provided)  
**Talisman (0-8)**: `hs_ty`, `eb_ty`, `hs_tm`, `eb_tm`, `hs_td`, `eb_td`, `hs_th`, `eb_th` (optional, user-provided for harmony)

**Note**: Talisman y/m/d/h suffixes are **positional** (slot 1-4), not semantic. Users can input ANY of the 60 pillars.

**CRITICAL**: Talismans can be **partial** - HS and EB are independent:
- HS-only: `talisman_year_hs=Jia` (creates only `hs_ty`)
- EB-only: `talisman_year_eb=Zi` (creates only `eb_ty`)
- Both: Provide both parameters (creates both nodes)
- Mixed: Any combination across slots (e.g., `year_hs + month_eb` = 2 nodes)

Each node: independent qi inventory, tracks interactions, transformation state.

### Node Response Structure
```json
{
  "base": {"id": "Bing", "qi": {"Bing": 100.0}},
  "post": {"id": "Bing", "qi": {"Bing": 58.0, "Ren": 42.0}},
  "interaction_ids": ["STEM_COMBINATION~Bing-Xin~hs_10yl-hs_yl"],
  "badges": [
    {
      "interaction_id": "STEM_COMBINATION~Bing-Xin~hs_10yl-hs_yl",
      "type": "transformation",
      "badge": "Ren",
      "size": "lg"
    }
  ],
  "transformed": true,
  "transformation_badge": "Ren",
  "alive": true,
  "interacted": ["hs_yl"]
}
```

## Key Implementation Details

### Element Production (add_element method)
```python
def add_element(self, element, amount, polarity=None):
    if polarity:
        # Specific polarity (e.g., Geng Metal, not Xin)
        # USE THIS for branch receivers with primary qi polarity
        key = f"{polarity} {element}"
        self.elements[key]["score"] += amount
    else:
        # Split 50/50 Yang/Yin (backward compatible)
        for pol in ["Yang", "Yin"]:
            self.elements[f"{pol} {element}"]["score"] += amount / 2
```

**Critical**: When adding generated elements to EB nodes, pass `polarity=get_primary_qi_polarity(node.value)`

### Transformation Check (HS Combinations)
```python
# Check ALL branches including luck pillars AND talismans
for pos in position_codes:  # Includes natal, luck, AND talismans
    eb_id = f"eb_{pos}"
    if eb_id in nodes and EARTHLY_BRANCHES[nodes[eb_id].value]["element"] == required_element:
        transforming_element_exists = True
```

**Critical**: Use `position_codes` iteration to include ALL nodes (natal, luck, talismans). Water in `eb_10yl` OR `eb_ty` can support HS transformation.

### Distance Calculation
```python
def calculate_interaction_distance(pos1, pos2):
    NATAL = [0, 1, 2, 3]         # y, m, d, h
    LUCK = [4, 5, 6, 7, 8]       # 10yl, yl, ml, dl, hl (temporal overlays)
    TALISMAN = [9, 10, 11, 12]     # ay, am, ad, ah (external harmony tools)
    
    # Luck/Talisman ↔ Natal: conceptually adjacent (distance 0)
    if (pos1 in LUCK and pos2 in NATAL) or (pos2 in LUCK and pos1 in NATAL):
        return 0
    if (pos1 in TALISMAN and pos2 in NATAL) or (pos2 in TALISMAN and pos1 in NATAL):
        return 0
    
    return abs(pos1 - pos2)  # Normal spatial distance
```

## Interaction Types

The system detects and processes **14 interaction types** across 24 code locations:

**Positive (Earthly Branch Combinations):**
1. THREE_MEETINGS (三會) - Directional combinations
2. THREE_COMBINATIONS (三合) - Triangular combinations  
3. HALF_MEETINGS (半會) - Partial directional combinations
4. SIX_HARMONIES (六合) - Pair harmonies
5. HALF_COMBINATIONS (半合) - Partial triangular combinations
6. ARCHED_COMBINATIONS (拱合) - Arched combinations

**Positive (Heavenly Stem Combinations):**
7. STEM_COMBINATIONS (天干合) - 5 stem pairs that combine

**Negative (Conflicts):**
8. STEM_CONFLICTS (天干沖) - Heavenly stem clashes (same polarity only)
9. CLASHES (地支沖) - Earthly branch oppositions
10. PUNISHMENTS (刑) - Ungrateful/power/rudeness punishments
11. HARMS (害) - Mutual harm relationships
12. DESTRUCTION (破) - Destructive relationships

**Special:**
13. SEASONAL_ADJUSTMENT - Month-based element adjustments
14. ENERGY_FLOW - Natural WuXing production cycles

## Interaction Log Structure

Every interaction in the `interactions` array follows this format:

```json
{
  "type": "SIX_HARMONIES",
  "pattern": "Yin-Hai",
  "ids_affected": ["eb_y", "eb_m"],
  "distance": "1",
  "transformed": true,
  "element": "Wood",
  "score": 35,
  "description": "Yin-Hai harmonize to Wood"
}
```

**Key Fields:**
- `distance`: Numeric string "1"/"2"/"3"/"4" (ALL interactions have this except SEASONAL_ADJUSTMENT and ENERGY_FLOW summary)
- `transformed`: Boolean `true/false` (for EB/HS combinations)
- `ids_affected`: List of node IDs affected by this interaction
- `score`: Actual score applied (after distance multipliers)

**Note**: `adjacent` field was removed (redundant with `distance: "1"`).

---

## Library.py Constants (Examples)

### Formula-Based Scoring System

All interaction scores are calculated using base scores × distance multipliers:

```python
# Base scores for each interaction type
BASE_SCORES = {
    "THREE_MEETINGS": {"combined": 35, "transformed": 61.8},
    "THREE_COMBINATIONS": {"combined": 25, "transformed": 45},
    "SIX_HARMONIES": {"combined": 18, "transformed": 35},
    "STEM_COMBINATIONS": {"combined": 19, "transformed": 38},
    # ... etc
}

# Distance multipliers (golden ratio-based)
DISTANCE_MULTIPLIERS = {
    "three_branch": {  # For THREE_MEETINGS, THREE_COMBINATIONS
        "2": 1.0,      # Three consecutive nodes (best)
        "3": 0.786,    
        "4": 0.618,    
        "5": 0.500,    
        "6": 0.382,
        "7": 0.236,    
    },
    "two_branch": {  # For all other interactions
        "1": 1.0,      # Adjacent/luck-natal
        "2": 0.618,    
        "3": 0.382,    
        "4": 0.236,    
    }
}

# Actual score = base_score × multiplier
# Example: SIX_HARMONIES transformed at distance 2
#   = 35 × 0.618 = 21.63
```

This replaces manual hardcoding in each pattern's scoring dict.

### Core Constants

```python
HEAVENLY_STEMS = {
    "Jia": {"element": "Wood", "polarity": "Yang", "chinese": "甲", ...},
    "Yi": {"element": "Wood", "polarity": "Yin", "chinese": "乙", ...},
    # ... all 10 stems
}

EARTHLY_BRANCHES = {
    "Zi": {
        "element": "Water", "polarity": "Yang", "chinese": "子",
        "qi": [{"stem": "Gui", "score": 100}, {"stem": "Ren", "score": 20}]
        # PRIMARY QI = qi[0] = Gui (Yin!)
    },
    "Si": {
        "element": "Fire", "polarity": "Yin", "chinese": "巳",
        "qi": [{"stem": "Bing", "score": 70}, ...]
        # PRIMARY QI = qi[0] = Bing (Yang!)
    },
    # ... all 12 branches
}

STEM_COMBINATIONS = {
    "Bing-Xin": {
        "transform_to": "Ren",
        "transform_element": "Water",
        "transformation_requirement": {"element": "Water", "location": "eb"},
        "scoring": {
            "combined": {      # Was "detected"
                "1": 19,        # Was "adjacent"
                "2": 14.25,
                "3": 8.87,
                "4": 5.49
            },
            "transformed": {
                "1": 38,
                "2": 28.5,
                "3": 17.75,
                "4": 11.0
            }
        }
    },
    # ... all 5 combinations
}

# All interaction patterns defined with embedded scoring:
# - EB Combinations: THREE_MEETINGS, THREE_COMBINATIONS, SIX_HARMONIES, 
#   HALF_MEETINGS, HALF_COMBINATIONS, ARCHED_COMBINATIONS
# - HS Combinations: STEM_COMBINATIONS
# - Negative: PUNISHMENTS, HARMS, CLASHES, DESTRUCTION, STEM_CONFLICTS
# - Special: SEASONAL_ADJUSTMENT, ENERGY_FLOW

# Transformation strength tiers (for future multiple transformations feature)
TRANSFORMATION_STRENGTH = {
    "THREE_MEETINGS": "strong",
    "THREE_COMBINATIONS": "normal",
    "ARCHED_COMBINATIONS": "normal",
    "SIX_HARMONIES": "weak",
    "HALF_COMBINATIONS": "weak"
}

STRENGTH_ORDER = {
    "ultra_strong": 0,
    "strong": 1,
    "normal": 2,
    "weak": 3
}
```

## API Endpoint

**GET** `/analyze_bazi`

**Required Parameters**: 
- `birth_date` (YYYY-MM-DD) - Birth date
- `gender` (male/female) - Gender for luck pillar calculation

**Optional Time Period Parameters**: 
- `birth_time` (HH:MM) - Birth time for hour pillar
- `analysis_year` (int) - Triggers 10-year luck pillar calculation
- `include_annual_luck` (bool, default: true) - Include annual luck when analysis_year provided
- `analysis_month` (1-12) - Month luck pillar (requires analysis_year)
- `analysis_day` (1-31) - Day luck pillar (requires analysis_month)
- `analysis_time` (HH:MM) - Hour luck pillar (requires analysis_day)

**Optional Talisman Parameters** (Nov 2025):
- `talisman_year_hs`, `talisman_year_eb` - Talisman slot 1 (any of 60 pillars)
- `talisman_month_hs`, `talisman_month_eb` - Talisman slot 2
- `talisman_day_hs`, `talisman_day_eb` - Talisman slot 3
- `talisman_hour_hs`, `talisman_hour_eb` - Talisman slot 4

**Optional Location Parameter** (Nov 2025):
- `location` (overseas/birthplace) - Non-interactive element boost based on residence location

**Returns**: Flat JSON structure with:
- All node data (base_qi, post_interaction_qi, badges, interactions)
- Interaction log (all 14 interaction types)
- Base/post element scores
- Daymaster analysis
- Chinese character mappings

## Development

```bash
# Setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run server
python run_bazingse.py  # http://localhost:8008

# Test
bash test_analyze_bazi.sh  # Bash test suite
python test_analyze_bazi.py  # Python test suite

# Quick test
curl "http://localhost:8008/analyze_bazi?birth_date=1990-01-15&gender=male&birth_time=13:45&analysis_year=2024"

# Test with talismans (for harmony/balance)
curl "http://localhost:8008/analyze_bazi?birth_date=1990-01-15&gender=male&talisman_year_hs=Ren&talisman_year_eb=Zi"
```

### Test Files

- `test_analyze_bazi.sh` - Bash test suite for API endpoints
- `test_analyze_bazi.py` - Python test suite for API endpoints

### Documentation

- `AGENTS.md` - This file (comprehensive coding guidelines)
- `README.md` - Project overview (currently empty)

## Core Coding Principles

### KISS (Keep It Super Simple)
**Our team is middle schoolers** - keep solutions linear and obvious.

- ❌ Over-engineering, fancy abstractions, function ping-pong
- ✅ Flat logic, direct access, simple loops
- ❌ Nested nested objects in JSON
- ✅ Flat structure, 1 level deep max

### Consistency
- Reference `library.py` for ALL constants
- Use `ELEMENT_POLARITY_STEMS[(element, polarity)]` for lookups
- Follow existing patterns exactly
- Test suite MUST pass before any commit

### Node Badge System (Oct-Nov 2025)

**Complete badge support for ALL interactions** - both positive (transformations) and negative (conflicts).

#### Badge Types (7 total)

**Positive (Additive):**
- `transformation`: Successful EB/HS combination with element support
  - Badge: Stem character of NEW element added (e.g., "Ren" for Water)
  - Color: Elemental color (green for Wood, red for Fire, etc.)
  - Size: Based on interaction strength (xl/lg/md/sm/xs)
  
- `combination`: Partial EB combination without full element support  
  - Badge: Stem character of partial element (e.g., "Yi" for partial Wood)
  - Color: Muted elemental color
  - Size: Smaller than transformation badges

**Negative (Reductive):**
- `punishment`: Xing 刑 - Punishment relationships
  - Badge: "XING" (icon identifier, not stem character)
  - Color: Neutral (not elemental)
  - Size: Based on damage severity
  
- `harm`: Hai 害 - Mutual harm relationships
  - Badge: "HAI"
  - Color: Neutral
  
- `clash`: Chong 沖 - Direct opposition  
  - Badge: "CHONG"
  - Color: Neutral
  
- `destruction`: Po 破 - Destructive relationships
  - Badge: "PO"
  - Color: Neutral
  
- `stem_conflict`: Ke 剋 - Heavenly stem conflicts (same polarity only)
  - Badge: "KE"
  - Color: Neutral

#### Badge Data Structure

**Positive Badges** (transformation/combination):
```json
{
  "interaction_id": "SIX_HARMONIES~Chen-You~eb_m-eb_h",
  "type": "transformation",
  "badge": "Xin",  // Stem ID to display (elemental character)
  "size": "sm"     // xl, lg, md, sm, xs
}
```

**Negative Badges** (punishment/harm/clash/destruction):
```json
{
  "interaction_id": "CLASH~Zi-Wu~eb_h-eb_y",
  "type": "clash",
  "badge": "CHONG",  // Icon identifier (XING, HAI, CHONG, PO)
  "size": "md"       // xl, lg, md, sm, xs
}
```

**Key Principles**: 
- **Positive badges**: Display stem character → elemental visualization
- **Negative badges**: Display icon identifier → neutral visualization  
- **Badge distribution**: 
  - Positive: Badge appears on each node showing what it gains
  - Negative: Both controller AND victim receive badges (Nov 2025 fix)
- **Size calculation**:
  - Positive: `strength_to_badge_size()` based on TRANSFORMATION_STRENGTH
  - Negative: `reduction_to_badge_size()` based on damage percentage

**Important**: STEM_CONFLICTS (stem_conflict badge type) only occur between **same polarity** stems:
- Jia (Yang Wood) vs Geng (Yang Metal) ✓ Conflict
- Yi (Yin Wood) vs Xin (Yin Metal) ✓ Conflict  
- Yi (Yin) vs Geng (Yang) ✗ No conflict (different polarities)

---

### Scoring System Refactor (Oct 2025)

**Complete overhaul of scoring structure** - moved from tuple keys to nested dicts for Python compliance.

#### Key Changes

1. **Terminology**: `"detected"` → `"combined"` (semantic clarity)
2. **Structure**: Tuple keys `("detected", "adjacent")` → Nested dicts `["combined"]["adjacent"]`
3. **Embedded Scoring**: All scoring parameters now embedded in interaction definitions (no global constants)
4. **Formula-Based**: Distance multipliers with base scores for consistency

#### Old vs New

```python
# ❌ OLD (broke with list keys)
"scoring": {
    ("detected", "adjacent"): 20,
    ("transformed", "adjacent"): 70
}
score = scoring_dict[("detected", "adjacent")]

# ✅ NEW (Python-compliant nested dicts)
"scoring": {
    "combined": {
        "adjacent": 20
    },
    "transformed": {
        "adjacent": 70
    }
}
score = scoring_dict.get("combined", {}).get("adjacent", default)
```

#### Removed Global Constants

- ❌ `THREE_COMBINATIONS_POINTS` (deleted)
- ❌ `STEM_CONFLICTS_SCORING` (deleted)
- ❌ `NATURAL_WUXING_SCORING` (deleted)  
- ❌ `HIDDEN_QI_DAMAGE` (deleted)

All scoring now embedded in: `STEM_CONFLICTS[pattern]["scoring"]`, `WUXING_ENERGY_FLOW["scoring"]`, etc.

---

### Distance Field Standardization (Oct 2025)

**ALL interactions now have numeric `distance` field** (22 of 24 interaction types).

#### Changes

1. **Removed**: `adjacent: bool` field (redundant)
2. **Added**: `distance: "1"/"2"/"3"/"4"` (numeric strings)
3. **Helper Functions**: `get_distance_key()` for 2-node, `get_distance_key_3nodes()` for 3-node
4. **Grid System**: 2D Manhattan distance (4x2 chessboard)

#### Distance Logic

```python
# 2-node interactions
distance = get_distance_key("hs_y", "eb_m")  # Returns "2"

# 3-node interactions (max pairwise distance)
distance = get_distance_key_3nodes("eb_y", "eb_m", "eb_d")  # Returns "2"

# Interaction log includes distance
{
  "type": "SIX_HARMONIES",
  "distance": "2",  # Numeric, transparent
  "transformed": true
}
```

**Implementation**: Uses `get_distance_key()` for 2-node interactions and `get_distance_key_3nodes()` for 3-node interactions.

---

### Multiple Transformations (DESIGN ONLY - NOT IMPLEMENTED)

**Status**: Design documentation exists (`TRANSFORMATION_DESIGN.md`, `MULTIPLE_TRANSFORMATIONS_SUMMARY.md`) but NOT yet implemented in code.

#### Proposed Feature

Allow nodes to track ALL transformations simultaneously (currently only tracks one):
- Node participates in THREE_MEETINGS (Si-Wu-Wei) → Fire (ultra_strong)
- Same node participates in SIX_HARMONIES (Si-Shen) → Water (normal)

#### Current State

**Code does NOT have**:
- `node.transformations = []` list
- Multiple transformation tracking
- Strength-based prioritization

**Only has**:
- Single transformation fields: `transformation_element`, `transformation_pattern`, `transformation_badge`
- `TRANSFORMATION_STRENGTH` and `STRENGTH_ORDER` constants (ready for implementation)

**Action**: If implementing this feature, follow the design principle: nodes should track all transformations they participate in, with strength-based prioritization for badge display.

---

### Recent Critical Fixes & Features (Oct-Nov 2025)

#### Fix 1: Branch Polarity for EB Transformations (CORRECTED Oct 2025)
**Problem**: EB transformation badges were using PRIMARY QI polarity instead of BRANCH polarity.
- Si 巳 (Yin branch, Bing Yang primary) → Fire was showing Bing badge ❌ → Should show Ding badge ✅
- Wu 午 (Yang branch, Ding Yin primary) → Fire was showing Ding badge ❌ → Should show Bing badge ✅
- Affected THREE_MEETINGS, THREE_COMBINATIONS, SIX_HARMONIES, etc.

**Solution**: Updated transformation badge logic to use branch's own polarity:
- `transform_to_element()` method: Now uses `EARTHLY_BRANCHES[branch_id]["polarity"]`
- `get_transformation_badge()` function: Now uses branch polarity instead of primary qi
- **Note**: Energy flow still uses primary qi polarity (different rule!)

#### Fix 2: Primary Qi Polarity for Energy Flow
**Problem**: Natural WuXing generation split 50/50 between Yang/Yin instead of targeting receiver's primary qi.
- Chou (Ji/Yin Earth) → Shen (Geng/Yang Metal) was producing 50% Geng + 50% Xin ❌
- Should produce 100% Geng (respecting Shen's Yang primary qi) ✅

**Solution**: Updated `add_element(element, amount, polarity=None)` with optional polarity parameter:
- Natural energy flow: Passes receiver's primary qi polarity (lines 1877, 1909)
- All EB combinations: Pass primary qi polarity when adding generated elements (7 locations)
- Backward compatible: `polarity=None` still splits 50/50

#### Fix 3: HS Combinations with Luck Pillars (4 bugs)
**Problem**: Bing-Xin between `hs_10yl` and `hs_yl` not transforming despite Water in `eb_10yl`.

**Bugs Fixed:**
1. **EB check missing luck pillars** (lines 1327, 1526): Now checks all EB nodes including `eb_10yl`, `eb_yl`, `eb_ml`, `eb_dl`, `eb_hl`
2. **Missing transformed flag** (lines 1387, 1602): Now sets `node.transformed = True` for HS combinations
3. **Wrong position map** (line 1538-1544): Now uses global `position_to_index` instead of hardcoded natal positions
4. **Response builder logic** (lines 2555-2558): Now uses `getattr(node, 'transformed', False)` instead of ID comparison

**Result**: All HS combinations (Jia-Ji, Yi-Geng, Bing-Xin, Ding-Ren, Wu-Gui) work correctly across natal and luck pillars.

#### Fix 4: Deterministic Constants
**Problem**: Used dynamic `get_element_character()` function for lookups.

**Solution**: Replaced with deterministic constants in `library.py`:
```python
ELEMENT_CHARACTERS = {"Wood": "木", "Yang Wood": "甲", ...}
ELEMENT_POLARITY_TO_STEM = {"Yang Wood": "Jia", ...}
```

#### Fix 5: Negative Badge Icons (Nov 2025)
**Problem**: 
1. Negative interaction badges only appeared on victim node (controller had no badge)
2. Badges used elemental stem characters instead of neutral icons

**Example**:
- Zi-You destruction: Badge only on You (victim) ❌, Zi (controller) had nothing
- Badge showed "Gui" (elemental) instead of neutral destruction icon

**Solution**: 
1. **Both nodes get badges**: Controller and victim both receive badges for ALL negative interactions
2. **Icon identifiers**: Replaced stem characters with neutral icon IDs:
   - PUNISHMENT → "XING" (刑)
   - HARM → "HAI" (害)
   - CLASH → "CHONG" (沖)
   - DESTRUCTION → "PO" (破)

**Affected Interactions**:
- DESTRUCTION (opposite + same): Both nodes get "PO"
- CLASH (opposite + same): Both nodes get "CHONG"
- HARM: Both nodes get "HAI"
- PUNISHMENT (2-node + 3-node + self): All nodes get "XING"

**Rationale**: 
- Negative interactions don't transform elements → neutral icons more appropriate
- Both participants affected → both should show visual indicator
- Easier to distinguish from positive transformation badges

#### Fix 6: STEM_CONFLICTS Missing Badges (Nov 2025)
**Problem**: STEM_CONFLICTS (天干沖) had NO badge generation - neither controller nor victim received any visual indicators despite damage being applied.

**Solution**: Added "KE" (剋 = control/restrain) badges to BOTH nodes:
- Adjacent conflicts: Badges added at line ~2041
- Non-adjacent conflicts: Badges added at line ~2261
- Both nodes (controller + victim) receive badges

**Note**: STEM_CONFLICTS only occur between SAME polarity stems:
- Jia-Geng, Yi-Xin, Bing-Ren, Ding-Gui, Wu-Gui
- Different polarities don't conflict (e.g., Yi vs Geng has no conflict)

#### Fix 7: HALF_MEETINGS Incorrect Blocking Logic (Nov 2025)
**Problem**: HALF_MEETINGS had blocking logic that prevented transformation even when the required element existed in Heavenly Stems.

**Example Case**: 1988-02-02 chart
- Hai + Chou present (HALF_MEETING pattern)
- Gui (Water) exists in HS ✓
- Blocking branches (Mao, Wei) present in chart
- Old behavior: "combined" with reason "Missing Zi blocked by Mao, Wei" ❌
- Expected: "transformed" since Water exists in HS ✅

**Root Cause**: `blocked_by` logic incorrectly checked for presence of blocking branches in chart, preventing transformation despite HS element support.

**Solution**: Removed blocking logic entirely - transformation now depends ONLY on element in Heavenly Stems (consistent with other EB combinations).

**Changes**:
```python
# OLD (lines 910-914)
all_branches = [node.value for _, _, node in branch_data]
is_blocked = any(blocker in all_branches for blocker in blocked_by)
can_transform = element in heavenly_stems_elements and not is_blocked

# NEW (lines 908-909)
can_transform = element in heavenly_stems_elements
```

**Impact**:
- HALF_MEETINGS now transform correctly when HS element exists
- Transformed boost scores apply (40 vs 20 at distance 1)
- Badge type changes from "combination" to "transformation"
- No "reason" field in interaction log
- Consistent with THREE_COMBINATIONS, SIX_HARMONIES rules

**Scoring**:
- Combined: 20 points (base)
- Transformed: 40 points (2x multiplier when HS element present)

**Note**: This fix ensures HALF_MEETINGS transform consistently with other EB combinations.

#### Fix 8: Talisman Nodes Implementation (Nov 2025)
**Feature**: Optional user-provided nodes for creating harmony and balance in charts.

**Purpose**: After analyzing natal + luck interactions, users can identify imbalances and add talisman nodes to create harmony. Talismans are external harmony tools (物 / talismans) that participate in all interactions.

**Implementation**:
- **8 new optional nodes**: hs_ty, eb_ty, hs_tm, eb_tm, hs_td, eb_td, hs_th, eb_th
- **Positional naming**: y/m/d/h suffixes are slot identifiers (1-4), NOT semantic time periods
- **Any 60 pillars**: Users can input any Heavenly Stem + Earthly Branch combination
- **Distance logic**: Talismans treated like luck pillars (distance 0 to natal, full interaction strength)
- **Pattern-based**: No special interaction logic needed - talismans automatically participate in ALL interactions

**Example**: Chart has excess Fire → Add Ren-Zi (Water) talisman → Creates Water interactions, supports transformations

**Files modified**:
- `app/routes.py`: Added 8 talisman parameters
- `app/bazingse.py`: Node creation, position mapping, distance calculation
- `app/library.py`: NODE_COORDINATES, get_distance_key() updates

**Tests**: Verified via test_analyze_bazi.sh and test_analyze_bazi.py, zero regression.

**Distance Logic**: Talismans follow same rules as 10-year luck pillar - distance 1 to all natal nodes for maximum interaction strength.

#### Fix 9: Location Boost Feature (Nov 2025)
**Feature**: Non-interactive element boost based on residence location (overseas vs birthplace).

**Purpose**: Model the metaphysical impact of living in a foreign land (水土不服 / water-earth mismatch) vs. birthplace (土生土长 / earth-born earth-raised) without creating actual nodes or interactions. Pure element addition for daymaster strength calculation.

**Key Principle**: Location is NOT a node - it's an environmental factor that adds elemental qi directly to the chart's element inventory. Think of it as "ambient qi" from the land itself.

**Implementation**:
```python
# Overseas: 2 Water pillars (Ren-Zi + Gui-Hai)
Ren (HS): 100 Yang Water
Zi (EB): 80 Yang Water + 40 Yin Water
Gui (HS): 100 Yin Water  
Hai (EB): 70 Yin Water + 30 Yang Water + 10 Yang Wood + 10 Yang Earth
Total boost: +210 Ren, +210 Gui, +10 Jia, +10 Wu

# Birthplace: 4 Earth pillars at 50% (Ji-Wei + Ji-Chou + Wu-Xu + Wu-Chen)
4 stems at 50%: (100 Ji + 100 Ji + 100 Wu + 100 Wu) * 0.5 = 200 Ji + 200 Wu
4 branches at 50%: (Wei + Chou + Xu + Chen hidden qi) * 0.5
Total boost: +195 Ji, +195 Wu, +15 Ding, +12.5 Yi, +12.5 Gui, +15 Xin
```

**Architecture Decision**: Direct element addition (no node creation)
- ✅ Simple: Just modifies element_scores dict
- ✅ No interaction risk: Not in nodes dict, can't participate in combinations/clashes
- ✅ Transparent: Clear separation between natal/luck/talisman nodes vs. environmental boost
- ✅ KISS compliant: Minimal code, maximum clarity

**Code Location**:
- `bazingse.py` line 179: Added `location` parameter to `analyze_8_node_interactions()`
- `bazingse.py` lines 2940-2979: Helper function `apply_location_boost()` and application
- `routes.py` line 74: Added API parameter with Literal type validation
- `routes.py` line 226: Passed location to analysis function

**Behavior**:
1. Boost applied to BOTH `naive_ten_elements` (base) and `final_ten_elements` (post)
2. Location elements are static - appear identically in base and post scores
3. No new interactions created - interaction count unchanged
4. Fractional values (12.5) are preserved (int-converted at response serialization)

**Testing**:
```bash
# Test overseas boost
curl "http://localhost:8008/analyze_bazi?birth_date=1990-01-15&gender=male&location=overseas"
# Ren: 0 → 210, Gui: 25 → 235

# Test birthplace boost  
curl "http://localhost:8008/analyze_bazi?birth_date=1990-01-15&gender=male&location=birthplace"
# Ji: 195 → 390, Wu: 105 → 300

# Comprehensive test suite
bash test_location_boost.sh
```

**Files modified**:
- `app/routes.py`: Added location parameter (overseas/birthplace)
- `app/bazingse.py`: Added location boost logic
- `test_location_boost.sh`: Comprehensive test suite (NEW)

**Tests**: All existing tests pass (zero regression), new test suite validates boost calculations and non-interaction guarantee.

**Design Philosophy**: Location is an environmental factor, not a structural element. Unlike talisman nodes (which ARE nodes that interact), location is ambient qi that simply adds to the chart's elemental inventory. This distinction maintains architectural clarity while modeling real BaZi principles about geographic influence.

#### Fix 10: 2-Tier Element Scoring System (Nov 2025)
**Feature**: Separate natal destiny vs. full chart element scores for clear analysis of birth destiny vs. current life situation.

**Purpose**: Enable users to distinguish between:
1. **Core natal destiny** (birth chart only, unchangeable)
2. **Full chart reality** (natal + luck + talisman + location, current life situation)

**Problem Statement**: Previous system mixed natal and luck elements in both base and post scores, making it impossible to see pure birth chart vs. current situation.

**Solution: 2-Tier Scoring with Correct Calculation**

```python
1. base_element_score   # Natal chart ONLY (8 nodes), before interactions
2. post_element_score   # ALL nodes (natal + luck + talisman + location), after interactions
```

**Key Implementation Details**:

1. **Base Score** (natal chart only, pure birth destiny):
   ```python
   natal_node_ids = {'hs_y', 'eb_y', 'hs_m', 'eb_m', 'hs_d', 'eb_d', 'hs_h', 'eb_h'}
   base_nodes = {id: nodes[id] for id in natal_node_ids if id in nodes}
   base_ten_elements = calculate_ten_element_totals(base_nodes)  # Before interactions
   ```
   - Always 6 or 8 nodes (depends on birth_time provided)
   - NO luck pillars, NO talisman, NO location boost
   - NO interactions applied
   - Pure snapshot of birth chart elements

2. **Post Score** (full chart, current life situation):
   ```python
   post_ten_elements = calculate_ten_element_totals(nodes)  # All nodes, after interactions
   if location:
       apply_location_boost(post_ten_elements, location)    # Add location
   ```
   - Includes ALL nodes: Natal (8) + Luck (0-10) + Talisman (0-8)
   - Includes location boost (overseas or birthplace)
   - ALL interactions calculated and applied
   - Represents complete current situation

3. **Interaction Effects**:
   - Natal nodes CAN be affected by luck/talisman node interactions
   - Example: 10-year luck pillar You transforms with natal Si → Metal
   - Post score includes these cross-pillar transformations
   - Base score remains pure natal (unaffected by luck interactions)

**API Response Structure**:

```json
{
  "base_element_score": {"Jia": 0, "Yi": 15, ...},   // Natal chart only, before interactions
  "post_element_score": {"Jia": 67, "Yi": 19, ...}   // All nodes + location, after interactions
}
```

**Example Analysis** (1990-01-15 male + 2024 analysis year + overseas location):

```
Base (natal chart only, before interactions):
  Ren: 0, Gui: 25 (birth chart has minimal Water)

Post (full chart: natal + luck + location, after interactions):
  Ren: 210, Gui: 275 (0 natal + 110 luck + 210 location - interactions)

Insight: Birth chart lacks Water (weak Output), but current life situation 
         (luck pillars + overseas location) provides abundant Water support.
         
Breakdown:
  - Natal: 25 Gui from birth chart
  - Luck pillars: +110 Gui from 10-year and annual
  - Location: +210 Ren + 210 Gui from overseas
  - Interactions: -70 Gui from conflicts
  = Final: 210 Ren, 275 Gui
```

**Use Cases**:

1. **Daymaster Strength**: Use `post_element_score` (full chart reality)
2. **Natal Potential**: Use `base_element_score` (unchangeable birth destiny)
3. **Life Impact**: Compare post vs base (how luck/location/interactions change situation)

**Code Changes**:
- `bazingse.py` lines 2925-2943: Calculate 2 element score sets (base=natal, post=all)
- `bazingse.py` lines 2981-2983: Location boost only to post scores
- `bazingse.py` line 3319: Daymaster analysis uses `post_five_elements`
- `bazingse.py` lines 3704-3706: Return 2 scores
- `routes.py` lines 284-287: Pass 2 scores to response

**Testing**:
```bash
# Test natal-only (base should equal post minus interactions)
curl "http://localhost:8008/analyze_bazi?birth_date=1990-01-15&gender=male"
# base: natal only, post: natal after interactions

# Test with luck (post should have more elements than base)
curl "http://localhost:8008/analyze_bazi?birth_date=1990-01-15&gender=male&analysis_year=2024"
# base: natal only, post: natal + luck + interactions

# Test with location (post should have location boost, base unchanged)
curl "http://localhost:8008/analyze_bazi?birth_date=1990-01-15&gender=male&location=overseas"
# base: Ren=0, post: Ren=210 (location boost)
```

**Philosophy**: Separating base (natal) vs. post (everything) respects the BaZi principle that birth destiny (命 / ming) is fixed, while life circumstances (運 / yun) are variable. This 2-tier system allows users to see both their unchangeable birth chart AND their current life situation's influences, with maximum clarity and simplicity.

## Dependencies
- **sxtwl**: Chinese calendar (accurate date conversions)
- **FastAPI** + **Pydantic**: API framework + validation
- **uvicorn**: ASGI server (auto-reload in dev)

---

**TL;DR for AI Agents:**
1. **EB transformations use BRANCH polarity**, **energy flow uses PRIMARY QI polarity** - Different rules!
2. All constants are **deterministic** (no dynamic functions)
3. HS combinations check **ALL EB nodes** including luck pillars AND talismans for transformation
4. Use `get_primary_qi_polarity()` helper when adding elements to EB nodes in energy flow
5. Scoring uses **nested dicts**, not tuples - Access with `.get("combined", {}).get("adjacent")`
6. All interactions have `distance` field and `badges` list
7. Up to 26 nodes supported: 8 natal + 10 luck + 8 talisman (all optional except natal)
8. **Location boost**: Non-interactive element addition (overseas=Water, birthplace=Earth) - NOT a node!
9. **2-tier scoring**: base=natal only (before interactions), post=everything (all nodes + location, after interactions)
10. Keep code **KISS** - linear, flat, middle-schooler-friendly
11. Test suite must pass before any commit
