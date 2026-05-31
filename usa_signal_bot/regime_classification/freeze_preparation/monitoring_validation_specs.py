from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import MonitoringValidationRuleKind, MonitoringValidationStatus
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import (
    MonitoringValidationRule,
    create_monitoring_validation_rule_id,
    _now_utc_str
)

def build_monitoring_validation_rule(
    rule_kind: MonitoringValidationRuleKind,
    passed: bool,
    observed_value: Optional[Any] = None,
    expected_value: Optional[Any] = None,
    rationale: str = ""
) -> MonitoringValidationRule:
    return MonitoringValidationRule(
        rule_id=create_monitoring_validation_rule_id(),
        created_at_utc=_now_utc_str(),
        rule_kind=rule_kind,
        name=rule_kind.value if hasattr(rule_kind, 'value') else rule_kind,
        status=MonitoringValidationStatus.PASS if passed else MonitoringValidationStatus.FAIL,
        required=True,
        passed=passed,
        expected_value=expected_value,
        observed_value=observed_value,
        rationale=rationale,
        warnings=[],
        errors=[] if passed else [f"Rule failed: {rule_kind}"],
        risk_flags=[],
        metadata={}
    )

def build_default_monitoring_validation_rules() -> List[MonitoringValidationRule]:
    kinds = [
        MonitoringValidationRuleKind.MONITORING_REVIEW_VALID,
        MonitoringValidationRuleKind.BASELINE_AVAILABLE,
        MonitoringValidationRuleKind.SNAPSHOT_AVAILABLE,
        MonitoringValidationRuleKind.DRIFT_RESULT_AVAILABLE,
        MonitoringValidationRuleKind.DEGRADATION_DIAGNOSTICS_AVAILABLE,
        MonitoringValidationRuleKind.MONITORING_READINESS_GATE_PASSED,
        MonitoringValidationRuleKind.BASELINE_HASH_VALID,
        MonitoringValidationRuleKind.SNAPSHOT_HASH_VALID,
        MonitoringValidationRuleKind.DRIFT_RESULT_VALID,
        MonitoringValidationRuleKind.DEGRADATION_RESULT_VALID,
        MonitoringValidationRuleKind.CONSISTENCY_VALID,
        MonitoringValidationRuleKind.SAFETY_BOUNDARY_VALID,
        MonitoringValidationRuleKind.NO_SIGNAL_OUTPUT,
        MonitoringValidationRuleKind.NO_ORDER_OUTPUT,
        MonitoringValidationRuleKind.NO_PORTFOLIO_OUTPUT,
        MonitoringValidationRuleKind.NO_EXECUTION_OUTPUT,
        MonitoringValidationRuleKind.NO_MODEL_TRAINING
    ]

    return [build_monitoring_validation_rule(k, False, rationale="Default rule pending evaluation") for k in kinds]

def validate_monitoring_validation_rules(rules: List[MonitoringValidationRule]) -> List[str]:
    errors = []
    kinds = set(r.rule_kind for r in rules)
    req_kinds = set(r.rule_kind for r in build_default_monitoring_validation_rules())

    missing = req_kinds - kinds
    for m in missing:
        errors.append(f"Missing required rule kind: {m}")

    return errors

def monitoring_validation_specs_summary(rules: List[MonitoringValidationRule]) -> Dict[str, Any]:
    return {"rule_count": len(rules)}

def monitoring_validation_specs_to_text(rules: List[MonitoringValidationRule], limit: int = 200) -> str:
    return f"Rules: {len(rules)}"[:limit]
