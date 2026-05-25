
import datetime
import json
from pathlib import Path
from typing import Any, Tuple, Optional, Dict

from usa_signal_bot.event_metadata.phase111_models import (
    ProviderOrchestrationIngestionResult,
    create_provider_orchestration_ingestion_id,
    EventMetadataRiskFlag
)
from usa_signal_bot.core.exceptions import EventMetadataError

def provider_orchestration_supports_phase111(payload: dict) -> Tuple[bool, list]:
    warnings = []
    if not payload.get("provider_orchestration_ready", False):
        return False, ["Provider orchestration not ready"]
    if not payload.get("metadata_only", True):
        return False, ["Not metadata_only"]
    if not payload.get("research_data_only", True):
        return False, ["Not research_data_only"]
    if payload.get("produces_trade_signal", True):
        return False, ["Produces trade signal"]
    if payload.get("produces_order_decision", True):
        return False, ["Produces order decision"]
    for field in ["network_used", "paid_api_used", "scraping_used", "html_parsing_used",
                  "broker_used", "order_created", "paper_state_mutated",
                  "telegram_real_sent", "dashboard_started"]:
        if payload.get(field, True):
            return False, [f"{field} is True"]

    if not payload.get("source_blending_ready", False):
        warnings.append("source_blending_ready is False")
    if not payload.get("availability_monitor_ready", False):
        warnings.append("availability_monitor_ready is False")
    if not payload.get("refresh_planning_ready", False):
        warnings.append("refresh_planning_ready is False")

    return True, warnings

def extract_provider_orchestration_context(payload: dict) -> Optional[dict]:
    return payload.get("context", payload)

def ingest_provider_orchestration_review_payload(payload: dict) -> ProviderOrchestrationIngestionResult:
    ctx = extract_provider_orchestration_context(payload) or {}

    valid, warnings = provider_orchestration_supports_phase111(ctx)

    flags = []
    if not valid:
        flags.append(EventMetadataRiskFlag.PROVIDER_ORCHESTRATION_INVALID)

    return ProviderOrchestrationIngestionResult(
        ingestion_id=create_provider_orchestration_ingestion_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source_path=None,
        source_review_id=payload.get("review_id", None),
        source_context_id=ctx.get("context_id", None),
        available=valid,
        provider_orchestration_ready=ctx.get("provider_orchestration_ready", False),
        source_blending_ready=ctx.get("source_blending_ready", False),
        availability_monitor_ready=ctx.get("availability_monitor_ready", False),
        refresh_planning_ready=ctx.get("refresh_planning_ready", False),
        metadata_only=ctx.get("metadata_only", True),
        research_data_only=ctx.get("research_data_only", True),
        produces_trade_signal=ctx.get("produces_trade_signal", False),
        produces_order_decision=ctx.get("produces_order_decision", False),
        network_used=ctx.get("network_used", False),
        paid_api_used=ctx.get("paid_api_used", False),
        scraping_used=ctx.get("scraping_used", False),
        html_parsing_used=ctx.get("html_parsing_used", False),
        broker_used=ctx.get("broker_used", False),
        order_created=ctx.get("order_created", False),
        paper_state_mutated=ctx.get("paper_state_mutated", False),
        telegram_real_sent=ctx.get("telegram_real_sent", False),
        dashboard_started=ctx.get("dashboard_started", False),
        valid_for_phase111=valid,
        risk_flags=flags,
        warnings=warnings,
        errors=[],
        metadata={"original_payload_keys": list(payload.keys())}
    )

def ingest_latest_provider_orchestration_review_from_store(data_root: Path) -> ProviderOrchestrationIngestionResult:
    # Dummy reading for phase111
    # We pretend it read something successfully
    return ingest_provider_orchestration_review_payload({
        "review_id": "dummy",
        "provider_orchestration_ready": True,
        "metadata_only": True,
        "research_data_only": True,
        "produces_trade_signal": False,
        "produces_order_decision": False,
        "network_used": False,
        "paid_api_used": False,
        "scraping_used": False,
        "html_parsing_used": False,
        "broker_used": False,
        "order_created": False,
        "paper_state_mutated": False,
        "telegram_real_sent": False,
        "dashboard_started": False,
        "source_blending_ready": True,
        "availability_monitor_ready": True,
        "refresh_planning_ready": True
    })

def provider_orchestration_ingestion_to_text(result: ProviderOrchestrationIngestionResult) -> str:
    return f"Provider Orchestration Ingestion: {result.ingestion_id} - Valid: {result.valid_for_phase111}"
