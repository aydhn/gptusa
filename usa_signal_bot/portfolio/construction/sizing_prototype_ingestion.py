import json
from pathlib import Path
from typing import Any, Dict, List, Tuple
from datetime import datetime, timezone
import logging

from usa_signal_bot.portfolio.construction.phase155_models import (
    SizingPrototypeIngestionResult,
    create_sizing_prototype_ingestion_id,
    _now_str
)
from usa_signal_bot.core.enums import PortfolioConstructionRiskFlag

logger = logging.getLogger(__name__)

def ingest_sizing_prototype_review_payload(payload: Dict[str, Any], source_path: str | None = None) -> SizingPrototypeIngestionResult:
    is_valid, block_reasons = sizing_prototype_supports_phase155(payload)

    risk_flags = []
    if not payload:
        risk_flags.append(PortfolioConstructionRiskFlag.SIZING_PROTOTYPE_REVIEW_MISSING)
    if not is_valid:
        risk_flags.append(PortfolioConstructionRiskFlag.SIZING_PROTOTYPE_REVIEW_INVALID)

    ingestion = SizingPrototypeIngestionResult(
        ingestion_id=create_sizing_prototype_ingestion_id(),
        created_at_utc=_now_str(),
        source_path=source_path,
        source_review_id=payload.get("review_id"),
        source_context_id=payload.get("context", {}).get("context_id"),
        available=bool(payload),
        portfolio_foundation_ingested=payload.get("context", {}).get("portfolio_foundation_ingested", False),
        inputs_resolved=payload.get("context", {}).get("inputs_resolved", False),
        sizing_policy_built=payload.get("context", {}).get("sizing_policy_built", False),
        method_contracts_built=payload.get("context", {}).get("method_contracts_built", False),
        fixed_fractional_sizing_built=payload.get("context", {}).get("fixed_fractional_sizing_built", False),
        volatility_adjusted_sizing_built=payload.get("context", {}).get("volatility_adjusted_sizing_built", False),
        drawdown_adjusted_sizing_built=payload.get("context", {}).get("drawdown_adjusted_sizing_built", False),
        cost_aware_sizing_built=payload.get("context", {}).get("cost_aware_sizing_built", False),
        liquidity_aware_sizing_built=payload.get("context", {}).get("liquidity_aware_sizing_built", False),
        robustness_adjusted_sizing_built=payload.get("context", {}).get("robustness_adjusted_sizing_built", False),
        comparison_matrix_built=payload.get("context", {}).get("comparison_matrix_built", False),
        sizing_diagnostics_built=payload.get("context", {}).get("sizing_diagnostics_built", False),
        sensitivity_report_built=payload.get("context", {}).get("sensitivity_report_built", False),
        risk_budget_adherence_built=payload.get("context", {}).get("risk_budget_adherence_built", False),
        safety_boundary_validated=payload.get("context", {}).get("safety_boundary_validated", False),
        phase155_readiness_gate_built=payload.get("phase155_readiness_gate", {}).get("ready_for_phase155") is not None,
        phase155_readiness_gate_passed=payload.get("phase155_readiness_gate", {}).get("ready_for_phase155", False),
        ready_for_phase155=payload.get("phase155_readiness_gate", {}).get("ready_for_phase155", False),
        research_data_only=payload.get("context", {}).get("research_data_only", True),
        sizing_research_prototype_only=payload.get("context", {}).get("sizing_research_prototype_only", True),
        deterministic=payload.get("context", {}).get("deterministic", True),
        live_trading_enabled=payload.get("context", {}).get("live_trading_enabled", False),
        paper_trading_enabled=payload.get("context", {}).get("paper_trading_enabled", False),
        broker_execution_enabled=payload.get("context", {}).get("broker_execution_enabled", False),
        real_order_creation_enabled=payload.get("context", {}).get("real_order_creation_enabled", False),
        paper_state_mutation_enabled=payload.get("context", {}).get("paper_state_mutation_enabled", False),
        telegram_real_send_enabled=payload.get("context", {}).get("telegram_real_send_enabled", False),
        strategy_activation_allowed=payload.get("context", {}).get("strategy_activation_allowed", False),
        actual_portfolio_construction_executed=payload.get("context", {}).get("actual_portfolio_construction_executed", False),
        actual_position_sizing_executed=payload.get("context", {}).get("actual_position_sizing_executed", False),
        portfolio_optimization_enabled=payload.get("context", {}).get("portfolio_optimization_enabled", False),
        rebalancing_enabled=payload.get("context", {}).get("rebalancing_enabled", False),
        target_weights_produced=payload.get("context", {}).get("target_weights_produced", False),
        allocation_output_produced=payload.get("context", {}).get("allocation_output_produced", False),
        order_size_produced=payload.get("context", {}).get("order_size_produced", False),
        capital_deployment_allowed=payload.get("context", {}).get("capital_deployment_allowed", False),
        deployment_allowed=payload.get("context", {}).get("deployment_allowed", False),
        network_used=payload.get("context", {}).get("network_used", False),
        paid_api_used=payload.get("context", {}).get("paid_api_used", False),
        scraping_used=payload.get("context", {}).get("scraping_used", False),
        html_parsing_used=payload.get("context", {}).get("html_parsing_used", False),
        dashboard_started=payload.get("context", {}).get("dashboard_started", False),
        daemon_started=payload.get("context", {}).get("daemon_started", False),
        scheduler_enabled=payload.get("context", {}).get("scheduler_enabled", False),
        produces_live_signal=payload.get("context", {}).get("produces_live_signal", False),
        produces_order_decision=payload.get("context", {}).get("produces_order_decision", False),
        produces_portfolio_weights=payload.get("context", {}).get("produces_portfolio_weights", False),
        investment_advice=payload.get("context", {}).get("investment_advice", False),
        valid_for_phase155=is_valid,
        risk_flags=risk_flags,
        warnings=[],
        errors=block_reasons,
        metadata={"source": "phase154_sizing_prototype_review"}
    )
    return ingestion

