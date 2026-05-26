from typing import Dict, Any, Optional, Tuple, List
from pathlib import Path
import json

from usa_signal_bot.feature_engine.advanced_features.phase118_models import (
    CoreIndicatorIngestionResult,
    AdvancedFeatureRiskFlag,
    create_core_indicator_ingestion_id
)
import datetime

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def core_indicator_supports_phase118(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []

    # We expect a payload from phase 117
    # Example fields: core_indicators_ready, feature_table_ready, produces_trade_signal, etc.
    if not payload.get("core_indicators_ready", False):
        warnings.append("core_indicators_ready is False")
    if not payload.get("feature_table_ready", False):
        warnings.append("feature_table_ready is False")

    if payload.get("produces_trade_signal", False):
        warnings.append("produces_trade_signal is True")
    if payload.get("broker_execution_enabled", False):
        warnings.append("broker_execution_enabled is True")

    ready = len(warnings) == 0
    return ready, warnings

def extract_core_indicator_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("context", payload)

def extract_core_feature_table_paths(payload: Dict[str, Any]) -> Dict[str, str]:
    # Returns mapping of symbol to file path
    return payload.get("output_paths", {})

def ingest_core_indicator_review_payload(payload: Dict[str, Any]) -> CoreIndicatorIngestionResult:
    ready_for_phase118, warnings = core_indicator_supports_phase118(payload)

    risk_flags = []
    errors = []

    if payload.get("produces_trade_signal") or payload.get("produces_order_decision"):
        errors.append("Core indicator payload has execution enabled.")
        risk_flags.append(AdvancedFeatureRiskFlag.TRADE_SIGNAL_COLUMN_RISK)

    if payload.get("network_default_enabled") or payload.get("network_used"):
        errors.append("Core indicator payload used network.")
        risk_flags.append(AdvancedFeatureRiskFlag.NETWORK_FETCH_ATTEMPTED)

    ctx = extract_core_indicator_context(payload) or {}

    return CoreIndicatorIngestionResult(
        ingestion_id=create_core_indicator_ingestion_id(),
        created_at_utc=_now(),
        source_path=payload.get("_source_path"),
        source_review_id=payload.get("review_id"),
        source_context_id=ctx.get("context_id"),
        available=True,
        core_indicators_ready=ctx.get("core_indicators_ready", True),
        rolling_window_engine_ready=ctx.get("rolling_window_engine_ready", True),
        feature_table_ready=ctx.get("feature_table_ready", True),
        ready_for_phase118=ready_for_phase118,
        metadata_only=True,
        research_data_only=True,
        activation_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        html_parse_enabled=False,
        paid_api_enabled=False,
        dashboard_enabled=False,
        network_default_enabled=False,
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
        valid_for_phase118=(len(errors) == 0 and ready_for_phase118),
        risk_flags=risk_flags,
        warnings=warnings,
        errors=errors,
        metadata={}
    )

def ingest_latest_core_indicator_review_from_store(data_root: Path) -> CoreIndicatorIngestionResult:
    # Look for Phase 117 reports
    # fallback stub for dry run
    d = data_root / "feature_engine" / "core_indicators" / "reviews"
    if not d.exists():
        # return an empty mock
        return ingest_core_indicator_review_payload({})

    files = sorted(list(d.glob("*.json")))
    if not files:
        return ingest_core_indicator_review_payload({})

    with open(files[-1], "r", encoding="utf-8") as f:
        payload = json.load(f)
        payload["_source_path"] = str(files[-1])
        return ingest_core_indicator_review_payload(payload)

def core_indicator_ingestion_to_text(result: CoreIndicatorIngestionResult) -> str:
    return f"Ingestion {result.ingestion_id}: ReadyForPhase118={result.ready_for_phase118}, Errors={len(result.errors)}"
