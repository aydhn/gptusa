from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    RegimeTransitionType,
    RegimeTransitionRisk,
    TrendRegime,
    VolatilityMapRegime,
    LiquidityMapRegime,
    MomentumRegime,
    BreadthRegime,
    CrossSectionalRegime
)
from usa_signal_bot.regime_map.regime_map_models import (
    MultiTimeframeRegimeConfirmation,
    CrossSectionalRegimeMap,
    RegimeTransitionSignal,
    create_regime_transition_signal_id
)

def build_transition_signal(symbol: str | None, universe_name: str | None, transition_type: RegimeTransitionType, evidence: dict[str, Any]) -> RegimeTransitionSignal:
    return RegimeTransitionSignal(
        transition_id=create_regime_transition_signal_id(symbol),
        symbol=symbol,
        universe_name=universe_name,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        transition_type=transition_type,
        risk=RegimeTransitionRisk.UNKNOWN, # Set later
        score=None,
        evidence=evidence,
        warnings=[],
        errors=[]
    )

def detect_symbol_regime_transition(current: MultiTimeframeRegimeConfirmation, previous: MultiTimeframeRegimeConfirmation | None = None) -> list[RegimeTransitionSignal]:
    signals = []

    if not previous:
        # Without previous state, try to infer from snapshot conflicts (e.g. daily vs weekly)
        return infer_transition_from_snapshot_conflicts(current)

    curr_trend = current.dominant_trend_regime
    prev_trend = previous.dominant_trend_regime

    # Trend transitions
    if prev_trend in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND] and curr_trend in [TrendRegime.RANGE, TrendRegime.CHOPPY]:
        signals.append(build_transition_signal(current.symbol, None, RegimeTransitionType.TREND_TO_RANGE, {"prev": prev_trend.value, "curr": curr_trend.value}))
    elif prev_trend in [TrendRegime.RANGE, TrendRegime.CHOPPY] and curr_trend in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND, TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND]:
        signals.append(build_transition_signal(current.symbol, None, RegimeTransitionType.RANGE_TO_TREND, {"prev": prev_trend.value, "curr": curr_trend.value}))
    elif prev_trend in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND] and curr_trend in [TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND]:
        signals.append(build_transition_signal(current.symbol, None, RegimeTransitionType.UPTREND_TO_DOWNTREND, {"prev": prev_trend.value, "curr": curr_trend.value}))
    elif prev_trend in [TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND] and curr_trend in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND]:
         signals.append(build_transition_signal(current.symbol, None, RegimeTransitionType.DOWNTREND_TO_UPTREND, {"prev": prev_trend.value, "curr": curr_trend.value}))

    # Volatility transitions
    curr_vol = current.dominant_volatility_regime
    prev_vol = previous.dominant_volatility_regime
    if prev_vol in [VolatilityMapRegime.COMPRESSED, VolatilityMapRegime.NORMAL] and curr_vol in [VolatilityMapRegime.EXPANDING, VolatilityMapRegime.HIGH, VolatilityMapRegime.EXTREME]:
        signals.append(build_transition_signal(current.symbol, None, RegimeTransitionType.LOW_VOL_TO_HIGH_VOL, {"prev": prev_vol.value, "curr": curr_vol.value}))
    elif prev_vol in [VolatilityMapRegime.HIGH, VolatilityMapRegime.EXTREME, VolatilityMapRegime.EXPANDING] and curr_vol in [VolatilityMapRegime.NORMAL, VolatilityMapRegime.COMPRESSED]:
        signals.append(build_transition_signal(current.symbol, None, RegimeTransitionType.HIGH_VOL_TO_LOW_VOL, {"prev": prev_vol.value, "curr": curr_vol.value}))

    # Liquidity transitions
    curr_liq = current.dominant_liquidity_regime
    prev_liq = previous.dominant_liquidity_regime
    if prev_liq in [LiquidityMapRegime.NORMAL, LiquidityMapRegime.DEEP] and curr_liq in [LiquidityMapRegime.THINNING, LiquidityMapRegime.THIN, LiquidityMapRegime.ILLIQUID]:
        signals.append(build_transition_signal(current.symbol, None, RegimeTransitionType.LIQUIDITY_NORMAL_TO_THIN, {"prev": prev_liq.value, "curr": curr_liq.value}))

    # Momentum transitions
    curr_mom = current.dominant_momentum_regime
    prev_mom = previous.dominant_momentum_regime
    if prev_mom in [MomentumRegime.POSITIVE, MomentumRegime.STRONG_POSITIVE] and curr_mom in [MomentumRegime.EXHAUSTED, MomentumRegime.NEUTRAL, MomentumRegime.NEGATIVE]:
        signals.append(build_transition_signal(current.symbol, None, RegimeTransitionType.MOMENTUM_EXHAUSTION, {"prev": prev_mom.value, "curr": curr_mom.value}))

    return signals

