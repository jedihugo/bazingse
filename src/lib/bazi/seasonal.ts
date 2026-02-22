import 'server-only';

// =============================================================================
// SEASONAL STRENGTH & TRANSFORMATION RULES
// =============================================================================
// Season/element_states are now embedded in BRANCHES (core.ts).
// This file derives seasonal lookups from that embedded data.

import { BRANCHES, type Element, type BranchName, type ElementState } from './core';

// Build SEASONAL_STRENGTH from BRANCHES.element_states
// Format: Element -> {State -> BranchName[]}
type SeasonalStrengthMap = Record<Element, Partial<Record<ElementState, BranchName[]>>>;

const _seasonalStrength: SeasonalStrengthMap = {
  Wood: {}, Fire: {}, Earth: {}, Metal: {}, Water: {},
};

for (const branchId of Object.keys(BRANCHES) as BranchName[]) {
  const branch = BRANCHES[branchId];
  for (const [element, state] of Object.entries(branch.element_states) as [Element, ElementState][]) {
    if (!_seasonalStrength[element][state]) {
      _seasonalStrength[element][state] = [];
    }
    _seasonalStrength[element][state]!.push(branchId);
  }
}

export const SEASONAL_STRENGTH: Readonly<SeasonalStrengthMap> = _seasonalStrength;

export const SEASONAL_ADJUSTMENT = {
  // Balanced multipliers for seasonal effects (旺相休囚死)
  // Reduced impact for more subtle seasonal influence
  prosperous: 1.382,     // 旺 Wang - Peak/thriving (strongest)
  strengthening: 1.236,  // 相 Xiang - Growing phase
  resting: 1.0,          // 休 Xiu - Baseline (no change)
  trapped: 0.886,        // 囚 Qiu - Trapped/declining
  dead: 0.786,           // 死 Si - Dead/weakest
} as const;

// Alias for backward compatibility
export const ELEMENT_SEASONAL_STATES = SEASONAL_STRENGTH;
