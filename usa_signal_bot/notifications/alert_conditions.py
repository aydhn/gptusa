from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import AlertConditionOperator
from usa_signal_bot.notifications.alert_models import AlertCondition

@dataclass
class AlertConditionResult:
    condition_name: str
    passed: bool
    observed_value: Any
    message: str
    missing: bool = False
    error: Optional[str] = None

def get_value_by_field_path(payload: Dict[str, Any], field_path: str) -> Any:
    parts = field_path.split(".")
    curr = payload
    for part in parts:
        if isinstance(curr, dict) and part in curr:
            curr = curr[part]
        elif hasattr(curr, part):
            curr = getattr(curr, part)
        else:
            return None
    return curr

def safe_compare_values(value: Any, operator: AlertConditionOperator, threshold: Any = None, lower: Optional[float] = None, upper: Optional[float] = None) -> bool:
    try:
        if operator == AlertConditionOperator.EXISTS:
            return value is not None
        if value is None:
            return False

        if operator == AlertConditionOperator.IS_TRUE:
            return bool(value) is True
        if operator == AlertConditionOperator.IS_FALSE:
            return bool(value) is False

        if operator == AlertConditionOperator.EQ:
            return value == threshold
        if operator == AlertConditionOperator.NEQ:
            return value != threshold
        if operator == AlertConditionOperator.GT:
            return value > threshold
        if operator == AlertConditionOperator.GTE:
            return value >= threshold
        if operator == AlertConditionOperator.LT:
            return value < threshold
        if operator == AlertConditionOperator.LTE:
            return value <= threshold
        if operator == AlertConditionOperator.BETWEEN:
            if lower is None or upper is None:
                return False
            return lower <= value <= upper
        if operator == AlertConditionOperator.IN:
            if not isinstance(threshold, (list, set, tuple)):
                return False
            return value in threshold

        return False
    except Exception:
        return False

def evaluate_alert_condition(condition: AlertCondition, payload: Dict[str, Any]) -> AlertConditionResult:
    try:
        val = get_value_by_field_path(payload, condition.field_path)
        if val is None:
            if condition.operator == AlertConditionOperator.EXISTS:
                passed = safe_compare_values(val, condition.operator)
                return AlertConditionResult(condition.name, passed, val, "Field exists check evaluated", missing=not passed)
            else:
                return AlertConditionResult(condition.name, False, None, f"Field {condition.field_path} is missing", missing=True)

        passed = safe_compare_values(val, condition.operator, condition.threshold, condition.lower, condition.upper)
        return AlertConditionResult(condition.name, passed, val, f"Evaluated operator {condition.operator.value if hasattr(condition.operator, 'value') else condition.operator}")
    except Exception as e:
        return AlertConditionResult(condition.name, False, None, "Evaluation error", error=str(e))

def evaluate_alert_conditions(conditions: List[AlertCondition], payload: Dict[str, Any]) -> List[AlertConditionResult]:
    return [evaluate_alert_condition(c, payload) for c in conditions]

def all_required_conditions_passed(results: List[AlertConditionResult], conditions: List[AlertCondition]) -> bool:
    condition_map = {c.name: c for c in conditions}
    for res in results:
        c = condition_map.get(res.condition_name)
        if c and c.required and not res.passed:
            return False
    return True

def condition_results_to_dict(results: List[AlertConditionResult]) -> List[Dict[str, Any]]:
    return [
        {
            "condition_name": r.condition_name,
            "passed": r.passed,
            "observed_value": r.observed_value,
            "message": r.message,
            "missing": r.missing,
            "error": r.error
        }
        for r in results
    ]
