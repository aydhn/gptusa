from typing import Any, Dict, List, Optional, Tuple
from usa_signal_bot.core.enums import RuleConditionOperator, RuleConditionStatus, RuleStrategyFamily, RuleSignalBias, SignalAction
from usa_signal_bot.strategies.rule_models import RuleCondition, RuleConditionResult
import math

def get_latest_feature_row(rows: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not rows:
        return None
    return rows[-1]

def get_previous_feature_row(rows: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if len(rows) < 2:
        return None
    return rows[-2]

def safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        f_val = float(value)
        if math.isnan(f_val) or math.isinf(f_val):
            return None
        return f_val
    except (ValueError, TypeError):
        return None

def detect_cross_above(current_value: float, previous_value: float, current_reference: float, previous_reference: float) -> bool:
    return previous_value <= previous_reference and current_value > current_reference

def detect_cross_below(current_value: float, previous_value: float, current_reference: float, previous_reference: float) -> bool:
    return previous_value >= previous_reference and current_value < current_reference

def evaluate_condition(current_row: Dict[str, Any], previous_row: Optional[Dict[str, Any]], condition: RuleCondition) -> RuleConditionResult:
    feature_name = condition.feature_name

    if feature_name not in current_row:
        return RuleConditionResult(
            condition=condition,
            status=RuleConditionStatus.MISSING_FEATURE,
            passed=False,
            observed_value=None,
            message=f"Missing feature: {feature_name}",
            score_contribution=0.0
        )

    current_val = current_row[feature_name]

    if current_val is None:
        return RuleConditionResult(
            condition=condition,
            status=RuleConditionStatus.INVALID_VALUE,
            passed=False,
            observed_value=None,
            message=f"Invalid value for {feature_name}: None",
            score_contribution=0.0
        )

    passed = False
    status = RuleConditionStatus.FAILED
    score_contribution = 0.0

    if condition.operator == RuleConditionOperator.IS_TRUE:
        passed = bool(current_val)
    elif condition.operator == RuleConditionOperator.IS_FALSE:
        passed = not bool(current_val)
    elif condition.operator in [RuleConditionOperator.CROSS_ABOVE, RuleConditionOperator.CROSS_BELOW]:
        f_curr = safe_float(current_val)
        f_ref_curr = safe_float(condition.threshold) if isinstance(condition.threshold, (int, float, str)) else safe_float(current_row.get(condition.threshold)) if isinstance(condition.threshold, str) else None

        if previous_row and feature_name in previous_row:
            f_prev = safe_float(previous_row[feature_name])
            f_ref_prev = safe_float(condition.threshold) if isinstance(condition.threshold, (int, float, str)) else safe_float(previous_row.get(condition.threshold)) if isinstance(condition.threshold, str) else None

            if f_curr is not None and f_prev is not None and f_ref_curr is not None and f_ref_prev is not None:
                if condition.operator == RuleConditionOperator.CROSS_ABOVE:
                    passed = detect_cross_above(f_curr, f_prev, f_ref_curr, f_ref_prev)
                else:
                    passed = detect_cross_below(f_curr, f_prev, f_ref_curr, f_ref_prev)
            else:
                 return RuleConditionResult(
                    condition=condition,
                    status=RuleConditionStatus.INVALID_VALUE,
                    passed=False,
                    observed_value=current_val,
                    message=f"Invalid float conversion for crossover logic",
                    score_contribution=0.0
                )
        else:
            return RuleConditionResult(
                condition=condition,
                status=RuleConditionStatus.MISSING_FEATURE,
                passed=False,
                observed_value=current_val,
                message=f"Missing previous row/feature for crossover logic",
                score_contribution=0.0
            )

    else:
        f_curr = safe_float(current_val)
        if f_curr is None:
             return RuleConditionResult(
                condition=condition,
                status=RuleConditionStatus.INVALID_VALUE,
                passed=False,
                observed_value=current_val,
                message=f"Could not convert {feature_name} to float",
                score_contribution=0.0
            )

        if condition.operator == RuleConditionOperator.BETWEEN:
            passed = condition.lower <= f_curr <= condition.upper
        elif condition.operator == RuleConditionOperator.OUTSIDE:
            passed = f_curr < condition.lower or f_curr > condition.upper
        else:
            f_ref = safe_float(condition.threshold) if isinstance(condition.threshold, (int, float, str)) else safe_float(current_row.get(condition.threshold)) if isinstance(condition.threshold, str) else None
            if f_ref is None:
                return RuleConditionResult(
                    condition=condition,
                    status=RuleConditionStatus.INVALID_VALUE,
                    passed=False,
                    observed_value=current_val,
                    message=f"Invalid reference threshold: {condition.threshold}",
                    score_contribution=0.0
                )

            if condition.operator == RuleConditionOperator.GT:
                passed = f_curr > f_ref
            elif condition.operator == RuleConditionOperator.GTE:
                passed = f_curr >= f_ref
            elif condition.operator == RuleConditionOperator.LT:
                passed = f_curr < f_ref
            elif condition.operator == RuleConditionOperator.LTE:
                passed = f_curr <= f_ref
            elif condition.operator == RuleConditionOperator.EQ:
                passed = math.isclose(f_curr, f_ref)
            elif condition.operator == RuleConditionOperator.NEQ:
                passed = not math.isclose(f_curr, f_ref)

    if passed:
        status = RuleConditionStatus.PASSED
        score_contribution = condition.weight

    msg = f"Passed" if passed else f"Failed"
    return RuleConditionResult(
        condition=condition,
        status=status,
        passed=passed,
        observed_value=current_val,
        message=msg,
        score_contribution=score_contribution
    )

def evaluate_conditions(current_row: Dict[str, Any], previous_row: Optional[Dict[str, Any]], conditions: List[RuleCondition]) -> List[RuleConditionResult]:
    return [evaluate_condition(current_row, previous_row, c) for c in conditions]

def calculate_rule_score(results: List[RuleConditionResult]) -> float:
    return sum(r.score_contribution for r in results)

def normalize_rule_score(raw_score: float, max_score: float) -> float:
    if max_score <= 0:
        return 0.0
    return max(0.0, min(100.0, (raw_score / max_score) * 100.0))

def classify_rule_bias(strategy_family: RuleStrategyFamily, score: float, action: SignalAction) -> RuleSignalBias:
    if action == SignalAction.LONG:
        return RuleSignalBias.BULLISH
    elif action == SignalAction.SHORT:
        return RuleSignalBias.BEARISH
    elif action == SignalAction.FLAT:
        return RuleSignalBias.NEUTRAL
    elif action == SignalAction.AVOID:
        return RuleSignalBias.AVOID

    # If WATCH or other
    if score >= 70:
        return RuleSignalBias.BULLISH
    elif score <= 30:
        return RuleSignalBias.BEARISH

    return RuleSignalBias.WATCH

def build_rule_reasons(results: List[RuleConditionResult], max_reasons: int = 8) -> List[str]:
    reasons = []
    for r in results:
        if r.passed:
            reasons.append(f"[{r.condition.name}] Passed ({r.observed_value})")
        elif r.status == RuleConditionStatus.MISSING_FEATURE:
             reasons.append(f"[{r.condition.name}] Missing feature {r.condition.feature_name}")
        elif r.status == RuleConditionStatus.INVALID_VALUE:
             reasons.append(f"[{r.condition.name}] Invalid value: {r.message}")
        else:
             reasons.append(f"[{r.condition.name}] Failed ({r.observed_value})")

    return reasons[:max_reasons]
