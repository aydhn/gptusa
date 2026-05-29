import json
from pathlib import Path
from typing import Any

from usa_signal_bot.core.enums import MarketBehaviorRiskFlag
from usa_signal_bot.core.exceptions import RegimeTransitionIngestionError
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    RegimeTransitionIngestionResult
)

def ingest_regime_transition_review_payload(payload: dict[str, Any]) -> RegimeTransitionIngestionResult:
    res = RegimeTransitionIngestionResult()
    res.available = True

    ctx = extract_regime_transition_context(payload)
    if not ctx:
        res.valid_for_phase130 = False
        res.risk_flags.append(MarketBehaviorRiskFlag.REGIME_TRANSITION_REVIEW_MISSING)
        res.errors.append("Transition review context missing in payload.")
        return res

    res.source_review_id = payload.get("review_id")
    res.source_context_id = ctx.get("context_id")

    res.labeling_ingested = ctx.get("labeling_ingested", False)
    res.sequences_loaded = ctx.get("sequences_loaded", False)
    res.transition_matrix_built = ctx.get("transition_matrix_built", False)
    res.persistence_analytics_built = ctx.get("persistence_analytics_built", False)
    res.duration_analytics_built = ctx.get("duration_analytics_built", False)
    res.churn_diagnostics_built = ctx.get("churn_diagnostics_built", False)
    res.stability_diagnostics_built = ctx.get("stability_diagnostics_built", False)
    res.readiness_gate_ready = ctx.get("readiness_gate_ready", False)
    res.ready_for_phase130 = ctx.get("ready_for_phase130", False)

    # Flags mapping
    res.metadata_only = ctx.get("metadata_only", True)
    res.research_data_only = ctx.get("research_data_only", True)
    res.activation_allowed = ctx.get("activation_allowed", False)
    res.strategy_activation_allowed = ctx.get("strategy_activation_allowed", False)
    res.deployment_allowed = ctx.get("deployment_allowed", False)
    res.active_paper_enabled = ctx.get("active_paper_enabled", False)
    res.broker_execution_enabled = ctx.get("broker_execution_enabled", False)
    res.order_creation_enabled = ctx.get("order_creation_enabled", False)
    res.paper_state_mutation_enabled = ctx.get("paper_state_mutation_enabled", False)
    res.telegram_real_send_enabled = ctx.get("telegram_real_send_enabled", False)
    res.scraping_enabled = ctx.get("scraping_enabled", False)
    res.html_parse_enabled = ctx.get("html_parse_enabled", False)
    res.paid_api_enabled = ctx.get("paid_api_enabled", False)
    res.dashboard_enabled = ctx.get("dashboard_enabled", False)
    res.network_default_enabled = ctx.get("network_default_enabled", False)
    res.model_training_used = ctx.get("model_training_used", False)
    res.model_prediction_used = ctx.get("model_prediction_used", False)
    res.heavy_ml_dependency_used = ctx.get("heavy_ml_dependency_used", False)
    res.produces_trade_signal = ctx.get("produces_trade_signal", False)
    res.produces_order_decision = ctx.get("produces_order_decision", False)
    res.produces_portfolio_weights = ctx.get("produces_portfolio_weights", False)
    res.investment_advice = ctx.get("investment_advice", False)

    valid, errors = regime_transition_supports_phase130(payload)
    if not valid:
        res.valid_for_phase130 = False
        res.errors.extend(errors)
        res.risk_flags.append(MarketBehaviorRiskFlag.REGIME_TRANSITION_REVIEW_INVALID)
    else:
        res.valid_for_phase130 = True

    return res

def ingest_latest_regime_transition_review_from_store(data_root: Path) -> RegimeTransitionIngestionResult:
    review_dir = data_root / "regime_classification" / "transition_analytics" / "reviews"
    if not review_dir.exists():
        return RegimeTransitionIngestionResult(available=False, valid_for_phase130=False, errors=["review_dir not found."])

    files = list(review_dir.glob("*.json"))
    if not files:
        return RegimeTransitionIngestionResult(available=False, valid_for_phase130=False, errors=["No transition review files found."])

    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    latest_file = files[0]
    try:
        with open(latest_file, "r") as f:
            payload = json.load(f)
        res = ingest_regime_transition_review_payload(payload)
        res.source_path = str(latest_file)
        return res
    except Exception as e:
        raise RegimeTransitionIngestionError(f"Failed to read payload: {e}")

def extract_regime_transition_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_transition_matrices(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("transition_matrices", [])

def extract_persistence_profiles(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("persistence_profiles", [])

def extract_churn_diagnostics(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("churn_diagnostics", [])

def extract_stability_diagnostics(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("stability_diagnostics", [])

def regime_transition_supports_phase130(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    ctx = payload.get("context", {})
    errs = []

    if not ctx.get("labeling_ingested"): errs.append("labeling_ingested is False.")
    if not ctx.get("transition_matrix_built"): errs.append("transition_matrix_built is False.")
    if not ctx.get("persistence_analytics_built"): errs.append("persistence_analytics_built is False.")
    if not ctx.get("duration_analytics_built"): errs.append("duration_analytics_built is False.")
    if not ctx.get("churn_diagnostics_built"): errs.append("churn_diagnostics_built is False.")
    if not ctx.get("stability_diagnostics_built"): errs.append("stability_diagnostics_built is False.")
    if not ctx.get("readiness_gate_ready"): errs.append("readiness_gate_ready is False.")
    if not ctx.get("ready_for_phase130"): errs.append("ready_for_phase130 is False.")

    if not ctx.get("research_data_only", True): errs.append("research_data_only is False.")

    bad_flags = [
        "activation_allowed", "strategy_activation_allowed", "deployment_allowed",
        "broker_execution_enabled", "order_creation_enabled", "paper_state_mutation_enabled",
        "telegram_real_send_enabled", "scraping_enabled", "html_parse_enabled",
        "paid_api_enabled", "dashboard_enabled", "network_default_enabled",
        "produces_trade_signal", "produces_order_decision", "produces_portfolio_weights",
        "investment_advice", "model_training_used", "model_prediction_used", "heavy_ml_dependency_used"
    ]
    for flag in bad_flags:
        if ctx.get(flag):
            errs.append(f"{flag} must be False.")

    return len(errs) == 0, errs

def regime_transition_ingestion_to_text(result: RegimeTransitionIngestionResult) -> str:
    lines = [
        f"Ingestion ID: {result.ingestion_id}",
        f"Available: {result.available}",
        f"Valid for Phase 130: {result.valid_for_phase130}",
        f"Errors: {len(result.errors)}"
    ]
    return "\n".join(lines)
