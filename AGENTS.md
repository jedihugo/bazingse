# AGENTS.md

Guidance for AI agents working on **BaZingSe** - a full-stack Chinese BaZi (Four Pillars/八字) astrology application.

**Status**: Production-ready API with 8-26 node extensible architecture, Vue 3 + Vite frontend, comprehensive test suite.

---

## Project Overview

- **Frontend**: Vue 3 + Vite (Pure SPA) with Custom CSS
- **Backend**: Python FastAPI + sxtwl calendar library
- **Architecture**: Backend-driven calculation engine with frontend display layer

---

## CRITICAL: Pattern-Based Thinking (READ THIS FIRST!)

**When given an example, NEVER hardcode for just that one case. Always identify the pattern and apply it universally.**

### WRONG Approach:
```
User: "Add distance field to SIX_HARMONIES interactions"
Agent: *Only adds distance to SIX_HARMONIES*
Result: 23 other interaction types still missing distance field!
```

### CORRECT Approach:
```
User: "Add distance field to SIX_HARMONIES interactions"
Agent:
  1. Understands: User wants distance for scoring transparency
  2. Searches: How many interaction types exist? (grep for interaction_log.append)
  3. Discovers: 14 interaction types, 24 locations total
  4. Applies: Adds distance to ALL interaction types
  5. Verifies: Checks that ALL interactions now have distance field
Result: Complete fix, no follow-up needed!
```

### Key Questions to Ask:
1. **"Is this a single instance or a pattern?"** (Usually a pattern!)
2. **"Where else does this pattern occur?"** (Search with grep/Glob)
3. **"What's the root cause?"** (Fix the source, not symptoms)
4. **"Are there similar cases?"** (Apply fix universally)

---

## CRITICAL: API is the Single Source of Truth

**ALL data, logic, calculations, and display metadata MUST live in the Python API backend.**

This includes:
- BaZi calculations and astrology knowledge
- **Colors (hex values)** for elements, stems, branches
- **Styling metadata** for Ten Gods, event types, badges
- **Icons and labels** for all UI elements
- Hidden stem percentages, qi values, transformations
- All mappings and reference data

**Frontend responsibilities (ONLY):**
- Collect user inputs (forms, date pickers)
- Call backend APIs
- Display returned data using API-provided styling
- Handle UI interactions (hover, click, toggle, animations)
- Layout and responsive design

**Frontend must NEVER:**
- Calculate elements, stems, branches, or Ten Gods
- Implement BaZi rules or interaction logic
- Hardcode Chinese astrology knowledge
- **Hardcode hex colors** - use `mappings.elements[element].hex_color`
- **Hardcode styling** - use `mappings.ten_gods_styling[id].hex_color`
- **Create mock/fallback data** - if API doesn't provide it, request API enhancement

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

**Implementation:** In `transform_to_element()`, use `EARTHLY_BRANCHES[branch_id]["polarity"]`

#### B. Energy Flow (Natural Production)
**When Earthly Branches generate elements through WuXing cycle, use PRIMARY QI polarity.**

Applies to: Natural element generation, receiver nodes in energy flow

**Examples:**
- Si 巳 (Yin branch) has Bing 丙 (Yang) primary → Produces **Geng** 庚 (Yang Metal)
- Wu 午 (Yang branch) has Ding 丁 (Yin) primary → Produces **Xin** 辛 (Yin Metal)

**Implementation:** Use `get_primary_qi_polarity(branch_id)` helper in `add_element()` calls

| Context | Use | Example |
|---------|-----|---------|
| EB Transformation Badge | Branch Polarity | Si (Yin) → Fire = Ding badge |
| Energy Generation/Flow | Primary Qi Polarity | Si (Bing Yang primary) → Metal = Geng |

### 2. BaZi Is Deterministic
**Use constants, never dynamic functions.** All mappings are fixed forever.

```python
# CORRECT: Deterministic constants
ELEMENT_CHARACTERS = {"Wood": "木", "Fire": "火", ...}
ELEMENT_POLARITY_TO_STEM = {"Yang Wood": "Jia", "Yin Wood": "Yi", ...}

# WRONG: Dynamic lookup functions
def get_element_character(name): ...  # Don't do this!
```

### 3. Interaction Logic Flow
All interactions follow this sequence:

