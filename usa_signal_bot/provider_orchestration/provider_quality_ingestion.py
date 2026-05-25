from typing import Any
from pathlib import Path
from datetime import datetime, timezone
import json

from usa_signal_bot.core.exceptions import ProviderQualityIngestionError
from usa_signal_bot.core.enums import ProviderOrchestrationRiskFlag
from usa_signal_bot.provider_orchestration.phase110_models import (
    ProviderQualityIngestionResult, create_provider_quality_ingestion_id,
    validate_provider_quality_ingestion_result
)

def ingest_provider_quality_review_payload(payload: dict[str, Any]) -> ProviderQualityIngestionResult:
    review_id = payload.get("review_id")
    context = payload.get("context", {})

    provider_quality_ready = context.get("provider_quality_ready", False)
    source_trust_ready = context.get("source_trust_ready", False)
    provider_selection_scoring_ready = context.get("provider_selection_scoring_ready", False)

    valid, errors = provider_quality_supports_phase110(payload)

    result = ProviderQualityIngestionResult(
        ingestion_id=create_provider_quality_ingestion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_path=None,
        source_review_id=review_id,
        source_context_id=context.get("context_id"),
        available=review_id is not None,
        provider_quality_ready=provider_quality_ready,
        source_trust_ready=source_trust_ready,
        provider_selection_scoring_ready=provider_selection_scoring_ready,
        metadata_only=context.get("metadata_only", True),
        research_data_only=context.get("research_data_only", True),
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
        valid_for_phase110=valid,
        warnings=[],
        errors=errors,
        metadata={"payload_summary": extract_provider_quality_context(payload)}
    )

    try:
        validate_provider_quality_ingestion_result(result)
    except ValueError as e:
        result.valid_for_phase110 = False
        result.errors.append(str(e))

    if not result.valid_for_phase110:
        result.risk_flags.append(ProviderOrchestrationRiskFlag.PROVIDER_QUALITY_INVALID)

    return result

def ingest_latest_provider_quality_review_from_store(data_root: Path) -> ProviderQualityIngestionResult:
    reviews_dir = data_root / "provider_quality" / "reviews"
    if not reviews_dir.exists():
        return _empty_invalid_ingestion("Reviews directory does not exist")

    files = list(reviews_dir.glob("*.json"))
    if not files:
        return _empty_invalid_ingestion("No review files found")

    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    latest_file = files[0]

    try:
        with open(latest_file, "r") as f:
            payload = json.load(f)
        result = ingest_provider_quality_review_payload(payload)
        result.source_path = str(latest_file)
        return result
    except Exception as e:
        return _empty_invalid_ingestion(f"Failed to read or parse latest review file: {e}")

def _empty_invalid_ingestion(error_msg: str) -> ProviderQualityIngestionResult:
    return ProviderQualityIngestionResult(
        ingestion_id=create_provider_quality_ingestion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_path=None,
        source_review_id=None,
        source_context_id=None,
        available=False,
        provider_quality_ready=False,
        source_trust_ready=False,
        provider_selection_scoring_ready=False,
        metadata_only=True,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        valid_for_phase110=False,
        risk_flags=[ProviderOrchestrationRiskFlag.PROVIDER_QUALITY_MISSING],
        warnings=[],
        errors=[error_msg],
        metadata={}
    )

def extract_provider_quality_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_provider_rankings(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("rankings", [])

def extract_provider_selection_scores(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("selection_scores", [])

def provider_quality_supports_phase110(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []
    if not payload:
        return False, ["Payload is empty"]

    context = payload.get("context", {})
    if not context.get("provider_quality_ready"):
        errors.append("provider_quality_ready must be True")
    if not context.get("source_trust_ready"):
        errors.append("source_trust_ready must be True")
    if not context.get("provider_selection_scoring_ready"):
        errors.append("provider_selection_scoring_ready must be True")

    return len(errors) == 0, errors

def provider_quality_ingestion_to_text(result: ProviderQualityIngestionResult) -> str:
    lines = [
        f"--- Provider Quality Ingestion ---",
        f"ID: {result.ingestion_id}",
        f"Available: {result.available}",
        f"Valid for Phase 110: {result.valid_for_phase110}",
    ]
    if result.errors:
        lines.append(f"Errors: {result.errors}")
    if result.risk_flags:
        lines.append(f"Risk Flags: {[f.value for f in result.risk_flags]}")
    return "\n".join(lines)
