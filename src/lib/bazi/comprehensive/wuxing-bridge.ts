import 'server-only';

// =============================================================================
// WUXING BRIDGE — ChartData <-> WuxingInput conversion
// =============================================================================
// Extracted to its own file to avoid circular dependencies between
// engine.ts, report.ts, environment.ts, and adapter.ts.
// =============================================================================

import type { ChartData } from './models';
import type { WuxingInput } from '../wuxing/calculator';

/**
 * Convert ChartData into WuxingInput for the wuxing calculator.
 * Reusable helper for any module that needs to compute wuxing results
 * from a ChartData object.
 */
export function chartToWuxingInput(chart: ChartData): WuxingInput {
  return {
    yearPillar: { stem: chart.pillars.year.stem, branch: chart.pillars.year.branch },
    monthPillar: { stem: chart.pillars.month.stem, branch: chart.pillars.month.branch },
    dayPillar: { stem: chart.pillars.day.stem, branch: chart.pillars.day.branch },
    hourPillar: { stem: chart.pillars.hour.stem, branch: chart.pillars.hour.branch },
    age: chart.age,
    gender: chart.gender === 'male' ? 'M' : 'F',
    location: 'hometown',
  };
}
