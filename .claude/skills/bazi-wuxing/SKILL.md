---
name: bazi-wuxing
description: Use when calculating BaZi Four Pillars elemental balance using the point-based Wu Xing scoring method with pillar pair interactions
---

# BaZi Wu Xing Elemental Balance

Calculate Five Element balance from a BaZi chart using point-based scoring with pillar pair interactions.

## Parameters

| Param | Required | Values | Description |
|-------|----------|--------|-------------|
| Gender | Yes | M / F | Chart owner gender |
| YP | Yes | HS-EB | Year Pillar (e.g., Bing-Yin) |
| MP | Yes | HS-EB | Month Pillar |
| DP | Yes | HS-EB | Day Pillar (Day Master) |
| HP | No | HS-EB | Hour Pillar |
| 10YL | No | HS-EB | Current 10-Year Luck Pillar |
| Location | Yes | hometown / out_of_town / overseas | Residence relative to birthplace |

## Output Budget

**Total output MUST fit within ~10K tokens.** Strict enforcement:
- **ALL steps use compact table format** — NO multi-line prose logs, NO paragraph explanations
- **Steps 0–6**: One table per step. Each interaction = one table row. No prose between rows.
- **Step 7**: Palace-centric summary table ONLY — no per-interaction logs
- **Step 9**: ONLY the 5-Gods table — ZERO thinking, ZERO scenarios, ZERO scores, ZERO explanations

**FORBIDDEN in output:**
- Multi-line interaction descriptions (use table rows)
- "Meaning:" or "Type:" prose lines (derivable from Palace Reference + node names)
- Repeating calculation rules from this skill doc
- Explanations of WHY a formula works
- Showing intermediate arithmetic (just show: basis → result)

## Output Format: Compact Tables

**ALL steps output tables, NOT prose.** Each interaction = 1 table row. Downstream skills (Ten Gods, palace readings) consume these tables.

### Node Naming

`{Pillar}.{Position}` — e.g., YP.HS, MP.EB, DP.EB.h1

| Node | Meaning |
|------|---------|
| YP.HS / YP.EB / YP.EB.h1,h2 | Year Pillar (Ancestry Palace 祖上宫) |
| MP.HS / MP.EB / MP.EB.h1,h2 | Month Pillar (Career Palace 事业宫) |
| DP.HS / DP.EB / DP.EB.h1,h2 | Day Pillar (Spouse Palace 配偶宫; DP.HS = Day Master) |
| HP.HS / HP.EB / HP.EB.h1,h2 | Hour Pillar (Children Palace 子女宫) |

### Table Schemas Per Step

**Step 0 — Chart + Initial Points:** Single table with all nodes.
```
Chart: 丙寅·己亥·丁丑·丁未 | DM: 丁 Yin Fire | Age 40 → DP active | Priority: DP→MP→HP→YP

| Pillar | HS (10pt) | EB | Main Qi (8pt) | h1 (3pt) | h2 (1pt) |
|--------|-----------|----|---------------|----------|----------|
| YP | 丙 Bing Y Fire | 寅 Yin | 甲 Jia Y Wood | 丙 Bing Fire | 戊 Wu Earth |
| MP | 己 Ji N Earth | 亥 Hai | 壬 Ren Y Water 8 | 甲 Jia Wood 3 | — |
...
```

**Step 1 — Pillar Pairs:** One row per pillar. No row if same-element (no interaction).
```
| Pillar | Relation | Basis | Node A: Before→After (Δ) | Node B: Before→After (Δ) |
|--------|----------|-------|--------------------------|--------------------------|
| YP 丙寅 | EB→HS Wood→Fire | 8 | 甲 Wood: 8→6.4 (-1.6) | 丙 Fire: 10→12.4 (+2.4) |
| MP 己亥 | HS盖EB Earth克Water | 8 | 己 Earth: 10→8.4 (-1.6) | 壬 Water: 8→5.6 (-2.4) |
```

**Steps 2–3 — Positive Interactions:** One row per combo.
```
| # | Nodes | Type | →Elem | Gap×Mult | Basis | Rate | /Node | Attn% | Eff/Node | Xform |
|---|-------|------|-------|----------|-------|------|-------|-------|----------|-------|
| 1 | 丑+亥 | 半三会 | Water | 0×1.0 | 6.3 | .20 | 1.26 | 100% | 1.26 | — |
```
Append one summary line: `Bonus: +X.XX Wood, +X.XX Water` (etc.)

**Steps 4–5 — Negative Interactions:** One row per clash/harm/etc.
```
| # | Nodes | Type | Atk→Vic | Gap×Mult | Basis | Attn% | Atk Δ | Vic Δ | Note |
|---|-------|------|---------|----------|-------|-------|-------|-------|------|
| 1 | 丑↔未 | 六冲 | — | 0×1.0 | 10.4 | — | — | — | same-elem |
```
Use `Note` column for: `same-elem` (log-only), `adj-only` (六害), etc.

**Step 6 — Seasonal:** Already a table (keep as-is).

### Palace Reference (for downstream skills)

| Pillar | Palace | Represents |
|--------|--------|------------|
| YP | Ancestry 祖上宫 | Family origin, grandparents, early environment |
| MP | Career 事业宫 | Career, authority, social status, parents |
| DP | Spouse 配偶宫 | Marriage, partner, self (DP.HS = Day Master) |
| HP | Children 子女宫 | Children, subordinates, late life, legacy |

### Pillar Pair Meanings (reference, do NOT output per-row)

| Relationship | Meaning |
|-------------|---------|
| HS produces EB | Person gives/invests into that palace |
| EB produces HS | Palace supports/feeds the person |
| HS controls EB (盖头) | Person dominates that palace |
| EB controls HS (截脚) | Palace constrains the person |
| Same element | Harmony — aligned |

---

## Step 0: Initial Element Point Assignment

### Heavenly Stems — 10 pts each (pure single element)

| HS | Element | Polarity |
|----|---------|----------|
| 甲 Jia | Wood | Yang |
| 乙 Yi | Wood | Yin |
| 丙 Bing | Fire | Yang |
| 丁 Ding | Fire | Yin |
| 戊 Wu | Earth | Yang |
| 己 Ji | Earth | Yin |
| 庚 Geng | Metal | Yang |
| 辛 Xin | Metal | Yin |
| 壬 Ren | Water | Yang |
| 癸 Gui | Water | Yin |

### Earthly Branches — Hidden Stem Point Distribution

Points distributed among hidden stems based on qi count.

**Pure Qi (1 hidden stem) — 10 pts total:**

| EB | Main Qi | Pts |
|----|---------|-----|
| 子 Zi | 癸 Gui Water | 10 |
| 卯 Mao | 乙 Yi Wood | 10 |
| 酉 You | 辛 Xin Metal | 10 |

**2 Qi (2 hidden stems) — 8 + 3 = 11 pts total:**

| EB | Main Qi | Pts | Hidden 1 | Pts |
|----|---------|-----|----------|-----|
| 午 Wu | 丁 Ding Fire | 8 | 己 Ji Earth | 3 |
| 亥 Hai | 壬 Ren Water | 8 | 甲 Jia Wood | 3 |

