from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    RegimeAlignmentStatus,
    TrendRegime,
    BreadthRegime,
    CrossSectionalRegime
)
from usa_signal_bot.regime_map.regime_map_models import (
    MultiTimeframeRegimeConfirmation,
    CrossSectionalRegimeMap,
    SymbolRegimeAlignment,
    create_symbol_regime_alignment_id
)


def calculate_alignment_score(symbol_confirmation: MultiTimeframeRegimeConfirmation, universe_map: CrossSectionalRegimeMap) -> float | None:
    if symbol_confirmation.dominant_trend_regime == TrendRegime.INSUFFICIENT_DATA or universe_map.cross_sectional_regime == CrossSectionalRegime.INSUFFICIENT_DATA:
        return None

    score = 50.0 # Base score

    sym_trend = symbol_confirmation.dominant_trend_regime
    xs_regime = universe_map.cross_sectional_regime

    # Uptrend alignments
    if sym_trend in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND]:
        if xs_regime in [CrossSectionalRegime.BROAD_UPTREND, CrossSectionalRegime.SELECTIVE_UPTREND]:
            score += 40
        elif xs_regime == CrossSectionalRegime.ROTATION:
            score += 10
        elif xs_regime in [CrossSectionalRegime.BROAD_DOWNTREND, CrossSectionalRegime.RISK_OFF]:
            score -= 40

    # Downtrend alignments
    elif sym_trend in [TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND]:
        if xs_regime in [CrossSectionalRegime.BROAD_DOWNTREND, CrossSectionalRegime.RISK_OFF]:
            score += 40
        elif xs_regime in [CrossSectionalRegime.BROAD_UPTREND, CrossSectionalRegime.SELECTIVE_UPTREND]:
            score -= 40

    return min(max(score, 0.0), 100.0)

def alignment_conflict_reasons(symbol_confirmation: MultiTimeframeRegimeConfirmation, universe_map: CrossSectionalRegimeMap) -> list[str]:
    reasons = []
    sym_trend = symbol_confirmation.dominant_trend_regime
    xs_regime = universe_map.cross_sectional_regime
    breadth = universe_map.breadth_regime

    if sym_trend in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND] and breadth in [BreadthRegime.RISK_OFF, BreadthRegime.DETERIORATING]:
        reasons.append("Symbol is in uptrend while market breadth is deteriorating or risk-off.")

    if sym_trend in [TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND] and breadth in [BreadthRegime.BROAD_RISK_ON, BreadthRegime.RISK_ON]:
        reasons.append("Symbol is in downtrend while market breadth is risk-on.")

    if sym_trend in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND] and xs_regime == CrossSectionalRegime.DISPERSION_HIGH:
        reasons.append("Symbol is in uptrend but market dispersion is very high (potential rotation/whipsaw risk).")

    return reasons

def recommended_guards_for_alignment(alignment: SymbolRegimeAlignment) -> list[str]:
    guards = []
    if alignment.status == RegimeAlignmentStatus.DIVERGENT:
        guards.append("REDUCE_POSITION_SIZE")
        guards.append("TIGHTEN_STOPS")
    elif alignment.status == RegimeAlignmentStatus.CONFLICTED:
        guards.append("SUPPRESS_SIGNAL")
        guards.append("REQUIRE_MANUAL_REVIEW")
    return guards

def evaluate_symbol_regime_alignment(symbol_confirmation: MultiTimeframeRegimeConfirmation, universe_map: CrossSectionalRegimeMap) -> SymbolRegimeAlignment:
    score = calculate_alignment_score(symbol_confirmation, universe_map)
    reasons = alignment_conflict_reasons(symbol_confirmation, universe_map)

    status = RegimeAlignmentStatus.UNKNOWN
    if score is None:
        status = RegimeAlignmentStatus.INSUFFICIENT_DATA
    elif score >= 80:
        status = RegimeAlignmentStatus.ALIGNED
    elif score >= 60:
        status = RegimeAlignmentStatus.MOSTLY_ALIGNED
    elif score >= 40:
        status = RegimeAlignmentStatus.MIXED
    elif score >= 20:
        status = RegimeAlignmentStatus.DIVERGENT
    else:
        status = RegimeAlignmentStatus.CONFLICTED

    alignment = SymbolRegimeAlignment(
        alignment_id=create_symbol_regime_alignment_id(symbol_confirmation.symbol),
        symbol=symbol_confirmation.symbol,
        universe_name=universe_map.universe_name,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=status,
        symbol_confirmation=symbol_confirmation,
        universe_regime_map=universe_map,
        alignment_score=score,
        conflict_reasons=reasons,
        recommended_guards=[],
        warnings=[],
        errors=[]
    )

    alignment.recommended_guards = recommended_guards_for_alignment(alignment)
    return alignment

def symbol_regime_alignment_to_text(alignment: SymbolRegimeAlignment) -> str:
    base = f"Alignment: {alignment.status.value}"
    if alignment.alignment_score is not None:
        base += f" (Score: {alignment.alignment_score:.1f})"
    if alignment.conflict_reasons:
        base += f" Conflicts: {', '.join(alignment.conflict_reasons)}"
    return base
