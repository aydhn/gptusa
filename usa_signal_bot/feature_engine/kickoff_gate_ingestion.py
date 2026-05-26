import datetime
from pathlib import Path
from typing import Any

from usa_signal_bot.feature_engine.phase116_models import (
    FeatureFactorKickoffIngestionResult,
    create_feature_factor_kickoff_ingestion_id,
    validate_feature_factor_kickoff_ingestion_result
)
from usa_signal_bot.core.enums import FeatureFoundationRiskFlag

def extract_feature_factor_kickoff_gate(payload: dict[str, Any]) -> dict[str, Any] | None:
    if not payload:
        return None
    return payload.get("kickoff_gate") or payload

def feature_factor_kickoff_supports_phase116(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    gate = extract_feature_factor_kickoff_gate(payload)
    if not gate:
        return False, ["Missing kickoff gate in payload"]
    errors = []
    if not gate.get("phase116_ready", False):
        errors.append("Kickoff gate phase116_ready must be True")
    if gate.get("activation_allowed", True):
        errors.append("activation_allowed must be false")
    if gate.get("broker_execution_enabled", True):
        errors.append("broker_execution_enabled must be false")

    return len(errors) == 0, errors

def ingest_feature_factor_kickoff_gate_payload(payload: dict[str, Any]) -> FeatureFactorKickoffIngestionResult:
    gate = extract_feature_factor_kickoff_gate(payload) or {}

    available = bool(gate)
    ready_for_phase116 = gate.get("phase116_ready", False)
    phase116_scope_allowed = gate.get("phase116_scope_allowed", False)

    metadata_only = gate.get("metadata_only", True)
    research_data_only = gate.get("research_data_only", True)
    sealed = gate.get("sealed", True)
    immutable = gate.get("immutable", True)
    frozen = gate.get("frozen", True)
    activation_allowed = gate.get("activation_allowed", False)
    active_paper_enabled = gate.get("active_paper_enabled", False)
    broker_execution_enabled = gate.get("broker_execution_enabled", False)
    order_creation_enabled = gate.get("order_creation_enabled", False)
    paper_state_mutation_enabled = gate.get("paper_state_mutation_enabled", False)
    telegram_real_send_enabled = gate.get("telegram_real_send_enabled", False)
    scraping_enabled = gate.get("scraping_enabled", False)
    html_parse_enabled = gate.get("html_parse_enabled", False)
    paid_api_enabled = gate.get("paid_api_enabled", False)
    dashboard_enabled = gate.get("dashboard_enabled", False)
    network_default_enabled = gate.get("network_default_enabled", False)
    produces_trade_signal = gate.get("produces_trade_signal", False)
    produces_order_decision = gate.get("produces_order_decision", False)

    res = FeatureFactorKickoffIngestionResult(
        ingestion_id=create_feature_factor_kickoff_ingestion_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        source_path=None,
        source_gate_id=gate.get("gate_id"),
        source_review_id=None,
        available=available,
        ready_for_phase116=ready_for_phase116,
        phase116_scope_allowed=phase116_scope_allowed,
        metadata_only=metadata_only,
        research_data_only=research_data_only,
        sealed=sealed,
        immutable=immutable,
        frozen=frozen,
        activation_allowed=activation_allowed,
        active_paper_enabled=active_paper_enabled,
        broker_execution_enabled=broker_execution_enabled,
        order_creation_enabled=order_creation_enabled,
        paper_state_mutation_enabled=paper_state_mutation_enabled,
        telegram_real_send_enabled=telegram_real_send_enabled,
        scraping_enabled=scraping_enabled,
        html_parse_enabled=html_parse_enabled,
        paid_api_enabled=paid_api_enabled,
        dashboard_enabled=dashboard_enabled,
        network_default_enabled=network_default_enabled,
        produces_trade_signal=produces_trade_signal,
        produces_order_decision=produces_order_decision,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        valid_for_phase116=False,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata=gate
    )

    if not available:
        res.valid_for_phase116 = False
        res.risk_flags.append(FeatureFoundationRiskFlag.KICKOFF_GATE_MISSING)
        return res

    validate_feature_factor_kickoff_ingestion_result(res)

    res.valid_for_phase116 = len(res.errors) == 0
    if not res.valid_for_phase116:
        res.risk_flags.append(FeatureFoundationRiskFlag.KICKOFF_GATE_INVALID)

    return res

def ingest_latest_feature_factor_kickoff_gate_from_store(data_root: Path) -> FeatureFactorKickoffIngestionResult:
    # Local read logic would go here. For now we just return a mocked failure if no real payload.
    return ingest_feature_factor_kickoff_gate_payload({})

def feature_factor_kickoff_ingestion_to_text(result: FeatureFactorKickoffIngestionResult) -> str:
    lines = [
        f"Ingestion ID: {result.ingestion_id}",
        f"Available: {result.available}",
        f"Ready for Phase 116: {result.ready_for_phase116}",
        f"Valid for Phase 116: {result.valid_for_phase116}",
        f"Errors: {len(result.errors)}"
    ]
    return "\n".join(lines)
