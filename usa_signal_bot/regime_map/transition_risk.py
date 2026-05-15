from usa_signal_bot.core.enums import RegimeTransitionType, RegimeTransitionRisk
from usa_signal_bot.regime_map.regime_map_models import RegimeTransitionSignal

def calculate_transition_risk_score(signal: RegimeTransitionSignal) -> float | None:
    return signal.score

def classify_transition_risk(score: float | None, transition_type: RegimeTransitionType | None = None) -> RegimeTransitionRisk:
    if score is None:
        return RegimeTransitionRisk.INSUFFICIENT_DATA
    if score >= 85:
        return RegimeTransitionRisk.CRITICAL
    if score >= 70:
        return RegimeTransitionRisk.HIGH
    if score >= 50:
        return RegimeTransitionRisk.MODERATE
    if score >= 20:
        return RegimeTransitionRisk.LOW
    return RegimeTransitionRisk.NONE

def aggregate_transition_risk(signals: list[RegimeTransitionSignal]) -> RegimeTransitionRisk:
    if not signals:
        return RegimeTransitionRisk.NONE

    has_critical = False
    has_high = False
    has_moderate = False
    has_low = False

    score_sum = 0.0
    valid_scores = 0

    for s in signals:
        if s.risk == RegimeTransitionRisk.CRITICAL: has_critical = True
        elif s.risk == RegimeTransitionRisk.HIGH: has_high = True
        elif s.risk == RegimeTransitionRisk.MODERATE: has_moderate = True
        elif s.risk == RegimeTransitionRisk.LOW: has_low = True

        if s.score is not None:
             score_sum += s.score
             valid_scores += 1

    # Combination logic
    types = [s.transition_type for s in signals]

    if RegimeTransitionType.BREADTH_RISK_ON_TO_OFF in types and RegimeTransitionType.LOW_VOL_TO_HIGH_VOL in types:
         return RegimeTransitionRisk.CRITICAL

    if has_critical:
        return RegimeTransitionRisk.CRITICAL
    if has_high:
        if len(signals) >= 3: # Multiple high/moderate might push to critical
            return RegimeTransitionRisk.CRITICAL
        return RegimeTransitionRisk.HIGH
    if has_moderate:
        if len(signals) >= 3:
             return RegimeTransitionRisk.HIGH
        return RegimeTransitionRisk.MODERATE
    if has_low:
        return RegimeTransitionRisk.LOW

    return RegimeTransitionRisk.NONE

def transition_risk_recommended_guards(signals: list[RegimeTransitionSignal]) -> list[str]:
    guards = set()
    agg_risk = aggregate_transition_risk(signals)

    if agg_risk in [RegimeTransitionRisk.CRITICAL, RegimeTransitionRisk.HIGH]:
         guards.add("REDUCE_EXPOSURE")
         guards.add("TIGHTEN_STOPS_AGGRESSIVELY")
         guards.add("PREFER_CASH")

    types = [s.transition_type for s in signals]
    if RegimeTransitionType.LIQUIDITY_NORMAL_TO_THIN in types:
         guards.add("INCREASE_LIQUIDITY_FILTER")
    if RegimeTransitionType.LOW_VOL_TO_HIGH_VOL in types:
         guards.add("DECREASE_POSITION_SIZE_FOR_VOL")

    return list(guards)

def transition_risk_to_text(signals: list[RegimeTransitionSignal]) -> str:
    agg = aggregate_transition_risk(signals)
    text = f"Aggregate Transition Risk: {agg.value}\n"
    guards = transition_risk_recommended_guards(signals)
    if guards:
         text += f"Guards: {', '.join(guards)}"
    return text
