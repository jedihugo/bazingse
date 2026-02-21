# Qi Phase Contextual Analysis + Spiritual Sensitivity Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add contextual qi phase interpretations (all 12 phases x 4 pillars + tandem effects with Shen Sha) and a spiritual sensitivity assessment that detects whether a person can perceive other dimensions.

**Architecture:** Two new Python modules in `api/library/comprehensive/` — one for qi phase contextual analysis, one for spiritual sensitivity scoring. Both integrate into the existing `analyze_bazi` API response. Frontend displays both on the profile page via new components. The `/bazi` skill is updated with new sections.

**Tech Stack:** Python (FastAPI backend), React/Next.js (frontend), TypeScript

---

### Task 1: Update the /bazi Skill with New Sections

**Files:**
- Modify: `/Users/macbookair/.claude/skills/bazi/SKILL.md`

**Step 1: Add Section 5B (Qi Phase Analysis) and Section 5C (Spiritual Sensitivity) to the skill**

After the existing Section 5 (Shen Sha Full Audit), add these two new sections:

```markdown
## SECTION 5B: QI PHASE CONTEXTUAL ANALYSIS (十二长生深度分析)

For EACH of the four natal pillars, calculate the Day Master's Qi Phase (十二长生) in that branch and provide contextual interpretation.

The 12 phases: 长生 → 沐浴 → 冠带 → 临官 → 帝旺 → 衰 → 病 → 死 → 墓 → 绝 → 胎 → 养

### Per-Pillar Interpretation

Each phase has DIFFERENT meaning depending on which pillar it appears in:

| Pillar | Governs | Context |
|--------|---------|---------|
| Year (年柱) | Parents, ancestry, childhood (0-15) | Family karma, inherited traits |
| Month (月柱) | Career, social status, youth (16-32) | Professional path, public life |
| Day (日柱) | Self, spouse, middle age (33-48) | Personal nature, marriage quality |
| Hour (时柱) | Children, legacy, old age (49+) | Offspring fate, twilight years |

### Full 12 x 4 Phase Meanings

**长生 (Chang Sheng / Birth):**
- Year: Born into a growing family, ancestors who started fresh, pioneering lineage
- Month: Career with fresh beginnings, good for entrepreneurship, building from scratch
- Day: Vitality in self and marriage, spouse brings new energy, relationship grows over time
- Hour: Children with great potential, legacy of new beginnings, vibrant old age

**沐浴 (Mu Yu / Bathing):**
- Year: Family scandals or instability in ancestry, parents with romantic complications
- Month: Career instability, romantic entanglements at work, changing jobs frequently
- Day: Romantic but turbulent marriage, strong sexual energy, spouse with wild streak
- Hour: Children with rebellious nature, unstable later years, romance in old age

**冠带 (Guan Dai / Capping):**
- Year: Family gaining recognition, ancestors who rose in social status
- Month: Career advancement phase, gaining professional credentials, respected at work
- Day: Maturing self/marriage, taking responsibility in partnership, growing together
- Hour: Children who achieve recognition, legacy of achievement, dignified old age

**临官 (Lin Guan / Official):**
- Year: Powerful family, ancestors in government or authority positions
- Month: Strong career authority, leadership roles, professional peak
- Day: Authoritative personality, spouse with power/status, commanding presence
- Hour: Children in authority positions, legacy of power, respected elder

**帝旺 (Di Wang / Emperor):**
- Year: Extremely powerful family, peak of ancestral fortune (but turning point — what goes up must come down)
- Month: Career at absolute peak — but danger of decline. Maximum achievement but also maximum vulnerability
- Day: Maximum personal power, dominant in marriage (risk of overbearing). At the turning point of life
- Hour: Children at peak potential but risk of excess, legacy that peaks then transforms

**衰 (Shuai / Decline):**
- Year: Family past its prime, declining ancestral fortune, inherited debts or burdens
- Month: Career losing momentum, need to conserve resources, past professional peak
- Day: Personal energy declining, marriage entering comfortable but less passionate phase
- Hour: Children face declining circumstances, legacy needs protection, health-conscious old age needed

**病 (Bing / Illness):**
- Year: Sickly ancestors, inherited health vulnerabilities, childhood health issues
- Month: Career struggles, professional setbacks, work-related stress/health issues
- Day: Personal health vulnerabilities, marriage under stress, spouse may have health issues
- Hour: Children with health concerns, old age requiring medical attention, fragile legacy

**死 (Si / Death):**
- Year: Ancestral endings, family line transformation, loss of heritage
- Month: Career ending or major transformation, old profession dies to birth new one
- Day: Transformation of self, marriage through death-and-rebirth cycle, complete personal change
- Hour: Children bring endings that create new beginnings, twilight as transformation

**墓 (Mu / Tomb/Storage):**
- Year: Hidden family wealth or secrets, ancestors left buried treasures (literal or figurative)
- Month: Career potential locked away, stored professional capabilities awaiting release (needs clash to open)
- Day: Spouse carries hidden assets or hidden emotional depth, relationship has buried potential
- Hour: Children hold things inside, legacy stored for future generations, retirement savings

**绝 (Jue / Extinction):**
- Year: Complete break from ancestry, orphan energy, family line cut
- Month: Career void, complete professional restart needed, old path extinct
- Day: Self at void point — but this is the seed of complete rebirth. Marriage may start from absolute zero
- Hour: Children face starting from nothing, legacy of spiritual emptiness that becomes freedom

**胎 (Tai / Embryo):**
- Year: Family in transition, new generation forming, pregnancy in family history
- Month: Career plans forming but not yet manifest, professional ideas gestating
- Day: Relationship developing, potential not yet realized, self in planning stage
- Hour: Children planned or forming, legacy being conceived, old age as new beginning

**养 (Yang / Nurturing):**
- Year: Protected childhood, well-nurtured ancestry, family that builds slowly
- Month: Career being nurtured by mentors, slow professional development, building foundation
- Day: Nurturing relationship, patient partnership, self being cultivated
- Hour: Children well-cared for, legacy being tended, comfortable retirement

### Tandem Effects (Phase + Shen Sha Combinations)

When a Qi Phase appears alongside specific Shen Sha or Ten God patterns, the meaning AMPLIFIES or CHANGES:

| Combination | Effect |
|-------------|--------|
| 沐浴 + 桃花 (Bathing + Peach Blossom) | EXTREMELY strong romantic/affair energy — sexual magnetism at maximum |
| 沐浴 + 偏印 (Bathing + Indirect Resource) | Vulnerability + unconventional thinking = spiritual opening, psychic sensitivity |
| 帝旺 + 羊刃 (Emperor + Yang Blade) | Dangerously aggressive, accident-prone, but also extremely powerful if channeled |
| 帝旺 + 将星 (Emperor + General Star) | Born commander — natural authority at peak, military/leadership destiny |
| 墓 + 华盖 (Tomb + Canopy Star) | Deep spiritual storage — can perceive hidden/mystical things, meditation talent |
| 墓 + 空亡 (Tomb + Void) | Buried emptiness — hidden losses, but also gateway to spiritual realm |
| 长生 + 贵人 (Birth + Noble Star) | Blessed beginning — protected by helpers, smooth start in that palace's domain |
| 长生 + 禄神 (Birth + Prosperity Star) | Born into wealth flow, self-renewing prosperity |
| 绝 + 空亡 (Extinction + Void) | Complete emptiness — thin veil between worlds, extreme spiritual sensitivity |
| 绝 + 童子 (Extinction + Child Star) | Past-life soul — strong indicator of being a spirit sent from heaven |
| 临官 + 文昌 (Official + Academic Star) | Scholar-official destiny — authority through education/knowledge |
| 病 + 天医 (Illness + Heavenly Doctor) | Healer archetype — illness in chart drives toward medical/healing career |
| 衰 + 劫煞 (Decline + Robbery Star) | Declining energy + robbery = vulnerable to loss, timing of financial setback |
| 胎 + 红鸾 (Embryo + Red Phoenix) | New romance forming — pregnancy of love, relationship about to be born |

Show each pillar's qi phase, its contextual meaning, and flag any tandem effects with present Shen Sha.

## SECTION 5C: SPIRITUAL SENSITIVITY ASSESSMENT (灵性敏感度评估)

Assess whether this person has heightened spiritual sensitivity — the ability to perceive beyond the physical dimension, sense spirits, have prophetic dreams, or "see" things others cannot.

### Indicators (check ALL and score):

**Primary Indicators (high weight):**
- 华盖 (Hua Gai / Canopy Star) present: +25 — THE classical spiritual marker. Solitary, introspective, drawn to metaphysics
- 童子 (Tong Zi / Child Star) present: +20 — "Spirit child" sent from heaven, soul not fully of this world
- 太极贵人 (Tai Ji Noble) present: +15 — Metaphysical intelligence, natural affinity for yin-yang and the unseen
- 空亡 (Kong Wang / Void) on day or hour pillar: +15 — "Empty space" in the chart = thin barrier between worlds
- 偏印 (Indirect Resource) prominent: +15 — Unconventional perception, channel for non-physical knowledge

**Secondary Indicators (moderate weight):**
- 亡神 (Wang Shen / Lost Spirit) present: +10 — Spirit energy scattered, porous boundary with spirit realm
- Day Master 壬 or 癸 (Ren/Gui Water): +5 — Water element naturally intuitive, reflective, psychic
- Multiple Yin (阴) stems in chart (3+): +5 — Yin energy more receptive to spiritual/invisible realm
- 墓 + 华盖 combo (Tomb + Canopy in same pillar): +10 bonus — Deep spiritual storage, meditation talent, can access hidden knowledge
- 沐浴 + 偏印 combo (Bathing + Indirect Resource): +10 bonus — Vulnerability + psychic channel = spiritual opening
- 绝 + 空亡 combo (Extinction + Void): +10 bonus — Complete void = extremely thin veil between worlds

**Dampening Indicators (reduce score):**
- 正印 (Direct Resource) dominant over 偏印: -10 — Orthodox thinking overrides intuition
- Very strong DM (score > 75): -5 — Too grounded/material, less spiritual receptivity
- 正官 (Direct Officer) very prominent: -5 — Rigid structure suppresses spiritual sensitivity

### Sensitivity Levels:

| Score | Level | Description |
|-------|-------|-------------|
| 0-20 | Normal | Grounded, practical, not particularly spiritual. Trusts what can be seen and touched. |
| 21-40 | Mild Awareness | Gets "gut feelings" that turn out correct. Intuitive but dismisses it as coincidence. |
| 41-60 | Moderate Sensitivity | Vivid dreams that sometimes come true. Senses presence of spirits. Drawn to temples/churches. Feels energy of places. |
| 61-80 | Strong Sensitivity | Can perceive spirits or energies. Attracted to mystical/occult knowledge. May have experienced unexplainable events. Should develop this ability rather than suppress it. |
| 81-100 | Extremely Sensitive | "Third eye" naturally open. Sees/senses other dimensions. Prophetic dreams are common. May have been told they're "different" since childhood. Needs grounding practices to stay balanced. |

### Assessment Output:

1. **Score**: X/100
2. **Level**: [Level name]
3. **Indicators found**: List each present indicator with its weight
4. **Tandem effects**: Flag any qi phase + shen sha combos that amplify spiritual sensitivity
5. **Description**: 2-3 sentences describing this person's spiritual profile in plain language
6. **Guidance**: If score > 40, recommend spiritual development practices. If score > 60, warn about need for grounding. If score > 80, note that suppressing this ability causes psychological distress — it should be developed and managed, not ignored.
```

