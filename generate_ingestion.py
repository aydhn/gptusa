content = """
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import json

from usa_signal_bot.integration.phase158_models import Phase158HandoffIngestionResult
from usa_signal_bot.core.enums import FullSystemIntegrationRiskFlag

def ingest_phase158_handoff_package_payload(payload: Dict[str, Any]) -> Phase158HandoffIngestionResult:
    result = Phase158HandoffIngestionResult()
    result.available = True

    if not payload:
        result.valid_for_phase158 = False
        result.risk_flags.append(FullSystemIntegrationRiskFlag.PHASE158_HANDOFF_INVALID)
        return result

    result.package_valid = payload.get("package_valid", False)
    result.closure_certificate_valid = payload.get("closure_certificate_valid", False)
    result.phase158_readiness_gate_passed = payload.get("phase158_readiness_gate_passed", False)
    result.ready_for_phase158 = payload.get("ready_for_phase158", False)

    # Read-only checks
    result.read_only = payload.get("read_only", True)
    result.research_data_only = payload.get("research_data_only", True)
    result.integration_handoff_only = payload.get("integration_handoff_only", True)

    # Execution checks (MUST be false)
    result.live_trading_enabled = payload.get("live_trading_enabled", False)
    result.paper_trading_enabled = payload.get("paper_trading_enabled", False)
    result.broker_execution_enabled = payload.get("broker_execution_enabled", False)
    result.real_order_creation_enabled = payload.get("real_order_creation_enabled", False)
    result.paper_state_mutation_enabled = payload.get("paper_state_mutation_enabled", False)
    result.telegram_real_send_enabled = payload.get("telegram_real_send_enabled", False)
    result.strategy_activation_allowed = payload.get("strategy_activation_allowed", False)
    result.actual_target_weights_produced = payload.get("actual_target_weights_produced", False)
    result.actual_allocation_produced = payload.get("actual_allocation_produced", False)
    result.actual_position_size_produced = payload.get("actual_position_size_produced", False)
    result.order_size_produced = payload.get("order_size_produced", False)
    result.capital_deployment_allowed = payload.get("capital_deployment_allowed", False)
    result.deployment_allowed = payload.get("deployment_allowed", False)
    result.network_used = payload.get("network_used", False)
    result.scraping_used = payload.get("scraping_used", False)
    result.html_parsing_used = payload.get("html_parsing_used", False)
    result.dashboard_started = payload.get("dashboard_started", False)
    result.daemon_started = payload.get("daemon_started", False)
    result.scheduler_enabled = payload.get("scheduler_enabled", False)
    result.investment_advice = payload.get("investment_advice", False)

    supports_integration, violations = phase158_handoff_supports_integration(payload)
    if not supports_integration:
        result.valid_for_phase158 = False
        result.errors.extend(violations)
        return result

    result.valid_for_phase158 = True
    return result

def ingest_latest_phase158_handoff_package_from_store(data_root: Path) -> Phase158HandoffIngestionResult:
    # Simulating fetching the latest package
    # In a real scenario, this would load the most recent file from the data path
    return Phase158HandoffIngestionResult(available=False)

def extract_portfolio_band_closure_certificate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("closure_certificate")

def extract_phase158_readiness_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("phase158_readiness_gate")

def phase158_handoff_supports_integration(payload: Dict[str, Any]) -> Tuple[bool, list[str]]:
    violations = []

    if not payload.get("package_valid", False):
        violations.append("package_valid=False")
    if not payload.get("closure_certificate_valid", False):
        violations.append("closure_certificate_valid=False")
    if not payload.get("phase158_readiness_gate_passed", False):
        violations.append("phase158_readiness_gate_passed=False")
    if not payload.get("ready_for_phase158", False):
        violations.append("ready_for_phase158=False")
    if not payload.get("read_only", True):
        violations.append("read_only=False")
    if not payload.get("research_data_only", True):
        violations.append("research_data_only=False")
    if not payload.get("integration_handoff_only", True):
        violations.append("integration_handoff_only=False")

    # Check execution flags
    execution_flags = [
        "live_trading_enabled", "paper_trading_enabled", "broker_execution_enabled",
        "real_order_creation_enabled", "paper_state_mutation_enabled",
        "telegram_real_send_enabled", "strategy_activation_allowed",
        "actual_target_weights_produced", "actual_allocation_produced",
        "actual_position_size_produced", "order_size_produced",
        "capital_deployment_allowed", "deployment_allowed", "network_used",
        "scraping_used", "html_parsing_used", "dashboard_started",
        "daemon_started", "scheduler_enabled", "investment_advice"
    ]

    for flag in execution_flags:
        if payload.get(flag, False):
            violations.append(f"{flag}=True is forbidden in Phase 158.")

    return len(violations) == 0, violations

def phase158_handoff_ingestion_to_text(result: Phase158HandoffIngestionResult) -> str:
    return f"Handoff Ingestion: {result.ingestion_id} - Valid: {result.valid_for_phase158}"
"""

with open("usa_signal_bot/integration/phase157_handoff_ingestion.py", "w") as f:
    f.write(content)
