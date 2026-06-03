from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import WalkForwardRiskFlag
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    WalkForwardContext,
    WalkForwardValidationReport,
    FoldReplayResult,
    TemporalStabilityAuditReport,
    WalkForwardSafetyBoundaryResult,
    Phase151ReadinessGate
)

UNSAFE_KEYWORDS = [
    "live trading", "real order", "broker execution", "buy order", "sell order",
    "guaranteed profit", "investment advice", "strategy active", "deploy to production"
]

def walk_forward_text_has_trade_or_execution_language(text: str) -> bool:
    if not text:
        return False
    lower_text = text.lower()
    return any(k in lower_text for k in UNSAFE_KEYWORDS)

def validate_walk_forward_context_safety(context: WalkForwardContext) -> List[str]:
    errors = []
    if context.live_trading_enabled:
        errors.append("live_trading_enabled is true")
    if context.paper_trading_enabled:
        errors.append("paper_trading_enabled is true")
    if context.broker_execution_enabled:
        errors.append("broker_execution_enabled is true")
    if context.real_order_creation_enabled:
        errors.append("real_order_creation_enabled is true")
    if context.paper_state_mutation_enabled:
        errors.append("paper_state_mutation_enabled is true")
    if context.telegram_real_send_enabled:
        errors.append("telegram_real_send_enabled is true")
    if context.strategy_activation_allowed:
        errors.append("strategy_activation_allowed is true")
    if context.portfolio_optimization_enabled:
        errors.append("portfolio_optimization_enabled is true")
    if context.portfolio_allocation_output_enabled:
        errors.append("portfolio_allocation_output_enabled is true")
    if context.deployment_allowed:
        errors.append("deployment_allowed is true")
    if context.network_used:
        errors.append("network_used is true")
    if context.paid_api_used:
        errors.append("paid_api_used is true")
    if context.dashboard_started:
        errors.append("dashboard_started is true")
    if context.daemon_started:
        errors.append("daemon_started is true")
    if context.scheduler_enabled:
        errors.append("scheduler_enabled is true")
    if context.stress_test_executed:
        errors.append("stress_test_executed is true")
    if context.monte_carlo_executed:
        errors.append("monte_carlo_executed is true")
    if context.produces_live_signal:
        errors.append("produces_live_signal is true")
    if context.produces_order_decision:
        errors.append("produces_order_decision is true")
    if context.produces_portfolio_weights:
        errors.append("produces_portfolio_weights is true")
    if context.investment_advice:
        errors.append("investment_advice is true")
    return errors

def validate_walk_forward_validation_report_safety(report: WalkForwardValidationReport) -> List[str]:
    errors = []
    if report.stress_test_executed:
        errors.append("stress_test_executed is true in report")
    if report.monte_carlo_executed:
        errors.append("monte_carlo_executed is true in report")
    if report.portfolio_optimization_enabled:
        errors.append("portfolio_optimization_enabled is true in report")
    if report.strategy_activation_allowed:
        errors.append("strategy_activation_allowed is true in report")
    if report.investment_advice:
        errors.append("investment_advice is true in report")
    return errors

def validate_fold_replay_results_safety(items: List[FoldReplayResult]) -> List[str]:
    errors = []
    for r in items:
        if r.real_order_created:
            errors.append(f"Result {r.result_id} real_order_created is true")
        if r.broker_execution_used:
            errors.append(f"Result {r.result_id} broker_execution_used is true")
        if r.paper_state_mutated:
            errors.append(f"Result {r.result_id} paper_state_mutated is true")
    return errors

def validate_temporal_stability_audit_safety(audit: TemporalStabilityAuditReport) -> List[str]:
    errors = []
    if not audit.no_strategy_activation:
        errors.append("audit no_strategy_activation is false")
    if not audit.no_investment_advice:
        errors.append("audit no_investment_advice is false")
    return errors

def validate_walk_forward_boundary_safety(result: WalkForwardSafetyBoundaryResult) -> List[str]:
    errors = []
    if not result.boundary_passed:
        errors.append("safety boundary failed")
    return errors

def validate_phase151_readiness_gate_safety(gate: Phase151ReadinessGate) -> List[str]:
    errors = []
    if gate.live_trading_enabled:
        errors.append("gate live_trading_enabled is true")
    if gate.stress_test_executed:
        errors.append("gate stress_test_executed is true")
    return errors

def validate_walk_forward_dataframe_output_safety(df: Any) -> List[str]:
    try:
        from usa_signal_bot.backtesting.walk_forward.walk_forward_input_resolver import detect_forbidden_walk_forward_columns
        cols = list(df.columns)
        forbidden = detect_forbidden_walk_forward_columns(cols)
        if forbidden:
            return [f"DataFrame contains forbidden columns: {forbidden}"]
    except Exception:
        pass
    return []

def collect_walk_forward_risk_flags(context: Optional[WalkForwardContext] = None) -> List[WalkForwardRiskFlag]:
    flags = set()
    if context:
        flags.update(context.risk_flags)
        for i in context.input_references:
            flags.update(i.risk_flags)
        flags.update(context.window_policy.risk_flags)
        for f in context.folds:
            flags.update(f.risk_flags)
        flags.update(context.validation_report.risk_flags)
        flags.update(context.temporal_stability_audit.risk_flags)
        flags.update(context.safety_boundary.risk_flags)
        flags.update(context.phase151_readiness_gate.risk_flags)
    return list(flags)

def walk_forward_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "safe": len(errors) == 0,
        "error_count": len(errors)
    }

def walk_forward_safety_to_text(errors: List[str]) -> str:
    return "Safe" if not errors else f"Unsafe ({len(errors)} errors)"
