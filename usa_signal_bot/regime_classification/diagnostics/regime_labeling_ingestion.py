import json
from pathlib import Path
from typing import Any, Tuple, List, Dict

from usa_signal_bot.core.exceptions import RegimeLabelingIngestionError
from usa_signal_bot.core.enums import RegimeTransitionRiskFlag
from usa_signal_bot.regime_classification.diagnostics.phase129_models import (
    RegimeLabelingIngestionResult,
    create_regime_labeling_ingestion_id,
    _now
)

def extract_regime_labeling_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_label_sequences(payload: dict[str, Any]) -> list[dict[str, Any]]:
    context = extract_regime_labeling_context(payload)
    if not context:
        return []
    result_data = context.get("result", {})
    return result_data.get("label_sequences", [])

def extract_labeled_table_paths(payload: dict[str, Any]) -> dict[str, str]:
    return payload.get("output_paths", {}).get("labeled_tables", {})

def extract_stability_profiles(payload: dict[str, Any]) -> list[dict[str, Any]]:
    context = extract_regime_labeling_context(payload)
    if not context:
        return []
    result_data = context.get("result", {})
    return result_data.get("stability_profiles", [])

def regime_labeling_supports_phase129(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    context = extract_regime_labeling_context(payload)
    if not context:
        warnings.append("Missing context in payload.")
        return False, warnings

    if not context.get("ready_for_phase129", False):
        warnings.append("Context not ready for phase 129.")
        return False, warnings

    return True, warnings

def ingest_regime_labeling_review_payload(payload: dict[str, Any]) -> RegimeLabelingIngestionResult:
    context = extract_regime_labeling_context(payload)

    warnings = []
    errors = []
    risk_flags = []

    if not context:
        errors.append("Invalid Phase 128 payload: missing context.")
        risk_flags.append(RegimeTransitionRiskFlag.REGIME_LABELING_REVIEW_INVALID)
        available = False
    else:
        available = True

    is_supported, support_warnings = regime_labeling_supports_phase129(payload)
    warnings.extend(support_warnings)

    if not is_supported:
        risk_flags.append(RegimeTransitionRiskFlag.PHASE128_NOT_READY)

    valid = True
    if context:
        if context.get("activation_allowed") or context.get("strategy_activation_allowed") or context.get("deployment_allowed"):
            valid = False
            errors.append("Payload has activation/deployment enabled, violating non-execution policy.")
            risk_flags.append(RegimeTransitionRiskFlag.DEPLOYMENT_RISK)

        if context.get("broker_execution_enabled") or context.get("order_creation_enabled") or context.get("paper_state_mutation_enabled"):
            valid = False
            errors.append("Payload has broker/order/mutation enabled.")
            risk_flags.append(RegimeTransitionRiskFlag.BROKER_RISK)

        if context.get("model_training_used") or context.get("model_prediction_used"):
            valid = False
            errors.append("Payload used model training/prediction.")
            risk_flags.append(RegimeTransitionRiskFlag.MODEL_TRAINING_ATTEMPTED)

        if context.get("produces_trade_signal") or context.get("produces_order_decision") or context.get("investment_advice"):
            valid = False
            errors.append("Payload produced trade signals or investment advice.")
            risk_flags.append(RegimeTransitionRiskFlag.TRADE_SIGNAL_COLUMN_RISK)

    ctx = context or {}

    return RegimeLabelingIngestionResult(
        ingestion_id=create_regime_labeling_ingestion_id(),
        created_at_utc=_now(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=ctx.get("context_id"),
        available=available,
        feature_engineering_ingested=ctx.get("feature_engineering_ingested", False),
        inputs_loaded=ctx.get("inputs_loaded", False),
        labeling_specs_ready=ctx.get("labeling_specs_ready", False),
        heuristic_labels_ready=ctx.get("heuristic_labels_ready", False),
        rolling_windows_ready=ctx.get("rolling_windows_ready", False),
        candidates_validated=ctx.get("candidates_validated", False),
        label_stability_profiled=ctx.get("label_stability_profiled", False),
        readiness_gate_ready=ctx.get("readiness_gate_ready", False),
        ready_for_phase129=ctx.get("ready_for_phase129", False),
        metadata_only=True,
        research_data_only=True,
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
        valid_for_phase129=(valid and is_supported),
        risk_flags=risk_flags,
        warnings=warnings,
        errors=errors,
        metadata={}
    )

def ingest_latest_regime_labeling_review_from_store(data_root: Path) -> RegimeLabelingIngestionResult:
    reviews_dir = data_root / "regime_classification" / "labeling" / "reviews"
    if not reviews_dir.exists():
        res = ingest_regime_labeling_review_payload({})
        res.errors.append(f"No reviews directory found at {reviews_dir}")
        res.valid_for_phase129 = False
        res.risk_flags.append(RegimeTransitionRiskFlag.REGIME_LABELING_REVIEW_MISSING)
        return res

    review_files = sorted(reviews_dir.glob("*.json"))
    if not review_files:
        res = ingest_regime_labeling_review_payload({})
        res.errors.append("No review JSON files found.")
        res.valid_for_phase129 = False
        res.risk_flags.append(RegimeTransitionRiskFlag.REGIME_LABELING_REVIEW_MISSING)
        return res

    latest_file = review_files[-1]
    try:
        with open(latest_file, "r") as f:
            payload = json.load(f)
        res = ingest_regime_labeling_review_payload(payload)
        res.source_path = str(latest_file)
        return res
    except Exception as e:
        raise RegimeLabelingIngestionError(f"Failed to ingest from {latest_file}: {e}")

def regime_labeling_ingestion_to_text(result: RegimeLabelingIngestionResult) -> str:
    status = "VALID" if result.valid_for_phase129 else "INVALID"
    lines = [
        f"Regime Labeling Ingestion [{status}]",
        f"ID: {result.ingestion_id}",
        f"Source Review ID: {result.source_review_id}",
        f"Ready for Phase 129: {result.ready_for_phase129}",
        f"Errors: {len(result.errors)}"
    ]
    if result.errors:
        lines.append("Errors:")
        for e in result.errors:
            lines.append(f" - {e}")
    if result.risk_flags:
        lines.append("Risk Flags:")
        for r in result.risk_flags:
            lines.append(f" - {r}")
    return "\n".join(lines)