1. **DETECTION**: Required stems/branches present?
2. **DISTANCE**: Adjacent (0), nearby (1), or far (2+)?
3. **TRANSFORMATION**: Transforming element exists?
   - HS combinations: Check if target element exists in **ANY EB** (including luck pillars!)
   - EB combinations: Check if target element exists in **ANY HS**

### 4. Hidden Qi Interaction Depth (藏干相剋)

**Classical BaZi principle: Primary, Secondary, AND Tertiary Qi can interact.**

| Qi Pairing | Strength Multiplier | Notes |
|------------|---------------------|-------|
| Primary-Primary | 1.0 | Full interaction |
| Primary-Secondary | 0.5 | Half strength |
| Secondary-Secondary | 0.25 | Quarter strength |
| Primary-Tertiary | 0.30 | Tertiary engagement |
| Secondary-Tertiary | 0.15 | Cross-level |
| Tertiary-Tertiary | 0.10 | Rare, both have tertiary |

### 5. Stem-Branch Unity (干支一體)

**Classical BaZi principle: HS and EB within the same pillar form a unified energy.**

Calculated FIRST before other interactions (innate pillar nature):

| Relationship | Effect | Example |
|--------------|--------|---------|
| HS produces EB | +10% boost to EB | Wood stem + Fire branch |
| HS controls EB | -8% penalty to EB | Fire stem + Metal branch |
| Same element | +5% boost to both | Fire stem + Fire branch |

### 6. Punishment Hierarchy (刑法輕重)

| Category | Chinese | Severity | Multiplier | Pattern |
|----------|---------|----------|------------|---------|
| 勢刑 (Shi Xing) | Power/Bullying | Severe | 1.0 | Yin-Si-Shen |
| 無禮刑 (Wu Li Xing) | Rudeness | Moderate | 0.85 | Chou-Wei-Xu |
| 恩刑 (En Xing) | Ungrateful | Light | 0.70 | Zi-Mao |
| 自刑 (Zi Xing) | Self-punishment | Self | 0.60 | Chen-Chen, etc. |

### 7. Rooting and Support (通根/透出)

**Same element relationships indicate strength without qi exchange.**

#### Primary Qi (本氣) vs Hidden Stems (藏干)

| Index | Term | Chinese | Description | Hidden? |
|-------|------|---------|-------------|---------|
| 0 | **Primary Qi** | 本氣 | Main/dominant energy of the branch | NO - visible |
| 1+ | **Hidden Stems** | 藏干 | Secondary/tertiary energies | YES - actually hidden |

**Example - Yin Tiger (寅)**:
- Index 0: Jia (甲 Wood, 60) = **Primary Qi (本氣)** - NOT hidden
- Index 1: Bing (丙 Fire, 30) = **Hidden Stem (藏干)** - secondary, hidden
- Index 2: Wu (戊 Earth, 10) = **Hidden Stem (藏干)** - tertiary, hidden

---

## Architecture

### File Structure
```
bazingse/
├── api/                             # Backend - Python FastAPI
│   ├── bazingse.py (~4,000 lines)   # Core interaction engine (8-26 nodes)
│   ├── chart_constructor.py         # Pillar generation (uses sxtwl)
│   ├── routes.py                    # FastAPI endpoint /analyze_bazi
│   ├── run_bazingse.py              # Entry point (uvicorn on port 8008)
│   ├── library/                     # Modular BaZi constants & utilities
│   │   ├── __init__.py              # Package exports
│   │   ├── core.py                  # STEMS & BRANCHES - single source of truth
│   │   ├── derived.py               # Computed data from core
│   │   ├── seasonal.py              # Seasonal strength multipliers (旺相休囚死)
│   │   ├── combinations.py          # Positive interactions (三會/三合/六合)
│   │   ├── conflicts.py             # Negative interactions (沖/害/刑/破)
│   │   ├── scoring.py               # Distance multipliers & base scores
│   │   ├── distance.py              # Node coordinate calculations
│   │   ├── unity.py                 # Wu Xing Combat Engine (控/生)
│   │   ├── unit_tracker.py          # Qi Story Timeline tracker
│   │   ├── dong_gong.py             # Dong Gong date selection
│   │   └── wealth_storage.py        # 财库 (wealth storage) detection
│   └── test_analyze_bazi.py         # Python test suite
│
├── app/                             # Frontend - Vue 3 + Vite
│   ├── index.html                   # Entry HTML
│   ├── vite.config.js               # Vite configuration (port 3000)
│   ├── package.json                 # npm dependencies
│   ├── public/                      # Static assets
│   │   ├── bazingse-logo.png        # App logo
│   │   └── favicon.ico              # Favicon
│   └── src/
│       ├── main.js                  # Vue app entry point
│       ├── App.vue (~5,500 lines)   # Main Vue component
│       ├── styles.css               # Global styles
│       ├── types/
│       │   └── bazi.ts              # TypeScript interfaces
│       └── utils/
│           └── baziHelpers.ts       # BaZi utility functions
│
├── composables/                     # Vue composables
│   └── useBaziData.ts               # BaZi data composable
│
└── AGENTS.md                        # AI coding guidelines (this file)
```