**3 Qi (3 hidden stems) — 8 + 3 + 1 = 12 pts total:**

| EB | Main Qi | Pts | Hidden 1 | Pts | Hidden 2 | Pts |
|----|---------|-----|----------|-----|----------|-----|
| 丑 Chou | 己 Ji Earth | 8 | 癸 Gui Water | 3 | 辛 Xin Metal | 1 |
| 寅 Yin | 甲 Jia Wood | 8 | 丙 Bing Fire | 3 | 戊 Wu Earth | 1 |
| 辰 Chen | 戊 Wu Earth | 8 | 乙 Yi Wood | 3 | 癸 Gui Water | 1 |
| 巳 Si | 丙 Bing Fire | 8 | 戊 Wu Earth | 3 | 庚 Geng Metal | 1 |
| 未 Wei | 己 Ji Earth | 8 | 丁 Ding Fire | 3 | 乙 Yi Wood | 1 |
| 申 Shen | 庚 Geng Metal | 8 | 壬 Ren Water | 3 | 戊 Wu Earth | 1 |
| 戌 Xu | 戊 Wu Earth | 8 | 辛 Xin Metal | 3 | 丁 Ding Fire | 1 |

## Step 1: Pillar Pair Interaction (HS-EB Same Pillar)

Determine the Wu Xing relationship between the HS element and the EB's **main qi** element. Use the **smaller** of the two point values as the **basis**. Both production (生) and control (克) use this basis for their percentages.

### Basis Calculation

`basis = min(HS pts, EB main qi pts)`

### Production Cycle (生): Wood→Fire→Earth→Metal→Water→Wood

Producer loses 20% of basis, produced gains 30% of basis.

| Direction | Who loses 20% of basis | Who gains 30% of basis |
|-----------|------------------------|------------------------|
| EB main qi produces HS | EB main qi element | HS element |
| HS produces EB main qi | HS element | EB main qi element |

### Control Cycle (克 / 盖头截脚): Wood→Earth→Water→Fire→Metal→Wood

Controller loses 20% of basis, controlled loses 30% of basis.

| Direction | Who loses 20% of basis | Who loses 30% of basis |
|-----------|------------------------|------------------------|
| HS controls EB main qi (盖头) | HS element | EB main qi element |
| EB main qi controls HS (截脚) | EB main qi element | HS element |

### Same Element — No Interaction

When HS and EB main qi are the same element, no pillar pair interaction occurs.

### Relationship Lookup Table (MUST use — do NOT derive from memory)

Look up HS element (row) × EB main qi element (column):

| HS↓ \ EB→ | Wood | Fire | Earth | Metal | Water |
|------------|------|------|-------|-------|-------|
| **Wood** | — | HS生EB | HS克EB盖头 | EB克HS截脚 | EB生HS |
| **Fire** | EB生HS | — | **HS生EB** | HS克EB盖头 | EB克HS截脚 |
| **Earth** | EB克HS截脚 | EB生HS | — | HS生EB | HS克EB盖头 |
| **Metal** | HS克EB盖头 | EB克HS截脚 | EB生HS | — | HS生EB |
| **Water** | HS生EB | HS克EB盖头 | EB克HS截脚 | EB生HS | — |

**Common mistake:** Fire HS + Earth EB is **HS生EB** (Fire produces Earth), NOT Earth controls Fire. Earth does not control Fire — Water controls Fire.

### Example Output (compact table)

```
Step 1: Pillar Pair Interactions

| Pillar | Relation | Basis | Node A: Before→After (Δ) | Node B: Before→After (Δ) |
|--------|----------|-------|--------------------------|--------------------------|
| YP 丙寅 | EB生HS Wood→Fire | 8 | 甲 Wood: 8→6.4 (-1.6) | 丙 Fire: 10→12.4 (+2.4) |
| MP 己亥 | HS克EB盖头 Earth→Water | 8 | 己 Earth: 10→8.4 (-1.6) | 壬 Water: 8→5.6 (-2.4) |
| DP 丁丑 | HS生EB Fire→Earth | 8 | 丁 Fire: 10→8.4 (-1.6) | 己 Earth: 8→10.4 (+2.4) |
| HP 丁未 | HS生EB Fire→Earth | 8 | 丁 Fire: 10→8.4 (-1.6) | 己 Earth: 8→10.4 (+2.4) |
```

---

## Cross-Pillar Gap Penalty

**Applies to all cross-pillar interactions (Steps 2–5).**

Pillar arrangement: **YP — MP — DP — HP**

| Gap | Description | Multiplier |
|-----|-------------|------------|
| 0 | Adjacent 紧贴 (no pillar between) | 1.0 |
| 1 | One pillar between 隔柱 | 0.75 |
| 2 | Two pillars between 遥隔 | 0.5 |
| 3+ | Three or more pillars between | 0.25 |

### Pillar Gap Matrix

| Pair | Gap | Multiplier |
|------|-----|------------|
| YP–MP | 0 | 1.0 |
| MP–DP | 0 | 1.0 |
| DP–HP | 0 | 1.0 |
| YP–DP | 1 | 0.75 |
| MP–HP | 1 | 0.75 |
| YP–HP | 2 | 0.5 |

**Multi-branch combos (三会, 三合, 三刑):** Count the **number of non-participating pillar positions** in the chain between the combining branches.

`gaps = (pillar positions spanned from leftmost to rightmost) − (number of combining branches)`

**Examples:**
- 巳(HP) 午(DP) 未(YP): spans YP–[MP]–DP–HP → 4 positions − 3 branches = **1 gap** → ×0.75
- 亥(MP) 卯(DP) 未(HP): spans MP–DP–HP → 3 positions − 3 branches = **0 gap** → ×1.0
- 寅(YP) 午(DP) 戌(HP): spans YP–[MP]–DP–HP → 4 positions − 3 branches = **1 gap** → ×0.75

**Special rule:** 六害 (Harm) requires 0 gap (adjacent only) — does not apply at gap 1+.

Formula adjustment: `effective pts = base pts × gap multiplier`

---

## Three-Branch Priority

When all 3 branches of a trio interaction are present in the chart, the trio takes priority. **Any 2-branch interaction where BOTH branches belong to the same active trio is nullified** — the trio has its own meaning and calculation.

**Pre-scan:** Before calculating points in Steps 2 and 4, identify all valid 3-branch interactions first. Then skip any 2-branch interaction where both branches are part of an active trio.

**Positive trios absorb positive pairs:**

| Active Trio | Nullified 2-Branch Pairs |
|------------|--------------------------|
| 三会 (e.g., 巳午未) | All 半三会 of same season (巳午, 午未, 巳未) + any 六合 between trio branches (午未 六合) |
| 三会 (e.g., 亥子丑) | All 半三会 (亥子, 子丑, 亥丑) + 子丑 六合 |
| 三合 (e.g., 亥卯未) | Corresponding 拱合 (亥未) |

**Negative trios absorb negative pairs:**