Also update SECTION 6 (Red Flags) to include:
- Reference qi phase findings when they reinforce other indicators
- Add "Spiritual Sensitivity" as a life area if score > 40

Also update SECTION 9 (Remedies) to add:

```markdown
### 9h. Spiritual Sensitivity Management
Based on Section 5C findings:
- If score > 60: recommend meditation, temple visits, spiritual teacher/guide. Warn against suppression — causes anxiety/depression.
- If score > 80: recommend formal spiritual development (meditation retreat, spiritual mentor). Note that this person likely already experiences phenomena — validate rather than dismiss.
- If 华盖 + 空亡 combo: recommend structured spiritual practice (Buddhism, Taoism, yoga) rather than unstructured exploration.
- If 童子 (Child Star): classical remedy is "送替身" (sending a substitute) — the person may need symbolic ritual to settle their spirit.
- Grounding practices for highly sensitive people: physical exercise, Earth element remedies, structured daily routine.
```

**Step 2: Verify the skill file reads correctly**

Run: Read the updated skill file and check formatting is clean.

**Step 3: Commit**

```bash
git add /Users/macbookair/.claude/skills/bazi/SKILL.md
git commit -m "feat: add qi phase contextual analysis + spiritual sensitivity to /bazi skill"
```

---

### Task 2: Create Qi Phase Contextual Analysis Module

