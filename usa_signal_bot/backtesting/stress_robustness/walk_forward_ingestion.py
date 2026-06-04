from typing import Any
import datetime
from pathlib import Path
import json

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    WalkForwardIngestionResult,
    create_walk_forward_ingestion_id
)
from usa_signal_bot.core.enums import StressRobustnessRiskFlag

def ingest_walk_forward_review_payload(payload: dict[str, Any]) -> WalkForwardIngestionResult:
    valid_for_phase151, errors, warnings, risk_flags = _validate_walk_forward_payload(payload)

    return WalkForwardIngestionResult(
        ingestion_id=create_walk_forward_ingestion_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        source_path=payload.get("source_path"),
        source_review_id=payload.get("review_id"),
        source_context_id=payload.get("context", {}).get("context_id"),
        available=True,
        benchmark_comparison_ingested=payload.get("context", {}).get("ingestion", {}).get("benchmark_comparison_ingested", False),
        window_policy_built=payload.get("context", {}).get("window_policy_built", False),
        anchored_splits_built=payload.get("context", {}).get("anchored_splits_built", False),
        rolling_splits_built=payload.get("context", {}).get("rolling_splits_built", False),
        fold_replay_configs_built=payload.get("context", {}).get("fold_replay_configs_built", False),
        fold_replays_built=payload.get("context", {}).get("fold_replays_built", False),
        fold_performance_metrics_built=payload.get("context", {}).get("fold_performance_metrics_built", False),
        fold_benchmark_comparisons_built=payload.get("context", {}).get("fold_benchmark_comparisons_built", False),
        oos_robustness_metrics_built=payload.get("context", {}).get("oos_robustness_metrics_built", False),
        temporal_stability_built=payload.get("context", {}).get("temporal_stability_built", False),
        degradation_diagnostics_built=payload.get("context", {}).get("degradation_diagnostics_built", False),
        robustness_summary_built=payload.get("context", {}).get("robustness_summary_built", False),
        walk_forward_validation_report_built=payload.get("context", {}).get("walk_forward_validation_report_built", False),
        temporal_stability_audit_built=payload.get("context", {}).get("temporal_stability_audit_built", False),
        safety_boundary_validated=payload.get("context", {}).get("safety_boundary_validated", False),
        phase151_readiness_gate_built=payload.get("context", {}).get("phase151_readiness_gate_built", False),
        phase151_readiness_gate_passed=payload.get("context", {}).get("phase151_readiness_gate_passed", False),
        ready_for_phase151=payload.get("context", {}).get("ready_for_phase151", False),
        research_data_only=payload.get("context", {}).get("research_data_only", True),
        offline_backtest_research_only=payload.get("context", {}).get("offline_backtest_research_only", True),
        deterministic=payload.get("context", {}).get("deterministic", True),
        live_trading_enabled=payload.get("context", {}).get("live_trading_enabled", False),
        paper_trading_enabled=payload.get("context", {}).get("paper_trading_enabled", False),
        broker_execution_enabled=payload.get("context", {}).get("broker_execution_enabled", False),
        real_order_creation_enabled=payload.get("context", {}).get("real_order_creation_enabled", False),
        paper_state_mutation_enabled=payload.get("context", {}).get("paper_state_mutation_enabled", False),
        telegram_real_send_enabled=payload.get("context", {}).get("telegram_real_send_enabled", False),
        strategy_activation_allowed=payload.get("context", {}).get("strategy_activation_allowed", False),
        portfolio_optimization_enabled=payload.get("context", {}).get("portfolio_optimization_enabled", False),
        portfolio_allocation_output_enabled=payload.get("context", {}).get("portfolio_allocation_output_enabled", False),
        deployment_allowed=payload.get("context", {}).get("deployment_allowed", False),
        network_used=payload.get("context", {}).get("network_used", False),
        paid_api_used=payload.get("context", {}).get("paid_api_used", False),
        scraping_used=payload.get("context", {}).get("scraping_used", False),
        html_parsing_used=payload.get("context", {}).get("html_parsing_used", False),
        dashboard_started=payload.get("context", {}).get("dashboard_started", False),
        daemon_started=payload.get("context", {}).get("daemon_started", False),
        scheduler_enabled=payload.get("context", {}).get("scheduler_enabled", False),
        walk_forward_executed=payload.get("context", {}).get("walk_forward_executed", True),
        stress_test_executed=payload.get("context", {}).get("stress_test_executed", False),
        monte_carlo_executed=payload.get("context", {}).get("monte_carlo_executed", False),
        produces_live_signal=payload.get("context", {}).get("produces_live_signal", False),
        produces_order_decision=payload.get("context", {}).get("produces_order_decision", False),
        produces_portfolio_weights=payload.get("context", {}).get("produces_portfolio_weights", False),
        investment_advice=payload.get("context", {}).get("investment_advice", False),
        valid_for_phase151=valid_for_phase151,
        risk_flags=risk_flags,
        warnings=warnings,
        errors=errors,
        metadata={"source_report_type": payload.get("report_type")}
    )