| Active Trio | Nullified 2-Branch Pairs |
|------------|--------------------------|
| 三刑 寅巳申 (all 3 present) | 寅申 六冲, 寅巳 六害, 巳申 破 |
| 三刑 丑未戌 (all 3 present) | 丑未 六冲, 未戌 破 |

**Partial trios (2 of 3 branches):** No nullification. The partial interaction AND any overlapping pair interactions all count normally.

---

## Attention Spread 分心效应 (Fēn Xīn Xiào Yìng)

Each EB node has limited "attention." The more cross-pillar interactions a node participates in, the less effective each interaction becomes — **both positive AND negative**. Interactions compete for a node's focus **proportionally to their significance**, not equally.

### Attention Weight Table

Weights reflect **completeness and significance** of each interaction type, organized in tiers:

| Tier | Interaction | Weight | Rationale |
|------|-----------|--------|-----------|
| 4 | 三会 Sān Huì (Seasonal Direction) | **63** | Full seasonal alignment — strongest combo |
| 3 | 三合 Sān Hé (Three Combo) | **42** | Complete triangular formation |
| 3 | 六冲 Liù Chōng (Six Clash) | **42** | Direct opposition — strongest negative |
| 3 | 三刑全 Sān Xíng Quán (Punishment, full trio) | **42** | Full corrective triangle |
| 2 | 六合 Liù Hé (Six Combo) | **28** | Direct pair harmony |
| 2 | 破 Pò (Destruction) | **28** | Direct pair disruption |
| 2 | 六害 Liù Hài (Six Harm) | **28** | Direct pair harm |
| 1 | 半三会 Bàn Sān Huì (Half Seasonal) | **12** | Incomplete seasonal |
| 0 | 拱合 Gǒng Hé (Arched Combo) | **7** | Incomplete triangle |

**Key relationships:** Complete combos outweigh negatives of same tier. 三会 (63) dominates even 六冲 (42). Incomplete combos (半三会, 拱合) are heavily discounted.

### Verification Matrix (positive vs negative matchups)

| Positive | Negative | Share | Result |
|----------|----------|-------|--------|
| 三会 (63) | 六冲 (42) | 63/105 | **60 / 40** |
| 三会 (63) | 破 (28) | 63/91 | **69 / 31 ≈ 70 / 30** |
| 三合 (42) | 六冲 (42) | 42/84 | **50 / 50** |
| 三合 (42) | 破 (28) | 42/70 | **60 / 40** |
| 六合 (28) | 六冲 (42) | 28/70 | **40 / 60** |
| 六合 (28) | 破 (28) | 28/56 | **50 / 50** |
| 半三会 (12) | 破 (28) | 12/40 | **30 / 70** |
| 拱合 (7) | 破 (28) | 7/35 | **20 / 80** |

### Process

1. **Pre-scan:** After applying Three-Branch Priority, identify all valid cross-pillar EB interactions (positive + negative)
2. **Weight per node:** For each EB node, sum the attention weights of all interactions it participates in → Σ_weights
3. **Apply share:** Each interaction's effect **on that specific node** = base calculated effect × (interaction_weight / Σ_weights)

`attention_share(interaction X, node A) = weight(X) / Σ(weights of all interactions involving A)`

With a single interaction: share = 1.0 (full effect). Reduces to simple ÷N when all weights are equal.

### What Counts as an Interaction

Each of these counts per participating node, using its assigned weight:

| Category | Interaction | Weight |
|----------|-----------|--------|
| Positive | 三会 | 63 |
| Positive | 三合 | 42 |
| Positive | 六合 | 28 |
| Positive | 半三会 | 12 |
| Positive | 拱合 | 7 |
| Negative | 六冲 | 42 |
| Negative | 三刑全 (each pair within full trio) | 42 per pair |
| Negative | 六害 | 28 |
| Negative | 破 | 28 |
| Log-only | Same-element 六冲, 破 | Same weight as type (42, 28) |

**Does NOT count:** Step 1 pillar pair interactions (HS-EB within same pillar) — inherent to the pillar, not cross-pillar "attention."

### Key: Log-Only Interactions Still Occupy Attention

Same-element interactions (e.g., 未戌 破 Earth↔Earth) have no point calculation, but they **still use their type's attention weight**. They occupy the node's attention and dilute other interactions — their palace/象 significance diverts focus.

### Example: 亥(YP) 未(MP) 戌(DP) 申(HP)

Interactions detected:
- 亥未 拱合 (positive, weight 7) — involves 亥, 未
- 申戌 半三会 (positive, weight 12) — involves 申, 戌
- 未戌 破 same-element (log-only, weight 28) — involves 未, 戌

Weighted attention per node:

| Node | Interactions (weight) | Σ | Shares |
|------|----------------------|---|--------|
| 亥 Hai | 拱合 (7) | 7 | 拱合 = 7/7 = **100%** |
| 未 Wei | 拱合 (7) + 破 (28) | 35 | 拱合 = 7/35 = **20%**, 破 = 28/35 = **80%** |
| 戌 Xu | 半三会 (12) + 破 (28) | 40 | 半三会 = 12/40 = **30%**, 破 = 28/40 = **70%** |
| 申 Shen | 半三会 (12) | 12 | 半三会 = 12/12 = **100%** |

Effects (assuming transformed combo pts = 2.4 for 拱合, 3.2 for 半三会):
- 拱合 bonus on 亥: 2.4 × 100% = 2.4 (undivided — only interaction)
- 拱合 bonus on 未: 2.4 × 20% = 0.48 (heavily drawn to 破 with 戌)
- 半三会 bonus on 戌: 3.2 × 30% = 0.96 (mostly occupied by 破 with 未)
- 半三会 bonus on 申: 3.2 × 100% = 3.2 (undivided)
- 破 on 未: log-only, no pts (but consumes 80% of 未's attention)
- 破 on 戌: log-only, no pts (but consumes 70% of 戌's attention)

### Asymmetric Per-Node

Each side of an interaction may have a **different share**. In the example above, 未戌 破:
- 破 consumes 80% of 未's attention (未's alternative is weak 拱合, weight 7)
- 破 consumes 70% of 戌's attention (戌's alternative is stronger 半三会, weight 12)

---

## Step 2: EB Positive Interactions (Combinations 合/会)

Scan all EBs in the chart for combination groups. When found, **each participating EB node** receives bonus points of the produced element.

### Basis & Formula

`basis = min(main qi pts of all combining EBs)`
`combo pts per node = basis × rate × gap multiplier`
`total combo pts = combo pts per node × number of nodes`
`transform: combo pts per node × 2.5 (per node)` (if transformation condition met)

**Transformation condition (cross-check):** A visible **HS** anywhere in the chart has the **same element** as the combination's produced element. (EB combos check HS.)

### Polarity Rule

Each EB node produces the element in **its own polarity**. Yang EB → Yang stem version, Yin EB → Yin stem version. This determines the Ten God identity of the bonus — critical for downstream analysis.

