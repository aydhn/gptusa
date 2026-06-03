from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
import datetime

from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import (
    BacktestAnalyticsIngestionResult,
    create_backtest_analytics_ingestion_id,
    BenchmarkComparisonRiskFlag
)


def extract_backtest_analytics_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("context")


def extract_backtest_analytics_report(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("analytics_report")


def extract_run_validation_report(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("run_validation")


def extract_backtest_analytics_safety_boundary(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("safety_boundary")


def extract_phase149_readiness_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("phase149_readiness_gate")


def backtest_analytics_supports_phase149(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []

    gate = extract_phase149_readiness_gate(payload)
    if not gate:
        return False, ["Missing phase149_readiness_gate"]

    if not gate.get("ready_for_phase149", False):
        return False, ["ready_for_phase149 is False"]

    if not payload.get("research_data_only", True):
        warnings.append("research_data_only is not strictly True in payload root")

    return True, warnings


def ingest_backtest_analytics_review_payload(payload: Dict[str, Any]) -> BacktestAnalyticsIngestionResult:
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    ingestion_id = create_backtest_analytics_ingestion_id()

    context = extract_backtest_analytics_context(payload)
    report = extract_backtest_analytics_report(payload)
    validation = extract_run_validation_report(payload)
    safety = extract_backtest_analytics_safety_boundary(payload)
    gate = extract_phase149_readiness_gate(payload)

    available = bool(context and report and validation and safety and gate)

    result = BacktestAnalyticsIngestionResult(
        ingestion_id=ingestion_id,
        created_at_utc=now_utc,
        source_path=payload.get("_source_path"),
        source_review_id=payload.get("review_id"),
        source_context_id=context.get("context_id") if context else None,
        available=available,
        backtest_run_ingested=True if report else False,
        inputs_resolved=True if report else False,
        return_series_built=True if report else False,
        rolling_analytics_built=True if report else False,
        advanced_performance_metrics_built=True if report else False,
        trade_diagnostics_built=True if report else False,
        fill_diagnostics_built=True if report else False,
        cost_diagnostics_built=True if report else False,
        exposure_diagnostics_built=True if report else False,
        drawdown_diagnostics_built=True if report else False,
        ledger_reconciliation_built=True if report else False,
        determinism_validation_built=True if report else False,
        run_validation_report_built=True if validation else False,
        analytics_report_built=True if report else False,
        safety_boundary_validated=True if safety else False,
        phase149_readiness_gate_built=True if gate else False,
        phase149_readiness_gate_passed=gate.get("passed", False) if gate else False,
        ready_for_phase149=gate.get("ready_for_phase149", False) if gate else False,
        research_data_only=payload.get("research_data_only", True),
        offline_backtest_research_only=payload.get("offline_backtest_research_only", True),
        deterministic=payload.get("deterministic", True),
        live_trading_enabled=payload.get("live_trading_enabled", False),
        paper_trading_enabled=payload.get("paper_trading_enabled", False),
        broker_execution_enabled=payload.get("broker_execution_enabled", False),
        real_order_creation_enabled=payload.get("real_order_creation_enabled", False),
        paper_state_mutation_enabled=payload.get("paper_state_mutation_enabled", False),
        telegram_real_send_enabled=payload.get("telegram_real_send_enabled", False),
        strategy_activation_allowed=payload.get("strategy_activation_allowed", False),
        portfolio_optimization_enabled=payload.get("portfolio_optimization_enabled", False),
        deployment_allowed=payload.get("deployment_allowed", False),
        network_used=payload.get("network_used", False),
        paid_api_used=payload.get("paid_api_used", False),
        scraping_used=payload.get("scraping_used", False),
        html_parsing_used=payload.get("html_parsing_used", False),
        dashboard_started=payload.get("dashboard_started", False),
        daemon_started=payload.get("daemon_started", False),
        scheduler_enabled=payload.get("scheduler_enabled", False),
        benchmark_comparison_executed=False, # From Phase 148, it should be False
        walk_forward_executed=payload.get("walk_forward_executed", False),
        stress_test_executed=payload.get("stress_test_executed", False),
        monte_carlo_executed=payload.get("monte_carlo_executed", False),
        produces_live_signal=payload.get("produces_live_signal", False),
        produces_order_decision=payload.get("produces_order_decision", False),
        produces_portfolio_weights=payload.get("produces_portfolio_weights", False),
        investment_advice=payload.get("investment_advice", False),
        valid_for_phase149=False,
    )

    supports, warnings = backtest_analytics_supports_phase149(payload)
    result.warnings.extend(warnings)

    if not available:
        result.errors.append("Missing required Phase 148 artifacts in review payload.")
        result.risk_flags.append(BenchmarkComparisonRiskFlag.BACKTEST_ANALYTICS_REVIEW_MISSING)

    if not result.ready_for_phase149:
        result.errors.append("Phase 148 review is not ready for Phase 149.")
        result.risk_flags.append(BenchmarkComparisonRiskFlag.PHASE148_NOT_READY)

    if result.live_trading_enabled or result.paper_trading_enabled or result.broker_execution_enabled:
        result.errors.append("Live/paper/broker execution enabled in review.")
        result.risk_flags.append(BenchmarkComparisonRiskFlag.LIVE_TRADING_RISK)

    if result.walk_forward_executed or result.stress_test_executed or result.monte_carlo_executed:
        result.errors.append("Advanced evaluation (walk-forward/stress/monte carlo) already executed.")
        result.risk_flags.append(BenchmarkComparisonRiskFlag.WALK_FORWARD_ATTEMPTED)

    if payload.get("benchmark_comparison_executed", False):
        result.errors.append("Benchmark comparison already executed in Phase 148 (should be Phase 149).")
        result.risk_flags.append(BenchmarkComparisonRiskFlag.BACKTEST_ANALYTICS_REVIEW_INVALID)

    if not result.errors:
        result.valid_for_phase149 = True

    return result


def ingest_latest_backtest_analytics_review_from_store(data_root: Path) -> BacktestAnalyticsIngestionResult:
    pass


def backtest_analytics_ingestion_to_text(result: BacktestAnalyticsIngestionResult) -> str:
    lines = [
        f"Ingestion ID: {result.ingestion_id}",
        f"Available: {result.available}",
        f"Valid for Phase 149: {result.valid_for_phase149}",
        f"Research Data Only: {result.research_data_only}"
    ]
    if result.errors:
        lines.append("Errors:")
        for err in result.errors:
            lines.append(f"  - {err}")
    return "\n".join(lines)