def ingest_latest_sizing_prototype_review_from_store(data_root: Path) -> SizingPrototypeIngestionResult:
    store_dir = data_root / "portfolio" / "sizing" / "reviews"
    if not store_dir.exists():
        return ingest_sizing_prototype_review_payload({})

    try:
        files = list(store_dir.glob("*.json"))
        if not files:
            return ingest_sizing_prototype_review_payload({})

        latest_file = max(files, key=lambda p: p.stat().st_mtime)
        with open(latest_file, "r") as f:
            payload = json.load(f)
            return ingest_sizing_prototype_review_payload(payload, source_path=str(latest_file))
    except Exception as e:
        logger.error(f"Failed to ingest sizing prototype review: {e}")
        return ingest_sizing_prototype_review_payload({})

def extract_sizing_policy(payload: Dict[str, Any]) -> Dict[str, Any] | None:
    return payload.get("policy")

def extract_sizing_method_contracts(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("context", {}).get("method_contracts", [])

def extract_sizing_comparison_matrix(payload: Dict[str, Any]) -> Dict[str, Any] | None:
    return payload.get("comparison_matrix")

def extract_sizing_sensitivity_report(payload: Dict[str, Any]) -> Dict[str, Any] | None:
    return payload.get("context", {}).get("sensitivity_report")

def extract_risk_budget_adherence_report(payload: Dict[str, Any]) -> Dict[str, Any] | None:
    return payload.get("risk_budget_adherence")

def extract_sizing_safety_boundary(payload: Dict[str, Any]) -> Dict[str, Any] | None:
    return payload.get("safety_boundary")

def extract_phase155_readiness_gate(payload: Dict[str, Any]) -> Dict[str, Any] | None:
    return payload.get("phase155_readiness_gate")

def sizing_prototype_supports_phase155(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if not payload:
        return False, ["Payload is empty."]

    gate = payload.get("phase155_readiness_gate", {})
    ctx = payload.get("context", {})

    checks = [
        (not gate.get("ready_for_phase155", False), "ready_for_phase155 is False or missing."),
        (not ctx.get("safety_boundary_validated", False), "safety_boundary_validated is False."),
        (not ctx.get("comparison_matrix_built", False), "comparison_matrix_built is False."),
        (not ctx.get("risk_budget_adherence_built", False), "risk_budget_adherence_built is False."),
        (not ctx.get("research_data_only", True), "research_data_only is False."),
        (not ctx.get("sizing_research_prototype_only", True), "sizing_research_prototype_only is False."),
        (ctx.get("actual_target_weights_produced", False) or ctx.get("target_weights_produced", False), "actual_target_weights_produced is True."),
        (ctx.get("actual_allocation_produced", False) or ctx.get("allocation_output_produced", False), "actual_allocation_produced is True."),
        (ctx.get("order_size_produced", False), "order_size_produced is True."),
        (ctx.get("capital_deployment_allowed", False), "capital_deployment_allowed is True.")
    ]

    unsafe_flags = [
        "live_trading_enabled", "paper_trading_enabled", "broker_execution_enabled",
        "real_order_creation_enabled", "paper_state_mutation_enabled", "telegram_real_send_enabled",
        "deployment_allowed", "network_used", "dashboard_started", "daemon_started", "scheduler_enabled",
        "produces_live_signal", "produces_order_decision", "produces_portfolio_weights", "investment_advice"
    ]

    checks.extend([(ctx.get(flag, False), f"{flag} is True.") for flag in unsafe_flags])

    block_reasons = [msg for condition, msg in checks if condition]

    return len(block_reasons) == 0, block_reasons

def sizing_prototype_ingestion_to_text(result: SizingPrototypeIngestionResult) -> str:
    lines = [
        f"Sizing Prototype Ingestion: {result.ingestion_id}",
        f"Valid for Phase 155: {result.valid_for_phase155}",
        f"Ready for Phase 155: {result.ready_for_phase155}",
        f"Research Data Only: {result.research_data_only}",
        f"Sizing Research Prototype Only: {result.sizing_research_prototype_only}"
    ]
    if result.errors:
        lines.append("\nErrors blocking Phase 155 ingestion:")
        for err in result.errors:
            lines.append(f"- {err}")
    return "\n".join(lines)