**EB Polarity reference:**
- Yang: 子 Zi, 寅 Yin, 辰 Chen, 午 Wu, 申 Shen, 戌 Xu
- Yin: 丑 Chou, 卯 Mao, 巳 Si, 未 Wei, 酉 You, 亥 Hai

### Combination Types (strongest → weakest)

#### 1. Seasonal Direction 三会 (Sān Huì) — rate 0.30

Three consecutive seasonal branches. **Strongest combination.**

| Branches | Produced Element |
|----------|-----------------|
| 寅卯辰 Yin-Mao-Chen | Wood |
| 巳午未 Si-Wu-Wei | Fire |
| 申酉戌 Shen-You-Xu | Metal |
| 亥子丑 Hai-Zi-Chou | Water |

#### 2. Three Combination 三合 (Sān Hé) — rate 0.25

Growth (长生) + Peak (帝旺) + Tomb (墓) branches.

| Branches | Produced Element |
|----------|-----------------|
| 亥卯未 Hai-Mao-Wei | Wood |
| 寅午戌 Yin-Wu-Xu | Fire |
| 巳酉丑 Si-You-Chou | Metal |
| 申子辰 Shen-Zi-Chen | Water |

#### 3. Six Combination 六合 (Liù Hé) — rate 0.20

Branch pairs that harmonize.

| Branches | Produced Element |
|----------|-----------------|
| 子丑 Zi-Chou | Earth |
| 寅亥 Yin-Hai | Wood |
| 卯戌 Mao-Xu | Fire |
| 辰酉 Chen-You | Metal |
| 巳申 Si-Shen | Water |
| 午未 Wu-Wei | Fire |

#### 4. Half Seasonal 半三会 (Bàn Sān Huì) — rate 0.20

Any two of three seasonal direction branches present.

| Branches | Produced Element |
|----------|-----------------|
| 寅卯 or 卯辰 or 寅辰 | Wood |
| 巳午 or 午未 or 巳未 | Fire |
| 申酉 or 酉戌 or 申戌 | Metal |
| 亥子 or 子丑 or 亥丑 | Water |

#### 5. Arched Combination 拱合 (Gǒng Hé) — rate 0.15

Growth + Tomb branches of a 三合 group (Peak branch missing — "arched over").

| Branches | Missing Peak | Produced Element |
|----------|-------------|-----------------|
| 亥未 Hai-Wei | 卯 Mao | Wood |
| 寅戌 Yin-Xu | 午 Wu | Fire |
| 巳丑 Si-Chou | 酉 You | Metal |
| 申辰 Shen-Chen | 子 Zi | Water |

### Processing Rules

**EBs are NOT consumed.** An EB can participate in multiple combinations.

**Continuous basis:** Use the current (post-previous-interaction) main qi values. Each combination uses the latest point state.

**Age-based pillar priority:** Each pillar spans 16 years. Processing order follows these rules:

1. **Active pillar first** (determined by age)
2. **DP is always 2nd** (Day Master priority) — unless DP is already 1st
3. **Remaining pillars by proximity** — closest age boundary to current age goes next

| Age | Active Pillar |
|-----|--------------|
| 0–16 | YP |
| 17–32 | MP |
| 33–48 | DP |
| 49–64 | HP |

**Proximity rule:** After slots 1–2, compare current age to the nearest boundary of each remaining pillar's range. Closer range → higher priority.

**Examples:**

| Age | Slot 1 (Active) | Slot 2 (DP) | Slot 3 (Closer) | Slot 4 (Furthest) |
|-----|-----------------|-------------|-----------------|-------------------|
| 15 | YP | DP | MP (17 is 2 away) | HP (49 is 34 away) |
| 25 | MP | DP | YP (16 is 9 away) | HP (49 is 24 away) |
| 39 | DP (=DM) | MP (32 is 7 away) | HP (49 is 10 away) | YP (16 is 23 away) |
| 55 | HP | DP | MP (32 is 23 away) | YP (16 is 39 away) |

For each pillar in order: find all valid combinations involving that pillar's EB (not yet processed), strongest → weakest (三会 → 三合 → 六合 → 半三会 → 拱合).

**Attention Spread applied:** Each node's combo bonus = base bonus ÷ N (where N = that node's total interaction count from pre-scan). See Attention Spread section.

### Example Output (compact table)

Chart: 丙寅·己亥·丁丑·丁未 (age 39 → DP→MP→HP→YP)

```
Step 2: EB Positive Interactions
Attn pre-scan: 丑(半三会12+六冲42=54), 亥(半三会12+六合28+拱合7=47), 寅(六合28), 未(拱合7+六冲42=49)

| # | Anchor | Nodes | Type | →Elem | Gap×Mult | Basis | Rate | /Node | Attn% | Eff/Node | Xform |
|---|--------|-------|------|-------|----------|-------|------|-------|-------|----------|-------|
| 1 | DP | 丑+亥 | 半三会 | Water | 0×1.0 | 6.3 | .20 | 1.26 | 丑22%,亥26% | 0.28,0.33 | — |
| 2 | MP | 寅+亥 | 六合 | Wood | 0×1.0 | 6.4 | .20 | 1.28 | 寅100%,亥60% | 1.28,0.77 | — |
| 3 | MP | 亥+未 | 拱合 | Wood | 1×0.75 | 7.56 | .15 | 0.85 | 亥15%,未14% | 0.13,0.12 | — |
Bonus: +2.30 Wood, +0.61 Water | No transforms (no Wood/Water HS)
```

---

## Step 3: HS Positive Interactions (天干五合 Stem Combinations)

Scan all visible HS pairs across different pillars for the five stem combinations. Same basis method as previous steps.

### The Five HS Combinations

| Pair | Produced Element |
|------|-----------------|
| 甲己 Jia + Ji | Earth |
| 乙庚 Yi + Geng | Metal |
| 丙辛 Bing + Xin | Water |
| 丁壬 Ding + Ren | Wood |
| 戊癸 Wu + Gui | Fire |

### Formula

`basis = min(HS₁ pts, HS₂ pts)` (use current continuous values)
`combo pts per node = basis × 0.30 × gap multiplier`
`transform pts = combo pts per node × 2.5` (if transformation condition met)

**Transformation condition (cross-check):** An **EB's main qi** anywhere in the chart has the **same element** as the combination's produced element. (HS combos check EB.)

### Processing Order

Same age-based pillar priority as Step 2. Anchor on each pillar's HS in order, find valid combos with other pillars' HSs not yet processed.

**Output format:** Same compact table as Step 2 (one row per combo, summary line at end).

---

## Step 4: EB Negative Interactions (冲刑害破)

Scan all EBs for negative interactions. Same basis method: `basis = min(main qi pts of interacting EBs)`.

### Direction Rule

For any two different elements in a negative interaction, determine attacker/victim by Wu Xing relationship:
- **Control** (A controls B): A is attacker, B is victim
- **Production** (A produces B): B is attacker (drainer), A is victim (drained)

**Same-element interactions:** No elemental point calculation. **Log the interaction only** — record which palaces are interacting and which Ten Gods are involved. Significant for palace/象 analysis but does not alter element balance.

