import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from usa_signal_bot.core.enums import WalkForwardRiskFlag
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    BenchmarkComparisonIngestionResult,
    create_benchmark_comparison_ingestion_id,
    _now_utc,
)


def extract_benchmark_comparison_context(
    payload: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    return payload.get("context")


def extract_baseline_comparison_report(
    payload: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    return payload.get("baseline_comparison_report")


def extract_relative_performance_validation(
    payload: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    return payload.get("relative_performance_validation")


def extract_benchmark_safety_boundary(
    payload: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    return payload.get("safety_boundary")


def extract_phase150_readiness_gate(
    payload: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    return payload.get("phase150_readiness_gate")


def benchmark_comparison_supports_phase150(
    payload: Dict[str, Any],
) -> Tuple[bool, list[str]]:
    gate = extract_phase150_readiness_gate(payload)
    if not gate:
        return False, ["Missing phase150_readiness_gate in payload"]
    passed = gate.get("ready_for_phase150", False)
    if not passed:
        return False, ["ready_for_phase150 is False"]

    if payload.get("live_trading_enabled", False):
        return False, ["live_trading_enabled is True"]

    return True, []


def _extract_empty_flags() -> Dict[str, bool]:
    return {
        "backtest_analytics_ingested": False,
        "inputs_resolved": False,
        "benchmark_universe_contract_built": False,
        "passive_benchmark_config_built": False,
        "cash_benchmark_built": False,
        "buy_and_hold_benchmark_built": False,
        "equal_weight_metadata_benchmark_built": False,
        "market_index_reference_benchmark_built": False,
        "benchmark_return_series_built": False,
        "strategy_benchmark_alignment_built": False,
        "relative_performance_metrics_built": False,
        "benchmark_diagnostics_built": False,
        "baseline_comparison_report_built": False,
        "relative_performance_validation_built": False,
        "safety_boundary_validated": False,
        "research_data_only": True,
        "offline_backtest_research_only": True,
        "deterministic": True,
        "paper_trading_enabled": False,
        "broker_execution_enabled": False,
        "real_order_creation_enabled": False,
        "paper_state_mutation_enabled": False,
        "telegram_real_send_enabled": False,
        "strategy_activation_allowed": False,
        "portfolio_optimization_enabled": False,
        "portfolio_allocation_output_enabled": False,
        "deployment_allowed": False,
        "network_used": False,
        "external_benchmark_fetch_used": False,
        "paid_api_used": False,
        "scraping_used": False,
        "html_parsing_used": False,
        "dashboard_started": False,
        "daemon_started": False,
        "scheduler_enabled": False,
        "benchmark_comparison_executed": False,
        "monte_carlo_executed": False,
        "produces_live_signal": False,
        "produces_order_decision": False,
        "produces_portfolio_weights": False,
    }


def _extract_ingestion_flags(
    payload: Dict[str, Any], ctx: Dict[str, Any]
) -> Dict[str, bool]:
    return {
        "backtest_analytics_ingested": ctx.get("backtest_analytics_ingested", False),
        "inputs_resolved": ctx.get("inputs_resolved", False),
        "benchmark_universe_contract_built": ctx.get(
            "benchmark_universe_contract_built", False
        ),
        "passive_benchmark_config_built": ctx.get(
            "passive_benchmark_config_built", False
        ),
        "cash_benchmark_built": ctx.get("cash_benchmark_built", False),
        "buy_and_hold_benchmark_built": ctx.get("buy_and_hold_benchmark_built", False),
        "equal_weight_metadata_benchmark_built": ctx.get(
            "equal_weight_metadata_benchmark_built", False
        ),
        "market_index_reference_benchmark_built": ctx.get(
            "market_index_reference_benchmark_built", False
        ),
        "benchmark_return_series_built": ctx.get(
            "benchmark_return_series_built", False
        ),
        "strategy_benchmark_alignment_built": ctx.get(
            "strategy_benchmark_alignment_built", False
        ),
        "relative_performance_metrics_built": ctx.get(
            "relative_performance_metrics_built", False
        ),
        "benchmark_diagnostics_built": ctx.get("benchmark_diagnostics_built", False),
        "baseline_comparison_report_built": payload.get("baseline_comparison_report")
        is not None,
        "relative_performance_validation_built": payload.get(
            "relative_performance_validation"
        )
        is not None,
        "safety_boundary_validated": payload.get("safety_boundary", {}).get(
            "boundary_passed", False
        ),
        "research_data_only": payload.get("research_data_only", True),
        "offline_backtest_research_only": payload.get(
            "offline_backtest_research_only", True
        ),
        "deterministic": payload.get("deterministic", True),
        "paper_trading_enabled": payload.get("paper_trading_enabled", False)
        or ctx.get("paper_trading_enabled", False),
        "broker_execution_enabled": payload.get("broker_execution_enabled", False)
        or ctx.get("broker_execution_enabled", False),
        "real_order_creation_enabled": payload.get("real_order_creation_enabled", False)
        or ctx.get("real_order_creation_enabled", False),
        "paper_state_mutation_enabled": payload.get(
            "paper_state_mutation_enabled", False
        )
        or ctx.get("paper_state_mutation_enabled", False),
        "telegram_real_send_enabled": payload.get("telegram_real_send_enabled", False)
        or ctx.get("telegram_real_send_enabled", False),
        "strategy_activation_allowed": payload.get("strategy_activation_allowed", False)
        or ctx.get("strategy_activation_allowed", False),
        "portfolio_optimization_enabled": payload.get(
            "portfolio_optimization_enabled", False
        )
        or ctx.get("portfolio_optimization_enabled", False),
        "portfolio_allocation_output_enabled": payload.get(
            "portfolio_allocation_output_enabled", False
        )
        or ctx.get("portfolio_allocation_output_enabled", False),
        "deployment_allowed": payload.get("deployment_allowed", False)
        or ctx.get("deployment_allowed", False),
        "network_used": payload.get("network_used", False)
        or ctx.get("network_used", False),
        "external_benchmark_fetch_used": payload.get(
            "external_benchmark_fetch_used", False
        )
        or ctx.get("external_benchmark_fetch_used", False),
        "paid_api_used": payload.get("paid_api_used", False)
        or ctx.get("paid_api_used", False),
        "scraping_used": payload.get("scraping_used", False)
        or ctx.get("scraping_used", False),
        "html_parsing_used": payload.get("html_parsing_used", False)
        or ctx.get("html_parsing_used", False),
        "dashboard_started": payload.get("dashboard_started", False)
        or ctx.get("dashboard_started", False),
        "daemon_started": payload.get("daemon_started", False)
        or ctx.get("daemon_started", False),
        "scheduler_enabled": payload.get("scheduler_enabled", False)
        or ctx.get("scheduler_enabled", False),
        "benchmark_comparison_executed": payload.get(
            "benchmark_comparison_executed", False
        )
        or ctx.get("benchmark_comparison_executed", False),
        "monte_carlo_executed": payload.get("monte_carlo_executed", False)
        or ctx.get("monte_carlo_executed", False),
        "produces_live_signal": payload.get("produces_live_signal", False)
        or ctx.get("produces_live_signal", False),
        "produces_order_decision": payload.get("produces_order_decision", False)
        or ctx.get("produces_order_decision", False),
        "produces_portfolio_weights": payload.get("produces_portfolio_weights", False)
        or ctx.get("produces_portfolio_weights", False),
    }


def ingest_benchmark_comparison_review_payload(
    payload: Dict[str, Any],
) -> BenchmarkComparisonIngestionResult:
    ingestion_id = create_benchmark_comparison_ingestion_id()
    created_at = _now_utc()

    if not payload:
        flags = _extract_empty_flags()
        return BenchmarkComparisonIngestionResult(
            ingestion_id=ingestion_id,
            created_at_utc=created_at,
            source_path=None,
            source_review_id=None,
            source_context_id=None,
            available=False,
            phase150_readiness_gate_built=False,
            phase150_readiness_gate_passed=False,
            ready_for_phase150=False,
            live_trading_enabled=False,
            walk_forward_executed=False,
            stress_test_executed=False,
            investment_advice=False,
            valid_for_phase150=False,
            risk_flags=[WalkForwardRiskFlag.BENCHMARK_COMPARISON_REVIEW_MISSING],
            errors=["Payload is empty"],
            **flags,
        )

    ctx = extract_benchmark_comparison_context(payload)
    if not ctx:
        flags = _extract_empty_flags()
        return BenchmarkComparisonIngestionResult(
            ingestion_id=ingestion_id,
            created_at_utc=created_at,
            source_path=payload.get("source_path"),
            source_review_id=payload.get("review_id"),
            source_context_id=None,
            available=True,
            phase150_readiness_gate_built=False,
            phase150_readiness_gate_passed=False,
            ready_for_phase150=False,
            live_trading_enabled=False,
            walk_forward_executed=False,
            stress_test_executed=False,
            investment_advice=False,
            valid_for_phase150=False,
            risk_flags=[WalkForwardRiskFlag.BENCHMARK_COMPARISON_REVIEW_INVALID],
            errors=["Context is missing from payload"],
            **flags,
        )

    gate = extract_phase150_readiness_gate(payload)
    gate_passed = gate.get("ready_for_phase150", False) if gate else False

    valid, errors = benchmark_comparison_supports_phase150(payload)

    # Specific safety checks
    live_trading = payload.get("live_trading_enabled", False) or ctx.get(
        "live_trading_enabled", False
    )
    investment_advice = payload.get("investment_advice", False) or ctx.get(
        "investment_advice", False
    )
    stress_test = payload.get("stress_test_executed", False) or ctx.get(
        "stress_test_executed", False
    )
    walk_forward = payload.get("walk_forward_executed", False) or ctx.get(
        "walk_forward_executed", False
    )

    if walk_forward:
        valid = False
        errors.append(
            "Phase 149 output indicates walk_forward_executed=True, which is forbidden before Phase 150."
        )

    risk_flags = []
    if not valid:
        risk_flags.append(WalkForwardRiskFlag.PHASE149_NOT_READY)

    if live_trading:
        risk_flags.append(WalkForwardRiskFlag.LIVE_TRADING_RISK)
        valid = False

    if investment_advice:
        risk_flags.append(WalkForwardRiskFlag.INVESTMENT_ADVICE_LANGUAGE_RISK)
        valid = False

    flags = _extract_ingestion_flags(payload, ctx)
    return BenchmarkComparisonIngestionResult(
        ingestion_id=ingestion_id,
        created_at_utc=created_at,
        source_path=payload.get("source_path"),
        source_review_id=payload.get("review_id"),
        source_context_id=ctx.get("context_id"),
        available=True,
        phase150_readiness_gate_built=gate is not None,
        phase150_readiness_gate_passed=gate_passed,
        ready_for_phase150=valid,
        live_trading_enabled=live_trading,
        walk_forward_executed=walk_forward,
        stress_test_executed=stress_test,
        investment_advice=investment_advice,
        valid_for_phase150=valid,
        risk_flags=risk_flags,
        errors=errors,
        **flags,
    )


def ingest_latest_benchmark_comparison_review_from_store(
    data_root: Path,
) -> BenchmarkComparisonIngestionResult:
    reviews_dir = data_root / "backtesting" / "benchmark_comparison" / "reviews"
    if not reviews_dir.exists():
        return ingest_benchmark_comparison_review_payload({})

    files = list(reviews_dir.glob("*.json"))
    if not files:
        return ingest_benchmark_comparison_review_payload({})

    latest_file = max(files, key=lambda f: f.stat().st_mtime)
    with open(latest_file, "r") as f:
        payload = json.load(f)

    payload["source_path"] = str(latest_file)
    return ingest_benchmark_comparison_review_payload(payload)


def benchmark_comparison_ingestion_to_text(
    result: BenchmarkComparisonIngestionResult,
) -> str:
    lines = [
        f"BenchmarkComparisonIngestionResult:",
        f"  ID: {result.ingestion_id}",
        f"  Valid for Phase 150: {result.valid_for_phase150}",
        f"  Ready for Phase 150: {result.ready_for_phase150}",
        f"  Errors: {len(result.errors)}",
    ]
    if result.errors:
        lines.append(f"  First Error: {result.errors[0]}")
    return "\n".join(lines)
