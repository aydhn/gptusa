from typing import Any

from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    NonActivationMLClosureBoundaryResult,
    NonActivationMLClosureBoundaryRule,
    NonActivationMLClosureRuleKind,
    create_non_activation_ml_closure_boundary_result_id,
    create_non_activation_ml_closure_boundary_rule_id,
    current_time
)

def build_non_activation_ml_closure_boundary_rules(context_payload: dict[str, Any] | None = None) -> list[NonActivationMLClosureBoundaryRule]:
    rules = []

    # OFFLINE_RESEARCH_ONLY
    rules.append(NonActivationMLClosureBoundaryRule(
        rule_id=create_non_activation_ml_closure_boundary_rule_id(),
        created_at_utc=current_time(),
        rule_kind=NonActivationMLClosureRuleKind.OFFLINE_RESEARCH_ONLY,
        name="Offline Research Only Check",
        required=True,
        passed=True,
        expected_value=True,
        observed_value=True,
        rationale="Phase 145 is an offline research band",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    # NO_STRATEGY_ACTIVATION
    rules.append(NonActivationMLClosureBoundaryRule(
        rule_id=create_non_activation_ml_closure_boundary_rule_id(),
        created_at_utc=current_time(),
        rule_kind=NonActivationMLClosureRuleKind.NO_STRATEGY_ACTIVATION,
        name="No Strategy Activation Check",
        required=True,
        passed=True,
        expected_value=False,
        observed_value=False,
        rationale="Strategy activation is strictly forbidden in Phase 145",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    return rules

def build_non_activation_ml_closure_boundary_result(rules: list[NonActivationMLClosureBoundaryRule]) -> NonActivationMLClosureBoundaryResult:
    passed = all(r.passed for r in rules if r.required)

    return NonActivationMLClosureBoundaryResult(
        boundary_id=create_non_activation_ml_closure_boundary_result_id(),
        created_at_utc=current_time(),
        rules=rules,
        boundary_passed=passed,
        offline_research_only=True,
        explainability_metadata_only=True,
        governance_closure_only=True,
        no_live_inference=True,
        no_online_inference=True,
        no_live_monitoring=True,
        no_alert_sender=True,
        no_trade_signal_output=True,
        no_order_decision_output=True,
        no_portfolio_weight_output=True,
        no_strategy_activation=True,
        no_broker_execution=True,
        no_paper_mutation=True,
        no_telegram_real_send=True,
        no_deployment=True,
        no_dashboard=True,
        no_live_daemon=True,
        no_scheduler=True,
        no_backtest_execution=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def non_activation_ml_closure_boundary_passed(result: NonActivationMLClosureBoundaryResult) -> bool:
    return result.boundary_passed

def validate_non_activation_ml_closure_boundary_result(result: NonActivationMLClosureBoundaryResult) -> list[str]:
    errors = []
    if not result.no_strategy_activation:
        errors.append("Boundary allows strategy activation")
    if not result.no_broker_execution:
        errors.append("Boundary allows broker execution")
    if not result.no_deployment:
        errors.append("Boundary allows deployment")
    if not result.no_backtest_execution:
        errors.append("Boundary allows backtest execution")
    return errors

def non_activation_ml_closure_boundary_summary(result: NonActivationMLClosureBoundaryResult) -> dict[str, Any]:
    return {
        "passed": result.boundary_passed,
        "rule_count": len(result.rules)
    }

def non_activation_ml_closure_boundary_to_text(result: NonActivationMLClosureBoundaryResult, limit: int = 300) -> str:
    summary = non_activation_ml_closure_boundary_summary(result)
    return f"Non-Activation Boundary Passed: {summary['passed']}. Rules evaluated: {summary['rule_count']}"
