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

    gate = extract_phase153_readiness_gate(payload)
    gate_ready = gate.get("ready_for_phase153", False) if gate else False

    if not payload.get("ready_for_phase153", False) and not gate_ready:
        errors.append("Not ready for Phase 153")

    if not gate_ready:
        errors.append("Phase 153 readiness gate is false or missing")

    safety = extract_handoff_safety_boundary(payload)
    if not safety or not safety.get("boundary_passed", False):
        errors.append("Handoff safety boundary passed is false or missing")

    context = payload.get("context")

    required_built = [
        ("phase153_handoff_contract_built", "Phase 153 handoff contract built is false or missing"),
        ("phase153_handoff_package_built", "Phase 153 handoff package built is false or missing")
    ]
    for field, msg in required_built:
        if not payload.get(field, False) and not (context and context.get(field)):
            errors.append(msg)

    if not payload.get("research_data_only", True) and not (context and context.get("research_data_only", True)):
        errors.append("Research data only must be true")

    forbidden_groups = [
        (
            [
                "portfolio_construction_executed", "position_sizing_executed",
                "target_weights_produced", "allocation_output_produced"
            ],
            "Actual portfolio construction or sizing fields are set to true"
        ),
        (
            [
                "live_trading_enabled", "paper_trading_enabled", "broker_execution_enabled",
                "real_order_creation_enabled", "paper_state_mutation_enabled",
                "telegram_real_send_enabled", "deployment_allowed", "network_used",
                "dashboard_started", "daemon_started", "scheduler_enabled"
            ],
            "Live trading or similar dangerous fields are set to true"
        ),
        (
            [
                "produces_live_signal", "produces_order_decision", "produces_portfolio_weights"
            ],
            "Signal producing fields are set to true"
        ),
        (
            ["investment_advice"],
            "Investment advice is set to true"
        )
    ]

    for fields, msg in forbidden_groups:
        if any(payload.get(f, False) for f in fields):
            errors.append(msg)

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
