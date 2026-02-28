# Wu Xing Calculator — Deterministic Point-Based Scoring

**Date:** 2026-02-22
**Status:** Approved
**Replaces:** `scoring.ts`, `dynamic-scoring.ts`, scoring logic in `comprehensive/strength.ts`

---

## Summary

Replace the existing golden-ratio-based scoring system with a deterministic, step-by-step point calculator that follows the `bazi-wuxing` skill exactly. All 10 stems and 12 branches have fixed initial point values. Points flow through 9 sequential steps (pillar pairs, combinations, clashes, seasonal, cross-pillar flow, balance simulation) to produce final element totals, DM strength, and the 5 Gods.

## Decisions

| Question | Answer |
|----------|--------|
| Replace or parallel? | **Replace** existing scoring entirely |
| Scope | **Steps 0–9** (full implementation) |
| Per-node exposure | **Yes** — API returns per-node breakdown |
| Architecture | **Single monolithic file** + separate tables file |

## Data Model

### Node Tracking

Every qi source is an individual node with a mutable point value:

- `{Pillar}.HS` — Heavenly Stem (10 pts initial)
- `{Pillar}.EB` — Earthly Branch main qi (8 or 10 pts)
- `{Pillar}.EB.h1` — First hidden stem (3 pts)
- `{Pillar}.EB.h2` — Second hidden stem (1 pt)

Bonus nodes are created by combo/transform interactions (Steps 2–3).

### State Object

```
WuxingState {
  nodes[]         — all natal nodes with current points
  bonusNodes[]    — combo/transform bonus nodes
  interactions[]  — audit trail of all interactions
  season          — element from month branch
  pillarPriority  — age-based processing order
  attentionMap    — pre-scanned attention weights per EB node
}
```

## File Structure

```
src/lib/bazi/wuxing/
├── tables.ts         — Pure data: HS/EB points, hidden stems, combos,
│                       clashes, seasonal matrix, attention weights,
│                       gap matrix (~300 lines)
└── calculator.ts     — All 9 steps + entry point (~1500-2000 lines)
```

## Steps (from bazi-wuxing skill)

| Step | Name | What it does |
|------|------|-------------|
| 0 | Initial Points | Assign 10pt per HS, 8/3/1 per EB hidden stems |
| 1 | Pillar Pairs | HS↔EB main qi within same pillar: production ±20%/30%, control ±20%/30% |
| 2 | EB Positive | Branch combos (三会/三合/六合/半三会/拱合) → bonus element points |
| 3 | HS Positive | Stem combos (天干五合) → bonus element points |
| 4 | EB Negative | Branch clashes/punishments/harms/destructions → asymmetric damage |
| 5 | HS Negative | Stem clashes (天干四冲) → asymmetric damage |
| 6 | Seasonal | 旺相休囚死 multipliers per node based on month branch |
| 7 | Natural Flow | Cross-pillar production/control at half Step 1 rates |
| 8 | Report | Aggregate per-node → element totals, DM%, strength verdict |
| 9 | Balance Sim | Simulate +10pt hovering HS for each stem, minimize σ → 5 Gods |

### Key Mechanics

- **Continuous basis**: Each step uses the latest point values (not frozen snapshots)
- **Gap penalty**: Cross-pillar multipliers 1.0/0.75/0.5/0.25 by pillar distance
- **Three-Branch Priority**: Full trios nullify their component pair interactions
- **Attention Spread**: Weighted share system — nodes in multiple interactions split their attention proportionally by interaction weight (三会=63, 三合=42, 六冲=42, 六合=28, etc.)
- **Age-based priority**: Active pillar first, DP second, then by proximity
- **Transformation**: EB combos check HS for matching element; HS combos check EB main qi

## Entry Point

```typescript
calculateWuxing({
  yearPillar: "Bing-Yin",
  monthPillar: "Ji-Hai",
  dayPillar: "Ding-Chou",
  hourPillar: "Ding-Wei",
  age: 40,
  gender: "M",
  location: "hometown"
}) → WuxingResult
```

## Output Shape

```typescript
WuxingResult {
  nodes: Record<NodeId, { stem, element, initial, final, delta }>
  bonusNodes: BonusNode[]
  elements: Record<Element, { total, percent, rank }>
  dayMaster: { stem, element, percent, strength }
  gods: { useful, favorable, unfavorable, enemy, idle }
  interactions: InteractionLog[]
}
```

## Integration

1. `comprehensive/engine.ts` calls `calculateWuxing()` instead of `assessDayMasterStrength()`
2. `comprehensive/adapter.ts` maps `WuxingResult` → existing frontend JSON contract
3. Delete: `scoring.ts`, `dynamic-scoring.ts`, scoring logic from `strength.ts`
4. Frontend receives same shape — no frontend changes needed

## DM Strength Thresholds

| DM % | Strength | Label |
|------|----------|-------|
| >40% | Dominant | 极强 |
| 25–40% | Strong | 偏强 |
| 15–25% | Balanced | 中和 |
| 8–15% | Weak | 偏弱 |
| <8% | Very Weak | 极弱 |