**Files:**
- Create: `api/library/comprehensive/qi_phase_analysis.py`

**Step 1: Create the qi phase contextual meanings database**

This module contains all 12 phases x 4 pillars = 48 interpretations, plus the tandem effects table. Uses the existing `get_qi_phase_for_pillar()` from `api/library/qi_phase.py` for calculation, then layers contextual meaning on top.

```python
# api/library/comprehensive/qi_phase_analysis.py
"""
Qi Phase Contextual Analysis (十二长生深度分析)
All 12 phases x 4 pillars + tandem effects with Shen Sha.
"""

from typing import List, Dict, Optional, Tuple
from ..qi_phase import get_qi_phase_for_pillar
from ..core import STEMS, BRANCHES
from .models import ChartData, ShenShaResult


# =============================================================================
# PILLAR-CONTEXTUAL MEANINGS (12 phases x 4 positions)
# =============================================================================
# Keys: qi phase id from qi_phase.py (changsheng, muyu, guandai, etc.)
# Each maps to {year, month, day, hour} interpretations.

PHASE_PILLAR_MEANINGS: Dict[str, Dict[str, str]] = {
    "changsheng": {
        "year": "Born into a growing family, pioneering lineage, ancestors who started fresh",
        "month": "Career with fresh beginnings, good for entrepreneurship, building from scratch",
        "day": "Vitality in self and marriage, spouse brings new energy, relationship grows over time",
        "hour": "Children with great potential, legacy of new beginnings, vibrant old age",
    },
    "muyu": {
        "year": "Family scandals or instability in ancestry, parents with romantic complications",
        "month": "Career instability, romantic entanglements at work, changing jobs frequently",
        "day": "Romantic but turbulent marriage, strong sexual energy, spouse with wild streak",
        "hour": "Children with rebellious nature, unstable later years, romance in old age",
    },
    "guandai": {
        "year": "Family gaining recognition, ancestors who rose in social status",
        "month": "Career advancement phase, gaining professional credentials, respected at work",
        "day": "Maturing self/marriage, taking responsibility in partnership, growing together",
        "hour": "Children who achieve recognition, legacy of achievement, dignified old age",
    },
    "linguan": {
        "year": "Powerful family, ancestors in government or authority positions",
        "month": "Strong career authority, leadership roles, professional peak",
        "day": "Authoritative personality, spouse with power/status, commanding presence",
        "hour": "Children in authority positions, legacy of power, respected elder",
    },
    "diwang": {
        "year": "Extremely powerful family, peak of ancestral fortune — but at turning point",
        "month": "Career at absolute peak — maximum achievement but also maximum vulnerability to decline",
        "day": "Maximum personal power, dominant in marriage — risk of overbearing. Life's turning point",
        "hour": "Children at peak potential but risk of excess, legacy that peaks then transforms",
    },
    "shuai": {
        "year": "Family past its prime, declining ancestral fortune, inherited debts or burdens",
        "month": "Career losing momentum, need to conserve resources, past professional peak",
        "day": "Personal energy declining, marriage entering comfortable but less passionate phase",
        "hour": "Children face declining circumstances, legacy needs protection, health-conscious old age",
    },
    "bing": {
        "year": "Sickly ancestors, inherited health vulnerabilities, childhood health issues",
        "month": "Career struggles, professional setbacks, work-related stress or health issues",
        "day": "Personal health vulnerabilities, marriage under stress, spouse may have health issues",
        "hour": "Children with health concerns, old age requiring medical attention, fragile legacy",
    },
    "si": {
        "year": "Ancestral endings, family line transformation, loss of heritage",
        "month": "Career ending or major transformation, old profession dies to birth new one",
        "day": "Transformation of self, marriage through death-and-rebirth cycle, complete personal change",
        "hour": "Children bring endings that create new beginnings, twilight as transformation",
    },
    "mu": {
        "year": "Hidden family wealth or secrets, ancestors left buried treasures — literal or figurative",
        "month": "Career potential locked away, stored professional capabilities awaiting release via clash",
        "day": "Spouse carries hidden assets or hidden emotional depth, relationship has buried potential",
        "hour": "Children hold things inside, legacy stored for future generations, retirement savings",
    },
    "jue": {
        "year": "Complete break from ancestry, orphan energy, family line cut",
        "month": "Career void, complete professional restart needed, old path extinct",
        "day": "Self at void point — seed of complete rebirth. Marriage may start from absolute zero",
        "hour": "Children face starting from nothing, legacy of spiritual emptiness becoming freedom",
    },
    "tai": {
        "year": "Family in transition, new generation forming, pregnancy energy in family history",
        "month": "Career plans forming but not yet manifest, professional ideas gestating",
        "day": "Relationship developing, potential not yet realized, self in planning stage",
        "hour": "Children planned or forming, legacy being conceived, old age as new beginning",
    },
    "yang": {
        "year": "Protected childhood, well-nurtured ancestry, family that builds slowly",
        "month": "Career being nurtured by mentors, slow professional development, building foundation",
        "day": "Nurturing relationship, patient partnership, self being cultivated over time",
        "hour": "Children well-cared for, legacy being tended carefully, comfortable retirement",
    },
}


# =============================================================================
# TANDEM EFFECTS: Qi Phase + Shen Sha combinations
# =============================================================================
# Each entry: (qi_phase_id, shen_sha_chinese, effect_description, spiritual_bonus)
# spiritual_bonus: extra points added to spiritual sensitivity score when this combo fires

TANDEM_EFFECTS: List[Tuple[str, str, str, int]] = [
    ("muyu", "桃花", "EXTREMELY strong romantic/affair energy — sexual magnetism at maximum", 0),
    ("muyu", "偏印", "Vulnerability + unconventional thinking = spiritual opening, psychic sensitivity", 5),
    ("diwang", "羊刃", "Dangerously aggressive, accident-prone — but extremely powerful if channeled", 0),
    ("diwang", "将星", "Born commander — natural authority at peak, military/leadership destiny", 0),
    ("mu", "华盖", "Deep spiritual storage — can perceive hidden/mystical things, meditation talent", 10),
    ("mu", "空亡", "Buried emptiness — hidden losses, but also gateway to spiritual realm", 5),
    ("changsheng", "天乙贵人", "Blessed beginning — protected by helpers, smooth start in that domain", 0),
    ("changsheng", "禄神", "Born into wealth flow, self-renewing prosperity", 0),
    ("jue", "空亡", "Complete emptiness — extremely thin veil between worlds, high spiritual sensitivity", 10),
    ("jue", "童子", "Past-life soul — strong indicator of being a spirit sent from heaven", 10),
    ("linguan", "文昌贵人", "Scholar-official destiny — authority through education and knowledge", 0),
    ("bing", "天医", "Healer archetype — illness in chart drives toward medical/healing career", 0),
    ("shuai", "劫煞", "Declining energy + robbery = vulnerable to loss, timing of financial setback", 0),
    ("tai", "红鸾", "New romance forming — pregnancy of love, relationship about to be born", 0),
    ("si", "华盖", "Death + solitude = deep mystical transformation, near-death spiritual awakening", 8),
    ("yang", "天乙贵人", "Nurturing protected by noble people — slow but blessed development", 0),
]


def analyze_qi_phases(chart: ChartData, shen_sha_results: List[ShenShaResult]) -> Dict:
    """
    Analyze qi phases for all four natal pillars with contextual interpretations
    and tandem effects with present Shen Sha.

    Returns:
        {
            "pillars": {
                "year": { "phase_id", "phase_chinese", "phase_english",
                          "strength", "interpretation", "tandem_effects": [...] },
                "month": { ... },
                "day": { ... },
                "hour": { ... },
            },
            "spiritual_bonus": int  # extra spiritual points from tandem combos
        }
    """
    dm_stem = chart.day_master
    present_shen_sha = {r.name_chinese for r in shen_sha_results if r.present}

    # Build a map of shen_sha per palace for tandem detection
    shen_sha_by_palace: Dict[str, set] = {"year": set(), "month": set(), "day": set(), "hour": set()}
    for r in shen_sha_results:
        if r.present and r.palace and r.palace in shen_sha_by_palace:
            shen_sha_by_palace[r.palace].add(r.name_chinese)

    result_pillars = {}
    total_spiritual_bonus = 0

    for pos in ["year", "month", "day", "hour"]:
        pillar = chart.pillars[pos]
        phase = get_qi_phase_for_pillar(dm_stem, pillar.branch)

        if not phase:
            result_pillars[pos] = {
                "phase_id": None,
                "phase_chinese": "未知",
                "phase_english": "Unknown",
                "strength": "unknown",
                "interpretation": "Cannot determine qi phase",
                "tandem_effects": [],
            }
            continue

        phase_id = phase["id"]
        meanings = PHASE_PILLAR_MEANINGS.get(phase_id, {})
        interpretation = meanings.get(pos, "No specific interpretation available")

        # Check tandem effects for this pillar
        tandem_hits = []
        for t_phase, t_shensha, t_effect, t_spiritual in TANDEM_EFFECTS:
            if phase_id == t_phase:
                # Check if the shen sha is present in this specific palace OR globally
                if t_shensha in shen_sha_by_palace[pos] or t_shensha in present_shen_sha:
                    tandem_hits.append({
                        "shen_sha": t_shensha,
                        "effect": t_effect,
                        "spiritual_bonus": t_spiritual,
                    })
                    total_spiritual_bonus += t_spiritual

        result_pillars[pos] = {
            "phase_id": phase_id,
            "phase_chinese": phase["chinese"],
            "phase_english": phase["english"],
            "strength": phase.get("strength", "unknown"),
            "interpretation": interpretation,
            "tandem_effects": tandem_hits,
        }

    return {
        "pillars": result_pillars,
        "spiritual_bonus": total_spiritual_bonus,
    }
```