### Formula

`basis = min(main qi pts of interacting EBs)`

**Different-element interactions — asymmetric damage:**

| Type | Attacker loses | Victim loses |
|------|---------------|-------------|
| 六冲 Clash | basis × 0.25 × gap | basis × 0.50 × gap |
| 三刑 Punishment | basis × 0.20 × gap | basis × 0.40 × gap |
| 六害 Harm | basis × 0.20 × gap | basis × 0.40 × gap |
| 破 Destruction | basis × 0.20 × gap | basis × 0.40 × gap |

### Negative Interaction Types (strongest → weakest)

#### 1. Six Clashes 六冲 (Liù Chōng)

Direct opposition. Most forceful EB negative interaction — always activates. 《滴天髓》: "支神只以冲为重" (Among branch interactions, only clash truly matters).

**Control clashes** — asymmetric (attacker -25% basis, victim -50% basis):

| Clash Pair | Attacker | Victim | Wu Xing basis |
|-----------|----------|--------|---------------|
| 子午 Zi-Wu | 子 Water | 午 Fire | Water controls Fire |
| 寅申 Yin-Shen | 申 Metal | 寅 Wood | Metal controls Wood |
| 卯酉 Mao-You | 酉 Metal | 卯 Wood | Metal controls Wood |
| 巳亥 Si-Hai | 亥 Water | 巳 Fire | Water controls Fire |

**Same-element clashes** — log only, no point calculation:

| Clash Pair | Element | Note |
|-----------|---------|------|
| 丑未 Chou-Wei | Earth ↔ Earth | Log palace clash meaning only |
| 辰戌 Chen-Xu | Earth ↔ Earth | Log palace clash meaning only |

#### 2. Three Punishments 三刑 (Sān Xíng)

Corrective tension — legal, health, or disaster implications.

| Group | Branches | Name |
|-------|----------|------|
| Bullying 恃势之刑 | 寅巳申 Yin-Si-Shen | Three-way mutual punishment |
| Ungrateful 无恩之刑 | 丑未戌 Chou-Wei-Xu | Three-way mutual punishment |
| Rude 无礼之刑 | 子卯 Zi-Mao | Mutual punishment (pair) |
| Self 自刑 | 辰辰 / 午午 / 酉酉 / 亥亥 | Same-branch punishment |

**Three-way punishment rules:**
- **恃势之刑 寅巳申 (Bullying):** All three present → each pair calculated separately (different-element pairs). Two of three → still triggers between the pair.
- **无恩之刑 丑未戌 (Ungrateful):** Requires **all three branches** present. Two of three does NOT trigger — there is no partial 丑未戌 三刑. (All Earth main qi — individual pairs interact only via 六冲 or 破, not 三刑.)

**Different-element pairs — asymmetric (attacker -20% basis, victim -40% basis):**

| Pair | Attacker | Victim | Wu Xing basis |
|------|----------|--------|---------------|
| 寅 ↔ 巳 | 巳 Fire | 寅 Wood | Wood produces Fire (drain) |
| 巳 ↔ 申 | 巳 Fire | 申 Metal | Fire controls Metal |
| 申 ↔ 寅 | 申 Metal | 寅 Wood | Metal controls Wood |
| 子 ↔ 卯 | 卯 Wood | 子 Water | Water produces Wood (drain) |

**Same-element groups — log only, no point calculation:**
- 无恩之刑 丑未戌 (all Earth main qi)
- 自刑 same-branch pairs (same element)

#### 3. Six Harms 六害 (Liù Hài)

Hidden, insidious damage. **Adjacent pillars only (0 gap).** Does not apply at gap 1+.

All 六害 pairs are different-element — all use asymmetric damage (attacker -20% basis, victim -40% basis).

| Harm Pair | Attacker | Victim | Wu Xing basis |
|----------|----------|--------|---------------|
| 子未 Zi-Wei | 未 Earth | 子 Water | Earth controls Water |
| 丑午 Chou-Wu | 丑 Earth | 午 Fire | Fire produces Earth (drain) |
| 寅巳 Yin-Si | 巳 Fire | 寅 Wood | Wood produces Fire (drain) |
| 卯辰 Mao-Chen | 卯 Wood | 辰 Earth | Wood controls Earth |
| 申亥 Shen-Hai | 亥 Water | 申 Metal | Metal produces Water (drain) |
| 酉戌 You-Xu | 酉 Metal | 戌 Earth | Earth produces Metal (drain) |

#### 4. Destructions 破 (Pò)

Weakest negative interaction — disrupts continuity.

**Different-element pairs — asymmetric (attacker -20% basis, victim -40% basis):**

| Destruction Pair | Attacker | Victim | Wu Xing basis |
|-----------------|----------|--------|---------------|
| 子酉 Zi-You | 子 Water | 酉 Metal | Metal produces Water (drain) |
| 寅亥 Yin-Hai | 寅 Wood | 亥 Water | Water produces Wood (drain) |
| 卯午 Mao-Wu | 午 Fire | 卯 Wood | Wood produces Fire (drain) |
| 巳申 Si-Shen | 巳 Fire | 申 Metal | Fire controls Metal |

**Same-element pairs — log only, no point calculation:**

| Destruction Pair | Element | Note |
|-----------------|---------|------|
| 丑辰 Chou-Chen | Earth ↔ Earth | Log palace interaction only |
| 未戌 Wei-Xu | Earth ↔ Earth | Log palace interaction only |

### Processing Rules

- **Pre-scan first** — identify all valid interactions (positive + negative), apply Three-Branch Priority, count Attention Spread N per node
- **Attention Spread applied** — each node's damage = base damage ÷ N (see Attention Spread section)
- **EBs NOT consumed** — can participate in multiple negative interactions
- **Continuous basis** — use latest point state
- **Age-based pillar priority** — same order as Steps 2–3
- **Gap penalty applied** — 六害 requires 0 gap (adjacent) only
- **Combo protection applied** — reduce damage on nodes with strong combos

For each pillar in order: find all valid negative interactions involving that pillar's EB (excluding nullified pairs), strongest → weakest (六冲 → 三刑 → 六害 → 破).

**Output format:** Use compact table from Table Schemas (Steps 4–5 schema). One row per interaction. `Note` column for same-elem/log-only.

---

## Step 5: HS Negative Interactions (天干四冲 Stem Clashes)

Scan all visible HS pairs across different pillars for stem clashes. HS clashes are **same-polarity control** (阳克阳 / 阴克阴) — more forceful than 天干五合 (opposite-polarity attraction).

### The Four HS Clashes

| Clash Pair | Relationship | Polarity |
|-----------|-------------|----------|
| 甲庚 Jia-Geng | Metal controls Wood | Yang vs Yang |
| 乙辛 Yi-Xin | Metal controls Wood | Yin vs Yin |
| 丙壬 Bing-Ren | Water controls Fire | Yang vs Yang |
| 丁癸 Ding-Gui | Water controls Fire | Yin vs Yin |

**戊己 (Earth) has no clash partner** — Earth sits in the center.