def infer_transition_from_snapshot_conflicts(confirmation: MultiTimeframeRegimeConfirmation) -> list[RegimeTransitionSignal]:
    signals = []
    daily_snap = next((s for s in confirmation.snapshots if s.timeframe.value == 'DAILY'), None)
    weekly_snap = next((s for s in confirmation.snapshots if s.timeframe.value == 'WEEKLY'), None)

    if not daily_snap or not weekly_snap:
        return signals

    # If weekly is uptrend but daily is down, might be transitioning to range or downtrend
    if weekly_snap.trend_regime in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND] and daily_snap.trend_regime in [TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND]:
         signals.append(build_transition_signal(confirmation.symbol, None, RegimeTransitionType.TREND_TO_RANGE, {"inferred_from": "daily_weekly_divergence"}))

    # If weekly is compressed but daily is expanding
    if weekly_snap.volatility_regime in [VolatilityMapRegime.COMPRESSED, VolatilityMapRegime.NORMAL] and daily_snap.volatility_regime in [VolatilityMapRegime.EXPANDING, VolatilityMapRegime.HIGH]:
         signals.append(build_transition_signal(confirmation.symbol, None, RegimeTransitionType.LOW_VOL_TO_HIGH_VOL, {"inferred_from": "daily_weekly_divergence"}))

    return signals

def detect_universe_regime_transition(current: CrossSectionalRegimeMap, previous: CrossSectionalRegimeMap | None = None) -> list[RegimeTransitionSignal]:
    signals = []

    if not previous:
        signal = infer_transition_from_breadth_deterioration(current)
        if signal:
            signals.append(signal)
        return signals

    curr_breadth = current.breadth_regime
    prev_breadth = previous.breadth_regime

    if prev_breadth in [BreadthRegime.BROAD_RISK_ON, BreadthRegime.RISK_ON] and curr_breadth in [BreadthRegime.DETERIORATING, BreadthRegime.RISK_OFF]:
        signals.append(build_transition_signal(None, current.universe_name, RegimeTransitionType.BREADTH_RISK_ON_TO_OFF, {"prev": prev_breadth.value, "curr": curr_breadth.value}))

    curr_xs = current.cross_sectional_regime
    prev_xs = previous.cross_sectional_regime

    if prev_xs == CrossSectionalRegime.BROAD_UPTREND and curr_xs in [CrossSectionalRegime.ROTATION, CrossSectionalRegime.DISPERSION_HIGH]:
        signals.append(build_transition_signal(None, current.universe_name, RegimeTransitionType.REGIME_BREAK, {"prev": prev_xs.value, "curr": curr_xs.value, "detail": "Transition to high dispersion"}))

    return signals

def infer_transition_from_breadth_deterioration(current: CrossSectionalRegimeMap, previous: CrossSectionalRegimeMap | None = None) -> RegimeTransitionSignal | None:
    # Example: Even without history, if breadth is deteriorating but cross-sectional is still technically broad uptrend
    if current.breadth_regime == BreadthRegime.DETERIORATING and current.cross_sectional_regime == CrossSectionalRegime.BROAD_UPTREND:
        return build_transition_signal(None, current.universe_name, RegimeTransitionType.BREADTH_RISK_ON_TO_OFF, {"inferred_from": "breadth_vs_xs_divergence"})
    return None

def transition_detector_summary_to_text(signals: list[RegimeTransitionSignal]) -> str:
    if not signals:
        return "No regime transitions detected."
    types = [s.transition_type.value for s in signals]
    return f"Detected Transitions: {', '.join(types)}"
