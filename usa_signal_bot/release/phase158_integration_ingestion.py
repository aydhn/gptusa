from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
import json

from usa_signal_bot.release.phase159_models import (
    Phase158IntegrationIngestionResult,
    create_phase158_integration_ingestion_id,
    generate_timestamp,
    AdvancedAcceptanceRiskFlag
)

def extract_phase159_readiness_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("phase159_readiness_gate")

def extract_integration_safety_boundary(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("integration_safety_boundary")

def extract_final_delivery_preparation_checklist(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("final_delivery_preparation_checklist")

def phase158_integration_supports_phase159(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    supported = True

    if not payload.get("ready_for_phase159", False):
        supported = False
        warnings.append("ready_for_phase159 is False")

    if not payload.get("research_data_only", False):
        supported = False
        warnings.append("research_data_only is False")

    if not payload.get("integration_only", False):
        supported = False
        warnings.append("integration_only is False")

    if not payload.get("dry_run_only", False):
        supported = False
        warnings.append("dry_run_only is False")

    if payload.get("live_trading_enabled", True):
        supported = False
        warnings.append("live_trading_enabled is True")

    return supported, warnings

def ingest_full_system_integration_review_payload(payload: Dict[str, Any]) -> Phase158IntegrationIngestionResult:
    supported, warnings = phase158_integration_supports_phase159(payload)

    risk_flags = []
    if not supported:
        risk_flags.append(AdvancedAcceptanceRiskFlag.PHASE158_REVIEW_INVALID)

    # check for execution features
    if payload.get("live_trading_enabled"):
        risk_flags.append(AdvancedAcceptanceRiskFlag.LIVE_TRADING_RISK)
    if payload.get("paper_trading_enabled"):
        risk_flags.append(AdvancedAcceptanceRiskFlag.PAPER_TRADING_RISK)
    if payload.get("broker_execution_enabled"):
        risk_flags.append(AdvancedAcceptanceRiskFlag.BROKER_RISK)

    gate = extract_phase159_readiness_gate(payload)
    boundary = extract_integration_safety_boundary(payload)
    checklist = extract_final_delivery_preparation_checklist(payload)

    return Phase158IntegrationIngestionResult(
        ingestion_id=create_phase158_integration_ingestion_id(),
        created_at_utc=generate_timestamp(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=payload.get("context_id"),
        available=True,
        phase158_handoff_ingested=True,
        artifact_inventory_built=bool(payload.get("system_artifact_inventory")),
        dependency_graph_built=bool(payload.get("integration_dependency_graph")),
        boundary_contract_built=bool(payload.get("integration_boundary_contract")),
        e2e_rehearsal_plan_built=bool(payload.get("e2e_rehearsal_plan")),
        dry_run_rehearsal_executed=payload.get("e2e_dry_run_rehearsal_executed", False),
        acceptance_result_built=bool(payload.get("integration_acceptance_result")),
        schema_compatibility_report_built=bool(payload.get("schema_compatibility_report")),
        cli_integration_report_built=bool(payload.get("cli_integration_report")),
        config_integration_report_built=bool(payload.get("config_integration_report")),
        storage_integration_report_built=bool(payload.get("storage_integration_report")),
        health_integration_report_built=bool(payload.get("health_integration_report")),
        quality_observability_report_built=bool(payload.get("quality_observability_integration_report")),
        notification_dry_run_report_built=bool(payload.get("notification_dry_run_report")),
        safety_boundary_validated=bool(boundary and boundary.get("boundary_passed")),
        final_delivery_checklist_built=bool(checklist),
        phase159_readiness_gate_built=bool(gate),
        phase159_readiness_gate_passed=bool(gate and gate.get("ready_for_phase159")),
        ready_for_phase159=supported,
        research_data_only=payload.get("research_data_only", False),
        integration_only=payload.get("integration_only", False),
        dry_run_only=payload.get("dry_run_only", False),
        deterministic=payload.get("deterministic", False),
        live_trading_enabled=payload.get("live_trading_enabled", False),
        paper_trading_enabled=payload.get("paper_trading_enabled", False),
        paper_state_mutation_enabled=payload.get("paper_state_mutation_enabled", False),
        broker_execution_enabled=payload.get("broker_execution_enabled", False),
        real_order_creation_enabled=payload.get("real_order_creation_enabled", False),
        telegram_real_send_enabled=payload.get("telegram_real_send_enabled", False),
        strategy_activation_allowed=payload.get("strategy_activation_allowed", False),
        deployment_allowed=payload.get("deployment_allowed", False),
        production_patch_allowed=payload.get("production_patch_allowed", False),
        network_used=payload.get("network_used", False),
        paid_api_used=payload.get("paid_api_used", False),
        scraping_used=payload.get("scraping_used", False),
        html_parsing_used=payload.get("html_parsing_used", False),
        dashboard_started=payload.get("dashboard_started", False),
        daemon_started=payload.get("daemon_started", False),
        scheduler_enabled=payload.get("scheduler_enabled", False),
        actual_target_weights_produced=payload.get("actual_target_weights_produced", False),
        actual_allocation_produced=payload.get("actual_allocation_produced", False),
        order_size_produced=payload.get("order_size_produced", False),
        capital_deployment_allowed=payload.get("capital_deployment_allowed", False),
        investment_advice=payload.get("investment_advice", False),
        valid_for_phase159=supported,
        risk_flags=risk_flags,
        warnings=warnings,
        errors=[],
        metadata={"original_payload_keys": list(payload.keys())}
    )

def ingest_latest_full_system_integration_review_from_store(data_root: Path) -> Phase158IntegrationIngestionResult:
    # Simulating loading from Phase 158 folder (not strictly implemented yet for Phase158, so mock a fallback)
    p = data_root / "release" / "phase158" / "reviews"
    if not p.exists():
        return ingest_full_system_integration_review_payload({})

    # Try to find latest json
    files = sorted(p.glob("*.json"))
    if not files:
        return ingest_full_system_integration_review_payload({})

    latest_file = files[-1]
    with open(latest_file, "r") as f:
        payload = json.load(f)

    res = ingest_full_system_integration_review_payload(payload)
    res.source_path = str(latest_file)
    return res

def phase158_integration_ingestion_to_text(result: Phase158IntegrationIngestionResult) -> str:
    lines = [
        f"Phase 158 Ingestion: {result.ingestion_id}",
        f"Valid for Phase 159: {result.valid_for_phase159}",
        f"Ready for Phase 159: {result.ready_for_phase159}"
    ]
    if result.warnings:
        lines.append("Warnings:")
        for w in result.warnings:
            lines.append(f" - {w}")
    return "\n".join(lines)