**Step 2: Verify syntax**

Run: `python3 -c "import py_compile; py_compile.compile('api/library/comprehensive/qi_phase_analysis.py', doraise=True)"`
Expected: No output (success)

**Step 3: Commit**

```bash
git add api/library/comprehensive/qi_phase_analysis.py
git commit -m "feat: add qi phase contextual analysis module (12x4 meanings + tandem effects)"
```

---

### Task 3: Create Spiritual Sensitivity Module

**Files:**
- Create: `api/library/comprehensive/spiritual_sensitivity.py`

**Step 1: Create the spiritual sensitivity scoring engine**

```python
# api/library/comprehensive/spiritual_sensitivity.py
"""
Spiritual Sensitivity Assessment (灵性敏感度评估)
Combines Shen Sha, Ten Gods, qi phase combos, and DM traits
to score a person's sensitivity to the spiritual/unseen realm.
"""

from typing import List, Dict
from ..core import STEMS
from ..derived import get_ten_god
from .models import ChartData, ShenShaResult


# =============================================================================
# SENSITIVITY LEVELS
# =============================================================================

SENSITIVITY_LEVELS = [
    {
        "min": 0, "max": 20,
        "level": "normal",
        "label_en": "Normal",
        "label_zh": "正常",
        "description_en": "Grounded, practical, not particularly spiritual. Trusts what can be seen and touched.",
        "description_zh": "脚踏实地、务实，没有特别的灵性倾向。相信眼见为实。",
    },
    {
        "min": 21, "max": 40,
        "level": "mild",
        "label_en": "Mild Awareness",
        "label_zh": "轻度感知",
        "description_en": "Gets 'gut feelings' that turn out correct. Intuitive but dismisses it as coincidence.",
        "description_zh": "经常有准确的"直觉"，但自己把它当作巧合。",
    },
    {
        "min": 41, "max": 60,
        "level": "moderate",
        "label_en": "Moderate Sensitivity",
        "label_zh": "中度敏感",
        "description_en": "Vivid dreams that sometimes come true. Senses presence of spirits. Drawn to temples/churches. Feels energy of places.",
        "description_zh": "梦境清晰，有时会成真。能感应到灵体的存在。被寺庙/教堂吸引。能感受到场所的能量。",
    },
    {
        "min": 61, "max": 80,
        "level": "strong",
        "label_en": "Strong Sensitivity",
        "label_zh": "高度敏感",
        "description_en": "Can perceive spirits or energies. Attracted to mystical/occult knowledge. May have experienced unexplainable events. Should develop this ability rather than suppress it.",
        "description_zh": "能感知灵体或能量。被神秘/玄学知识吸引。可能经历过无法解释的事件。应该发展这种能力，而不是压制它。",
    },
    {
        "min": 81, "max": 100,
        "level": "extreme",
        "label_en": "Extremely Sensitive",
        "label_zh": "极度敏感",
        "description_en": "'Third eye' naturally open. Sees/senses other dimensions. Prophetic dreams are common. Has been told they're 'different' since childhood. Needs grounding practices to stay balanced.",
        "description_zh": ""天眼"自然开启。能看到/感知另一个维度。预知梦很常见。从小就被认为"与众不同"。需要接地练习来保持平衡。",
    },
]


def _get_level(score: int) -> dict:
    """Get the sensitivity level for a given score."""
    clamped = max(0, min(100, score))
    for level in SENSITIVITY_LEVELS:
        if level["min"] <= clamped <= level["max"]:
            return level
    return SENSITIVITY_LEVELS[0]


def assess_spiritual_sensitivity(
    chart: ChartData,
    shen_sha_results: List[ShenShaResult],
    qi_phase_spiritual_bonus: int = 0,
) -> Dict:
    """
    Assess spiritual sensitivity based on Shen Sha, Ten Gods, DM traits,
    and qi phase tandem bonuses.

    Returns:
        {
            "score": int (0-100),
            "level": str,
            "label_en": str,
            "label_zh": str,
            "description_en": str,
            "description_zh": str,
            "indicators": [{"name", "name_zh", "weight", "reason"}, ...],
            "guidance_en": str,
            "guidance_zh": str,
        }
    """
    indicators = []
    score = 0

    present_shen_sha = {}
    for r in shen_sha_results:
        if r.present:
            present_shen_sha[r.name_chinese] = r

    # --- PRIMARY INDICATORS ---

    # 华盖 (Canopy Star) — #1 spiritual marker
    if "华盖" in present_shen_sha:
        w = 25
        score += w
        indicators.append({
            "name": "Canopy Star (Hua Gai)",
            "name_zh": "华盖",
            "weight": w,
            "reason": "THE classical spiritual marker — solitary, introspective, drawn to metaphysics",
        })

    # 童子 (Child Star) — spirit child
    if "童子" in present_shen_sha:
        w = 20
        score += w
        indicators.append({
            "name": "Child Star (Tong Zi)",
            "name_zh": "童子",
            "weight": w,
            "reason": "Spirit child sent from heaven — soul not fully of this world",
        })

    # 太极贵人 (Tai Ji Noble)
    if "太极贵人" in present_shen_sha:
        w = 15
        score += w
        indicators.append({
            "name": "Tai Ji Noble",
            "name_zh": "太极贵人",
            "weight": w,
            "reason": "Metaphysical intelligence — natural affinity for yin-yang and the unseen",
        })

    # 空亡 (Void) on day or hour pillar
    for r in shen_sha_results:
        if r.name_chinese == "空亡" and r.present and r.palace in ("day", "hour"):
            w = 15
            score += w
            indicators.append({
                "name": f"Void (Kong Wang) in {r.palace} pillar",
                "name_zh": f"空亡在{{'day': '日柱', 'hour': '时柱'}[r.palace]}",
                "weight": w,
                "reason": f"Empty space in {r.palace} palace = thin barrier between worlds",
            })
            break  # Only count once

    # 偏印 (Indirect Resource) prominence
    # Check if Indirect Resource appears as visible stem in any pillar
    dm = chart.day_master
    ir_count = 0
    for pos in ["year", "month", "day", "hour"]:
        stem = chart.pillars[pos].stem
        if stem != dm:
            tg = get_ten_god(dm, stem)
            if tg and tg.get("abbreviation") == "IR":
                ir_count += 1
    # Also check hidden stems
    for pos in ["year", "month", "day", "hour"]:
        for hs, _ in chart.pillars[pos].hidden_stems:
            if hs != dm:
                tg = get_ten_god(dm, hs)
                if tg and tg.get("abbreviation") == "IR":
                    ir_count += 1

    if ir_count >= 2:
        w = 15
        score += w
        indicators.append({
            "name": "Indirect Resource (Pian Yin) Prominent",
            "name_zh": "偏印突出",
            "weight": w,
            "reason": f"Unconventional perception — {ir_count} Indirect Resource stems found. Channel for non-physical knowledge",
        })
    elif ir_count == 1:
        w = 8
        score += w
        indicators.append({
            "name": "Indirect Resource (Pian Yin) Present",
            "name_zh": "偏印存在",
            "weight": w,
            "reason": "Some unconventional thinking — Indirect Resource present but not dominant",
        })

    # --- SECONDARY INDICATORS ---

    # 亡神 (Lost Spirit)
    if "亡神" in present_shen_sha:
        w = 10
        score += w
        indicators.append({
            "name": "Lost Spirit (Wang Shen)",
            "name_zh": "亡神",
            "weight": w,
            "reason": "Spirit energy scattered — porous boundary with spirit realm",
        })

    # Day Master 壬 or 癸 (Water)
    if dm in ("Ren", "Gui"):
        w = 5
        score += w
        indicators.append({
            "name": f"Water Day Master ({STEMS[dm]['chinese']})",
            "name_zh": f"日主{STEMS[dm]['chinese']}水",
            "weight": w,
            "reason": "Water element is naturally intuitive, reflective, and psychically receptive",
        })

    # Multiple Yin stems (3+)
    yin_count = sum(
        1 for pos in ["year", "month", "day", "hour"]
        if STEMS[chart.pillars[pos].stem]["polarity"] == "Yin"
    )
    if yin_count >= 3:
        w = 5
        score += w
        indicators.append({
            "name": f"Multiple Yin Stems ({yin_count}/4)",
            "name_zh": f"多阴干({yin_count}/4)",
            "weight": w,
            "reason": "Yin energy is more receptive to the spiritual/invisible realm",
        })

    # --- QI PHASE TANDEM BONUS ---
    if qi_phase_spiritual_bonus > 0:
        score += qi_phase_spiritual_bonus
        indicators.append({
            "name": "Qi Phase + Shen Sha Tandem Effects",
            "name_zh": "十二长生+神煞联动效应",
            "weight": qi_phase_spiritual_bonus,
            "reason": "Qi phase combinations amplify spiritual sensitivity (see qi phase analysis)",
        })

    # --- DAMPENING INDICATORS ---

    # 正印 (Direct Resource) dominant over 偏印
    dr_count = 0
    for pos in ["year", "month", "day", "hour"]:
        stem = chart.pillars[pos].stem
        if stem != dm:
            tg = get_ten_god(dm, stem)
            if tg and tg.get("abbreviation") == "DR":
                dr_count += 1
    if dr_count > ir_count and dr_count >= 2:
        w = -10
        score += w
        indicators.append({
            "name": "Direct Resource Dominant",
            "name_zh": "正印压制偏印",
            "weight": w,
            "reason": "Orthodox thinking overrides intuition — conventional mind suppresses psychic channel",
        })

    # 正官 (Direct Officer) very prominent
    do_count = 0
    for pos in ["year", "month", "day", "hour"]:
        stem = chart.pillars[pos].stem
        if stem != dm:
            tg = get_ten_god(dm, stem)
            if tg and tg.get("abbreviation") == "DO":
                do_count += 1
    if do_count >= 2:
        w = -5
        score += w
        indicators.append({
            "name": "Direct Officer Very Prominent",
            "name_zh": "正官太旺",
            "weight": w,
            "reason": "Rigid structure and rules suppress spiritual sensitivity",
        })

    # Clamp score
    score = max(0, min(100, score))

    # Get level
    level_info = _get_level(score)

    # Generate guidance
    guidance_en, guidance_zh = _generate_guidance(score, indicators, present_shen_sha)

    return {
        "score": score,
        "level": level_info["level"],
        "label_en": level_info["label_en"],
        "label_zh": level_info["label_zh"],
        "description_en": level_info["description_en"],
        "description_zh": level_info["description_zh"],
        "indicators": indicators,
        "guidance_en": guidance_en,
        "guidance_zh": guidance_zh,
    }


def _generate_guidance(score: int, indicators: list, present_shen_sha: dict) -> tuple:
    """Generate guidance text based on score and indicators."""
    if score <= 20:
        return (
            "No special spiritual development needed. Focus on practical life goals.",
            "无需特别的灵性发展。专注于实际生活目标。",
        )
    elif score <= 40:
        return (
            "Trust your gut feelings more — they are often correct. Light meditation or mindfulness practice would sharpen this natural intuition.",
            "多相信自己的直觉——它们往往是正确的。轻度冥想或正念练习可以增强这种天生的直觉。",
        )
    elif score <= 60:
        en = "You have real spiritual sensitivity. Consider structured spiritual practice — meditation, qigong, or temple visits."
        zh = "你有真正的灵性敏感度。建议进行有结构的灵性修行——冥想、气功或寺庙参拜。"
        if "华盖" in present_shen_sha:
            en += " The Canopy Star in your chart means solitude helps you connect with the spiritual realm — don't fight the need for alone time."
            zh += " 你命中的华盖意味着独处有助于连接灵性世界——不要抗拒独处的需要。"
        return (en, zh)
    elif score <= 80:
        en = "Strong spiritual sensitivity — you likely already experience unexplainable phenomena. This ability should be DEVELOPED, not suppressed. Suppressing it causes anxiety, insomnia, and restlessness."
        zh = "灵性敏感度很强——你很可能已经经历过无法解释的现象。这种能力应该被发展，而不是压制。压制它会导致焦虑、失眠和不安。"
        if "童子" in present_shen_sha:
            en += " The Child Star suggests your soul carries memories from before this life. Classical remedy: 送替身 ritual to settle the spirit."
            zh += " 童子星暗示你的灵魂携带着前世的记忆。古典化解方法：送替身仪式来安定灵体。"
        en += " Seek a qualified spiritual teacher or mentor."
        zh += " 建议寻找合格的灵性导师。"
        return (en, zh)
    else:
        en = "Extremely high spiritual sensitivity — your 'third eye' is naturally open. You likely see, sense, or dream things others cannot. This is NOT a disorder — it is a genuine ability that needs proper management."
        zh = "极高的灵性敏感度——你的"天眼"自然开启。你很可能看到、感知到或梦到别人无法触及的事物。这不是病——这是真正的能力，需要正确管理。"
        en += " CRITICAL: Grounding practices are essential — physical exercise, Earth element remedies, structured daily routine. Without grounding, this sensitivity can become overwhelming."
        zh += " 重要：接地练习至关重要——体育锻炼、土元素化解、有规律的日常作息。没有接地，这种敏感度可能变得难以承受。"
        if "华盖" in present_shen_sha and "空亡" in present_shen_sha:
            en += " Canopy + Void combination: structured spiritual practice (Buddhism, Taoism) is better than unstructured exploration."
            zh += " 华盖+空亡组合：有结构的灵性修行（佛教、道教）比无序探索更好。"
        return (en, zh)
```

