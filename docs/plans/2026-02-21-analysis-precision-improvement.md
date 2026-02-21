# Analysis Precision Improvement — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Improve precision and comprehensiveness of all natal analysis sections (Strength, Health, Honest Summary, Remedies) on the profile page.

**Architecture:** All changes are in 2 backend files: `adapter.py` (section builders) and `templates.py` (new template data). The frontend `ClientSummaryDisplay.tsx` already renders sections generically via `{title, text, items[]}` — richer backend data displays automatically. No frontend changes needed.

**Tech Stack:** Python (FastAPI backend), existing `ELEMENT_CYCLES` from `derived.py`, `ELEMENT_CONTROLS` from `life_aspects/base.py`, `HEALTH_ELEMENT_MAP` from `templates.py`

---

### Task 1: Add WHY-reasoning to Strength Assessment

**Files:**
- Modify: `api/library/comprehensive/adapter.py:1194-1212` (`_summary_strength()`)
- Modify: `api/library/comprehensive/templates.py` (add element role descriptions)

**Context:** Currently `_summary_strength()` returns items like `{"label": "Favorable", "value": "Water, Wood"}` with no explanation. We need to add relationship descriptions (e.g., "Water — generates your Wood (resource)") and an explanation paragraph.

**Step 1: Add element role description templates to `templates.py`**

At the end of `templates.py` (after line 609), add:

```python
# =============================================================================
# ELEMENT ROLE EXPLANATIONS
# =============================================================================
# Used by strength assessment to explain WHY elements are favorable/unfavorable.
# Keys are (role, verdict_group) tuples.

ELEMENT_ROLE_DESCRIPTIONS = {
    # For weak/extremely_weak DM
    "resource_favorable": "{elem} generates your {dm} (resource) — it's your nourishment",
    "companion_favorable": "{dm} is your own element — companions strengthen you",
    "output_unfavorable": "{elem} is your output — it exhausts your already weak {dm}",
    "wealth_unfavorable": "{elem} is your wealth element — it drains your weak {dm}",
    "officer_unfavorable": "{elem} controls/attacks {dm} — even low amounts are harmful",
    # For strong/extremely_strong DM
    "output_favorable": "{elem} is your output — it channels your excess {dm} energy productively",
    "wealth_favorable": "{elem} is your wealth — it absorbs your excess strength",
    "officer_favorable": "{elem} controls {dm} — it disciplines your excess energy",
    "resource_unfavorable": "{elem} generates more {dm} — fuels an already overpowered chart",
    "companion_unfavorable": "{dm} companions add more energy to an already overloaded chart",
    # For following chart
    "following_favorable": "{elem} aligns with the dominant force — go with the flow",
    "following_unfavorable": "{elem} fights the current — resistance weakens a following chart",
}

# Explanation paragraph templates
STRENGTH_EXPLANATION = {
    "weak": (
        "Your {dm_name} is weak at {score}/100. A weak Day Master needs nourishment "
        "({resource} generates {dm_element}) and companions ({dm_element}). "
        "{unfav_explanation} "
        "Low amounts of unfavorable elements are actually a blessing — less pressure on your weak {dm_element}."
    ),
    "extremely_weak": (
        "Your {dm_name} is extremely weak at {score}/100. You are severely depleted. "
        "{resource} (resource) and {dm_element} (companions) are absolutely critical. "
        "Everything else — {unfav_list} — drains or attacks you. "
        "Environment, career, and relationships MUST supply {resource} energy."
    ),
    "strong": (
        "Your {dm_name} is strong at {score}/100. You have abundant energy that needs outlets. "
        "{output} (output) and {wealth} (wealth) channel your excess energy productively. "
        "{officer} disciplines your strength. More {dm_element} or {resource} would overload the chart."
    ),
    "extremely_strong": (
        "Your {dm_name} is extremely strong at {score}/100. Overwhelming energy needs heavy draining. "
        "{output}, {wealth}, and {officer} are all critical to prevent stagnation. "
        "Avoid {dm_element} and {resource} — they fuel an already excessive chart."
    ),
    "neutral": (
        "Your {dm_name} is balanced at {score}/100. Small shifts in luck pillars have outsized effects. "
        "{output} and {wealth} keep the chart productive. "
        "Avoid excessive {officer} which could tip the balance toward weakness."
    ),
}

# Health-specific behavioral remedies per element
HEALTH_BEHAVIORAL_REMEDIES = {
    "Wood": "Practice eye care, stretch regularly, manage anger through movement/exercise",
    "Fire": "Protect cardiovascular health, manage anxiety, avoid overstimulation and burnout",
    "Earth": "Maintain regular eating schedule, avoid overthinking, strengthen digestive health",
    "Metal": "Practice deep breathing exercises, protect lungs and skin, wear scarves in cold weather",
    "Water": "Strengthen lower back and bones, protect hearing, manage fear and anxiety",
}

# Control cycle imbalance explanations
CONTROL_CYCLE_EXPLANATIONS = {
    ("Wood", "Earth"): "Wood controls Earth. Weak Wood means digestive system (Spleen/Stomach) can become unregulated.",
    ("Fire", "Metal"): "Fire controls Metal. Weak Fire means respiratory system (Lungs) and immune response are unregulated.",
    ("Earth", "Water"): "Earth controls Water. Weak Earth means urinary/reproductive system (Kidneys) can become unregulated.",
    ("Metal", "Wood"): "Metal controls Wood. Weak Metal means liver system (Liver/Gallbladder) can become unregulated.",
    ("Water", "Fire"): "Water controls Fire. Weak Water means cardiovascular system (Heart) can become unregulated.",
}
```