### Formula

Same-polarity control — **more forceful than natural control (Step 1)**. Amplified rates with gap penalty:

`basis = min(HS₁ pts, HS₂ pts)`
`controller (attacker) loses: basis × 0.25 × gap multiplier`
`controlled (victim) loses: basis × 0.50 × gap multiplier`

### Processing Order

Same age-based pillar priority. Anchor on each pillar's HS in order, find valid clashes with other pillars' HSs.

**Output format:** Same compact table as Step 4 (Steps 4–5 schema). One row per clash.

---

## Step 6: Seasonal Adjustment 令调 (Lìng Diào)

Apply a percentage multiplier to **each node's qi** (HS, EB main qi, and hidden stems) based on the **season** determined by the 月柱地支 (Yuè Zhù Dì Zhī, Month Pillar Earthly Branch). This reflects the 五行旺相休囚死 (Wǔ Xíng Wàng Xiāng Xiū Qiú Sǐ) seasonal strength cycle. Each node is adjusted individually by its element's seasonal state.

### Season by Month Branch

| 月支 (Yuè Zhī, Month Branch) | 季 (Jì, Season) | 令 (Lìng, Seasonal Element) |
|---|---|---|
| 寅 Yín (month 1) | 春 Chūn (Spring) | 木 Mù (Wood) |
| 卯 Mǎo (month 2) | 春 Chūn (Spring) | 木 Mù (Wood) |
| 辰 Chén (month 3) | 土旺 Tǔ Wàng (Earth transition) | 土 Tǔ (Earth) |
| 巳 Sì (month 4) | 夏 Xià (Summer) | 火 Huǒ (Fire) |
| 午 Wǔ (month 5) | 夏 Xià (Summer) | 火 Huǒ (Fire) |
| 未 Wèi (month 6) | 土旺 Tǔ Wàng (Earth transition) | 土 Tǔ (Earth) |
| 申 Shēn (month 7) | 秋 Qiū (Autumn) | 金 Jīn (Metal) |
| 酉 Yǒu (month 8) | 秋 Qiū (Autumn) | 金 Jīn (Metal) |
| 戌 Xū (month 9) | 土旺 Tǔ Wàng (Earth transition) | 土 Tǔ (Earth) |
| 亥 Hài (month 10) | 冬 Dōng (Winter) | 水 Shuǐ (Water) |
| 子 Zǐ (month 11) | 冬 Dōng (Winter) | 水 Shuǐ (Water) |
| 丑 Chǒu (month 12) | 土旺 Tǔ Wàng (Earth transition) | 土 Tǔ (Earth) |

### Five States 五行旺相休囚死

For each element, its relationship to the seasonal element determines the multiplier:

| State | 汉字 | Pinyin | Relationship to Seasonal Element | Multiplier |
|---|---|---|---|---|
| Prosperous | 旺 | Wàng | **Same** as seasonal element | **+25%** |
| Prime | 相 | Xiāng | **Produced by** seasonal element | **+15%** |
| Rest | 休 | Xiū | **Produces** the seasonal element | **0%** |
| Imprisoned | 囚 | Qiú | **Controls** the seasonal element | **-15%** |
| Dead | 死 | Sǐ | **Controlled by** seasonal element | **-25%** |

### Full Seasonal Matrix

Production cycle: 木→火→土→金→水→木
Control cycle: 木→土→水→火→金→木

| 令 Lìng (Season) | 旺 Wàng +25% | 相 Xiāng +15% | 休 Xiū 0% | 囚 Qiú -15% | 死 Sǐ -25% |
|---|---|---|---|---|---|
| 木 Mù (Wood/Spring) | 木 Wood | 火 Fire | 水 Water | 金 Metal | 土 Earth |
| 火 Huǒ (Fire/Summer) | 火 Fire | 土 Earth | 木 Wood | 水 Water | 金 Metal |
| 土 Tǔ (Earth/Transition) | 土 Earth | 金 Metal | 火 Fire | 木 Wood | 水 Water |
| 金 Jīn (Metal/Autumn) | 金 Metal | 水 Water | 土 Earth | 火 Fire | 木 Wood |
| 水 Shuǐ (Water/Winter) | 水 Water | 木 Wood | 金 Metal | 土 Earth | 火 Fire |

### Formula

Applied **per-node** — each individual qi node (HS, EB main qi, and hidden stems) is adjusted by its element's seasonal multiplier:

`adjusted_node_pts = current_node_pts × (1 + multiplier)`

Process every node in every pillar. Each node's element determines which multiplier applies.

### Output Format

**MUST cross-check:** After determining the season, look up the row for that season in the Full Seasonal Matrix above. Copy the 5 elements in order (旺→相→休→囚→死) directly from that row. Do NOT assign multipliers from memory.

Single header line + compact table. Use stem character only (no Pinyin in table body):

```
Season: 亥 → 冬 Water | Water×1.25(旺) Wood×1.15(相) Metal×1.00(休) Earth×0.85(囚) Fire×0.75(死)

| Node | Stem | Elem | Pre | State | ×Mult | Post |
|------|------|------|-----|-------|-------|------|
| YP.HS | 丙 | Fire | 12.4 | 死 | ×0.75 | 9.30 |
| YP.EB | 甲 | Wood | 6.4 | 相 | ×1.15 | 7.36 |
| YP.EB.h1 | 丙 | Fire | 3.0 | 死 | ×0.75 | 2.25 |
| YP.EB.h2 | 戊 | Earth | 1.0 | 囚 | ×0.85 | 0.85 |
...
(all nodes, then sum by element)
```

**Verification:** Each node's State column must match the header. If Fire=死(×0.75) in the header, EVERY Fire node must show 死 ×0.75.

---

## Step 7: Natural Element Flow 自然五行流转 (Zì Rán Wǔ Xíng Liú Zhuǎn)

Cross-pillar Wu Xing production/control between all **visible** primary qi and bonus qi (from combos/transforms). **Half rates of Step 1** — cross-pillar influence is weaker than within-pillar inherent relationship. Applied sequentially with continuous basis updates and gap penalties.

### Scope

**Included nodes:**
- Each pillar's HS (Heavenly Stem) — primary qi
- Each pillar's EB main qi — primary qi
- Bonus qi from Step 2/3 combos and transformations

**Excluded:**
- Same-pillar original HS↔EB main qi only (already handled in Step 1)
- Hidden stems (h1, h2) — hidden from cross-pillar flow

**Included same-pillar bonus interactions:**
- Native↔bonus at same grid position (e.g., YP.HS Wood ↔ YP.HS+ Metal)
- Cross-row within same pillar involving bonus nodes (e.g., YP.HS+ Metal ↔ YP.EB Water)

### Same-Element Bonus Consolidation

When bonus qi has the **same element** as the native node at the same position, combine into one node for interaction purposes. Example: HP.EB 庚 Metal (6.4) + HP.EB bonus 庚 Metal (3.2) → HP.EB Metal (9.6).

### Gap Grid

The chart forms a 2×4 grid. **Gap = Manhattan distance − 1.**