**Step 2: Verify syntax**

Run: `python3 -c "import py_compile; py_compile.compile('api/library/comprehensive/spiritual_sensitivity.py', doraise=True)"`
Expected: No output (success)

**Step 3: Commit**

```bash
git add api/library/comprehensive/spiritual_sensitivity.py
git commit -m "feat: add spiritual sensitivity assessment module (scoring + guidance)"
```

---

### Task 4: Integrate into API Response

**Files:**
- Modify: `api/bazingse.py` (~line 4907 and ~line 5023)
- Modify: `api/library/comprehensive/__init__.py` (add exports)

**Step 1: Add imports to bazingse.py**

Near the top of `bazingse.py` where other imports from `library` are, add:

```python
from library.comprehensive.qi_phase_analysis import analyze_qi_phases
from library.comprehensive.spiritual_sensitivity import assess_spiritual_sensitivity
from library.comprehensive.shen_sha import run_all_shen_sha as comp_run_all_shen_sha
from library.comprehensive.adapter import build_chart_data
```

**Step 2: Add computation after qi_phase loop**

After the existing qi_phase computation loop (~line 4907), add:

```python
# Qi Phase Contextual Analysis + Spiritual Sensitivity
qi_phase_analysis = None
spiritual_sensitivity = None
try:
    chart_data = build_chart_data(
        gender=gender,
        birth_year=birth_year,
        age=age,
        year_pillar={"stem": nodes_state["hs_y"]["id"], "branch": nodes_state["eb_y"]["id"]},
        month_pillar={"stem": nodes_state["hs_m"]["id"], "branch": nodes_state["eb_m"]["id"]},
        day_pillar={"stem": nodes_state["hs_d"]["id"], "branch": nodes_state["eb_d"]["id"]},
        hour_pillar={"stem": nodes_state["hs_h"]["id"], "branch": nodes_state["eb_h"]["id"]} if "hs_h" in nodes_state else None,
    )
    comp_shen_sha = comp_run_all_shen_sha(chart_data)
    qi_analysis = analyze_qi_phases(chart_data, comp_shen_sha)
    qi_phase_analysis = qi_analysis["pillars"]
    spiritual_sensitivity = assess_spiritual_sensitivity(
        chart_data, comp_shen_sha, qi_analysis["spiritual_bonus"]
    )
except Exception:
    pass  # Graceful degradation — these are supplementary analyses
```