**Step 2: Update `_summary_strength()` in adapter.py**

Replace the function at line 1194-1212 with:

```python
def _summary_strength(strength: StrengthAssessment) -> dict:
    """Section: DM strength assessment with WHY-reasoning."""
    from .templates import (
        STRENGTH_VERDICTS, ELEMENT_ROLE_DESCRIPTIONS,
        STRENGTH_EXPLANATION, _pick,
    )
    text = _pick(STRENGTH_VERDICTS.get(strength.verdict, ["No assessment available."]))

    dm_element = strength.useful_god  # We need the actual DM element
    # Reconstruct element roles from favorable/unfavorable lists
    # The useful god IS the resource element for weak DM, output element for strong DM

    # Build items with relationship descriptions
    items = [
        {"label": "Score", "value": f"{strength.score}/100"},
        {"label": "Useful God", "value": f"{strength.useful_god}"},
    ]

    # Favorable with WHY
    fav_parts = []
    for elem in strength.favorable_elements:
        fav_parts.append(elem)
    items.append({"label": "Favorable", "value": ", ".join(fav_parts)})

    # Unfavorable with WHY
    unfav_parts = []
    for elem in strength.unfavorable_elements:
        unfav_parts.append(elem)
    items.append({"label": "Unfavorable", "value": ", ".join(unfav_parts)})

    severity = ("strong" if strength.verdict in ("strong", "extremely_strong")
                else "weak" if strength.verdict in ("weak", "extremely_weak")
                else "neutral")
    return {
        "id": "strength",
        "title": "Strength Assessment",
        "title_zh": "日主強弱",
        "severity": severity,
        "text": text,
        "items": items,
    }
```

Wait — that doesn't add the WHY yet because `_summary_strength` doesn't have access to `chart`. We need to thread `chart` through. Let me fix the approach.

**Step 2 (revised): Update `_summary_strength()` signature and add WHY-reasoning**

In `adapter.py`, replace the existing `_summary_strength` (lines 1194-1212) with a version that accepts `chart: ChartData`:

```python
def _summary_strength(strength: StrengthAssessment, chart: ChartData) -> dict:
    """Section: DM strength assessment with WHY-reasoning for favorable/unfavorable."""
    from .templates import STRENGTH_VERDICTS, STRENGTH_EXPLANATION, _pick

    text = _pick(STRENGTH_VERDICTS.get(strength.verdict, ["No assessment available."]))

    dm_element = chart.dm_element
    dm_name = f"{chart.day_master} {dm_element}"
    resource = ELEMENT_CYCLES["generated_by"].get(dm_element, "")
    output = ELEMENT_CYCLES["generating"].get(dm_element, "")
    wealth = ELEMENT_CYCLES["controlling"].get(dm_element, "")
    officer = ELEMENT_CYCLES["controlled_by"].get(dm_element, "")

    # Role labels for each element relative to DM
    role_map = {
        dm_element: "companion",
        resource: "resource (generates you)",
        output: "output (exhausts you)" if strength.verdict in ("weak", "extremely_weak") else "output (channels your energy)",
        wealth: "wealth (drains you)" if strength.verdict in ("weak", "extremely_weak") else "wealth (absorbs strength)",
        officer: "officer (attacks you)" if strength.verdict in ("weak", "extremely_weak") else "officer (disciplines you)",
    }

    items = [
        {"label": "Score", "value": f"{strength.score}/100"},
        {"label": "Useful God", "value": f"{strength.useful_god} — {'generates your ' + dm_element if strength.verdict in ('weak', 'extremely_weak') else 'channels your ' + dm_element + ' energy'}"},
    ]

    # Favorable with role explanation
    fav_explained = []
    for elem in strength.favorable_elements:
        role = role_map.get(elem, "")
        fav_explained.append(f"{elem} ({role})" if role else elem)
    items.append({"label": "Favorable", "value": ", ".join(fav_explained)})

    # Unfavorable with role explanation
    unfav_explained = []
    for elem in strength.unfavorable_elements:
        role = role_map.get(elem, "")
        unfav_explained.append(f"{elem} ({role})" if role else elem)
    items.append({"label": "Unfavorable", "value": ", ".join(unfav_explained)})

    # Build explanation paragraph
    verdict_key = strength.verdict if strength.verdict in STRENGTH_EXPLANATION else "neutral"
    unfav_reasons = []
    for elem in strength.unfavorable_elements:
        role = role_map.get(elem, "")
        if role:
            unfav_reasons.append(f"{elem} {role}")
    explanation = STRENGTH_EXPLANATION[verdict_key].format(
        dm_name=dm_name, dm_element=dm_element, score=strength.score,
        resource=resource, output=output, wealth=wealth, officer=officer,
        unfav_list=", ".join(strength.unfavorable_elements),
        unfav_explanation=f"Unfavorable elements ({', '.join(strength.unfavorable_elements)}) all drain or attack your weak {dm_element}." if strength.verdict in ("weak", "extremely_weak") else "",
    )
    items.append({"label": "Why?", "value": explanation})

    severity = ("strong" if strength.verdict in ("strong", "extremely_strong")
                else "weak" if strength.verdict in ("weak", "extremely_weak")
                else "neutral")

    return {
        "id": "strength",
        "title": "Strength Assessment",
        "title_zh": "日主強弱",
        "severity": severity,
        "text": text,
        "items": items,
    }
```

**Step 3: Update all call sites of `_summary_strength` to pass `chart`**

In `adapter.py`, there are two call sites:
- Line ~1982: `_summary_strength(strength)` → change to `_summary_strength(strength, chart)`
- Line ~2034: in the full tier, also passes `strength` → change to `_summary_strength(strength, chart)`

Search for `_summary_strength(` in adapter.py and update both calls.

**Step 4: Verify syntax**

Run: `python3 -c "import py_compile; py_compile.compile('api/library/comprehensive/adapter.py', doraise=True); py_compile.compile('api/library/comprehensive/templates.py', doraise=True)"`
Expected: No output (success)

**Step 5: Commit**

```bash
git add api/library/comprehensive/adapter.py api/library/comprehensive/templates.py
git commit -m "feat: add WHY-reasoning to strength assessment (favorable/unfavorable explanations)"
```

---

