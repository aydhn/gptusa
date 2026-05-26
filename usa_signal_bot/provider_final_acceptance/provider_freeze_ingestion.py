import json
from pathlib import Path
from typing import Any, Tuple
from usa_signal_bot.provider_final_acceptance.phase115_models import (
    ProviderFreezeIngestionResult,
    create_provider_freeze_ingestion_id,
    _utc_now,
    validate_provider_freeze_ingestion_result,
    ProviderFinalAcceptanceRiskFlag
)
from usa_signal_bot.core.exceptions import ProviderFreezeIngestionError

def extract_provider_freeze_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    if not payload:
        return None
    context = payload.get("context")
    if not context:
        return None
    return context

def provider_freeze_supports_phase115(payload: dict[str, Any]) -> Tuple[bool, list[str]]:
    warnings = []
    if not payload:
        return False, ["Payload is empty."]

    context = payload.get("context", {})
    ready = context.get("ready_for_phase115", False)
    if not ready:
        warnings.append("ready_for_phase115 is missing or False")

    frozen = context.get("provider_expansion_frozen", False)
    if not frozen:
        warnings.append("provider_expansion_frozen is missing or False")

    return ready and frozen, warnings

def ingest_provider_freeze_review_payload(payload: dict[str, Any]) -> ProviderFreezeIngestionResult:
    if not payload:
        raise ProviderFreezeIngestionError("Payload is empty.")

    context = extract_provider_freeze_context(payload)
    if not context:
        context = {}

    supports, supp_warnings = provider_freeze_supports_phase115(payload)

    result = ProviderFreezeIngestionResult(
        ingestion_id=create_provider_freeze_ingestion_id(),
        created_at_utc=_utc_now(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=context.get("context_id"),
        available=True,
        provider_expansion_frozen=context.get("provider_expansion_frozen", False),
        multi_provider_review_passed=context.get("multi_provider_review_passed", False),
        data_layer_rehearsal_passed=context.get("data_layer_rehearsal_passed", False),
        output_contracts_passed=context.get("output_contracts_passed", False),
        metadata_only=context.get("metadata_only", True),
        research_data_only=context.get("research_data_only", True),
        activation_allowed=context.get("activation_allowed", False),
        active_paper_enabled=context.get("active_paper_enabled", False),
        broker_execution_enabled=context.get("broker_execution_enabled", False),
        order_creation_enabled=context.get("order_creation_enabled", False),
        paper_state_mutation_enabled=context.get("paper_state_mutation_enabled", False),
        telegram_real_send_enabled=context.get("telegram_real_send_enabled", False),
        scraping_enabled=context.get("scraping_enabled", False),
        html_parse_enabled=context.get("html_parse_enabled", False),
        paid_api_enabled=context.get("paid_api_enabled", False),
        dashboard_enabled=context.get("dashboard_enabled", False),
        network_default_enabled=context.get("network_default_enabled", False),
        produces_trade_signal=context.get("produces_trade_signal", False),
        produces_order_decision=context.get("produces_order_decision", False),
        network_used=context.get("network_used", False),
        paid_api_used=context.get("paid_api_used", False),
        scraping_used=context.get("scraping_used", False),
        html_parsing_used=context.get("html_parsing_used", False),
        broker_used=context.get("broker_used", False),
        order_created=context.get("order_created", False),
        paper_state_mutated=context.get("paper_state_mutated", False),
        telegram_real_sent=context.get("telegram_real_sent", False),
        dashboard_started=context.get("dashboard_started", False),
        ready_for_phase115=context.get("ready_for_phase115", False),
        valid_for_phase115=True,
        risk_flags=[],
        warnings=supp_warnings,
        errors=[],
        metadata={"source_report_type": payload.get("report_type")}
    )

    validate_provider_freeze_ingestion_result(result)

    if not result.valid_for_phase115:
        if ProviderFinalAcceptanceRiskFlag.PROVIDER_FREEZE_REVIEW_INVALID not in result.risk_flags:
            result.risk_flags.append(ProviderFinalAcceptanceRiskFlag.PROVIDER_FREEZE_REVIEW_INVALID)

    return result

def ingest_latest_provider_freeze_review_from_store(data_root: Path) -> ProviderFreezeIngestionResult:
    reviews_dir = data_root / "provider_freeze" / "reviews"
    if not reviews_dir.exists():
        res = ingest_provider_freeze_review_payload({})
        res.available = False
        res.valid_for_phase115 = False
        res.risk_flags.append(ProviderFinalAcceptanceRiskFlag.PROVIDER_FREEZE_REVIEW_MISSING)
        res.errors.append("Provider freeze reviews directory not found.")
        return res

    json_files = list(reviews_dir.glob("*.json"))
    if not json_files:
        res = ingest_provider_freeze_review_payload({})
        res.available = False
        res.valid_for_phase115 = False
        res.risk_flags.append(ProviderFinalAcceptanceRiskFlag.PROVIDER_FREEZE_REVIEW_MISSING)
        res.errors.append("No provider freeze reviews found.")
        return res

    latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
    try:
        with open(latest_file, "r") as f:
            payload = json.load(f)
        res = ingest_provider_freeze_review_payload(payload)
        res.source_path = str(latest_file)
        return res
    except Exception as e:
        res = ingest_provider_freeze_review_payload({})
        res.available = False
        res.valid_for_phase115 = False
        res.risk_flags.append(ProviderFinalAcceptanceRiskFlag.PROVIDER_FREEZE_REVIEW_INVALID)
        res.errors.append(f"Failed to read provider freeze review: {e}")
        return res

def provider_freeze_ingestion_to_text(result: ProviderFreezeIngestionResult) -> str:
    status = "VALID" if result.valid_for_phase115 else "INVALID"
    return f"Provider Freeze Ingestion [{status}] - Available: {result.available}, Ready for 115: {result.ready_for_phase115}"
