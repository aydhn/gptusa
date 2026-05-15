import datetime
from usa_signal_bot.core.enums import RegimeTransitionType, RegimeTransitionRisk, TrendRegime, VolatilityMapRegime, MomentumRegime, LiquidityMapRegime, BreadthRegime
from usa_signal_bot.regime_map.regime_map_models import MultiTimeframeRegimeConfirmation, CrossSectionalRegimeMap, RegimeTransitionSignal, create_regime_transition_signal_id

def detect_symbol_regime_transition(current: MultiTimeframeRegimeConfirmation, previous: MultiTimeframeRegimeConfirmation | None = None) -> list[RegimeTransitionSignal]:
    signals = []

    # Intrinsic transition inference (if we only have current but it shows conflicts typical of transitions)
    intrinsic = infer_transition_from_snapshot_conflicts(current)
    signals.extend(intrinsic)

    if not previous:
        return signals

    c_trend = current.dominant_trend_regime
    p_trend = previous.dominant_trend_regime

    # Trend to Range
    if p_trend in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND, TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND]:
        if c_trend in [TrendRegime.RANGE, TrendRegime.CHOPPY]:
            signals.append(_make_signal(current.symbol, None, RegimeTransitionType.TREND_TO_RANGE, RegimeTransitionRisk.LOW, 50.0, {"from": p_trend.value, "to": c_trend.value}))

    # Range to Trend
    if p_trend in [TrendRegime.RANGE, TrendRegime.CHOPPY]:
         if c_trend in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND, TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND]:
             signals.append(_make_signal(current.symbol, None, RegimeTransitionType.RANGE_TO_TREND, RegimeTransitionRisk.LOW, 50.0, {"from": p_trend.value, "to": c_trend.value}))

    # Trend Reversals
    if p_trend in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND] and c_trend in [TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND]:
         signals.append(_make_signal(current.symbol, None, RegimeTransitionType.UPTREND_TO_DOWNTREND, RegimeTransitionRisk.HIGH, 80.0, {"from": p_trend.value, "to": c_trend.value}))
    if p_trend in [TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND] and c_trend in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND]:
         signals.append(_make_signal(current.symbol, None, RegimeTransitionType.DOWNTREND_TO_UPTREND, RegimeTransitionRisk.MODERATE, 60.0, {"from": p_trend.value, "to": c_trend.value}))

    # Volatility
    c_vol = current.dominant_volatility_regime
    p_vol = previous.dominant_volatility_regime
    if p_vol in [VolatilityMapRegime.COMPRESSED, VolatilityMapRegime.NORMAL] and c_vol in [VolatilityMapRegime.EXPANDING, VolatilityMapRegime.HIGH, VolatilityMapRegime.EXTREME]:
        risk = RegimeTransitionRisk.MODERATE if c_vol == VolatilityMapRegime.EXPANDING else RegimeTransitionRisk.HIGH
        signals.append(_make_signal(current.symbol, None, RegimeTransitionType.LOW_VOL_TO_HIGH_VOL, risk, 70.0, {"from": p_vol.value, "to": c_vol.value}))

    # Liquidity
    c_liq = current.dominant_liquidity_regime
    p_liq = previous.dominant_liquidity_regime
    if p_liq in [LiquidityMapRegime.NORMAL, LiquidityMapRegime.DEEP] and c_liq in [LiquidityMapRegime.THINNING, LiquidityMapRegime.THIN, LiquidityMapRegime.ILLIQUID]:
         signals.append(_make_signal(current.symbol, None, RegimeTransitionType.LIQUIDITY_NORMAL_TO_THIN, RegimeTransitionRisk.MODERATE, 65.0, {"from": p_liq.value, "to": c_liq.value}))

    return signals

def detect_universe_regime_transition(current: CrossSectionalRegimeMap, previous: CrossSectionalRegimeMap | None = None) -> list[RegimeTransitionSignal]:
    signals = []

    if current.breadth_regime == BreadthRegime.DETERIORATING:
         signals.append(_make_signal(None, current.universe_name, RegimeTransitionType.BREADTH_RISK_ON_TO_OFF, RegimeTransitionRisk.HIGH, 75.0, {"current_breadth": "DETERIORATING"}))

    if not previous:
        return signals

    # Breadth Deterioration
    if previous.breadth_regime in [BreadthRegime.BROAD_RISK_ON, BreadthRegime.RISK_ON] and current.breadth_regime in [BreadthRegime.DETERIORATING, BreadthRegime.RISK_OFF]:
         # Avoid duplicate if added above
         if not any(s.transition_type == RegimeTransitionType.BREADTH_RISK_ON_TO_OFF for s in signals):
             signals.append(_make_signal(None, current.universe_name, RegimeTransitionType.BREADTH_RISK_ON_TO_OFF, RegimeTransitionRisk.HIGH, 80.0, {"from": previous.breadth_regime.value, "to": current.breadth_regime.value}))

    return signals

def infer_transition_from_snapshot_conflicts(confirmation: MultiTimeframeRegimeConfirmation) -> list[RegimeTransitionSignal]:
    signals = []
    # Exhaustion
    if confirmation.dominant_momentum_regime == MomentumRegime.EXHAUSTED and confirmation.dominant_trend_regime in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND]:
         signals.append(_make_signal(confirmation.symbol, None, RegimeTransitionType.MOMENTUM_EXHAUSTION, RegimeTransitionRisk.MODERATE, 60.0, {"momentum": "EXHAUSTED", "trend": confirmation.dominant_trend_regime.value}))

    return signals

def infer_transition_from_breadth_deterioration(current: CrossSectionalRegimeMap, previous: CrossSectionalRegimeMap | None = None) -> RegimeTransitionSignal | None:
    # Extracted to universe transitions
    return None

def transition_detector_summary_to_text(signals: list[RegimeTransitionSignal]) -> str:
    if not signals:
        return "No regime transitions detected."
    text = "Regime Transitions:\n"
    for s in signals:
        target = s.symbol or s.universe_name or "Unknown"
        text += f"- {target}: {s.transition_type.value} (Risk: {s.risk.value})\n"
    return text

def _make_signal(symbol: str | None, universe: str | None, t_type: RegimeTransitionType, risk: RegimeTransitionRisk, score: float, evidence: dict) -> RegimeTransitionSignal:
    return RegimeTransitionSignal(
        transition_id=create_regime_transition_signal_id(symbol),
        symbol=symbol,
        universe_name=universe,
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        transition_type=t_type,
        risk=risk,
        score=score,
        evidence=evidence,
        warnings=[],
        errors=[]
    )
