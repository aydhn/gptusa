from typing import Any
from usa_signal_bot.core.enums import RegimeTransitionType, RegimeTransitionRisk
from usa_signal_bot.regime_map.regime_map_models import RegimeTransitionSignal

def calculate_transition_risk_score(signal: RegimeTransitionSignal) -> float | None:
    score = 0.0
    t_type = signal.transition_type

    # Base risk by transition type
    if t_type == RegimeTransitionType.BREADTH_RISK_ON_TO_OFF:
        score += 80.0
    elif t_type == RegimeTransitionType.REGIME_BREAK:
        score += 70.0
    elif t_type == RegimeTransitionType.LOW_VOL_TO_HIGH_VOL:
        score += 60.0
    elif t_type == RegimeTransitionType.LIQUIDITY_NORMAL_TO_THIN:
        score += 50.0
    elif t_type == RegimeTransitionType.MOMENTUM_EXHAUSTION:
        score += 40.0
    elif t_type == RegimeTransitionType.UPTREND_TO_DOWNTREND:
        score += 50.0
    elif t_type == RegimeTransitionType.TREND_TO_RANGE:
        score += 30.0
    elif t_type == RegimeTransitionType.DOWNTREND_TO_UPTREND:
         score += 20.0 # Opportunities, less 'risk' in the traditional sense, maybe just uncertainty
    elif t_type == RegimeTransitionType.RANGE_TO_TREND:
         score += 20.0

    return score

def classify_transition_risk(score: float | None, transition_type: RegimeTransitionType | None = None) -> RegimeTransitionRisk:
    if score is None:
        return RegimeTransitionRisk.UNKNOWN

    if score >= 80:
        return RegimeTransitionRisk.CRITICAL
    elif score >= 60:
        return RegimeTransitionRisk.HIGH
    elif score >= 40:
        return RegimeTransitionRisk.MODERATE
    elif score >= 20:
        return RegimeTransitionRisk.LOW

    return RegimeTransitionRisk.NONE

def aggregate_transition_risk(signals: list[RegimeTransitionSignal]) -> RegimeTransitionRisk:
    if not signals:
        return RegimeTransitionRisk.NONE

    total_score = 0.0
    for s in signals:
        score = calculate_transition_risk_score(s)
        if score is not None:
             total_score += score
             s.score = score
             s.risk = classify_transition_risk(score, s.transition_type)

    # Non-linear aggregation: multiple moderate risks can sum to high risk
    agg_risk = classify_transition_risk(total_score)

    # If any single risk is critical, aggregate is critical
    if any(s.risk == RegimeTransitionRisk.CRITICAL for s in signals):
        return RegimeTransitionRisk.CRITICAL

    return agg_risk

def transition_risk_recommended_guards(signals: list[RegimeTransitionSignal]) -> list[str]:
    guards = set()
    for s in signals:
        if s.transition_type == RegimeTransitionType.BREADTH_RISK_ON_TO_OFF:
            guards.add("REDUCE_NET_LONG_EXPOSURE")
            guards.add("TIGHTEN_PORTFOLIO_STOPS")
        if s.transition_type == RegimeTransitionType.LOW_VOL_TO_HIGH_VOL:
            guards.add("REDUCE_POSITION_SIZES")
            guards.add("WIDEN_INITIAL_STOPS_REDUCE_SIZE")
        if s.transition_type == RegimeTransitionType.LIQUIDITY_NORMAL_TO_THIN:
             guards.add("APPLY_STIFFER_LIQUIDITY_FILTERS")
             guards.add("AVOID_MARKET_ORDERS")
    return list(guards)

def transition_risk_to_text(signals: list[RegimeTransitionSignal]) -> str:
    agg_risk = aggregate_transition_risk(signals)
    base = f"Aggregate Transition Risk: {agg_risk.value}"
    if signals:
         types = [s.transition_type.value for s in signals]
         base += f" ({', '.join(types)})"
    return base
