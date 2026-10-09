from typing import Any, Optional
from pathlib import Path

from usa_signal_bot.regime_classification.labeling.phase128_models import (
    RegimeFeatureEngineeringIngestionResult,
    create_regime_feature_engineering_ingestion_id,
    _now_utc
)
from usa_signal_bot.core.enums import RegimeLabelingRiskFlag
from usa_signal_bot.core.exceptions import RegimeFeatureEngineeringIngestionError

def extract_regime_feature_engineering_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_regime_feature_tables(payload: dict[str, Any]) -> dict[str, str]:
    return payload.get("output_paths", {})

def extract_candidate_preparation(payload: dict[str, Any]) -> dict[str, Any] | None:
    ctx = extract_regime_feature_engineering_context(payload)
    if not ctx:
        return None
    return ctx.get("candidate_preparation")

def extract_candidate_readiness_gate(payload: dict[str, Any]) -> dict[str, Any] | None:
    ctx = extract_regime_feature_engineering_context(payload)
    if not ctx:
        return None
    return ctx.get("candidate_readiness_gate")

def regime_feature_engineering_supports_phase128(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    warnings = []

    ctx = extract_regime_feature_engineering_context(payload)
    if not ctx:
        return False, ["Missing context in review payload"]

    if not ctx.get("ready_for_phase128", False):
        return False, ["ready_for_phase128 is not True"]

    if not ctx.get("research_data_only", True):
        warnings.append("research_data_only is not True")
        return False, warnings

    if ctx.get("activation_allowed", False):
        return False, ["activation_allowed is True"]

    if ctx.get("strategy_activation_allowed", False):
        return False, ["strategy_activation_allowed is True"]

    if ctx.get("deployment_allowed", False):
        return False, ["deployment_allowed is True"]

    return True, warnings

def _create_default_result(
    source_path: str | None = None,
    source_review_id: str | None = None,
    source_context_id: str | None = None,
    available: bool = False,
    errors: list[str] | None = None,
    risk_flags: list[RegimeLabelingRiskFlag] | None = None,
    warnings: list[str] | None = None,
    **kwargs
) -> RegimeFeatureEngineeringIngestionResult:
    defaults = dict(
        ingestion_id=create_regime_feature_engineering_ingestion_id(),
        created_at_utc=_now_utc(),
        source_path=source_path,
        source_review_id=source_review_id,
        source_context_id=source_context_id,
        available=available,
        foundation_ingested=False,
        inputs_loaded=False,
        metric_specs_ready=False,
        feature_specs_ready=False,
        metrics_computed=False,
        feature_table_ready=False,
        candidates_prepared=False,
        candidate_readiness_gate_ready=False,
        ready_for_phase128=False,
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
        valid_for_phase128=False,
        errors=errors or [],
        risk_flags=risk_flags or [],
        warnings=warnings or []
    )
    defaults.update(kwargs)
    return RegimeFeatureEngineeringIngestionResult(**defaults)

def ingest_regime_feature_engineering_review_payload(payload: dict[str, Any], source_path: str | None = None) -> RegimeFeatureEngineeringIngestionResult:
    review_id = payload.get("review_id")
    ctx = extract_regime_feature_engineering_context(payload)

    if not ctx:
        return _create_default_result(
            source_path=source_path,
            source_review_id=review_id,
            errors=["Missing context in review payload"],
            risk_flags=[RegimeLabelingRiskFlag.REGIME_FEATURE_ENGINEERING_REVIEW_INVALID]
        )

    supports_p128, warnings = regime_feature_engineering_supports_phase128(payload)

    risk_flags = []
    if not supports_p128:
        risk_flags.append(RegimeLabelingRiskFlag.PHASE127_NOT_READY)

    kwargs = {
        k: ctx.get(k, False) for k in [
            "foundation_ingested", "inputs_loaded", "metric_specs_ready", "feature_specs_ready",
            "metrics_computed", "feature_table_ready", "candidates_prepared", "candidate_readiness_gate_ready",
            "ready_for_phase128", "activation_allowed", "strategy_activation_allowed", "deployment_allowed",
            "active_paper_enabled", "broker_execution_enabled", "order_creation_enabled", "paper_state_mutation_enabled",
            "telegram_real_send_enabled", "scraping_enabled", "html_parse_enabled", "paid_api_enabled",
            "dashboard_enabled", "network_default_enabled", "model_training_used", "heavy_ml_dependency_used",
            "produces_trade_signal", "produces_order_decision", "produces_portfolio_weights", "investment_advice",
            "network_used", "paid_api_used", "scraping_used", "html_parsing_used", "broker_used",
            "order_created", "paper_state_mutated", "telegram_real_sent", "dashboard_started"
        ]
    }
    kwargs["metadata_only"] = ctx.get("metadata_only", True)
    kwargs["research_data_only"] = ctx.get("research_data_only", True)

    return _create_default_result(
        source_path=source_path,
        source_review_id=review_id,
        source_context_id=ctx.get("context_id"),
        available=True,
        valid_for_phase128=supports_p128,
        warnings=warnings,
        risk_flags=risk_flags,
        **kwargs
    )

def ingest_latest_regime_feature_engineering_review_from_store(data_root: Path) -> RegimeFeatureEngineeringIngestionResult:
    # Note: normally we would read from data_root / "regime_classification" / "feature_engineering" / "reviews"
    # But since this is a local mock, we'll try to find any file or return unavailable
    import json

    review_dir = data_root / "regime_classification" / "feature_engineering" / "reviews"
    if review_dir.exists() and review_dir.is_dir():
        files = list(review_dir.glob("*.json"))
        if files:
            files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            latest = files[0]
            try:
                with open(latest, "r") as f:
                    payload = json.load(f)
                return ingest_regime_feature_engineering_review_payload(payload, source_path=str(latest))
            except Exception as e:
                pass

    return _create_default_result(
        errors=["No regime feature engineering review found"],
        risk_flags=[RegimeLabelingRiskFlag.REGIME_FEATURE_ENGINEERING_REVIEW_MISSING]
    )

def regime_feature_engineering_ingestion_to_text(result: RegimeFeatureEngineeringIngestionResult) -> str:
    return f"Ingestion ID: {result.ingestion_id}\nValid for Phase 128: {result.valid_for_phase128}"