### Task 2: Deep Health Section

**Files:**
- Modify: `api/library/comprehensive/adapter.py:1327-1353` (`_summary_health()`)

**Context:** Currently `_summary_health()` uses simple threshold (count < 1.0 or > 3.0) and one-line per element. We need to add: seasonal state analysis, control cycle imbalances, and multi-line explanations per organ.

**Step 1: Replace `_summary_health()` in adapter.py**

Replace lines 1327-1353 with:

```python
def _summary_health(chart: ChartData, strength: StrengthAssessment) -> dict:
    """Section: health based on element balance + seasonal states + control cycle.

    Three layers of analysis:
    1. Element balance: deficient/excess elements → organ vulnerability
    2. Seasonal state: elements in Dead/Trapped state → heightened risk
    3. Control cycle: weak controller → uncontrolled target organ
    """
    from .templates import HEALTH_ELEMENT_MAP, CONTROL_CYCLE_EXPLANATIONS
    from ..derived import ELEMENT_CYCLES

    elem_counts = count_elements(chart)
    total = sum(elem_counts.values())
    avg = total / 5 if total > 0 else 1.0

    # Get seasonal states for all elements
    month_branch = chart.pillars["month"].branch
    seasonal_states = BRANCHES[month_branch].get("element_states", {})

    # Detect control cycle imbalances
    ELEMENT_CONTROLS_MAP = {
        "Wood": "Earth", "Fire": "Metal", "Earth": "Water",
        "Metal": "Wood", "Water": "Fire",
    }
    control_imbalances = {}  # controlled_element -> controller info
    for controller, controlled in ELEMENT_CONTROLS_MAP.items():
        controller_state = seasonal_states.get(controller, "Resting")
        controller_count = elem_counts.get(controller, 0)
        # Weak controller: Dead/Trapped state OR very low count
        if controller_state in ("Dead", "Trapped") or controller_count < avg * 0.3:
            control_imbalances[controlled] = {
                "controller": controller,
                "controller_state": controller_state,
                "controller_count": controller_count,
            }

    items = []
    # Severity weighting: Dead=2.0, Trapped=1.5
    SEASONAL_WEIGHT = {"Dead": 2.0, "Trapped": 1.5, "Resting": 1.0, "Strengthening": 0.7, "Prosperous": 0.5}

    for elem in ["Wood", "Fire", "Earth", "Metal", "Water"]:
        count = elem_counts.get(elem, 0)
        pct = (count / total * 100) if total > 0 else 20
        organ_info = HEALTH_ELEMENT_MAP.get(elem, {})
        yin_organ = organ_info.get("yin_organ", elem)
        yang_organ = organ_info.get("yang_organ", "")
        body_parts = organ_info.get("body_parts", "")
        seasonal_state = seasonal_states.get(elem, "Resting")
        seasonal_w = SEASONAL_WEIGHT.get(seasonal_state, 1.0)

        reasons = []
        severity = None

        # Layer 1: Element balance
        if count < avg * 0.5:
            reasons.append(f"{elem} severely deficient ({pct:.0f}%). {organ_info.get('deficiency', 'vulnerability')}")
            severity = "warning"
        elif count < avg * 0.75:
            reasons.append(f"{elem} below average ({pct:.0f}%). Mild {yin_organ.split('(')[0].strip().lower()} vulnerability")
            severity = "mild"
        elif count > avg * 1.8:
            reasons.append(f"{elem} in excess ({pct:.0f}%). {organ_info.get('excess', 'overactive')}")
            severity = "warning"
        elif count > avg * 1.4:
            reasons.append(f"{elem} above average ({pct:.0f}%). Watch for: {organ_info.get('excess', 'overactivity')}")
            severity = "mild"

        # Layer 2: Seasonal vulnerability
        if seasonal_state in ("Dead", "Trapped"):
            state_label = "Dead (死)" if seasonal_state == "Dead" else "Trapped (囚)"
            reasons.append(f"{elem} in {state_label} seasonal state — heightened {yin_organ.split('(')[0].strip().lower()} vulnerability")
            severity = "warning" if severity != "warning" else severity

        # Layer 3: Control cycle imbalance
        if elem in control_imbalances:
            imb = control_imbalances[elem]
            ctrl = imb["controller"]
            explanation = CONTROL_CYCLE_EXPLANATIONS.get((ctrl, elem), "")
            if explanation:
                reasons.append(explanation)
            else:
                reasons.append(f"{ctrl} is too weak to control {elem} — {yin_organ.split('(')[0].strip().lower()} system unregulated")
            if severity is None:
                severity = "mild"
            elif severity == "mild":
                severity = "warning"

        # Only include elements with issues
        if reasons:
            items.append({
                "label": f"{yin_organ} ({elem})",
                "value": ". ".join(reasons) + f". Body parts: {body_parts}.",
                "severity": severity or "info",
            })

    # If no issues found, show balanced message
    if not items:
        items.append({
            "label": "Overall",
            "value": "Element balance is healthy. No significant organ system vulnerabilities detected.",
            "severity": "positive",
        })

    return {
        "id": "health",
        "title": "Health",
        "title_zh": "健康",
        "items": items,
    }
```