### Node System (8-26 nodes)
**Natal (8)**: `hs_y`, `hs_m`, `hs_d`, `hs_h`, `eb_y`, `eb_m`, `eb_d`, `eb_h`
**10-Year Luck (2)**: `hs_10yl`, `eb_10yl` (when `analysis_year` provided)
**Annual (2)**: `hs_yl`, `eb_yl`
**Monthly (2)**: `hs_ml`, `eb_ml` (when `analysis_month` provided)
**Daily (2)**: `hs_dl`, `eb_dl` (when `analysis_day` provided)
**Hourly (2)**: `hs_hl`, `eb_hl` (when `analysis_time` provided)
**Talisman (0-8)**: `hs_ty`, `eb_ty`, `hs_tm`, `eb_tm`, `hs_td`, `eb_td`, `hs_th`, `eb_th` (optional)

**CRITICAL**: Talismans can be **partial** - HS and EB are independent:
- HS-only: `talisman_year_hs=Jia` (creates only `hs_ty`)
- EB-only: `talisman_year_eb=Zi` (creates only `eb_ty`)
- Both: Provide both parameters (creates both nodes)

### 18-Node System Architecture

**Position System:**
```
Display Order (Left to Right):
Hour | Day | Month | Year || 10Y Luck || Annual | Monthly | Daily | Hourly
時   | 日  | 月    | 年   || 運       || 年運   | 月運    | 日運  | 時運

Backend Position Codes:
0=Hour | 1=Day | 2=Month | 3=Year || 4=10YL | 5=Annual | 6=Monthly | 7=Daily | 8=Hourly
```

### Temporal Overlay Metaphysics

**Core BaZi Principle:**
Luck pillars (10Y, Annual, Monthly, Daily, Hourly) are NOT spatial positions—they are **temporal overlays** affecting the ENTIRE natal chart equally.

**Backend Implementation:**
- `calculate_interaction_distance()` treats luck positions (4-8) as **distance=0** to ALL natal positions (0-3)
- All luck-natal interactions receive full adjacency strength

---

## Development Commands

### Frontend (Vue 3 SPA - Port 3000)
```bash
cd /Users/macbookair/GitHub/bazingse/app
npm install
npm run dev     # Development server: http://localhost:3000
npm run build   # Production build → dist/
npm run preview # Preview production build
```

### Backend (FastAPI - Port 8008)
```bash
cd /Users/macbookair/GitHub/bazingse/api
# Create/activate venv if needed
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Run server
python run_bazingse.py  # http://localhost:8008
```

### Restart Backend with Changes
```bash
cd /Users/macbookair/GitHub/bazingse/api
pkill -f "python.*run_bazingse"
source .venv/bin/activate && nohup python run_bazingse.py > /tmp/bazingse.log 2>&1 &
```

### Test API Directly
```bash
curl "http://localhost:8008/analyze_bazi?birth_date=1986-11-29&birth_time=01:30&gender=male&analysis_year=2025&include_annual_luck=true&analysis_month=10" | python3 -m json.tool
```

---

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

**Optional Talisman Parameters**:
- `talisman_year_hs`, `talisman_year_eb` - Talisman slot 1 (any of 60 pillars)
- `talisman_month_hs`, `talisman_month_eb` - Talisman slot 2
- `talisman_day_hs`, `talisman_day_eb` - Talisman slot 3
- `talisman_hour_hs`, `talisman_hour_eb` - Talisman slot 4