```
YP.HS ——— MP.HS ——— DP.HS ——— HP.HS      (row 0)
  |          |          |          |
YP.EB ——— MP.EB ——— DP.EB ——— HP.EB      (row 1)
```

| Pair Type | Same-row adj | Same-row +1 | Same-row +2 | Cross-row adj | Cross-row +1 | Cross-row +2 |
|---|---|---|---|---|---|---|
| Manhattan | 1 | 2 | 3 | 2 | 3 | 4 |
| **Gap** | **0** | **1** | **2** | **1** | **2** | **3** |
| Multiplier | ×1.0 | ×0.75 | ×0.5 | ×0.75 | ×0.5 | ×0.25 |

### Interaction Rates

**Half of Step 1 rates** — cross-pillar natural flow is weaker than within-pillar inherent relationship (Step 1). This prevents the cascading snowball effect where dominant elements drain weaker ones to near-zero.

**Production (生):** `basis = min(node₁ pts, node₂ pts)`
- Producer: −basis × 0.10 × gap multiplier
- Produced: +basis × 0.15 × gap multiplier

**Control (克):** `basis = min(node₁ pts, node₂ pts)`
- Controller: −basis × 0.10 × gap multiplier
- Controlled: −basis × 0.15 × gap multiplier

**Rationale:** Step 1 (20%/30%) models the intimate HS-EB bond within a pillar. Step 7 (10%/15%) models the ambient flow between positions — still meaningful but inherently weaker. Full Step 1 rates across 48 interactions caused Earth (with 2 branches + seasonal 旺) to collapse to 8%, which contradicts traditional assessment where such Earth presence should remain moderate (~12%).

### Processing Order

**Age-based pillar priority** (same as Steps 2–5):

1. Active pillar (by age)
2. DP (Day Master) — unless already 1st
3. Closer remaining pillar (by age boundary distance)
4. Furthest remaining pillar
5. 10YL pillar always last (if present)

**Anchoring:** For each pillar in priority order, process all unprocessed interactions where **at least one** node belongs to that pillar. An interaction is anchored to whichever participating pillar comes **first** in the priority order.

**Within each anchor, sort by:**
1. Gap ascending (closest first)
2. Production before control (at same gap)

**Each node pair interacts exactly once.** Once processed, mark as done.

**Continuous basis:** Each interaction updates point values. Subsequent interactions use updated values.

### Output Format (Compact)

Calculate all Step 7 interactions internally using the rules above. **Do NOT output per-interaction logs.** Output only the palace-centric summary:

```
Step 7 Palace Summary (N interactions processed):

| Node | Pre-S7 | Post-S7 | Δ | Fed by 生 | Feeds 生 | Hit by 克 | Hits 克 |
|------|--------|---------|---|----------|---------|----------|---------|
| YP.HS 乙 Wood | 7.23 | 6.41 | -0.82 | 2(+1.44) | 1(-0.61) | 1(-1.12) | 0 |
| YP.EB 壬 Water | 4.73 | 4.04 | -0.69 | 1(+0.53) | 1(-0.34) | 1(-0.67) | 1(-0.21) |
| MP.HS ... | ... | ... | ... | ... | ... | ... | ... |
(one row per primary/bonus node)
```

Columns show: count of interacting nodes (sum Δ from that category). This preserves all information downstream skills need while cutting ~30 individual log entries to ~10-12 table rows.

---

## Step 8: Elemental Report 五行报告 (Wǔ Xíng Bào Gào)

Final element balance after all interaction steps.

### Node Sources

| Source | Values from | Notes |
|---|---|---|
| Primary qi (HS, EB main) | Post-Step 7 | Updated through natural flow |
| Bonus qi (combos/transforms) | Post-Step 7 | Updated through natural flow |
| Hidden stems (h1, h2) | Post-Step 6 | Unchanged — excluded from Step 7 |

### Report Format

**1. Node breakdown by pillar:**

```
YP: 乙 Yi Wood 8.53 | 壬 Ren Water 5.01 | [+Metal 6.70 combo] | h1:甲 Wood 2.70 | [+Wood 1.57 拱合]
MP: 癸 Gui Water 6.59 | 己 Ji Earth 4.39 | h1:丁 Fire 3.00 | h2:乙 Wood 0.90 | [+Wood 0.28 拱合]
DP: 庚 Geng Metal 17.74 | 戊 Wu Earth 4.71 | h1:辛 Metal 3.30 | h2:丁 Fire 1.00 | [+Metal 0.93 半三会]
HP: 甲 Jia Wood 2.61 | 庚 Geng Metal 11.38 | h1:壬 Water 2.40 | h2:戊 Earth 1.20
```

**2. Element totals and ranking:**

| Element | Total | % | Rank | Bar |
|---|---|---|---|---|
| Metal | XX.XX | XX.X% | 1 | ████... |
| Wood | XX.XX | XX.X% | 2 | ███... |
| Water | XX.XX | XX.X% | 3 | ██... |
| Earth | XX.XX | XX.X% | 4 | █... |
| Fire | XX.XX | XX.X% | 5 | █... |

**3. Day Master strength assessment:**

| DM % Range | Strength | 汉字 |
|---|---|---|
| >40% | Dominant | 极强 Jí Qiáng |
| 25–40% | Strong | 偏强 Piān Qiáng |
| 15–25% | Balanced | 中和 Zhōng Hé |
| 8–15% | Weak | 偏弱 Piān Ruò |
| <8% | Very Weak | 极弱 Jí Ruò |

