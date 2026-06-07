import json
from pathlib import Path
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    StressRobustnessIngestionResult, BacktestClosureRiskFlag
)
from usa_signal_bot.core.exceptions import StressRobustnessIngestionError

def ingest_stress_robustness_review_payload(payload: dict[str, Any]) -> StressRobustnessIngestionResult:
    result = StressRobustnessIngestionResult()

    if not payload:
        result.valid_for_phase152 = False
        result.risk_flags.append(BacktestClosureRiskFlag.STRESS_ROBUSTNESS_REVIEW_MISSING)
        return result

    result.available = True
    result.source_review_id = payload.get("review_id")
    result.source_context_id = payload.get("context", {}).get("context_id")

    ctx = payload.get("context", {})
    result.walk_forward_ingested = ctx.get("walk_forward_ingested", False)
    result.scenario_policy_built = ctx.get("scenario_policy_built", False)
    result.scenario_replays_built = ctx.get("scenario_replays_built", False)
    result.scenario_metrics_built = ctx.get("scenario_metrics_built", False)
    result.cost_liquidity_sensitivity_built = ctx.get("cost_liquidity_sensitivity_built", False)
    result.monte_carlo_policy_built = ctx.get("monte_carlo_policy_built", False)
    result.monte_carlo_paths_built = ctx.get("monte_carlo_paths_built", False)
    result.monte_carlo_replays_built = ctx.get("monte_carlo_replays_built", False)
    result.monte_carlo_distributions_built = ctx.get("monte_carlo_distributions_built", False)
    result.tail_risk_diagnostics_built = ctx.get("tail_risk_diagnostics_built", False)
    result.robustness_scorecard_built = ctx.get("robustness_scorecard_built", False)
    result.stress_validation_report_built = ctx.get("stress_validation_report_built", False)
    result.monte_carlo_robustness_report_built = ctx.get("monte_carlo_robustness_report_built", False)
    result.safety_boundary_validated = ctx.get("safety_boundary_validated", False)
    result.phase152_readiness_gate_built = ctx.get("phase152_readiness_gate_built", False)
    result.phase152_readiness_gate_passed = ctx.get("phase152_readiness_gate_passed", False)
    result.ready_for_phase152 = ctx.get("ready_for_phase152", False)

    # Safety flags
    result.research_data_only = ctx.get("research_data_only", True)
    result.offline_backtest_research_only = ctx.get("offline_backtest_research_only", True)
    result.live_trading_enabled = ctx.get("live_trading_enabled", False)
    result.paper_trading_enabled = ctx.get("paper_trading_enabled", False)
    result.broker_execution_enabled = ctx.get("broker_execution_enabled", False)
    result.real_order_creation_enabled = ctx.get("real_order_creation_enabled", False)
    result.paper_state_mutation_enabled = ctx.get("paper_state_mutation_enabled", False)
    result.telegram_real_send_enabled = ctx.get("telegram_real_send_enabled", False)
    result.strategy_activation_allowed = ctx.get("strategy_activation_allowed", False)
    result.portfolio_optimization_enabled = ctx.get("portfolio_optimization_enabled", False)
    result.portfolio_allocation_output_enabled = ctx.get("portfolio_allocation_output_enabled", False)
    result.deployment_allowed = ctx.get("deployment_allowed", False)
    result.network_used = ctx.get("network_used", False)
    result.paid_api_used = ctx.get("paid_api_used", False)
    result.scraping_used = ctx.get("scraping_used", False)
    result.html_parsing_used = ctx.get("html_parsing_used", False)
    result.dashboard_started = ctx.get("dashboard_started", False)
    result.daemon_started = ctx.get("daemon_started", False)
    result.scheduler_enabled = ctx.get("scheduler_enabled", False)
    result.produces_live_signal = ctx.get("produces_live_signal", False)
    result.produces_order_decision = ctx.get("produces_order_decision", False)
    result.produces_portfolio_weights = ctx.get("produces_portfolio_weights", False)
    result.investment_advice = ctx.get("investment_advice", False)

    result.stress_test_executed = ctx.get("stress_test_executed", False)
    result.monte_carlo_executed = ctx.get("monte_carlo_executed", False)

    valid, errors = stress_robustness_supports_phase152(payload)
    result.valid_for_phase152 = valid
    if not valid:
        result.errors.extend(errors)
        if "Missing safety_boundary_validated" in str(errors):
            result.risk_flags.append(BacktestClosureRiskFlag.STRESS_SAFETY_BOUNDARY_FAILED)
        elif "Ready for phase152 is False" in str(errors):
            result.risk_flags.append(BacktestClosureRiskFlag.PHASE151_NOT_READY)
        else:
            result.risk_flags.append(BacktestClosureRiskFlag.STRESS_ROBUSTNESS_REVIEW_INVALID)

    return result

