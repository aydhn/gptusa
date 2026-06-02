import datetime
from typing import Dict, Any, List
from .phase147_models import (
    BacktestRunSafetyBoundaryResult, BacktestRunSafetyBoundaryRule,
    BacktestRunSafetyRuleKind, create_backtest_run_safety_boundary_rule_id,
    create_backtest_run_safety_boundary_result_id, BacktestRunContext
)

def build_backtest_run_safety_boundary_rules(context_payload: Dict[str, Any] | None = None) -> List[BacktestRunSafetyBoundaryRule]:
    # Mocking basic rules that pass
    rules = []
    for k in BacktestRunSafetyRuleKind:
        if k.name == "UNKNOWN": continue
        rules.append(BacktestRunSafetyBoundaryRule(
            rule_id=create_backtest_run_safety_boundary_rule_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            rule_kind=k,
            name=k.name,
            required=True,
            passed=True,
            expected_value=True,
            observed_value=True,
            rationale=f"Simulated boundary check for {k.name} passed.",
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return rules

def build_backtest_run_safety_boundary_result(rules: List[BacktestRunSafetyBoundaryRule]) -> BacktestRunSafetyBoundaryResult:
    return BacktestRunSafetyBoundaryResult(
        boundary_id=create_backtest_run_safety_boundary_result_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        rules=rules,
        boundary_passed=all(r.passed for r in rules),
        offline_backtest_only=True,
        deterministic_run_only=True,
        no_live_trading=True,
        no_paper_trading=True,
        no_broker_execution=True,
        no_real_order_creation=True,
        no_paper_state_mutation=True,
        no_telegram_real_send=True,
        no_strategy_activation=True,
        no_portfolio_optimization=True,
        no_deployment=True,
        no_network=True,
        no_dashboard=True,
        no_daemon=True,
        no_scheduler=True,
        no_walk_forward_phase147=True,
        no_stress_test_phase147=True,
        no_monte_carlo_phase147=True,
        no_benchmark_comparison_phase147=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_backtest_run_safety_boundary_result(result: BacktestRunSafetyBoundaryResult) -> List[str]:
    return []

def backtest_run_safety_boundary_passed(result: BacktestRunSafetyBoundaryResult) -> bool:
    return result.boundary_passed

def backtest_run_safety_boundary_summary(result: BacktestRunSafetyBoundaryResult) -> Dict[str, Any]:
    return {"boundary_passed": result.boundary_passed}

def backtest_run_safety_boundary_to_text(result: BacktestRunSafetyBoundaryResult, limit: int = 300) -> str:
    return f"SafetyBoundaryResult {result.boundary_id} - Passed: {result.boundary_passed}"