NOTE: The exact integration depends on how `build_chart_data` works in `adapter.py`. The implementing agent MUST read `adapter.py` in full to understand the correct way to construct `ChartData` from the `nodes_state` dict. The agent may need to construct `Pillar` objects manually from `nodes_state` data. Do NOT blindly copy the code above — adapt it to match the actual `adapter.py` API.

**Step 3: Add to return dict**

In the final return dict (~line 5023), add two new keys:

```python
"qi_phase_analysis": qi_phase_analysis,
"spiritual_sensitivity": spiritual_sensitivity,
```

**Step 4: Verify the backend runs**

Run: `cd /Users/macbookair/GitHub/bazingse/api && python3 -c "from bazingse import *; print('OK')"`
Expected: "OK"

**Step 5: Commit**

```bash
git add api/bazingse.py api/library/comprehensive/__init__.py
git commit -m "feat: wire qi phase analysis + spiritual sensitivity into API response"
```

---

### Task 5: Frontend — Display Qi Phase on PillarCard

**Files:**
- Modify: `src/components/PillarCard.tsx` (add qi phase display)
- Modify: `src/components/BaZiChart.tsx` (pass qi phase analysis data)

**Step 1: Update PillarCard to render qi phase**

Currently `PillarCard.tsx` receives `qiPhase` but never renders it. The implementing agent MUST read the current `PillarCard.tsx` in full and add a small label showing the phase name + contextual interpretation. Add it to the **stem section** (the top section of the card), perhaps below the Ten God abbreviation.