DM % = (Day Master's element total) / (grand total) × 100

### Step 8b: DM Support-Pressure Lens 日主助力分析 (Rì Zhǔ Zhù Lì Fēn Xī)

Categorize all element points from Step 8a through the Day Master's perspective. Each element in the chart has one of 5 relationships to the DM — this step reveals the **life narrative** behind the numbers.

**Source data:** Step 8a element totals (post-Step 7). No new calculations — purely re-categorization.

#### The 5 DM Relationships (Ten God Groups)

Production cycle: Wood→Fire→Earth→Metal→Water→Wood
Control cycle: Wood→Earth→Water→Fire→Metal→Wood

| Relationship | 十神 Group | Wu Xing (if DM=Fire) | Category |
|-------------|-----------|---------------------|----------|
| Same element 同我 | 比劫 Bǐ Jié (Companion) | Fire=Fire | Support |
| Produces me 生我 | 印星 Yìn Xīng (Resource) | Wood→Fire | Support |
| I produce 我生 | 食伤 Shí Shāng (Output) | Fire→Earth | Drain |
| I control 我克 | 财星 Cái Xīng (Wealth) | Fire→Metal | Drain |
| Controls me 克我 | 官杀 Guān Shā (Power) | Water→Fire | Drain |

**Generic lookup (by DM element):**

| DM Element | 同我 Companion | 生我 Resource | 我生 Output | 我克 Wealth | 克我 Power |
|-----------|---------------|-------------|------------|------------|-----------|
| Wood | Wood | Water | Fire | Earth | Metal |
| Fire | Fire | Wood | Earth | Metal | Water |
| Earth | Earth | Fire | Metal | Water | Wood |
| Metal | Metal | Earth | Water | Wood | Fire |
| Water | Water | Metal | Wood | Fire | Earth |

**DM's own node (DP.HS) is excluded** — it IS the Day Master, not a supporter or drainer.

#### Each Relationship Has Dual Nature

**The narrative depends on DM strength × that category's proportion.** Same percentage reads completely differently for a strong vs weak DM.

| 十神 | Positive Face (适度) | Shadow Face (过度/不足) |
|------|---------------------|----------------------|
| 比劫 Companion | Allies, brotherhood, shared strength, peer support | Competition, rivalry, resource-splitting, too many mouths |
| 印星 Resource | Nurture, protection, knowledge, mentors, mother | Over-protection, dependency, complacency, spoon-fed |
| 食伤 Output | Creativity, productivity, expression, purpose, children | Exhaustion, over-giving, burnout, obligation to produce |
| 财星 Wealth | Ambition, acquisition, reward for effort, material comfort | Greed, overreach, spread thin, chasing what can't be held |
| 官杀 Power | Discipline, structure, career authority, status, husband(F) | Oppression, stress, restriction, crushed by expectations |

#### Narrative Rules (DM Strength × Category)

**High = category % is notably above 20% (balanced share). Low = notably below.**

**比劫 Companion (same element):**
- Weak DM + high 比劫 → "Carried by allies, not alone in struggle"
- Weak DM + low 比劫 → "Isolated, few peers, must stand alone"
- Strong DM + high 比劫 → "Too many competitors for same resources"
- Strong DM + low 比劫 → "Stands out, few rivals, clear field"

**印星 Resource (produces DM):**
- Weak DM + high 印星 → "Well-nurtured despite weakness, protected by elders/knowledge"
- Weak DM + low 印星 → "Self-taught, limited mentorship, early independence"
- Strong DM + high 印星 → "Over-protected, may lack drive, comfortable but stagnant"
- Strong DM + low 印星 → "Self-made strength, didn't need much nurturing"

**食伤 Output (DM produces):**
- Weak DM + high 食伤 → "Pressured to produce beyond capacity, burnt out by obligations"
- Weak DM + low 食伤 → "Conserves energy, limited output but sustainable"
- Strong DM + high 食伤 → "Natural creator, loves expression, productive and energized"
- Strong DM + low 食伤 → "Strong but unexpressive, potential untapped"

**财星 Wealth (DM controls):**
- Weak DM + high 财星 → "Wealth beyond grasp, ambitious but overextended"
- Weak DM + low 财星 → "Few material demands, simpler path"
- Strong DM + high 财星 → "Capable wealth-holder, ambitious and rewarded"
- Strong DM + low 财星 → "Strong but limited opportunity, talent without stage"

**官杀 Power (controls DM):**
- Weak DM + high 官杀 → "Crushed by authority, heavy external pressure"
- Weak DM + low 官杀 → "Few constraints, freedom but also less structure"
- Strong DM + high 官杀 → "Disciplined strength, authority channeled into achievement"
- Strong DM + low 官杀 → "Unchecked strength, may lack direction/accountability"

#### Cross-Row Patterns (most significant combinations)

When two categories interact, the combination tells a deeper story:

| Pattern | Condition | Narrative |
|---------|-----------|-----------|
| 杀印相生 | High 官杀 + High 印星 | Pressure channeled through mentorship → growth through adversity |
| 杀无印化 | High 官杀 + Low 印星 | Raw oppression without shelter → harsh, unprotected life |
| 食伤生财 | High 食伤 + High 财星 | Output converts to reward → hard work pays off materially |
| 食伤无财 | High 食伤 + Low 财星 | Produces much but gains little → creative but poor |
| 比劫夺财 | High 比劫 + Low 财星 | Many competitors, little to share → rivalry over scraps |
| 印重食轻 | High 印星 + Low 食伤 | Over-thinking, under-doing → sheltered but unproductive |
| 财多身弱 | High 财星 + Weak DM | Wealth crushes weak master → bites off more than can chew |
| 官杀混杂 | High 官杀 + High 比劫 | Authority vs rebellion → inner conflict, power struggles |

#### Seasonal Context

Note the DM element's seasonal state from Step 6 in the header. This provides environmental context:
- 旺 Prosperous / 相 Prime → Season supports DM (natural backing)
- 休 Rest → Season is neutral
- 囚 Imprisoned / 死 Dead → Season oppresses DM (environmental headwind)

#### Output Format

```
Step 8b: DM Lens 日主助力分析
DM: 丁 Yin Fire (18.2%) | Strength: 偏弱 | Season: 囚 (-15%)

| Role | 十神 | Element | Pts | % | Narrative |
|------|------|---------|-----|---|-----------|
| 同我 Companion | 比劫 | Fire | 12.3 | 11% | [context-dependent narrative] |
| 生我 Resource | 印星 | Wood | 8.1 | 7% | [context-dependent narrative] |
| SUPPORT | | | 20.4 | 18% | |
| 我生 Output | 食伤 | Earth | 28.5 | 26% | [context-dependent narrative] |
| 我克 Wealth | 财星 | Metal | 18.2 | 16% | [context-dependent narrative] |
| 克我 Power | 官杀 | Water | 14.8 | 13% | [context-dependent narrative] |
| DRAIN | | | 61.5 | 55% | |

Support 18% : Drain 55% → 0.3:1
Cross-patterns: [list applicable cross-row patterns from table above]
→ [1-2 line overall narrative synthesis]
```

**The 5 individual row narratives ARE the main output.** The Support:Drain ratio is a summary footnote. Each row tells its own story through the DM's eyes.

---

## Step 9: Balance Simulation 调和模拟 (Tiáo Hé Mó Nǐ)

**ZERO OUTPUT for this step except the final 5-Gods table below. No thinking, no scenarios, no scores, no explanations.**

Internally: simulate adding +10 pt hovering HS nodes (gap 1 to all natal nodes, half-rate Step 7 flow) for each of the 10 stems (甲乙丙丁戊己庚辛壬癸). Score each by σ = √(Σ(pᵢ−20%)²/5) with DM penalty (+5 if DM<8%, +3 if DM>40%). Lowest score → 用神, highest → 忌神.

**Output ONLY this filled table:**

| 神 God | Element |
|---|---|
| 用神 Useful God | _(best single-element)_ |
| 喜神 Favorable God | _(produces 用神)_ |
| 忌神 Unfavorable God | _(worst single-element)_ |
| 仇神 Enemy God | _(produces 忌神)_ |
| 闲神 Idle God | _(remaining)_ |

---

## Future Steps (to be added iteratively)

- Step 10: Location modifier effects (hometown / out_of_town / overseas)
- Step 11: Gender effects
- Step 12: 10-Year Luck Pillar integration — 10YL is a **temporal (hovering) pillar**, always **0 gap** with all natal chart pillars (not positional in the YP–MP–DP–HP chain)
- Step 13: Final interpretation and life-area analysis
