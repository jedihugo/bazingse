# Analysis Precision Improvement — Design Document

**Date:** 2026-02-21
**Goal:** Improve precision and comprehensiveness of BaZi natal analysis across all 4 sections: Strength, Health, Honest Summary, Remedies.

---

## Problem

The current natal analysis on the profile page has several gaps:

1. **Strength Assessment** shows favorable/unfavorable elements without explaining WHY
2. **Health Section** uses a shallow element-count threshold instead of the deep health engine that already exists in `life_aspects/health.py`
3. **Honest Summary** has limited personalization, no female spouse star check, generic templates
4. **Remedies** are not cross-linked with health findings

Example: A weak Jia Wood DM has 6% Metal. Metal is correctly listed as unfavorable (it attacks Wood), but the user reasonably asks "why isn't my low Metal element favorable?" — no explanation is provided.

---

## Part 1: Strength WHY-Reasoning

### Current
```
Score: 37.3/100
Useful God: Water
Favorable: Water, Wood
Unfavorable: Earth, Metal, Fire
```
No explanation of the reasoning.

### Proposed
Add a `reasoning` field to `_summary_strength()` that derives explanations from the actual element cycle:

```
Score: 37.3/100
Useful God: Water — generates your Wood (resource element)
Favorable: Water (generates you), Wood (companions strengthen you)
Unfavorable: Earth (your wealth — drains you), Metal (attacks/controls Wood), Fire (your output — exhausts you)
```

Also add an `explanation` text paragraph:
> "Your Jia Wood is weak at 37/100. A weak Day Master needs nourishment (Water → generates Wood) and companions (Wood). Metal controls Wood — even at 6%, more Metal would be harmful, not helpful. Low Metal is actually a blessing for weak Wood."

**Implementation:** Derive from `ELEMENT_CYCLES` in `determine_useful_god()` — the relationships are already computed, just not surfaced as text.

---

## Part 2: Deep Health Engine Integration

### Current
`_summary_health()` in adapter.py (line 1327) uses `count_elements()` with a simple threshold:
- If count < 1.0: "Low {elem} — {deficiency symptoms}"
- If count > 3.0: "Excess {elem} — {excess symptoms}"

One line per element. No clash/punishment analysis, no seasonal modifiers, no control cycle awareness.

### Existing Deep Engine
`life_aspects/health.py` already has:
- `ELEMENT_ORGANS` — full TCM Zang-Fu mapping with body parts, emotions
- `CONFLICT_HEALTH_WEIGHTS` — clash 1.0, punishment 0.85, harm 0.70, etc.
- `SEASONAL_HEALTH_MODIFIER` — Dead = 2.0x, Trapped = 1.5x vulnerability
- `detect_vulnerable_elements()` — conflict aggregation + control cycle imbalances + severity scoring
- `generate_analysis_text()` — multilingual natural language summary

### Proposed
Replace `_summary_health()` with a new version that:

1. **Element balance** — still shows deficient/excess elements (what exists)
2. **Control cycle analysis** — if Fire is weak, Metal is uncontrolled → amplified lung/respiratory risk
3. **Seasonal vulnerability** — element in Dead/Trapped state = higher risk
4. **Organ-specific detail** — Zang/Fu organs, body parts, associated emotions (from `ELEMENT_ORGANS`)
5. **Multi-line per element** — not just one generic line, but specific reasons WHY this element is concerning

For the natal chart (no interactions available), we adapt the deep engine to work with element counts and seasonal states rather than requiring interaction data.

**Output format per element:**
```
Label: "Lungs 肺 (Metal)"
Value: "Metal severely deficient (6%). Weak immune response, respiratory vulnerability, dry skin. Fire (23%) struggles to regulate Metal — control cycle imbalance amplifies risk."
Severity: "warning" / "critical" / "info"
```

---

## Part 3: Honest Summary Improvements

### Current Gaps
- No WHY-reasoning for favorable/unfavorable elements
- Female spouse star check missing (only checks male wife star = DW)
- Life lesson templates have 1 variant per scenario
- No health cross-reference

### Proposed Changes

1. **Add element cycle reasoning to useful god paragraph:**
   > "Your useful god is Water. Water generates your Wood DM — it's your nourishment. Favorable: Water, Wood. Unfavorable: Earth, Metal, Fire (they drain or attack your weak Wood). Everything improves with more Water exposure."

2. **Add female spouse star check:**
   - For females: check DO (Direct Officer) = husband star
   - Currently only checks DW for males at line 1747

3. **Richer strength description:**
   - Include what the weak/strong verdict means practically
   - Reference specific chart elements (not just generic templates)

---

## Part 4: Remedies Cross-Linked with Health

### Current
Remedies only reference useful god element: colors, direction, industries, avoid colors.

### Proposed
Add a health-aware remedy sub-section:
- If any element is deficient → add its remedy colors/foods alongside useful god remedies
- If useful god remedies already cover the deficient element, note the synergy
- If they conflict (e.g., useful god = Water, but health needs Metal), explain priority:
  > "Primary: Water element (for DM strength). Secondary: Metal element (for lung health) — wear white/silver accessories."

Also add behavioral health remedies:
- Deficient Metal → "Practice deep breathing, protect lungs, wear scarves in cold weather"
- Excess Fire → "Avoid overstimulation, manage anxiety, protect cardiovascular system"

---

## Files to Modify

| File | Change |
|------|--------|
| `api/library/comprehensive/adapter.py` | `_summary_strength()`, `_summary_health()`, `_summary_honest()`, `_summary_remedies()` |
| `api/library/comprehensive/templates.py` | Add WHY-reasoning templates, health remedy templates, element cycle explanation templates |
| `src/components/LifeEventBlock.tsx` | Update frontend to render new health detail format |

---

## Key Principle: Correctness First

All changes derive from existing BaZi theory already encoded in the codebase:
- Element cycles from `ELEMENT_CYCLES` in `derived.py`
- Seasonal states from `BRANCHES[branch]["element_states"]`
- TCM organ mapping from `ELEMENT_ORGANS` in `life_aspects/health.py`
- Control cycle from `ELEMENT_CONTROLS` in `life_aspects/base.py`

No new theory is introduced. We're surfacing calculations that already happen but aren't displayed.
