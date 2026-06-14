from typing import Any
from pathlib import Path
import json

from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    DriftMonitoringIngestionResult,
    create_drift_monitoring_ingestion_id,
    current_time,
)
from usa_signal_bot.core.exceptions import DriftMonitoringIngestionError


def extract_drift_monitoring_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")


def extract_monitoring_metadata_package(
    payload: dict[str, Any],
) -> dict[str, Any] | None:
    return payload.get("monitoring_metadata_package")


def extract_post_ensemble_governance(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("post_ensemble_governance")


def extract_non_activation_drift_boundary(
    payload: dict[str, Any],
) -> dict[str, Any] | None:
    return payload.get("non_activation_drift_boundary")


def extract_model_card_drift_updates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("model_card_drift_updates", [])


def extract_drift_readiness_gate(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("drift_readiness_gate")


def drift_monitoring_supports_phase145(
    payload: dict[str, Any],
) -> tuple[bool, list[str]]:
    warnings = []

    gate = extract_drift_readiness_gate(payload)
    if not gate:
        warnings.append("Missing drift_readiness_gate.")
        return False, warnings

    ready = gate.get("ready_for_phase145", False)
    if not ready:
        warnings.append("drift_readiness_gate says not ready for Phase 145.")
        return False, warnings

    return True, warnings


def _extract_unsafe_boundary_flags(boundary: dict[str, Any] | None) -> dict[str, bool]:
    flags = {
        "research_data_only": True,
        "live_monitoring_enabled": False,
        "alert_sender_enabled": False,
        "live_inference_enabled": False,
        "produces_trade_signal": False,
        "produces_portfolio_weights": False,
    }
    if boundary:
        if not boundary.get("research_data_only", True):
            flags["research_data_only"] = False
        if boundary.get("live_monitoring_enabled", False):
            flags["live_monitoring_enabled"] = True
        if boundary.get("alert_sender_enabled", False):
            flags["alert_sender_enabled"] = True
        if boundary.get("live_inference_enabled", False):
            flags["live_inference_enabled"] = True
        if boundary.get("produces_trade_signal", False):
            flags["produces_trade_signal"] = True
        if boundary.get("produces_portfolio_weights", False):
            flags["produces_portfolio_weights"] = True
    return flags


def _validate_ingestion_context(
    context: dict[str, Any] | None,
    gate: dict[str, Any] | None,
    supports_phase145: bool,
    errors: list[str],
) -> dict[str, bool]:
    context_flags = {
        "ensemble_prototype_ingested": (
            context.get("ensemble_prototype_ingested", False) if context else False
        ),
        "drift_inputs_resolved": (
            context.get("drift_inputs_resolved", False) if context else False
        ),
        "monitoring_metadata_package_built": (
            context.get("monitoring_metadata_package_built", False)
            if context
            else False
        ),
        "post_ensemble_governance_built": (
            context.get("post_ensemble_governance_built", False) if context else False
        ),
        "non_activation_boundary_validated": (
            context.get("non_activation_boundary_validated", False)
            if context
            else False
        ),
        "model_cards_updated": (
            context.get("model_cards_updated", False) if context else False
        ),
        "readiness_gate_passed": gate.get("gate_passed", False) if gate else False,
        "ready_for_phase145": supports_phase145,
    }

    for flag_name, is_valid in context_flags.items():
        if not is_valid:
            errors.append(f"{flag_name} is False")

    return context_flags


def _validate_safety_boundaries(flags: dict[str, bool], errors: list[str]) -> None:
    if not flags["research_data_only"]:
        errors.append("research_data_only must be True")
    if flags["live_monitoring_enabled"]:
        errors.append("live_monitoring_enabled must be False")
    if flags["alert_sender_enabled"]:
        errors.append("alert_sender_enabled must be False")
    if flags["produces_trade_signal"]:
        errors.append("produces_trade_signal must be False")
    if flags["produces_portfolio_weights"]:
        errors.append("produces_portfolio_weights must be False")


def ingest_drift_monitoring_review_payload(
    payload: dict[str, Any], source_path: str | None = None
) -> DriftMonitoringIngestionResult:
    warnings = []
    errors = []

    review_id = payload.get("review_id")
    context = extract_drift_monitoring_context(payload)
    context_id = context.get("context_id") if context else None

    supports_phase145, sup_warnings = drift_monitoring_supports_phase145(payload)
    warnings.extend(sup_warnings)

    if not review_id:
        errors.append("Missing review_id in payload.")

    monitoring_package = extract_monitoring_metadata_package(payload)
    post_gov = extract_post_ensemble_governance(payload)
    boundary = extract_non_activation_drift_boundary(payload)
    gate = extract_drift_readiness_gate(payload)

    if not monitoring_package:
        errors.append("Missing monitoring_metadata_package.")
    if not post_gov:
        errors.append("Missing post_ensemble_governance.")
    if not boundary:
        errors.append("Missing non_activation_drift_boundary.")
    if not gate:
        errors.append("Missing drift_readiness_gate.")

    context_flags = _validate_ingestion_context(
        context, gate, supports_phase145, errors
    )
    boundary_flags = _extract_unsafe_boundary_flags(boundary)
    _validate_safety_boundaries(boundary_flags, errors)

    valid_for_phase145 = len(errors) == 0

    return DriftMonitoringIngestionResult(
        ingestion_id=create_drift_monitoring_ingestion_id(),
        created_at_utc=current_time(),
        source_path=source_path,
        source_review_id=review_id,
        source_context_id=context_id,
        available=True,
        ensemble_prototype_ingested=context_flags["ensemble_prototype_ingested"],
        ensemble_artifacts_loaded=(
            context.get("ensemble_artifacts_loaded", False) if context else False
        ),
        drift_inputs_resolved=context_flags["drift_inputs_resolved"],
        monitoring_window_policy_built=(
            context.get("monitoring_window_policy_built", False) if context else False
        ),
        drift_baseline_specs_built=(
            context.get("drift_baseline_specs_built", False) if context else False
        ),
        feature_drift_baseline_built=(
            context.get("feature_drift_baseline_built", False) if context else False
        ),
        prediction_drift_baseline_built=(
            context.get("prediction_drift_baseline_built", False) if context else False
        ),
        score_distribution_drift_built=(
            context.get("score_distribution_drift_built", False) if context else False
        ),
        calibration_drift_baseline_built=(
            context.get("calibration_drift_baseline_built", False) if context else False
        ),
        residual_drift_baseline_built=(
            context.get("residual_drift_baseline_built", False) if context else False
        ),
        label_distribution_drift_built=(
            context.get("label_distribution_drift_built", False) if context else False
        ),
        regime_drift_baseline_built=(
            context.get("regime_drift_baseline_built", False) if context else False
        ),
        drift_metrics_built=(
            context.get("drift_metrics_built", False) if context else False
        ),
        monitoring_snapshot_built=(
            context.get("monitoring_snapshot_built", False) if context else False
        ),
        alert_rule_metadata_built=(
            context.get("alert_rule_metadata_built", False) if context else False
        ),
        monitoring_metadata_package_built=context_flags[
            "monitoring_metadata_package_built"
        ],
        post_ensemble_governance_built=context_flags["post_ensemble_governance_built"],
        non_activation_boundary_validated=context_flags[
            "non_activation_boundary_validated"
        ],
        model_cards_updated=context_flags["model_cards_updated"],
        readiness_gate_built=(
            context.get("readiness_gate_built", False) if context else False
        ),
        readiness_gate_passed=context_flags["readiness_gate_passed"],
        ready_for_phase145=context_flags["ready_for_phase145"],
        metadata_only=True,
        research_data_only=boundary_flags["research_data_only"],
        offline_ml_research_only=True,
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
        live_monitoring_enabled=boundary_flags["live_monitoring_enabled"],
        alert_sender_enabled=boundary_flags["alert_sender_enabled"],
        daemon_started=False,
        scheduler_enabled=False,
        live_inference_enabled=boundary_flags["live_inference_enabled"],
        online_inference_enabled=False,
        threshold_optimization_performed=False,
        heavy_ml_dependency_used=False,
        shap_lime_dependency_used=False,
        backtest_executed=False,
        produces_trade_signal=boundary_flags["produces_trade_signal"],
        produces_order_decision=False,
        produces_portfolio_weights=boundary_flags["produces_portfolio_weights"],
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
        valid_for_phase145=valid_for_phase145,
        risk_flags=[],
        warnings=warnings,
        errors=errors,
        metadata={},
    )


def ingest_latest_drift_monitoring_review_from_store(
    data_root: Path,
) -> DriftMonitoringIngestionResult:
    # Simulating finding the latest review
    reviews_dir = data_root / "ml_research" / "drift_monitoring" / "reviews"
    if not reviews_dir.exists():
        raise DriftMonitoringIngestionError(
            f"Reviews directory not found: {reviews_dir}"
        )

    files = list(reviews_dir.glob("*.json"))
    if not files:
        raise DriftMonitoringIngestionError(
            f"No drift monitoring reviews found in {reviews_dir}"
        )

    latest_file = max(files, key=lambda p: p.stat().st_mtime)
    with open(latest_file, "r") as f:
        payload = json.load(f)

    return ingest_drift_monitoring_review_payload(payload, source_path=str(latest_file))


def drift_monitoring_ingestion_to_text(result: DriftMonitoringIngestionResult) -> str:
    lines = [
        f"Ingestion ID: {result.ingestion_id}",
        f"Valid for Phase 145: {result.valid_for_phase145}",
        f"Source Review ID: {result.source_review_id}",
    ]
    if result.errors:
        lines.append("Errors:")
        for err in result.errors:
            lines.append(f"  - {err}")
    if result.warnings:
        lines.append("Warnings:")
        for warn in result.warnings:
            lines.append(f"  - {warn}")
    return "\n".join(lines)
