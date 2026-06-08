import json
from pathlib import Path
from typing import Any

from usa_signal_bot.portfolio.foundation.phase153_models import (
    BacktestClosureIngestionResult,
    create_backtest_closure_ingestion_id
)

def extract_phase153_handoff_package(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("handoff_package")

def extract_phase153_handoff_contract(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("handoff_contract")

def extract_handoff_safety_boundary(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("handoff_safety_boundary")

def extract_phase153_readiness_gate(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("phase153_readiness_gate")

def backtest_closure_supports_phase153(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []

    if not payload.get("ready_for_phase153", False):
        gate = extract_phase153_readiness_gate(payload)
        if gate and gate.get("ready_for_phase153", False):
            pass # Gate is OK but top level isn't? We'll rely on the gate if we have to, but top level is safer
        else:
            errors.append("Not ready for Phase 153")

    gate = extract_phase153_readiness_gate(payload)
    if not gate or not gate.get("ready_for_phase153", False):
        errors.append("Phase 153 readiness gate is false or missing")

    safety = extract_handoff_safety_boundary(payload)
    if not safety or not safety.get("boundary_passed", False):
        errors.append("Handoff safety boundary passed is false or missing")

    if not payload.get("phase153_handoff_contract_built", False) and not (payload.get("context") and payload.get("context").get("phase153_handoff_contract_built")):
        errors.append("Phase 153 handoff contract built is false or missing")

    if not payload.get("phase153_handoff_package_built", False) and not (payload.get("context") and payload.get("context").get("phase153_handoff_package_built")):
        errors.append("Phase 153 handoff package built is false or missing")

    if not payload.get("research_data_only", True) and not (payload.get("context") and payload.get("context").get("research_data_only", True)):
        errors.append("Research data only must be true")

    if payload.get("portfolio_construction_executed", False) or payload.get("position_sizing_executed", False) or payload.get("target_weights_produced", False) or payload.get("allocation_output_produced", False):
        errors.append("Actual portfolio construction or sizing fields are set to true")

    if payload.get("live_trading_enabled", False) or payload.get("paper_trading_enabled", False) or payload.get("broker_execution_enabled", False) or payload.get("real_order_creation_enabled", False) or payload.get("paper_state_mutation_enabled", False) or payload.get("telegram_real_send_enabled", False) or payload.get("deployment_allowed", False) or payload.get("network_used", False) or payload.get("dashboard_started", False) or payload.get("daemon_started", False) or payload.get("scheduler_enabled", False):
        errors.append("Live trading or similar dangerous fields are set to true")

    if payload.get("produces_live_signal", False) or payload.get("produces_order_decision", False) or payload.get("produces_portfolio_weights", False):
        errors.append("Signal producing fields are set to true")

    if payload.get("investment_advice", False):
        errors.append("Investment advice is set to true")

    return len(errors) == 0, errors

def ingest_backtest_closure_review_payload(payload: dict[str, Any]) -> BacktestClosureIngestionResult:
    res = BacktestClosureIngestionResult()
    res.source_review_id = payload.get("review_id")
    res.available = True

    context = payload.get("context", {})

    res.final_audit_report_built = payload.get("final_audit_report_built", context.get("final_audit_report_built", False))
    res.band_closure_certificate_built = payload.get("band_closure_certificate_built", context.get("band_closure_certificate_built", False))
    res.phase153_handoff_contract_built = payload.get("phase153_handoff_contract_built", context.get("phase153_handoff_contract_built", False))
    res.phase153_handoff_package_built = payload.get("phase153_handoff_package_built", context.get("phase153_handoff_package_built", False))
    res.handoff_safety_boundary_validated = payload.get("handoff_safety_boundary_validated", context.get("handoff_safety_boundary_validated", False))
    res.phase153_readiness_gate_built = payload.get("phase153_readiness_gate_built", context.get("phase153_readiness_gate_built", False))
    res.phase153_readiness_gate_passed = payload.get("phase153_readiness_gate_passed", context.get("phase153_readiness_gate_passed", False))
    res.ready_for_phase153 = payload.get("ready_for_phase153", context.get("ready_for_phase153", False))

    res.research_data_only = payload.get("research_data_only", context.get("research_data_only", True))
    res.offline_backtest_research_only = payload.get("offline_backtest_research_only", context.get("offline_backtest_research_only", True))
    res.deterministic = payload.get("deterministic", context.get("deterministic", True))

    res.live_trading_enabled = payload.get("live_trading_enabled", context.get("live_trading_enabled", False))
    res.paper_trading_enabled = payload.get("paper_trading_enabled", context.get("paper_trading_enabled", False))
    res.broker_execution_enabled = payload.get("broker_execution_enabled", context.get("broker_execution_enabled", False))
    res.real_order_creation_enabled = payload.get("real_order_creation_enabled", context.get("real_order_creation_enabled", False))
    res.paper_state_mutation_enabled = payload.get("paper_state_mutation_enabled", context.get("paper_state_mutation_enabled", False))
    res.telegram_real_send_enabled = payload.get("telegram_real_send_enabled", context.get("telegram_real_send_enabled", False))
    res.strategy_activation_allowed = payload.get("strategy_activation_allowed", context.get("strategy_activation_allowed", False))
    res.portfolio_construction_executed = payload.get("portfolio_construction_executed", context.get("portfolio_construction_executed", False))
    res.position_sizing_executed = payload.get("position_sizing_executed", context.get("position_sizing_executed", False))
    res.portfolio_optimization_enabled = payload.get("portfolio_optimization_enabled", context.get("portfolio_optimization_enabled", False))
    res.portfolio_allocation_output_enabled = payload.get("portfolio_allocation_output_enabled", context.get("portfolio_allocation_output_enabled", False))
    res.target_weights_produced = payload.get("target_weights_produced", context.get("target_weights_produced", False))
    res.deployment_allowed = payload.get("deployment_allowed", context.get("deployment_allowed", False))
    res.network_used = payload.get("network_used", context.get("network_used", False))
    res.paid_api_used = payload.get("paid_api_used", context.get("paid_api_used", False))
    res.scraping_used = payload.get("scraping_used", context.get("scraping_used", False))
    res.html_parsing_used = payload.get("html_parsing_used", context.get("html_parsing_used", False))
    res.dashboard_started = payload.get("dashboard_started", context.get("dashboard_started", False))
    res.daemon_started = payload.get("daemon_started", context.get("daemon_started", False))
    res.scheduler_enabled = payload.get("scheduler_enabled", context.get("scheduler_enabled", False))
    res.produces_live_signal = payload.get("produces_live_signal", context.get("produces_live_signal", False))
    res.produces_order_decision = payload.get("produces_order_decision", context.get("produces_order_decision", False))
    res.produces_portfolio_weights = payload.get("produces_portfolio_weights", context.get("produces_portfolio_weights", False))
    res.investment_advice = payload.get("investment_advice", context.get("investment_advice", False))

    valid, errors = backtest_closure_supports_phase153(payload)
    res.valid_for_phase153 = valid
    res.errors.extend(errors)

    if not payload.get("review_id"):
        res.valid_for_phase153 = False
        res.errors.append("Review ID missing")

    return res

def ingest_latest_backtest_closure_review_from_store(data_root: Path) -> BacktestClosureIngestionResult:
    # Simulating the path for phase 152 reviews
    reviews_dir = data_root / "backtesting" / "closure" / "reviews"
    if not reviews_dir.exists():
        res = BacktestClosureIngestionResult()
        res.errors.append(f"Directory {reviews_dir} does not exist")
        return res

    files = sorted([f for f in reviews_dir.iterdir() if f.suffix == ".json"], key=lambda x: x.stat().st_mtime, reverse=True)
    if not files:
        res = BacktestClosureIngestionResult()
        res.errors.append(f"No review files found in {reviews_dir}")
        return res

    try:
        with open(files[0], "r") as f:
            payload = json.load(f)
        res = ingest_backtest_closure_review_payload(payload)
        res.source_path = str(files[0])
        return res
    except Exception as e:
        res = BacktestClosureIngestionResult()
        res.errors.append(str(e))
        return res

def backtest_closure_ingestion_to_text(result: BacktestClosureIngestionResult) -> str:
    lines = [
        f"Ingestion ID: {result.ingestion_id}",
        f"Available: {result.available}",
        f"Valid for Phase 153: {result.valid_for_phase153}",
        f"Source: {result.source_path}",
    ]
    if result.errors:
        lines.append("Errors:")
        for e in result.errors:
            lines.append(f" - {e}")
    return "\n".join(lines)
