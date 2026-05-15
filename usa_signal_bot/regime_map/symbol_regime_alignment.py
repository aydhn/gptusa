import datetime
from usa_signal_bot.core.enums import RegimeAlignmentStatus, TrendRegime, CrossSectionalRegime, BreadthRegime
from usa_signal_bot.regime_map.regime_map_models import SymbolRegimeAlignment, MultiTimeframeRegimeConfirmation, CrossSectionalRegimeMap, create_symbol_regime_alignment_id

def evaluate_symbol_regime_alignment(symbol_confirmation: MultiTimeframeRegimeConfirmation, universe_map: CrossSectionalRegimeMap) -> SymbolRegimeAlignment:
    score = calculate_alignment_score(symbol_confirmation, universe_map)
    reasons = alignment_conflict_reasons(symbol_confirmation, universe_map)

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

    warnings = []
    if status in [RegimeAlignmentStatus.DIVERGENT, RegimeAlignmentStatus.CONFLICTED]:
        warnings.append("Symbol is fighting the overall market regime.")

    alignment = SymbolRegimeAlignment(
        alignment_id=create_symbol_regime_alignment_id(symbol_confirmation.symbol),
        symbol=symbol_confirmation.symbol,
        universe_name=universe_map.universe_name,
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        status=status,
        symbol_confirmation=symbol_confirmation,
        universe_regime_map=universe_map,
        alignment_score=score,
        conflict_reasons=reasons,
        recommended_guards=[],
        warnings=warnings,
        errors=[]
    )

    alignment.recommended_guards = recommended_guards_for_alignment(alignment)
    return alignment

def calculate_alignment_score(symbol_confirmation: MultiTimeframeRegimeConfirmation, universe_map: CrossSectionalRegimeMap) -> float | None:
    if symbol_confirmation.dominant_trend_regime == TrendRegime.INSUFFICIENT_DATA or universe_map.cross_sectional_regime == CrossSectionalRegime.INSUFFICIENT_DATA:
        return None

    score = 50.0 # Neutral start
    sym_trend = symbol_confirmation.dominant_trend_regime
    uni_regime = universe_map.cross_sectional_regime
    breadth = universe_map.breadth_regime

    up_trends = [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND]
    down_trends = [TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND]

    if sym_trend in up_trends:
        if uni_regime in [CrossSectionalRegime.BROAD_UPTREND, CrossSectionalRegime.SELECTIVE_UPTREND]:
             score += 40
        elif uni_regime == CrossSectionalRegime.ROTATION:
             score += 10
        elif uni_regime in [CrossSectionalRegime.BROAD_DOWNTREND, CrossSectionalRegime.RISK_OFF]:
             score -= 40

        if breadth in [BreadthRegime.BROAD_RISK_ON, BreadthRegime.RISK_ON]:
            score += 10
        elif breadth in [BreadthRegime.DETERIORATING, BreadthRegime.RISK_OFF]:
            score -= 20

    elif sym_trend in down_trends:
        if uni_regime in [CrossSectionalRegime.BROAD_DOWNTREND, CrossSectionalRegime.RISK_OFF]:
             score += 40
        elif uni_regime in [CrossSectionalRegime.BROAD_UPTREND, CrossSectionalRegime.SELECTIVE_UPTREND]:
             score -= 40

    # Bound between 0 and 100
    return max(0.0, min(100.0, score))

def alignment_conflict_reasons(symbol_confirmation: MultiTimeframeRegimeConfirmation, universe_map: CrossSectionalRegimeMap) -> list[str]:
    reasons = []
    sym_trend = symbol_confirmation.dominant_trend_regime
    uni_regime = universe_map.cross_sectional_regime
    breadth = universe_map.breadth_regime

    up_trends = [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND]
    down_trends = [TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND]

    if sym_trend in up_trends and uni_regime in [CrossSectionalRegime.BROAD_DOWNTREND, CrossSectionalRegime.RISK_OFF]:
         reasons.append("Symbol is in uptrend while universe is in broad downtrend/risk-off.")
    if sym_trend in up_trends and breadth == BreadthRegime.DETERIORATING:
         reasons.append("Symbol is in uptrend but overall market breadth is deteriorating.")
    if sym_trend in down_trends and uni_regime in [CrossSectionalRegime.BROAD_UPTREND, CrossSectionalRegime.SELECTIVE_UPTREND]:
         reasons.append("Symbol is in downtrend while universe is in uptrend.")

    return reasons

def recommended_guards_for_alignment(alignment: SymbolRegimeAlignment) -> list[str]:
    guards = []
    if alignment.status in [RegimeAlignmentStatus.CONFLICTED, RegimeAlignmentStatus.DIVERGENT]:
        guards.append("REDUCE_POSITION_SIZE")
        guards.append("TIGHTEN_STOPS")
        guards.append("REQUIRE_STRONGER_SIGNAL")
    return guards

def symbol_regime_alignment_to_text(alignment: SymbolRegimeAlignment) -> str:
    text = f"Alignment: {alignment.symbol} vs {alignment.universe_name} -> {alignment.status.value}\n"
    text += f"Score: {alignment.alignment_score:.2f}\n" if alignment.alignment_score is not None else "Score: N/A\n"
    if alignment.conflict_reasons:
        text += f"Conflicts: {'; '.join(alignment.conflict_reasons)}\n"
    if alignment.recommended_guards:
        text += f"Guards: {'; '.join(alignment.recommended_guards)}"
    return text