**Step 2: Update call sites of `_summary_health` to pass `strength`**

In `adapter.py`, find:
- `_summary_health(chart)` (line ~1988) → change to `_summary_health(chart, strength)`
- Any other call sites → update similarly

**Step 3: Verify syntax**

Run: `python3 -c "import py_compile; py_compile.compile('api/library/comprehensive/adapter.py', doraise=True)"`
Expected: No output (success)

**Step 4: Commit**

```bash
git add api/library/comprehensive/adapter.py
git commit -m "feat: deep health analysis with seasonal states + control cycle imbalances"
```

---

### Task 3: Improve Honest Summary

**Files:**
- Modify: `api/library/comprehensive/adapter.py:1694-1792` (`_summary_honest()`)

**Context:** The summary is decent but (a) doesn't explain WHY elements are favorable/unfavorable, (b) only checks male spouse star (DW), not female (DO), (c) no health cross-reference.

**Step 1: Update `_summary_honest()` in adapter.py**

Replace lines 1694-1792 with:

```python
def _summary_honest(chart: ChartData, strength: StrengthAssessment,
                     tg_classification: Dict[str, dict],
                     flags: Dict[str, List[RedFlag]]) -> dict:
    """Section: comprehensive honest life summary with WHY-reasoning."""
    from .templates import LIFE_LESSON_TEMPLATES, DM_NATURE, HEALTH_ELEMENT_MAP, _pick
    from .ten_gods import check_spouse_star

    dm_element = chart.dm_element
    dm_info = STEMS[chart.day_master]
    dm_key = (dm_info["element"], dm_info["polarity"].capitalize())
    nature = DM_NATURE.get(dm_key, {})

    resource = ELEMENT_CYCLES["generated_by"].get(dm_element, "")
    output = ELEMENT_CYCLES["generating"].get(dm_element, "")
    wealth = ELEMENT_CYCLES["controlling"].get(dm_element, "")
    officer = ELEMENT_CYCLES["controlled_by"].get(dm_element, "")

    # Life lesson
    if strength.is_following_chart:
        key = "following"
    elif strength.verdict in ("weak", "extremely_weak"):
        key = f"weak_{dm_element.lower()}"
    else:
        key = "strong_general"
    templates = LIFE_LESSON_TEMPLATES.get(key, LIFE_LESSON_TEMPLATES.get("strong_general", [""]))
    life_lesson = _pick(templates)

    parts = []

    # Who you are
    parts.append(f"You are {nature.get('name', chart.day_master)} ({nature.get('chinese', dm_info['chinese'])}). "
                 f"Personality: {nature.get('personality', 'unknown')}.")

    # Strength reality
    score = strength.score
    if score < 25:
        parts.append(f"Your Day Master is extremely weak ({score:.0f}/100). "
                     "You are easily overwhelmed by life's demands. "
                     "Your biggest challenge is finding support systems and environments that sustain you.")
    elif score < 42:
        parts.append(f"Your Day Master is weak ({score:.0f}/100). "
                     "You need more support than most people. "
                     "Resource and companion elements are your lifeline.")
    elif score < 58:
        parts.append(f"Your Day Master is balanced ({score:.0f}/100). "
                     "You have a flexible chart — small shifts in luck pillars have outsized effects on your life.")
    elif score < 75:
        parts.append(f"Your Day Master is strong ({score:.0f}/100). "
                     "You have abundant energy but need productive outlets. "
                     "Without channels for your strength, you become restless and domineering.")
    else:
        parts.append(f"Your Day Master is extremely strong ({score:.0f}/100). "
                     "You have overwhelming energy. The risk is stagnation and bulldozing over others.")

    # Marriage reality — GENDER-AWARE
    spouse = check_spouse_star(chart, tg_classification)
    marriage_flags = flags.get("marriage", [])

    # Also check female spouse star (DO = husband for females)
    if chart.gender == "female":
        do_strength = tg_classification.get("DO", {}).get("strength", "ABSENT")
        if do_strength == "ABSENT":
            parts.append("Marriage: Your husband star (正官 Direct Officer) is ABSENT. "
                         "This is the hardest marriage indicator for a woman — partnership comes very late, "
                         "with great difficulty, or through unconventional paths. "
                         "The right luck decade is critical.")
        elif spouse["is_critical_absent"]:
            parts.append(f"Marriage: Your {spouse['label']} is ABSENT. "
                         "Marriage is a major life challenge requiring conscious effort and the right timing.")
        elif marriage_flags:
            severe_count = sum(1 for f in marriage_flags if f.severity in ("severe", "critical"))
            if severe_count >= 2:
                parts.append("Marriage: Multiple severe marriage indicators. "
                             "Relationships are a major life challenge requiring active management.")
            elif severe_count == 1:
                parts.append("Marriage: One significant marriage challenge exists. "
                             "Awareness and timing can mitigate it.")
        else:
            parts.append("Marriage: No major obstacles in the natal chart. "
                         "Timing and luck pillar alignment will determine when.")
    else:
        # Male path (existing logic)
        if spouse["is_critical_absent"]:
            parts.append(f"Marriage: Your {spouse['label']} is ABSENT. "
                         "This is the single hardest indicator — marriage comes very late, "
                         "with great difficulty, or through unconventional paths. This is not a death sentence, "
                         "but it requires conscious effort and the right luck decade.")
        elif marriage_flags:
            severe_count = sum(1 for f in marriage_flags if f.severity in ("severe", "critical"))
            if severe_count >= 2:
                parts.append("Marriage: Multiple severe marriage indicators. "
                             "Relationships are a major life challenge requiring active management.")
            elif severe_count == 1:
                parts.append("Marriage: One significant marriage challenge exists. "
                             "Awareness and timing can mitigate it.")
        else:
            parts.append("Marriage: No major obstacles in the natal chart. "
                         "Timing and luck pillar alignment will determine when.")

    # Wealth reality
    dw = tg_classification.get("DW", {}).get("strength", "ABSENT")
    iw = tg_classification.get("IW", {}).get("strength", "ABSENT")
    rw = tg_classification.get("RW", {}).get("strength", "ABSENT")
    if dw == "ABSENT" and iw == "ABSENT":
        parts.append("Wealth: Both wealth stars absent. "
                     "Money doesn't come naturally — must be actively pursued through favorable elements and timing.")
    elif rw == "PROMINENT":
        parts.append("Wealth: Rob Wealth is prominent — money comes but also leaves through others. "
                     "Avoid partnerships and lending. Protect what you earn.")
    elif iw == "PROMINENT":
        parts.append("Wealth: Strong Indirect Wealth — windfall potential through speculation, business, or investments. "
                     "Risk tolerance is high, but so is the upside.")

    # Health cross-reference
    elem_counts = count_elements(chart)
    total_count = sum(elem_counts.values())
    avg_count = total_count / 5 if total_count > 0 else 1.0
    deficient_elements = [e for e in ["Wood", "Fire", "Earth", "Metal", "Water"]
                          if elem_counts.get(e, 0) < avg_count * 0.5]
    if deficient_elements:
        organs = []
        for e in deficient_elements:
            organ = HEALTH_ELEMENT_MAP.get(e, {}).get("yin_organ", e).split("(")[0].strip()
            organs.append(f"{organ} ({e})")
        parts.append(f"Health: Watch {', '.join(organs)} — these elements are deficient in your chart.")

    # The life lesson
    parts.append(f"Life lesson: {life_lesson}")

    # Useful God with WHY-reasoning
    if strength.verdict in ("weak", "extremely_weak"):
        parts.append(
            f"Your useful god is {strength.useful_god}. "
            f"{resource} generates your {dm_element} (resource — your nourishment), "
            f"{dm_element} companions strengthen you. "
            f"Unfavorable: {', '.join(strength.unfavorable_elements)} "
            f"(they drain or attack your weak {dm_element}). "
            f"Everything in your life improves when you increase {strength.useful_god} element exposure."
        )
    elif strength.verdict in ("strong", "extremely_strong"):
        parts.append(
            f"Your useful god is {strength.useful_god}. "
            f"{output} channels your excess {dm_element} energy (output), "
            f"{wealth} absorbs your strength (wealth). "
            f"Unfavorable: {dm_element} and {resource} (they overload an already powerful chart). "
            f"Everything in your life improves when you increase {strength.useful_god} element exposure."
        )
    else:
        parts.append(
            f"Your useful god is {strength.useful_god}. "
            f"Favorable: {', '.join(strength.favorable_elements)}. "
            f"Unfavorable: {', '.join(strength.unfavorable_elements)}. "
            f"Your chart is balanced — maintain exposure to {strength.useful_god} for optimal flow."
        )

    return {
        "id": "summary",
        "title": "Honest Summary",
        "title_zh": "總結",
        "text": " ".join(parts),
    }
```

