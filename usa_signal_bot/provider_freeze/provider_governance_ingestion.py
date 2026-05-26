from pathlib import Path
from typing import Any, Dict, Tuple, Optional
from usa_signal_bot.provider_freeze.phase114_models import (
    ProviderGovernanceIngestionResult,
    create_provider_governance_ingestion_id,
    _utcnow_str,
)
from usa_signal_bot.core.enums import ProviderFreezeRiskFlag
import json

def ingest_provider_governance_review_payload(payload: Dict[str, Any]) -> ProviderGovernanceIngestionResult:
    res = ProviderGovernanceIngestionResult(
        ingestion_id=create_provider_governance_ingestion_id(),
        created_at_utc=_utcnow_str()
    )

    if not payload:
        res.warnings.append("Empty payload provided.")
        res.risk_flags.append(ProviderFreezeRiskFlag.GOVERNANCE_REVIEW_MISSING)
        return res

    res.available = True
    res.source_review_id = payload.get("review_id")

    ctx = extract_provider_governance_context(payload)
    if not ctx:
        res.warnings.append("Provider governance context is missing or invalid.")
        res.risk_flags.append(ProviderFreezeRiskFlag.GOVERNANCE_REVIEW_INVALID)
        return res

    res.source_context_id = ctx.get("context_id")
    res.provider_governance_ready = ctx.get("provider_governance_ready", False)
    res.provider_expansion_accepted = ctx.get("provider_expansion_accepted", False)
    res.lineage_ready = ctx.get("lineage_ready", False)
    res.audit_ready = ctx.get("audit_ready", False)
    res.metadata_only = ctx.get("metadata_only", True)
    res.research_data_only = ctx.get("research_data_only", True)
    res.produces_trade_signal = ctx.get("produces_trade_signal", False)
    res.produces_order_decision = ctx.get("produces_order_decision", False)

    res.network_used = ctx.get("network_used", False)
    res.paid_api_used = ctx.get("paid_api_used", False)
    res.scraping_used = ctx.get("scraping_used", False)
    res.html_parsing_used = ctx.get("html_parsing_used", False)
    res.broker_used = ctx.get("broker_used", False)
    res.order_created = ctx.get("order_created", False)
    res.paper_state_mutated = ctx.get("paper_state_mutated", False)
    res.telegram_real_sent = ctx.get("telegram_real_sent", False)
    res.dashboard_started = ctx.get("dashboard_started", False)

    supported, support_warnings = provider_governance_supports_phase114(ctx)
    res.valid_for_phase114 = supported
    res.warnings.extend(support_warnings)
    if not supported:
        res.risk_flags.append(ProviderFreezeRiskFlag.GOVERNANCE_REVIEW_INVALID)

    res.metadata = {"ingested_keys": list(ctx.keys())}
    return res

def ingest_latest_provider_governance_review_from_store(data_root: Path) -> ProviderGovernanceIngestionResult:
    # Look up phase 113 output
    target = data_root / "provider_governance" / "reviews"
    if not target.exists():
        res = ProviderGovernanceIngestionResult(
            ingestion_id=create_provider_governance_ingestion_id(),
            created_at_utc=_utcnow_str()
        )
        res.warnings.append(f"Directory not found: {target}")
        res.risk_flags.append(ProviderFreezeRiskFlag.GOVERNANCE_REVIEW_MISSING)
        return res

    files = list(target.glob("*.json"))
    if not files:
        res = ProviderGovernanceIngestionResult(
            ingestion_id=create_provider_governance_ingestion_id(),
            created_at_utc=_utcnow_str()
        )
        res.warnings.append(f"No review files found in {target}")
        res.risk_flags.append(ProviderFreezeRiskFlag.GOVERNANCE_REVIEW_MISSING)
        return res

    latest_file = max(files, key=lambda f: f.stat().st_mtime)
    try:
        with open(latest_file, "r") as f:
            data = json.load(f)
    except Exception as e:
        res = ProviderGovernanceIngestionResult(
            ingestion_id=create_provider_governance_ingestion_id(),
            created_at_utc=_utcnow_str()
        )
        res.errors.append(f"Error reading {latest_file}: {e}")
        res.risk_flags.append(ProviderFreezeRiskFlag.GOVERNANCE_REVIEW_INVALID)
        return res

    res = ingest_provider_governance_review_payload(data)
    res.source_path = str(latest_file)
    return res

def extract_provider_governance_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("context")

def provider_governance_supports_phase114(ctx: Dict[str, Any]) -> Tuple[bool, list[str]]:
    warnings = []
    supported = True

    if not ctx.get("provider_governance_ready", False):
        warnings.append("provider_governance_ready is False.")
        supported = False
    if not ctx.get("provider_expansion_accepted", False):
        warnings.append("provider_expansion_accepted is False.")
        supported = False
    if not ctx.get("lineage_ready", False):
        warnings.append("lineage_ready is False.")
        supported = False
    if not ctx.get("audit_ready", False):
        warnings.append("audit_ready is False.")
        supported = False
    if not ctx.get("metadata_only", True):
        warnings.append("metadata_only is False.")
        supported = False
    if not ctx.get("research_data_only", True):
        warnings.append("research_data_only is False.")
        supported = False

    if ctx.get("produces_trade_signal", False):
        warnings.append("produces_trade_signal is True.")
        supported = False
    if ctx.get("produces_order_decision", False):
        warnings.append("produces_order_decision is True.")
        supported = False

    for f in ["network_used", "paid_api_used", "scraping_used", "html_parsing_used", "broker_used", "order_created", "paper_state_mutated", "telegram_real_sent", "dashboard_started"]:
        if ctx.get(f, False):
            warnings.append(f"{f} is True.")
            supported = False

    return supported, warnings

def provider_governance_ingestion_to_text(result: ProviderGovernanceIngestionResult) -> str:
    lines = [
        f"Ingestion ID: {result.ingestion_id}",
        f"Created At: {result.created_at_utc}",
        f"Available: {result.available}",
        f"Valid for Phase 114: {result.valid_for_phase114}"
    ]
    if result.warnings:
        lines.append("Warnings:")
        for w in result.warnings:
            lines.append(f" - {w}")
    if result.errors:
        lines.append("Errors:")
        for e in result.errors:
            lines.append(f" - {e}")
    return "\n".join(lines)
