
from pathlib import Path
from typing import Any, Optional
from usa_signal_bot.data_providers.phase106_models import ProviderKickoffGateIngestionResult, create_provider_kickoff_ingestion_id, _now

def ingest_provider_kickoff_gate_payload(payload: dict[str, Any]) -> ProviderKickoffGateIngestionResult:
    is_supported, errs = provider_kickoff_gate_supports_phase106(payload)
    return ProviderKickoffGateIngestionResult(
        ingestion_id=create_provider_kickoff_ingestion_id(),
        created_at_utc=_now(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_gate_id=payload.get("gate_id"),
        available=True,
        provider_ready=payload.get("provider_ready", False),
        ready_for_phase106=payload.get("ready_for_phase106", False),
        phase106_scope_allowed=payload.get("metadata_only", False),
        metadata_only=payload.get("metadata_only", False),
        activation_allowed=payload.get("allow_activation", False),
        active_paper_enabled=payload.get("allow_active_paper", False),
        broker_execution_enabled=payload.get("allow_broker_execution", False),
        paper_state_mutation_enabled=payload.get("allow_paper_state_mutation", False),
        telegram_real_send_enabled=payload.get("allow_telegram_real_send", False),
        scraping_enabled=payload.get("allow_scraping", False),
        html_parse_enabled=payload.get("allow_html_parsing", False),
        dashboard_enabled=payload.get("allow_dashboard", False),
        paid_api_enabled=payload.get("allow_paid_api", False),
        provider_network_fetch_required=payload.get("provider_network_fetch_required", False),
        valid_for_phase106=is_supported,
        errors=errs
    )

def ingest_latest_provider_kickoff_gate_from_store(data_root: Path) -> ProviderKickoffGateIngestionResult:
    raise NotImplementedError()

def extract_data_provider_kickoff_gate(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("data_provider_expansion_kickoff_gate")

def provider_kickoff_gate_supports_phase106(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    errs = []
    if not payload:
        return False, ["Gate missing"]
    if not payload.get("ready_for_phase106", False): errs.append("Not ready for phase 106")
    if not payload.get("metadata_only", False): errs.append("Not metadata only")
    if payload.get("allow_activation", False): errs.append("Activation allowed")
    if payload.get("allow_active_paper", False): errs.append("Active paper enabled")
    if payload.get("allow_broker_execution", False): errs.append("Broker execution enabled")
    if payload.get("allow_paper_state_mutation", False): errs.append("Paper state mutation enabled")
    if payload.get("allow_telegram_real_send", False): errs.append("Telegram real send enabled")
    if payload.get("allow_scraping", False): errs.append("Scraping enabled")
    if payload.get("allow_html_parsing", False): errs.append("HTML parsing enabled")
    if payload.get("allow_dashboard", False): errs.append("Dashboard enabled")
    if payload.get("allow_paid_api", False): errs.append("Paid API enabled")
    if payload.get("provider_network_fetch_required", False): errs.append("Provider network fetch required")
    return len(errs) == 0, errs

def provider_kickoff_gate_ingestion_to_text(result: ProviderKickoffGateIngestionResult) -> str:
    return f"Ingestion: {result.ingestion_id} - Valid: {result.valid_for_phase106}"