**Step 2: Verify syntax**

Run: `python3 -c "import py_compile; py_compile.compile('api/library/comprehensive/adapter.py', doraise=True)"`
Expected: No output (success)

**Step 3: Commit**

```bash
git add api/library/comprehensive/adapter.py
git commit -m "feat: improve honest summary with gender-aware spouse star + health cross-ref + WHY-reasoning"
```

---

### Task 4: Remedies Cross-Linked with Health

**Files:**
- Modify: `api/library/comprehensive/adapter.py:1356-1375` (`_summary_remedies()`)

**Context:** Remedies only show useful god colors/direction/industries. Need to add health-aware remedies for deficient/excess elements and behavioral health guidance.

**Step 1: Update `_summary_remedies()` in adapter.py**

Replace lines 1356-1375 with:

```python
def _summary_remedies(strength: StrengthAssessment, chart: ChartData) -> dict:
    """Section: remedies with health cross-linking."""
    from .templates import ELEMENT_REMEDIES, HEALTH_ELEMENT_MAP, HEALTH_BEHAVIORAL_REMEDIES

    useful = strength.useful_god
    remedies = ELEMENT_REMEDIES.get(useful, {})
    items = []

    if remedies:
        colors = ", ".join(remedies.get("colors", []))
        items.append({"label": "Colors", "value": f"Wear {colors} ({useful} element)"})
        items.append({"label": "Direction", "value": remedies.get("direction", "")})
        industries = ", ".join(remedies.get("industries", [])[:5])
        items.append({"label": "Industries", "value": industries})
        avoid = ", ".join(remedies.get("avoid_colors", []))
        if avoid:
            items.append({"label": "Avoid Colors", "value": avoid})

    # Health-aware remedies: check for deficient elements
    elem_counts = count_elements(chart)
    total = sum(elem_counts.values())
    avg = total / 5 if total > 0 else 1.0

    health_items = []
    for elem in ["Wood", "Fire", "Earth", "Metal", "Water"]:
        count = elem_counts.get(elem, 0)
        if count < avg * 0.5:
            elem_remedies = ELEMENT_REMEDIES.get(elem, {})
            organ = HEALTH_ELEMENT_MAP.get(elem, {}).get("yin_organ", elem).split("(")[0].strip()
            behavioral = HEALTH_BEHAVIORAL_REMEDIES.get(elem, "")

            if elem == useful:
                # Synergy: useful god already covers this element
                health_items.append({
                    "label": f"Health + Useful God synergy ({elem})",
                    "value": f"Your useful god ({useful}) also addresses your {organ.lower()} health. "
                             f"{behavioral}",
                    "severity": "positive",
                })
            else:
                # Secondary element remedy
                elem_colors = ", ".join(elem_remedies.get("colors", [])[:2])
                health_items.append({
                    "label": f"Health: {organ} ({elem})",
                    "value": f"Low {elem} weakens {organ.lower()}. "
                             f"Secondary remedy: add {elem_colors} accessories. {behavioral}",
                    "severity": "info",
                })

    # Add excess element warnings
    for elem in ["Wood", "Fire", "Earth", "Metal", "Water"]:
        count = elem_counts.get(elem, 0)
        if count > avg * 1.8:
            organ = HEALTH_ELEMENT_MAP.get(elem, {}).get("yin_organ", elem).split("(")[0].strip()
            behavioral = HEALTH_BEHAVIORAL_REMEDIES.get(elem, "")
            health_items.append({
                "label": f"Health: {organ} excess ({elem})",
                "value": f"High {elem} overloads {organ.lower()}. "
                         f"Reduce {elem} element exposure. {behavioral}",
                "severity": "warning",
            })

    items.extend(health_items)

    return {
        "id": "remedies",
        "title": "Remedies",
        "title_zh": "化解建議",
        "items": items,
    }
```