Display:
- Phase Chinese name (e.g. "帝旺")
- Phase English name (e.g. "Emperor")
- A tooltip or expandable section showing the contextual interpretation

Use the existing TUI styling — no new design system.

**Step 2: Pass qi_phase_analysis through BaZiChart**

Update `BaZiChart.tsx`'s `buildPillar()` function to also extract the contextual interpretation from the API response's `qi_phase_analysis` object and pass it into PillarCard.

**Step 3: Verify build**

Run: `cd /Users/macbookair/GitHub/bazingse && npx tsc --noEmit`
Expected: No errors

**Step 4: Commit**

```bash
git add src/components/PillarCard.tsx src/components/BaZiChart.tsx
git commit -m "feat: display qi phase on pillar cards with contextual interpretation"
```

---

### Task 6: Frontend — Spiritual Sensitivity Display

**Files:**
- Modify: `src/components/ProfilePage.tsx` or `src/components/LifeEventBlock.tsx` (add spiritual sensitivity section)

**Step 1: Add spiritual sensitivity section to the natal chart display**

The implementing agent MUST read `LifeEventBlock.tsx` and `ProfilePage.tsx` in full to determine the best insertion point. The spiritual sensitivity block should appear in the NATAL chart section (not life events) since it's a natal trait.

Display:
- Score bar (0-100) with color coding (green → yellow → orange → red → purple)
- Level label in both Chinese and English
- Description text
- Expandable list of indicators found with their weights
- Guidance text

