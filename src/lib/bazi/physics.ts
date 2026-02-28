
// =============================================================================
// PHYSICS SCHOOL — Yin/Yang Polarity Threshold
// =============================================================================
// Rule: When a Yin stem interacts with a Yang stem, the Yin stem's qi
// must be >= YIN_YANG_THRESHOLD * the Yang stem's qi for the interaction
// to proceed. Same-polarity interactions always proceed.

import type { Polarity } from './core';

export const YIN_YANG_THRESHOLD = 1.382;

/**
 * Return true if the interaction should be skipped due to Yin/Yang threshold.
 */
export function shouldSkipYinYang(
  hsPolarity: Polarity,
  qiPolarity: Polarity,
  hsQi: number,
  qiQi: number,
): boolean {
  if (hsPolarity === qiPolarity) return false;

  let yinQi: number;
  let yangQi: number;
  if (hsPolarity === "Yin") {
    yinQi = hsQi;
    yangQi = qiQi;
  } else {
    yinQi = qiQi;
    yangQi = hsQi;
  }

  return yinQi < YIN_YANG_THRESHOLD * yangQi;
}