**Step 2: Update all call sites of `_summary_remedies` to pass `chart`**

In `adapter.py`, find:
- `_summary_remedies(strength)` (line ~1989) → change to `_summary_remedies(strength, chart)`
- `_summary_remedies(strength)` (line ~2034 in full tier) → change to `_summary_remedies(strength, chart)`

**Step 3: Verify syntax**

Run: `python3 -c "import py_compile; py_compile.compile('api/library/comprehensive/adapter.py', doraise=True)"`
Expected: No output (success)

**Step 4: Commit**

```bash
git add api/library/comprehensive/adapter.py
git commit -m "feat: cross-link remedies with health (deficient element guidance + behavioral remedies)"
```

---

### Task 5: TypeScript Check + Build Verification

**Files:**
- No code changes — verification only

**Step 1: TypeScript type check**

Run: `cd /Users/macbookair/GitHub/bazingse && npx tsc --noEmit`
Expected: No output (success). The frontend doesn't need changes since `ClientSummaryDisplay.tsx` renders items generically.

**Step 2: Python syntax check (all modified files)**

Run: `cd /Users/macbookair/GitHub/bazingse/api && source .venv/bin/activate && python3 -c "import py_compile; [py_compile.compile(f, doraise=True) for f in ['library/comprehensive/adapter.py', 'library/comprehensive/templates.py']]"`
Expected: No output (success)

**Step 3: Full Next.js build**

Run: `cd /Users/macbookair/GitHub/bazingse && npm run build`
Expected: Build succeeds with all 3 pages generating

**Step 4: Import verification**

Run: `cd /Users/macbookair/GitHub/bazingse/api && source .venv/bin/activate && python3 -c "from library.comprehensive.adapter import adapt_to_frontend; from library.comprehensive.templates import STRENGTH_EXPLANATION, CONTROL_CYCLE_EXPLANATIONS, HEALTH_BEHAVIORAL_REMEDIES; print('All imports OK')"`
Expected: "All imports OK"