Use TUI styling consistent with the rest of the app.

**Step 2: Add tandem effects display**

If any qi phase tandem effects were found, show them as small badges or notes near the relevant pillar.

**Step 3: Verify build**

Run: `cd /Users/macbookair/GitHub/bazingse && npx tsc --noEmit`
Expected: No errors

**Step 4: Visual test**

Run: `cd /Users/macbookair/GitHub/bazingse && npm run dev`
Navigate to a profile page and verify both qi phase and spiritual sensitivity display correctly.

**Step 5: Commit**

```bash
git add src/components/
git commit -m "feat: display spiritual sensitivity assessment on profile page"
```

---

### Task 7: Final Integration Test + Cleanup

**Step 1: Start backend and test API response**

Run:
```bash
cd /Users/macbookair/GitHub/bazingse/api
python3 run_bazingse.py &
sleep 3
curl "http://localhost:8008/api/analyze_bazi?birth_date=1990-01-15&birth_time=14:30&gender=male" | python3 -m json.tool | grep -A5 qi_phase_analysis
curl "http://localhost:8008/api/analyze_bazi?birth_date=1990-01-15&birth_time=14:30&gender=male" | python3 -m json.tool | grep -A5 spiritual_sensitivity
```
Expected: Both keys present with populated data

**Step 2: Run Next.js build**

Run: `cd /Users/macbookair/GitHub/bazingse && npm run build`
Expected: Build succeeds

**Step 3: Final commit**

```bash
git add -A
git commit -m "feat: complete qi phase contextual analysis + spiritual sensitivity feature"
```
