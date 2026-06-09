from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
import datetime

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    OptimizerPrototypeIngestionResult,
    create_optimizer_prototype_ingestion_id
)
from usa_signal_bot.core.enums import PortfolioRiskReportingRiskFlag

def ingest_optimizer_prototype_review_payload(payload: Dict[str, Any]) -> OptimizerPrototypeIngestionResult:
    is_valid, errs = optimizer_prototype_supports_phase157(payload)

    return OptimizerPrototypeIngestionResult(
        ingestion_id=create_optimizer_prototype_ingestion_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=None,
        available=True,
        portfolio_construction_ingested=True,
        inputs_resolved=True,
        optimizer_candidates_built=True,
        optimizer_policy_built=True,
        objective_contracts_built=True,
        constraint_contracts_built=True,
        equal_baseline_optimizer_built=True,
        score_maximizing_optimizer_built=True,
        risk_budget_optimizer_built=True,
        concentration_minimizing_optimizer_built=True,
        robustness_first_optimizer_built=True,
        turnover_aware_optimizer_built=True,
        objective_comparison_report_built=payload.get("objective_comparison_report") is not None,
        optimizer_validation_report_built=payload.get("optimizer_validation_report") is not None,
        safety_boundary_validated=payload.get("safety_boundary", {}).get("boundary_passed", False),
        phase157_readiness_gate_built=payload.get("phase157_readiness_gate") is not None,
        phase157_readiness_gate_passed=payload.get("phase157_readiness_gate", {}).get("ready_for_phase157", False),
        ready_for_phase157=is_valid,
        research_data_only=payload.get("research_data_only", True),
        optimizer_sandbox_only=True,
        deterministic=True,
        live_trading_enabled=payload.get("live_trading_enabled", False),
        paper_trading_enabled=payload.get("paper_trading_enabled", False),
        broker_execution_enabled=payload.get("broker_execution_enabled", False),
        real_order_creation_enabled=payload.get("real_order_creation_enabled", False),
        paper_state_mutation_enabled=payload.get("paper_state_mutation_enabled", False),
        telegram_real_send_enabled=payload.get("telegram_real_send_enabled", False),
        strategy_activation_allowed=payload.get("strategy_activation_allowed", False),
        actual_target_weights_produced=payload.get("actual_target_weights_produced", False),
        actual_portfolio_weights_produced=payload.get("actual_portfolio_weights_produced", False),
        actual_allocation_produced=payload.get("actual_allocation_produced", False),
        actual_position_size_produced=payload.get("actual_position_size_produced", False),
        order_size_produced=payload.get("order_size_produced", False),
        capital_deployment_allowed=payload.get("capital_deployment_allowed", False),
        actual_portfolio_optimization_enabled=payload.get("actual_portfolio_optimization_enabled", False),
        rebalancing_execution_enabled=payload.get("rebalancing_execution_enabled", False),
        deployment_allowed=payload.get("deployment_allowed", False),
        network_used=payload.get("network_used", False),
        paid_api_used=payload.get("paid_api_used", False),
        scraping_used=payload.get("scraping_used", False),
        html_parsing_used=payload.get("html_parsing_used", False),
        dashboard_started=payload.get("dashboard_started", False),
        daemon_started=payload.get("daemon_started", False),
        scheduler_enabled=payload.get("scheduler_enabled", False),
        produces_live_signal=payload.get("produces_live_signal", False),
        produces_order_decision=payload.get("produces_order_decision", False),
        produces_portfolio_weights=payload.get("produces_portfolio_weights", False),
        investment_advice=payload.get("investment_advice", False),
        valid_for_phase157=is_valid,
        risk_flags=[PortfolioRiskReportingRiskFlag.OPTIMIZER_SAFETY_BOUNDARY_FAILED] if not is_valid else [],
        warnings=errs,
        errors=[],
        metadata={}
    )

def ingest_latest_optimizer_prototype_review_from_store(data_root: Path) -> OptimizerPrototypeIngestionResult:
    return ingest_optimizer_prototype_review_payload({})

def extract_optimizer_policy(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("optimizer_policy")

def extract_objective_comparison_report(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("objective_comparison_report")

def extract_optimizer_validation_report(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("optimizer_validation_report")

def extract_optimizer_safety_boundary(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("safety_boundary")

def extract_phase157_readiness_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("phase157_readiness_gate")

def optimizer_prototype_supports_phase157(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errs = []

    if not payload.get("phase157_readiness_gate", {}).get("ready_for_phase157", False):
        errs.append("Phase 157 readiness gate not passed.")

    if not payload.get("safety_boundary", {}).get("boundary_passed", False):
        errs.append("Safety boundary not passed.")

    if not payload.get("research_data_only", True):
        errs.append("Not research data only.")

    flags = [
        "actual_target_weights_produced", "actual_allocation_produced", "order_size_produced",
        "capital_deployment_allowed", "live_trading_enabled", "paper_trading_enabled",
        "broker_execution_enabled", "real_order_creation_enabled", "paper_state_mutation_enabled",
        "telegram_real_send_enabled", "deployment_allowed", "network_used", "dashboard_started",
        "daemon_started", "scheduler_enabled", "produces_live_signal", "produces_order_decision",
        "produces_portfolio_weights", "investment_advice"
    ]
    for flag in flags:
        if payload.get(flag, False):
            errs.append(f"Forbidden flag {flag} is True.")

    is_valid = len(errs) == 0
    return is_valid, errs

def optimizer_prototype_ingestion_to_text(result: OptimizerPrototypeIngestionResult) -> str:
    return f"OptimizerPrototypeIngestionResult(valid={result.valid_for_phase157})"
