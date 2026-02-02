# Life Aspects Analysis System - Architectural Plan

## Overview

A unified system for analyzing three life aspects from BaZi charts:
1. **Health** - TCM organ-element correlations
2. **Wealth** - Financial opportunities and risks
3. **Learning** - Education and skill development

## The Problem

Current `health_analysis.py` has a critical gap:
- Only detects **direct conflicts** (clashes, punishments, harms)
- Does NOT detect **Wu Xing control cycle imbalances**

Example (Test 1986-11-29 in 2020):
- Fire is "Dead" (seasonal state)
- Fire normally controls Metal
- Fire too weak → Metal becomes uncontrolled
- Metal governs skin → **Skin issues** (actual user experience: rashes)
- System predicted: "Fire/Heart stress" (wrong organ system)

## Root Cause

The `post_element_score` and `natal_element_score` are passed to `health_analysis.py` but **NEVER USED**.

## Proposed Solution

### Phase 1: Fix Health Analysis (Immediate)

Add Wu Xing control cycle imbalance detection:

```python
# New in health_analysis.py

ELEMENT_CONTROLS = {
    "Wood": "Earth",   # Wood breaks Earth → Digestive
    "Fire": "Metal",   # Fire melts Metal → Respiratory/Skin
    "Earth": "Water",  # Earth blocks Water → Urinary
    "Metal": "Wood",   # Metal cuts Wood → Hepatobiliary
    "Water": "Fire"    # Water extinguishes Fire → Cardiovascular
}

def detect_control_imbalances(seasonal_states: Dict[str, str]) -> List[dict]:
    """
    When a controller element is Dead/Trapped,
    the controlled element may become problematic.

    TCM principle: 相侮 (xiāng wǔ) - "Reverse Control"
    """
    imbalances = []

    for controller, controlled in ELEMENT_CONTROLS.items():
        controller_state = seasonal_states.get(controller, "Resting")

        if controller_state in ["Dead", "Trapped"]:
            organ_info = ELEMENT_ORGANS.get(controlled, {})
            imbalances.append({
                "type": "control_imbalance",
                "weak_controller": controller,
                "controller_state": controller_state,
                "uncontrolled_element": controlled,
                "organ_system": organ_info.get("system", ""),
                "body_parts": organ_info.get("body_parts", []),
                "severity": "moderate" if controller_state == "Trapped" else "elevated",
                "explanation": f"{controller} ({controller_state}) cannot properly control {controlled}"
            })

    return imbalances
```

### Phase 2: Unified Life Aspects Architecture (Future)

```
api/library/
├── life_aspects/
│   ├── __init__.py           # Export all aspects
│   ├── base.py               # Common detection patterns
│   │   ├── aggregate_by_element()
│   │   ├── calculate_severity()
│   │   ├── detect_control_imbalances()
│   │   └── generate_analysis_text()
│   │
│   ├── health.py             # TCM organ-element
│   │   ├── ELEMENT_ORGANS
│   │   └── generate_health_analysis()
│   │
│   ├── wealth.py             # Financial opportunities
│   │   ├── WEALTH_TEN_GODS = ["DW", "IW", "RW"]
│   │   ├── detect_wealth_opportunity()
│   │   ├── detect_wealth_risk()
│   │   └── generate_wealth_analysis()
│   │
│   └── learning.py           # Education/skills
│       ├── LEARNING_TEN_GODS = ["DR", "IR", "EG", "HO"]
│       ├── detect_learning_opportunity()
│       ├── detect_learning_block()
│       └── generate_learning_analysis()
```

### Phase 3: Wealth Analysis Module

```python
# wealth.py

WEALTH_TEN_GODS = {
    "DW": {"chinese": "正財", "type": "earned", "description": "Steady income, career wealth"},
    "IW": {"chinese": "偏財", "type": "windfall", "description": "Unexpected gains, investments"},
    "RW": {"chinese": "劫財", "type": "competitor", "description": "Competition, potential loss"},
}

def generate_wealth_analysis(
    interactions: Dict,
    post_element_score: Dict[str, float],
    seasonal_states: Dict[str, str],
    daymaster_element: str,
    wealth_storage_analysis: Dict
) -> dict:
    """
    Analyze chart for wealth opportunities and risks.

    Good wealth period indicators:
    - DW/IW present in luck pillars
    - Wealth element strong (score > threshold)
    - Wealth element in Prosperous/Strengthening state
    - Storage activated (opened + filled)
    - Day Master strong enough to handle wealth

    Bad wealth period indicators:
    - RW (Rob Wealth) strong
    - Wealth element under clash/harm
    - Wealth element in Dead/Trapped state
    - Storage unopened or blocked
    """
    pass  # Implementation
```