def _validate_walk_forward_payload(payload: dict[str, Any]) -> tuple[bool, list[str], list[str], list[StressRobustnessRiskFlag]]:
    errors = []
    warnings = []
    risk_flags = []
    valid = True

    if not payload:
        errors.append("Empty payload")
        risk_flags.append(StressRobustnessRiskFlag.WALK_FORWARD_REVIEW_MISSING)
        return False, errors, warnings, risk_flags

    context = payload.get("context", {})
    if not context:
        errors.append("Missing context")
        risk_flags.append(StressRobustnessRiskFlag.WALK_FORWARD_REVIEW_INVALID)
        valid = False

    if not context.get("ready_for_phase151"):
        errors.append("ready_for_phase151 is false")
        risk_flags.append(StressRobustnessRiskFlag.PHASE150_NOT_READY)
        valid = False

    if not context.get("safety_boundary_validated"):
        errors.append("safety_boundary_validated is false")
        risk_flags.append(StressRobustnessRiskFlag.WALK_FORWARD_SAFETY_BOUNDARY_FAILED)
        valid = False

    if not context.get("phase151_readiness_gate_passed"):
        errors.append("phase151_readiness_gate_passed is false")
        risk_flags.append(StressRobustnessRiskFlag.PHASE151_READINESS_GATE_FAILED)
        valid = False

    # Check for live trading flags
    unsafe_flags = [
        "live_trading_enabled", "paper_trading_enabled", "broker_execution_enabled",
        "real_order_creation_enabled", "paper_state_mutation_enabled", "telegram_real_send_enabled",
        "strategy_activation_allowed", "portfolio_optimization_enabled", "portfolio_allocation_output_enabled",
        "deployment_allowed", "produces_live_signal", "produces_order_decision",
        "produces_portfolio_weights", "investment_advice"
    ]
    for flag in unsafe_flags:
        if context.get(flag):
            errors.append(f"Unsafe flag detected: {flag}")
            valid = False

    if context.get("live_trading_enabled"):
        risk_flags.append(StressRobustnessRiskFlag.LIVE_TRADING_RISK)
    if context.get("broker_execution_enabled"):
        risk_flags.append(StressRobustnessRiskFlag.BROKER_RISK)
    if context.get("paper_state_mutation_enabled"):
        risk_flags.append(StressRobustnessRiskFlag.PAPER_MUTATION_RISK)
    if context.get("strategy_activation_allowed"):
        risk_flags.append(StressRobustnessRiskFlag.STRATEGY_ACTIVATION_RISK)
    if context.get("investment_advice"):
        risk_flags.append(StressRobustnessRiskFlag.INVESTMENT_ADVICE_LANGUAGE_RISK)

    if context.get("stress_test_executed"):
        errors.append("stress_test_executed is true in Phase 150 payload (forbidden)")
        valid = False
    if context.get("monte_carlo_executed"):
        errors.append("monte_carlo_executed is true in Phase 150 payload (forbidden)")
        valid = False

    return valid, errors, warnings, risk_flags

def ingest_latest_walk_forward_review_from_store(data_root: Path) -> WalkForwardIngestionResult:
    # Bu metod son phase150 review json okumak içindir
    from usa_signal_bot.backtesting.walk_forward.walk_forward_store import get_latest_walk_forward_review

    latest_path = get_latest_walk_forward_review(data_root)
    if not latest_path or not latest_path.exists():
        return WalkForwardIngestionResult(
            ingestion_id=create_walk_forward_ingestion_id(),
            created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
            source_path=None, source_review_id=None, source_context_id=None,
            available=False, benchmark_comparison_ingested=False, window_policy_built=False,
            anchored_splits_built=False, rolling_splits_built=False, fold_replay_configs_built=False,
            fold_replays_built=False, fold_performance_metrics_built=False, fold_benchmark_comparisons_built=False,
            oos_robustness_metrics_built=False, temporal_stability_built=False, degradation_diagnostics_built=False,
            robustness_summary_built=False, walk_forward_validation_report_built=False, temporal_stability_audit_built=False,
            safety_boundary_validated=False, phase151_readiness_gate_built=False, phase151_readiness_gate_passed=False,
            ready_for_phase151=False, research_data_only=False, offline_backtest_research_only=False,
            deterministic=False, live_trading_enabled=False, paper_trading_enabled=False, broker_execution_enabled=False,
            real_order_creation_enabled=False, paper_state_mutation_enabled=False, telegram_real_send_enabled=False,
            strategy_activation_allowed=False, portfolio_optimization_enabled=False, portfolio_allocation_output_enabled=False,
            deployment_allowed=False, network_used=False, paid_api_used=False, scraping_used=False, html_parsing_used=False,
            dashboard_started=False, daemon_started=False, scheduler_enabled=False, walk_forward_executed=False,
            stress_test_executed=False, monte_carlo_executed=False, produces_live_signal=False, produces_order_decision=False,
            produces_portfolio_weights=False, investment_advice=False, valid_for_phase151=False,
            risk_flags=[StressRobustnessRiskFlag.WALK_FORWARD_REVIEW_MISSING],
            warnings=[], errors=["No walk forward review found in store"], metadata={}
        )

    try:
        with open(latest_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        payload["source_path"] = str(latest_path)
        return ingest_walk_forward_review_payload(payload)
    except Exception as e:
        res = ingest_walk_forward_review_payload({})
        res.errors.append(f"Failed to load latest review: {str(e)}")
        return res
