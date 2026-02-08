# * =========================
# * PHYSICS SCHOOL — Yin/Yang Polarity Threshold
# * =========================
# Rule: When a Yin stem interacts with a Yang stem, the Yin stem's qi
# must be >= YIN_YANG_THRESHOLD × the Yang stem's qi for the interaction
# to proceed. Same-polarity interactions always proceed.

YIN_YANG_THRESHOLD = 1.382


def should_skip_yin_yang(hs_polarity, qi_polarity, hs_qi, qi_qi):
    """Return True if the interaction should be skipped due to Yin/Yang threshold."""
    if hs_polarity == qi_polarity:
        return False
    if hs_polarity == "Yin":
        yin_qi, yang_qi = hs_qi, qi_qi
    else:
        yin_qi, yang_qi = qi_qi, hs_qi
    return yin_qi < YIN_YANG_THRESHOLD * yang_qi