def stress_robustness_supports_phase152(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []
    ctx = payload.get("context", {})
    if not ctx.get("phase152_readiness_gate_passed"):
        errors.append("phase152_readiness_gate_passed is False")
    if not ctx.get("ready_for_phase152"):
        errors.append("Ready for phase152 is False")
    if not ctx.get("safety_boundary_validated"):
        errors.append("Missing safety_boundary_validated")
    if not ctx.get("stress_validation_report_built"):
        errors.append("Missing stress_validation_report_built")
    if not ctx.get("monte_carlo_robustness_report_built"):
        errors.append("Missing monte_carlo_robustness_report_built")
    if not ctx.get("robustness_scorecard_built"):
        errors.append("Missing robustness_scorecard_built")
    if not ctx.get("stress_test_executed"):
        errors.append("stress_test_executed is False")
    if not ctx.get("monte_carlo_executed"):
        errors.append("monte_carlo_executed is False")

    if not ctx.get("research_data_only", True):
        errors.append("research_data_only is False")
    if not ctx.get("offline_backtest_research_only", True):
        errors.append("offline_backtest_research_only is False")

    for field in ["live_trading_enabled", "paper_trading_enabled", "broker_execution_enabled",
                  "real_order_creation_enabled", "paper_state_mutation_enabled", "telegram_real_send_enabled",
                  "strategy_activation_allowed", "deployment_allowed", "network_used", "paid_api_used",
                  "scraping_used", "html_parsing_used", "dashboard_started", "daemon_started", "scheduler_enabled",
                  "portfolio_optimization_enabled", "portfolio_allocation_output_enabled",
                  "produces_live_signal", "produces_order_decision", "produces_portfolio_weights", "investment_advice"]:
        if ctx.get(field):
            errors.append(f"{field} is True")

    return len(errors) == 0, errors

def ingest_latest_stress_robustness_review_from_store(data_root: Path) -> StressRobustnessIngestionResult:
    review_dir = data_root / "backtesting" / "stress_robustness" / "reviews"
    if not review_dir.exists():
        res = StressRobustnessIngestionResult()
        res.valid_for_phase152 = False
        res.errors.append(f"Directory not found: {review_dir}")
        res.risk_flags.append(BacktestClosureRiskFlag.STRESS_ROBUSTNESS_REVIEW_MISSING)
        return res

    files = list(review_dir.glob("stress_robustness_full_review_*.json"))
    if not files:
        res = StressRobustnessIngestionResult()
        res.valid_for_phase152 = False
        res.errors.append("No stress robustness reviews found")
        res.risk_flags.append(BacktestClosureRiskFlag.STRESS_ROBUSTNESS_REVIEW_MISSING)
        return res

    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    latest = files[0]
    try:
        with open(latest, 'r') as f:
            payload = json.load(f)
        res = ingest_stress_robustness_review_payload(payload)
        res.source_path = str(latest)
        return res
    except Exception as e:
        raise StressRobustnessIngestionError(f"Failed to ingest: {e}")

def extract_stress_robustness_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_stress_validation_report(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("stress_validation_report")

def extract_monte_carlo_robustness_report(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("monte_carlo_robustness_report")

def extract_robustness_scorecard(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("robustness_scorecard")

def extract_stress_safety_boundary(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("safety_boundary")

def extract_phase152_readiness_gate(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("phase152_readiness_gate")

def stress_robustness_ingestion_to_text(result: StressRobustnessIngestionResult) -> str:
    return f"Stress Robustness Ingestion (Valid: {result.valid_for_phase152}): {len(result.errors)} errors, {len(result.risk_flags)} flags"