**Optional Location Parameter**:
- `location` (overseas/birthplace) - Non-interactive element boost based on residence location

**Returns**: Flat JSON structure with:
- All node data (base_qi, post_interaction_qi, badges, interactions)
- Interaction log (all 14 interaction types)
- Base/post element scores
- Daymaster analysis
- Chinese character mappings
- Unit tracker (Qi Story Timeline)

---

## Interaction Types

The system detects and processes **14 interaction types**:

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

---

## Node Badge System

### Badge Types (7 total)

**Positive (Additive):**
- `transformation`: Successful EB/HS combination with element support
  - Badge: Stem character of NEW element (e.g., "Ren" for Water)
  - Size: Based on interaction strength (xl/lg/md/sm/xs)

- `combination`: Partial EB combination without full element support
  - Badge: Stem character of partial element

**Negative (Reductive):**
- `punishment`: "XING" (刑)
- `harm`: "HAI" (害)
- `clash`: "CHONG" (沖)
- `destruction`: "PO" (破)
- `stem_conflict`: "KE" (剋)

**Key Principles**:
- **Positive badges**: Display stem character → elemental visualization
- **Negative badges**: Display icon identifier → neutral visualization
- **Badge distribution**: Both controller AND victim receive badges

---

## Unit Tracker (Qi Story Timeline)

The Unit Tracker provides a **video game-style narrative** of how qi flows through the chart.

### Timeline Phases (Processing Order)

```
 1. naive_assignment        → Register all qi units with initial values
 2. pillar_unity_d         → Day HS ↔ Day EB qi
 3. pillar_unity_y         → Year HS ↔ Year EB qi
 4. pillar_unity_m         → Month HS ↔ Month EB qi
 5. pillar_unity_h         → Hour HS ↔ Hour EB qi
 6. seasonal               → Apply 旺相休囚死 Fibonacci multipliers
 7. three_meetings         → 三會 detection and tracking
 8. three_combinations     → 三合 detection and tracking
 9. half_meetings          → 半會 detection and tracking
10. six_harmonies          → 六合 detection and tracking
11. conflicts              → 沖害刑 detection and tracking
12. half_combinations      → 半合 detection and tracking
13. arched_combinations    → 拱合 detection and tracking
14. cross_pillar           → Cross-pillar HS ↔ EB qi interactions
```

### Seasonal Adjustments (旺相休囚死)

| State | Chinese | Multiplier | Fibonacci Basis |
|-------|---------|------------|-----------------|
| Prosperous | 旺 Wang | 1.382 | Fibonacci advancement (strongest) |
| Strengthening | 相 Xiang | 1.236 | Fibonacci level |
| Resting | 休 Xiu | 1.000 | Baseline (no change) |
| Trapped | 囚 Qiu | 0.786 | Fibonacci retracement |
| Dead | 死 Si | 0.618 | Golden ratio retracement (weakest) |

---

## Frontend Structure

### Main Files

**Entry Point:**
- `app/index.html` - HTML entry point with Vue app mount target
- `app/src/main.js` - Vue app initialization
- `app/vite.config.js` - Vite configuration with API proxy to backend

**Primary Interface:**
- `app/src/App.vue` (~5,500 lines)
  - All-in-one Single File Component (SFC)
  - Complete BaZi interface: inputs, chart display, interactions, analysis
  - Explicit Vue 3 imports (ref, computed, watch, onMounted, etc.)

**Styling:**
- `app/src/styles.css` (~600 lines)
  - Custom CSS (converted from Tailwind)
  - **TUI-STYLE (Terminal UI)**: Content-first, minimal padding/margins
  - **MOBILE-FIRST responsive design**
  - **NO HORIZONTAL SCROLLING**

### Key State Management (in App.vue)

**Chart Data:**
- `chartData` - Complete backend response (18-node system data)
- `currentLuckPillar` - Current 10-year luck timing info

**View State:**
- `viewMode` - Toggle between 'base' (pre-interaction) and 'post' (post-interaction)
- `showInteractionLog` - Toggle for interaction log panel visibility

**Talisman State:**
- `showTalismans` - Toggle for talisman pillar display
- `talismanYearHS`, `talismanYearEB` - Year talisman stem/branch overrides

### Data Flow

