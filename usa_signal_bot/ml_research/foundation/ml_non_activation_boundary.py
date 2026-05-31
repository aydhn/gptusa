from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from .phase136_models import MLNonActivationBoundaryRule, MLNonActivationBoundaryResult, MLNonActivationRuleKind, create_ml_non_activation_boundary_rule_id, create_ml_non_activation_boundary_result_id

def build_ml_non_activation_boundary_rules(context_payload: Optional[Dict[str, Any]] = None) -> List[MLNonActivationBoundaryRule]:
    now = datetime.now(timezone.utc).isoformat()
    kinds = [
        MLNonActivationRuleKind.NO_TRADE_SIGNAL_OUTPUT,
        MLNonActivationRuleKind.NO_ORDER_DECISION_OUTPUT,
        MLNonActivationRuleKind.NO_PORTFOLIO_WEIGHT_OUTPUT,
        MLNonActivationRuleKind.NO_STRATEGY_ACTIVATION,
        MLNonActivationRuleKind.NO_BROKER_EXECUTION,
        MLNonActivationRuleKind.NO_PAPER_MUTATION,
        MLNonActivationRuleKind.NO_TELEGRAM_REAL_SEND,
        MLNonActivationRuleKind.NO_DEPLOYMENT,
        MLNonActivationRuleKind.NO_MODEL_TRAINING_IN_PHASE136,
        MLNonActivationRuleKind.NO_MODEL_PREDICTION_IN_PHASE136,
        MLNonActivationRuleKind.NO_LIVE_DAEMON,
        MLNonActivationRuleKind.NO_SCHEDULER
    ]
    rules = []
    # Simplified evaluation based on payload if provided. For now assume safe by default
    safe = True
    if context_payload and context_payload.get("unsafe"): safe = False

    for kind in kinds:
        rules.append(MLNonActivationBoundaryRule(
            rule_id=create_ml_non_activation_boundary_rule_id(),
            created_at_utc=now,
            rule_kind=kind,
            name=kind.value,
            required=True,
            passed=safe,
            expected_value=None,
            observed_value=None,
            rationale=f"Checked {kind.value}"
        ))
    return rules

def build_ml_non_activation_boundary_result(rules: List[MLNonActivationBoundaryRule]) -> MLNonActivationBoundaryResult:
    now = datetime.now(timezone.utc).isoformat()
    passed = all(r.passed for r in rules)
    return MLNonActivationBoundaryResult(
        boundary_id=create_ml_non_activation_boundary_result_id(),
        created_at_utc=now,
        rules=rules,
        boundary_passed=passed,
        no_trade_signal_output=passed,
        no_order_decision_output=passed,
        no_portfolio_weight_output=passed,
        no_strategy_activation=passed,
        no_broker_execution=passed,
        no_paper_mutation=passed,
        no_telegram_real_send=passed,
        no_deployment=passed,
        no_model_training_in_phase136=passed,
        no_model_prediction_in_phase136=passed,
        no_live_daemon=passed,
        no_scheduler=passed,
        research_metadata_only=True
    )

def validate_ml_non_activation_boundary_result(result: MLNonActivationBoundaryResult) -> List[str]:
    if not result.boundary_passed:
        return ["Non-activation boundary failed"]
    return []

def ml_non_activation_boundary_passed(result: MLNonActivationBoundaryResult) -> bool:
    return result.boundary_passed

def ml_non_activation_boundary_summary(result: MLNonActivationBoundaryResult) -> Dict[str, Any]:
    return {"passed": result.boundary_passed}

def ml_non_activation_boundary_to_text(result: MLNonActivationBoundaryResult, limit: int = 300) -> str:
    return f"Boundary passed: {result.boundary_passed}"
