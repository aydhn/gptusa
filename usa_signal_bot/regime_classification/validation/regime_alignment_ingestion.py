from pathlib import Path
from typing import Any, Optional
from usa_signal_bot.regime_classification.validation.phase132_models import (
    RegimeAlignmentIngestionResult,
    create_regime_alignment_ingestion_id,
    _now_utc,
    RegimeContextValidationRiskFlag
)
import json

def extract_regime_alignment_context(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("context")

def extract_compatibility_results(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("compatibility_results", [])

def extract_overlay_results(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("overlay_results", [])

def extract_alignment_diagnostics_profiles(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("diagnostics_profiles", [])

def extract_alignment_readiness_gate(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("readiness_gate")

def regime_alignment_supports_phase132(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []
    context = extract_regime_alignment_context(payload)
    if not context:
        return False, ["Missing regime alignment context"]

    if not context.get("market_behavior_ingested"):
        errors.append("market_behavior_ingested is not true")
    if not context.get("frozen_factors_loaded"):
        errors.append("frozen_factors_loaded is not true")
    if not context.get("behavior_artifacts_loaded"):
        errors.append("behavior_artifacts_loaded is not true")
    if not context.get("alignment_specs_ready"):
        errors.append("alignment_specs_ready is not true")
    if not context.get("overlays_built"):
        errors.append("overlays_built is not true")
    if not context.get("compatibility_computed"):
        errors.append("compatibility_computed is not true")
    if not context.get("diagnostics_built"):
        errors.append("diagnostics_built is not true")
    if not context.get("readiness_gate_ready"):
        errors.append("readiness_gate_ready is not true")
    if not context.get("ready_for_phase132"):
        errors.append("ready_for_phase132 is not true")
    if not context.get("research_data_only"):
        errors.append("research_data_only is not true")

    for flag in ["activation_allowed", "strategy_activation_allowed", "deployment_allowed",
                 "active_paper_enabled", "broker_execution_enabled", "order_creation_enabled",
                 "paper_state_mutation_enabled", "telegram_real_send_enabled", "scraping_enabled",
                 "html_parse_enabled", "paid_api_enabled", "dashboard_enabled", "network_default_enabled",
                 "produces_trade_signal", "produces_order_decision", "produces_portfolio_weights",
                 "investment_advice", "model_training_used", "model_prediction_used", "heavy_ml_dependency_used"]:
        if context.get(flag, False):
            errors.append(f"{flag} must be false")

    return len(errors) == 0, errors

def ingest_regime_alignment_review_payload(payload: dict[str, Any]) -> RegimeAlignmentIngestionResult:
    context = extract_regime_alignment_context(payload) or {}
    supports, errors = regime_alignment_supports_phase132(payload)

    risk_flags = []
    if not context:
        risk_flags.append(RegimeContextValidationRiskFlag.REGIME_ALIGNMENT_REVIEW_MISSING)
    if not supports:
        risk_flags.append(RegimeContextValidationRiskFlag.PHASE131_NOT_READY)

    if context.get("produces_trade_signal"):
        risk_flags.append(RegimeContextValidationRiskFlag.TRADE_SIGNAL_COLUMN_RISK)
    if context.get("produces_order_decision"):
        risk_flags.append(RegimeContextValidationRiskFlag.ORDER_DECISION_COLUMN_RISK)
    if context.get("produces_portfolio_weights"):
        risk_flags.append(RegimeContextValidationRiskFlag.PORTFOLIO_WEIGHT_COLUMN_RISK)
    if context.get("investment_advice"):
        risk_flags.append(RegimeContextValidationRiskFlag.INVESTMENT_ADVICE_LANGUAGE_RISK)

    return RegimeAlignmentIngestionResult(
        ingestion_id=create_regime_alignment_ingestion_id(),
        created_at_utc=_now_utc(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=context.get("context_id"),
        available=bool(context),
        market_behavior_ingested=context.get("market_behavior_ingested", False),
        frozen_factors_loaded=context.get("frozen_factors_loaded", False),
        behavior_artifacts_loaded=context.get("behavior_artifacts_loaded", False),
        alignment_specs_ready=context.get("alignment_specs_ready", False),
        overlays_built=context.get("overlays_built", False),
        compatibility_computed=context.get("compatibility_computed", False),
        diagnostics_built=context.get("diagnostics_built", False),
        readiness_gate_ready=context.get("readiness_gate_ready", False),
        ready_for_phase132=context.get("ready_for_phase132", False),
        metadata_only=context.get("metadata_only", True),
        research_data_only=context.get("research_data_only", True),
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
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
        model_training_used=False,
        model_prediction_used=False,
        heavy_ml_dependency_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        valid_for_phase132=supports,
        risk_flags=risk_flags,
        warnings=[],
        errors=errors,
        metadata={}
    )

def ingest_latest_regime_alignment_review_from_store(data_root: Path) -> RegimeAlignmentIngestionResult:
    # We will search the reviews dir from phase 131 if it exists
    # If not, we return an empty/failed ingestion
    reviews_dir = data_root / "regime_classification" / "alignment" / "reviews"
    if not reviews_dir.exists():
        res = ingest_regime_alignment_review_payload({})
        res.errors.append("Reviews directory not found")
        return res

    files = list(reviews_dir.glob("*.json"))
    if not files:
        res = ingest_regime_alignment_review_payload({})
        res.errors.append("No review files found")
        return res

    latest_file = max(files, key=lambda f: f.stat().st_mtime)
    try:
        with open(latest_file, "r") as f:
            payload = json.load(f)
        res = ingest_regime_alignment_review_payload(payload)
        res.source_path = str(latest_file)
        return res
    except Exception as e:
        res = ingest_regime_alignment_review_payload({})
        res.errors.append(f"Failed to read {latest_file}: {e}")
        return res

def regime_alignment_ingestion_to_text(result: RegimeAlignmentIngestionResult) -> str:
    lines = [
        f"Ingestion ID: {result.ingestion_id}",
        f"Valid for Phase 132: {result.valid_for_phase132}",
        f"Ready for Phase 132: {result.ready_for_phase132}",
        f"Available: {result.available}",
        f"Errors: {len(result.errors)}"
    ]
    if result.errors:
        lines.append("Errors details:")
        for e in result.errors:
            lines.append(f" - {e}")
    return "\n".join(lines)