1. User fills birth inputs + toggles "Time Travel" mode
2. Frontend calls `/api/analyze_bazi?...` with progressive parameters
3. Vite proxy forwards to backend `http://localhost:8008/analyze_bazi`
4. Backend calculates nodes + interactions (up to 26 nodes)
5. Frontend receives complete chart data
6. UI renders with smooth transitions

---

## Key Implementation Patterns

### Backend Development

**Adding New Calculations:**
1. Update `api/library/` if new constants needed
2. Add logic to `api/bazingse.py` or create new module
3. Expose via new parameter in `api/routes.py`
4. Return all calculated data in response (frontend should not re-calculate)

**Position System Rules:**
- Positions 0-3: Natal chart (spatial, normal distance calculation)
- Positions 4-8: Luck pillars (temporal overlay, distance=0 to natal)
- Positions 9-12: Talisman (external harmony tools, distance=0 to natal)

### Frontend Development

**NO BaZi Logic in Frontend:**
```javascript
// WRONG - Frontend calculating Ten God
function getTenGod(dayMaster, stem) {
  if (dayMaster === 'Jia' && stem === 'Yi') return 'R' // NO!
}

// CORRECT - Backend lookup only
const tenGod = chartData.mappings.ten_gods[dayMasterStem][stem].abbreviation
```

**State Management:**
- Explicit Vue 3 imports: `import { ref, computed, watch, onMounted } from 'vue'`
- All refs created with `ref()` or `shallowRef()` for performance
- localStorage for persistence
- No Pinia/Vuex - pure Vue 3 Composition API

---

## 2-Tier Element Scoring System

Separate natal destiny vs. full chart element scores:

```python
1. base_element_score   # Natal chart ONLY (8 nodes), before interactions
2. post_element_score   # ALL nodes (natal + luck + talisman + location), after interactions
```

**Base Score** (natal chart only, pure birth destiny):
- Always 6 or 8 nodes (depends on birth_time provided)
- NO luck pillars, NO talisman, NO location boost
- NO interactions applied

**Post Score** (full chart, current life situation):
- Includes ALL nodes: Natal (8) + Luck (0-10) + Talisman (0-8)
- Includes location boost (overseas or birthplace)
- ALL interactions calculated and applied

---

## Design Principles

1. **Backend is Source of Truth** - Never calculate BaZi logic in frontend
2. **KISS** - Keep solutions simple and understandable (middle-schooler friendly)
3. **Flat Data Structures** - Avoid deep nesting (max 1 level)
4. **Progressive Enhancement** - Features appear as user provides more input
5. **Visual Clarity** - Colors and borders indicate pillar types and interactions
6. **Temporal Overlay Concept** - Luck pillars interact equally with all natal pillars
7. **Mobile-First Responsive Design** - Base styles for mobile, enhanced for larger screens
8. **NO HORIZONTAL SCROLLING** - Page must NEVER scroll left/right
9. **TUI-STYLE (Terminal UI)** - Content-first design with minimal chrome

---

## Troubleshooting

**Interactions not showing for Monthly/Daily/Hourly:**
- Check backend restarted after `bazingse.py` position code changes
- Verify API params sent: `console.log('Calling API:', apiUrl)`
- Check response: `has_monthly`, `has_daily`, `has_hourly` flags

**Backend changes not reflecting:**
- Restart backend server (Python doesn't hot-reload all changes)
- Check `/tmp/bazingse.log` for errors
- Test endpoint directly with `curl` to isolate issue

**Vite/Vue Issues:**
- Port conflict: `lsof -ti:3000 | xargs kill -9`
- HMR not working: Check browser console, verify WS connection
- Blank page: Check console for errors, verify backend is running

---

## Dependencies

### Backend (api/)
- **sxtwl**: Chinese calendar (accurate date conversions)
- **FastAPI** + **Pydantic**: API framework + validation
- **uvicorn**: ASGI server (auto-reload in dev)

### Frontend (app/)
- **Vue 3**: Reactive UI framework
- **Vite**: Fast dev server and bundler
- Total: ~30 packages (~40MB node_modules)

---

## TL;DR for AI Agents

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
12. **Pattern-based thinking**: When given an example, apply fix to ALL similar cases

---

**Last Updated:** 2026-01-11 (Merged root + api AGENTS.md)
