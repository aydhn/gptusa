from typing import List, Dict, Any, Optional
from usa_signal_bot.core.enums import NonActivationEvaluationRuleKind
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    NonActivationEvaluationBoundaryRule,
    NonActivationEvaluationBoundaryResult,
    create_non_activation_evaluation_boundary_rule_id,
    create_non_activation_evaluation_boundary_result_id,
    _now_utc
)

def build_non_activation_evaluation_boundary_rules(context_payload: Optional[Dict[str, Any]] = None) -> List[NonActivationEvaluationBoundaryRule]:
    ctx = context_payload or {}
    rules = []

    kinds = [
        (NonActivationEvaluationRuleKind.NO_MODEL_TRAINING_IN_PHASE138, "training_started"),
        (NonActivationEvaluationRuleKind.NO_MODEL_PREDICTION_IN_PHASE138, "prediction_started"),
        (NonActivationEvaluationRuleKind.NO_TRADE_SIGNAL_OUTPUT, "produces_trade_signal"),
        (NonActivationEvaluationRuleKind.NO_ORDER_DECISION_OUTPUT, "produces_order_decision"),
        (NonActivationEvaluationRuleKind.NO_PORTFOLIO_WEIGHT_OUTPUT, "produces_portfolio_weights"),
        (NonActivationEvaluationRuleKind.NO_STRATEGY_ACTIVATION, "strategy_activation_allowed"),
        (NonActivationEvaluationRuleKind.NO_BROKER_EXECUTION, "broker_execution_enabled"),
        (NonActivationEvaluationRuleKind.NO_PAPER_MUTATION, "paper_state_mutation_enabled"),
        (NonActivationEvaluationRuleKind.NO_TELEGRAM_REAL_SEND, "telegram_real_send_enabled"),
        (NonActivationEvaluationRuleKind.NO_DEPLOYMENT, "deployment_allowed"),
        (NonActivationEvaluationRuleKind.NO_LIVE_DAEMON, "daemon_started"),
        (NonActivationEvaluationRuleKind.NO_SCHEDULER, "scheduler_enabled"),
    ]

    for kind, key in kinds:
        val = ctx.get(key, False)
        passed = not val
        rules.append(NonActivationEvaluationBoundaryRule(
            rule_id=create_non_activation_evaluation_boundary_rule_id(),
            created_at_utc=_now_utc(),
            rule_kind=kind,
            name=f"Enforce {kind.value}",
            required=True,
            passed=passed,
            expected_value=False,
            observed_value=val,
            rationale=f"{key} must be False"
        ))

    return rules

def build_non_activation_evaluation_boundary_result(rules: List[NonActivationEvaluationBoundaryRule]) -> NonActivationEvaluationBoundaryResult:
    passed = all(r.passed for r in rules if r.required)
    r_map = {r.rule_kind: r for r in rules}

    return NonActivationEvaluationBoundaryResult(
        boundary_result_id=create_non_activation_evaluation_boundary_result_id(),
        created_at_utc=_now_utc(),
        rules=rules,
        boundary_passed=passed,
        no_model_training_in_phase138=r_map[NonActivationEvaluationRuleKind.NO_MODEL_TRAINING_IN_PHASE138].passed,
        no_model_prediction_in_phase138=r_map[NonActivationEvaluationRuleKind.NO_MODEL_PREDICTION_IN_PHASE138].passed,
        no_trade_signal_output=r_map[NonActivationEvaluationRuleKind.NO_TRADE_SIGNAL_OUTPUT].passed,
        no_order_decision_output=r_map[NonActivationEvaluationRuleKind.NO_ORDER_DECISION_OUTPUT].passed,
        no_portfolio_weight_output=r_map[NonActivationEvaluationRuleKind.NO_PORTFOLIO_WEIGHT_OUTPUT].passed,
        no_strategy_activation=r_map[NonActivationEvaluationRuleKind.NO_STRATEGY_ACTIVATION].passed,
        no_broker_execution=r_map[NonActivationEvaluationRuleKind.NO_BROKER_EXECUTION].passed,
        no_paper_mutation=r_map[NonActivationEvaluationRuleKind.NO_PAPER_MUTATION].passed,
        no_telegram_real_send=r_map[NonActivationEvaluationRuleKind.NO_TELEGRAM_REAL_SEND].passed,
        no_deployment=r_map[NonActivationEvaluationRuleKind.NO_DEPLOYMENT].passed,
        no_live_daemon=r_map[NonActivationEvaluationRuleKind.NO_LIVE_DAEMON].passed,
        no_scheduler=r_map[NonActivationEvaluationRuleKind.NO_SCHEDULER].passed,
        research_metadata_only=True
    )

def validate_non_activation_evaluation_boundary_result(result: NonActivationEvaluationBoundaryResult) -> List[str]:
    errors = []
    if not result.boundary_passed:
        errors.append("Non-activation boundary failed.")
    for r in result.rules:
        if r.required and not r.passed:
            errors.append(f"Rule {r.rule_kind.value} failed.")
    return errors

def non_activation_evaluation_boundary_passed(result: NonActivationEvaluationBoundaryResult) -> bool:
    return result.boundary_passed

def non_activation_evaluation_boundary_summary(result: NonActivationEvaluationBoundaryResult) -> Dict[str, Any]:
    return {
        "passed": result.boundary_passed,
        "rules_total": len(result.rules),
        "rules_passed": sum(1 for r in result.rules if r.passed)
    }

def non_activation_evaluation_boundary_to_text(result: NonActivationEvaluationBoundaryResult, limit: int = 300) -> str:
    summary = non_activation_evaluation_boundary_summary(result)
    return f"Non-Activation Boundary: Passed={summary['passed']} ({summary['rules_passed']}/{summary['rules_total']} rules)"
