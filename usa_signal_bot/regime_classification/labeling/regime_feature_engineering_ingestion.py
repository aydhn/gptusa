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

def ingest_regime_feature_engineering_review_payload(payload: dict[str, Any], source_path: str | None = None) -> RegimeFeatureEngineeringIngestionResult:
    review_id = payload.get("review_id")
    ctx = extract_regime_feature_engineering_context(payload)

    if not ctx:
        return RegimeFeatureEngineeringIngestionResult(
            ingestion_id=create_regime_feature_engineering_ingestion_id(),
            created_at_utc=_now_utc(),
            source_path=source_path,
            source_review_id=review_id,
            source_context_id=None,
            available=False,
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
            errors=["Missing context in review payload"],
            risk_flags=[RegimeLabelingRiskFlag.REGIME_FEATURE_ENGINEERING_REVIEW_INVALID]
        )

    supports_p128, warnings = regime_feature_engineering_supports_phase128(payload)
    valid_for_phase128 = supports_p128

    risk_flags = []
    if not supports_p128:
        risk_flags.append(RegimeLabelingRiskFlag.PHASE127_NOT_READY)

    return RegimeFeatureEngineeringIngestionResult(
        ingestion_id=create_regime_feature_engineering_ingestion_id(),
        created_at_utc=_now_utc(),
        source_path=source_path,
        source_review_id=review_id,
        source_context_id=ctx.get("context_id"),
        available=True,
        foundation_ingested=ctx.get("foundation_ingested", False),
        inputs_loaded=ctx.get("inputs_loaded", False),
        metric_specs_ready=ctx.get("metric_specs_ready", False),
        feature_specs_ready=ctx.get("feature_specs_ready", False),
        metrics_computed=ctx.get("metrics_computed", False),
        feature_table_ready=ctx.get("feature_table_ready", False),
        candidates_prepared=ctx.get("candidates_prepared", False),
        candidate_readiness_gate_ready=ctx.get("candidate_readiness_gate_ready", False),
        ready_for_phase128=ctx.get("ready_for_phase128", False),
        metadata_only=ctx.get("metadata_only", True),
        research_data_only=ctx.get("research_data_only", True),
        activation_allowed=ctx.get("activation_allowed", False),
        strategy_activation_allowed=ctx.get("strategy_activation_allowed", False),
        deployment_allowed=ctx.get("deployment_allowed", False),
        active_paper_enabled=ctx.get("active_paper_enabled", False),
        broker_execution_enabled=ctx.get("broker_execution_enabled", False),
        order_creation_enabled=ctx.get("order_creation_enabled", False),
        paper_state_mutation_enabled=ctx.get("paper_state_mutation_enabled", False),
        telegram_real_send_enabled=ctx.get("telegram_real_send_enabled", False),
        scraping_enabled=ctx.get("scraping_enabled", False),
        html_parse_enabled=ctx.get("html_parse_enabled", False),
        paid_api_enabled=ctx.get("paid_api_enabled", False),
        dashboard_enabled=ctx.get("dashboard_enabled", False),
        network_default_enabled=ctx.get("network_default_enabled", False),
        model_training_used=ctx.get("model_training_used", False),
        heavy_ml_dependency_used=ctx.get("heavy_ml_dependency_used", False),
        produces_trade_signal=ctx.get("produces_trade_signal", False),
        produces_order_decision=ctx.get("produces_order_decision", False),
        produces_portfolio_weights=ctx.get("produces_portfolio_weights", False),
        investment_advice=ctx.get("investment_advice", False),
        network_used=ctx.get("network_used", False),
        paid_api_used=ctx.get("paid_api_used", False),
        scraping_used=ctx.get("scraping_used", False),
        html_parsing_used=ctx.get("html_parsing_used", False),
        broker_used=ctx.get("broker_used", False),
        order_created=ctx.get("order_created", False),
        paper_state_mutated=ctx.get("paper_state_mutated", False),
        telegram_real_sent=ctx.get("telegram_real_sent", False),
        dashboard_started=ctx.get("dashboard_started", False),
        valid_for_phase128=valid_for_phase128,
        warnings=warnings,
        risk_flags=risk_flags
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

    return RegimeFeatureEngineeringIngestionResult(
        ingestion_id=create_regime_feature_engineering_ingestion_id(),
        created_at_utc=_now_utc(),
        source_path=None,
        source_review_id=None,
        source_context_id=None,
        available=False,
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
        errors=["No regime feature engineering review found"],
        risk_flags=[RegimeLabelingRiskFlag.REGIME_FEATURE_ENGINEERING_REVIEW_MISSING]
    )

def regime_feature_engineering_ingestion_to_text(result: RegimeFeatureEngineeringIngestionResult) -> str:
    return f"Ingestion ID: {result.ingestion_id}\nValid for Phase 128: {result.valid_for_phase128}"