### Phase 4: Learning Analysis Module

```python
# learning.py

LEARNING_TEN_GODS = {
    "DR": {"chinese": "正印", "type": "formal", "description": "Formal education, traditional learning"},
    "IR": {"chinese": "偏印", "type": "unconventional", "description": "Self-taught, intuitive learning"},
    "EG": {"chinese": "食神", "type": "expression", "description": "Teaching, communicating knowledge"},
    "HO": {"chinese": "傷官", "type": "innovation", "description": "Creative disruption, challenging norms"},
}

def generate_learning_analysis(
    interactions: Dict,
    post_element_score: Dict[str, float],
    seasonal_states: Dict[str, str],
    daymaster_element: str,
    daymaster_strength: str
) -> dict:
    """
    Analyze chart for learning opportunities and blocks.

    Good learning period indicators:
    - DR/IR present in luck pillars
    - Resource element strong and in good seasonal state
    - Day Master strong enough to absorb (support 35-60%)
    - Output channels open (EG/HO healthy)

    Bad learning period indicators:
    - Resource element weak or Dead
    - Resource under heavy conflict
    - Day Master too weak (< 20%) - can't focus
    - Output channels blocked
    """
    pass  # Implementation
```

## Test Cases

### Health: 1986-11-29 in 2020 (Current Bug)
- **Expected**: Detect Metal/Skin vulnerability (Fire Dead → can't control Metal)
- **Current**: Only detects Fire/Heart stress
- **Fix**: Add `detect_control_imbalances()`

### Wealth: 1986-11-29 in 2020 (User reported: "Investment did really well")
- **Expected**: Detect wealth opportunity
- **Analysis**: Check if DW/IW elements strengthened in luck period
- **Validation**: Compare with user's actual experience

### Learning: 1986-11-29 in 2020 (User reported: "Breakthrough in learning")
- **Expected**: Detect learning opportunity
- **Analysis**: Check if DR/IR elements strengthened, Day Master capacity
- **Validation**: Compare with user's actual experience

## Implementation Priority

1. **Immediate**: Fix `health_analysis.py` with control cycle imbalance detection
2. **Short-term**: Create unified `life_aspects/` directory structure
3. **Medium-term**: Implement `wealth.py` module
4. **Long-term**: Implement `learning.py` module

## Data Flow

```
routes.py:/analyze_bazi
    │
    ├── interactions (14 types)
    ├── post_element_score (10 stems)
    ├── natal_element_score (10 stems)
    ├── seasonal_states (5 elements)
    ├── daymaster_analysis
    └── wealth_storage_analysis
           │
           ▼
    life_aspects/
    ├── health.py → health_analysis
    ├── wealth.py → wealth_analysis
    └── learning.py → learning_analysis
           │
           ▼
    API Response:
    {
        "health_analysis": {...},
        "wealth_analysis": {...},
        "learning_analysis": {...}
    }
```

## Principles (from AGENTS.md)

1. **Backend is Single Source of Truth** - All analysis in Python, frontend only displays
2. **KISS** - Keep solutions simple, middle-schooler friendly
3. **Deterministic** - Use constants, not dynamic functions
4. **Pattern-Based** - Apply fixes universally, not just to one case
5. **No Hallucination** - Only implement what's documented in BaZi theory

## Critical Dimension: Pillar Position = Relationship + Life Period

### Pillar-Relationship Mapping (六亲宫位)

| Pillar | Stem Represents | Branch Represents | Life Period |
|--------|-----------------|-------------------|-------------|
| Year (年柱) | Grandfather | Grandmother | 0-16 years (早年) |
| Month (月柱) | Father | Mother | 16-32 years (青年) |
| Day (日柱) | Self (日主) | Spouse (配偶宫) | 32-48 years (中年) |
| Hour (时柱) | Children | Descendants | 48+ years (晚年) |

### Ten Gods Position Meanings (十神在各柱)

**The SAME Ten God has DIFFERENT meanings in different pillars:**

| Ten God | Year Pillar | Month Pillar | Day Pillar | Hour Pillar |
|---------|-------------|--------------|------------|-------------|
| 正印 (DR) | Wealthy family | Education support | Self-cultivation | Lifelong learning |
| 偏印 (IR) | Unstable origins | Unconventional path | Intuitive nature | Late wisdom |
| 正財 (DW) | Inherited wealth | Career income | Spouse wealth | Late-life security |
| 偏財 (IW) | Windfall ancestry | Investment gains | Spouse's income | Children's fortune |
| 正官 (DO) | Honorable family | Career authority | Spouse (for women) | Children's status |
| 七殺 (7K) | Ancestral pressure | Career pressure | Spouse conflict | Children pressure |
| 食神 (EG) | Peaceful childhood | Creative expression | Gentle nature | Daughters (women) |
| 傷官 (HO) | Childhood struggle | Rebellious youth | Unconventional | Sons (women) |
| 比肩 (F) | Siblings/competition | Peer support | Self-reliance | Late independence |
| 劫財 (RW) | Family loss | Sibling rivalry | Spouse competition | Children rivalry |

### Implications for Life Aspect Analysis

**Health Analysis** should consider:
- Year pillar conflict → Childhood health issues
- Month pillar conflict → Youth health issues
- Day pillar conflict → Personal health (most important)
- Hour pillar conflict → Late-life health issues

**Wealth Analysis** should consider:
- Year pillar DW/IW → Inherited wealth, family fortune
- Month pillar DW/IW → Career earnings, salary
- Day pillar DW/IW → Spouse's wealth, joint assets
- Hour pillar DW/IW → Retirement, children's support

**Learning Analysis** should consider:
- Year pillar DR/IR → Early education foundation
- Month pillar DR/IR → Formal education period
- Day pillar DR/IR → Self-learning, spouse teaching
- Hour pillar DR/IR → Lifelong learning, mentoring others

### Implementation: Add Position Context

```python
# Node position to relationship mapping
NODE_RELATIONSHIPS = {
    # Natal pillars
    "hs_y": {"pillar": "year", "type": "stem", "represents": "grandfather/ancestors"},
    "eb_y": {"pillar": "year", "type": "branch", "represents": "grandmother/origins"},
    "hs_m": {"pillar": "month", "type": "stem", "represents": "father"},
    "eb_m": {"pillar": "month", "type": "branch", "represents": "mother"},
    "hs_d": {"pillar": "day", "type": "stem", "represents": "self (day master)"},
    "eb_d": {"pillar": "day", "type": "branch", "represents": "spouse"},
    "hs_h": {"pillar": "hour", "type": "stem", "represents": "children"},
    "eb_h": {"pillar": "hour", "type": "branch", "represents": "descendants"},
    # Luck pillars (temporal overlay)
    "hs_10yl": {"pillar": "10yr_luck", "type": "stem", "represents": "decade theme"},
    "eb_10yl": {"pillar": "10yr_luck", "type": "branch", "represents": "decade environment"},
    "hs_yl": {"pillar": "annual", "type": "stem", "represents": "year theme"},
    "eb_yl": {"pillar": "annual", "type": "branch", "represents": "year environment"},
    "hs_ml": {"pillar": "monthly", "type": "stem", "represents": "month theme"},
    "eb_ml": {"pillar": "monthly", "type": "branch", "represents": "month environment"},
}

# Life period mapping
PILLAR_LIFE_PERIODS = {
    "year": {"start_age": 0, "end_age": 16, "chinese": "早年"},
    "month": {"start_age": 16, "end_age": 32, "chinese": "青年"},
    "day": {"start_age": 32, "end_age": 48, "chinese": "中年"},
    "hour": {"start_age": 48, "end_age": 100, "chinese": "晚年"},
}
```

## Questions Before Implementation

1. Should wealth/learning analysis be in separate modules or combined with health?
2. What threshold determines "strong" vs "weak" element scores?
3. Should control cycle imbalances be "elevated" or "moderate" severity?
4. How should multiple life aspects interact (e.g., "good wealth but bad health")?
5. How deeply should we incorporate pillar position context in the first implementation?

## References

- [Four Pillars Meaning - Wonyan Consult](https://www.wonyanconsult.com/post/what-do-the-four-pillars-bazi-in-astrology-represent)
- [Ten Gods in BaZi - Master Sean Chan](https://www.masterseanchan.com/blog/ten-gods-bazi-profile-how-its-done/)
- [Four Pillars - Chi Chart](https://chichart.com/four-pillars-meaning/)
- [Imperial Harvest - Ten Gods](https://imperialharvest.com/blog/10-gods/)
