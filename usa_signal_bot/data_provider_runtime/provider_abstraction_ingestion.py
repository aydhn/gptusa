import json
from pathlib import Path
from typing import Any, Tuple, List, Optional
from datetime import datetime, timezone

from usa_signal_bot.data_provider_runtime.phase107_models import (
    ProviderAbstractionIngestionResult,
    create_provider_abstraction_ingestion_id
)
from usa_signal_bot.core.exceptions import ProviderAbstractionIngestionError
from usa_signal_bot.core.enums import ProviderRuntimeRiskFlag

def ingest_provider_abstraction_review_payload(payload: dict[str, Any]) -> ProviderAbstractionIngestionResult:
    result = ProviderAbstractionIngestionResult(
        ingestion_id=create_provider_abstraction_ingestion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        available=True
    )

    context = extract_provider_abstraction_context(payload)
    if not context:
        result.valid_for_phase107 = False
        result.errors.append("Missing provider abstraction context")
        result.risk_flags.append(ProviderRuntimeRiskFlag.PROVIDER_ABSTRACTION_MISSING)
        return result

    result.source_context_id = context.get("context_id")
    result.source_review_id = payload.get("review_id")

    valid_phase107, msgs = provider_abstraction_supports_phase107(context)
    result.valid_for_phase107 = valid_phase107
    result.errors.extend([m for m in msgs if "error" in m.lower() or "must be" in m.lower()])
    result.warnings.extend([m for m in msgs if "warning" in m.lower()])

    result.provider_abstraction_ready = context.get("provider_abstraction_ready", False)
    result.provider_skeletons_ready = context.get("provider_skeletons_ready", False)
    result.provider_registry_valid = context.get("provider_registry_valid", False)
    result.provider_safety_valid = context.get("provider_safety_valid", False)
    result.metadata_only = context.get("metadata_only", True)
    result.provider_network_fetch_enabled_now = context.get("provider_network_fetch_enabled_now", False)

    result.activation_allowed = context.get("activation_allowed", False)
    result.active_paper_enabled = context.get("active_paper_enabled", False)
    result.broker_execution_enabled = context.get("broker_execution_enabled", False)
    result.paper_state_mutation_enabled = context.get("paper_state_mutation_enabled", False)
    result.telegram_real_send_enabled = context.get("telegram_real_send_enabled", False)
    result.scraping_enabled = context.get("scraping_enabled", False)
    result.html_parse_enabled = context.get("html_parse_enabled", False)
    result.dashboard_enabled = context.get("dashboard_enabled", False)
    result.paid_api_enabled = context.get("paid_api_enabled", False)

    if not result.provider_abstraction_ready:
        result.risk_flags.append(ProviderRuntimeRiskFlag.PROVIDER_ABSTRACTION_INVALID)
    if not result.provider_registry_valid:
        result.risk_flags.append(ProviderRuntimeRiskFlag.PROVIDER_ABSTRACTION_INVALID)
    if not result.provider_safety_valid:
        result.risk_flags.append(ProviderRuntimeRiskFlag.PROVIDER_ABSTRACTION_INVALID)

    return result

def ingest_latest_provider_abstraction_review_from_store(data_root: Path) -> ProviderAbstractionIngestionResult:
    review_path = data_root / "data_providers" / "reviews"
    if not review_path.exists():
        res = ProviderAbstractionIngestionResult()
        res.warnings.append(f"Review path missing: {review_path}")
        return res

    files = sorted(list(review_path.glob("*.json")))
    if not files:
        res = ProviderAbstractionIngestionResult()
        res.warnings.append(f"No review files found in: {review_path}")
        return res

    latest = files[-1]
    try:
        with open(latest, "r") as f:
            payload = json.load(f)

        result = ingest_provider_abstraction_review_payload(payload)
        result.source_path = str(latest)
        return result
    except Exception as e:
        raise ProviderAbstractionIngestionError(f"Failed to ingest abstraction review: {str(e)}")

def extract_provider_abstraction_context(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("context")

def extract_provider_registry_entries(payload: dict[str, Any]) -> List[dict[str, Any]]:
    return payload.get("registry", {}).get("providers", [])

def provider_abstraction_supports_phase107(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    valid = True
    msgs = []

    if not payload.get("provider_abstraction_ready", False):
        valid = False
        msgs.append("provider_abstraction_ready must be True")
    if not payload.get("provider_registry_valid", False):
        valid = False
        msgs.append("provider_registry_valid must be True")
    if not payload.get("provider_safety_valid", False):
        valid = False
        msgs.append("provider_safety_valid must be True")
    if not payload.get("metadata_only", True):
        valid = False
        msgs.append("metadata_only must be True")
    if payload.get("provider_network_fetch_enabled_now", False):
        valid = False
        msgs.append("provider_network_fetch_enabled_now must be False")
    if payload.get("activation_allowed", False):
        valid = False
        msgs.append("activation_allowed must be False")

    return valid, msgs

def provider_abstraction_ingestion_to_text(result: ProviderAbstractionIngestionResult) -> str:
    lines = [
        "=== Provider Abstraction Ingestion Result ===",
        f"Ingestion ID: {result.ingestion_id}",
        f"Available: {result.available}",
        f"Valid for Phase 107: {result.valid_for_phase107}",
        f"Source: {result.source_path or 'Memory'}",
        ""
    ]
    if result.errors:
        lines.append("Errors:")
        for e in result.errors:
            lines.append(f" - {e}")
    if result.warnings:
        lines.append("Warnings:")
        for w in result.warnings:
            lines.append(f" - {w}")
    return "\n".join(lines)
