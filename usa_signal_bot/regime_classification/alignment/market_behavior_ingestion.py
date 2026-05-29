from typing import Any
import json
from pathlib import Path
from usa_signal_bot.regime_classification.alignment.phase131_models import (
    MarketBehaviorIngestionResult, create_market_behavior_ingestion_id, _now
)
from usa_signal_bot.core.enums import RegimeAlignmentRiskFlag

def ingest_market_behavior_review_payload(payload: dict[str, Any]) -> MarketBehaviorIngestionResult:
    supports, reasons = market_behavior_supports_phase131(payload)

    flags = []
    if not supports:
        flags.append(RegimeAlignmentRiskFlag.MARKET_BEHAVIOR_REVIEW_INVALID)
        if "ready_for_phase131 is false" in reasons:
             flags.append(RegimeAlignmentRiskFlag.PHASE130_NOT_READY)

    return MarketBehaviorIngestionResult(
        ingestion_id=create_market_behavior_ingestion_id(),
        created_at_utc=_now(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=payload.get("context", {}).get("context_id"),
        available=True,
        transition_analytics_ingested=payload.get("context", {}).get("transition_analytics_computed", False),
        diagnostics_loaded=payload.get("context", {}).get("diagnostics_loaded", False),
        profile_specs_ready=payload.get("context", {}).get("profile_specs_ready", False),
        behavior_profiles_ready=payload.get("context", {}).get("behavior_profiles_ready", False),
        regime_summaries_ready=payload.get("context", {}).get("regime_summaries_ready", False),
        diagnostics_interpreted=payload.get("context", {}).get("diagnostics_interpreted", False),
        report_built=payload.get("context", {}).get("report_built", False),
        report_qa_passed=payload.get("context", {}).get("report_qa_passed", False),
        readiness_gate_ready=payload.get("context", {}).get("readiness_gate_ready", False),
        ready_for_phase131=supports,
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
        valid_for_phase131=supports,
        risk_flags=flags,
        warnings=reasons if not supports else [],
        errors=[],
        metadata={"raw_keys": list(payload.keys())}
    )

def ingest_latest_market_behavior_review_from_store(data_root: Path) -> MarketBehaviorIngestionResult:
    reviews_dir = data_root / "regime_classification" / "behavior_reporting" / "reviews"
    if not reviews_dir.exists():
        return _empty_ingest_with_error("Reviews dir not found")

    try:
        files = sorted(list(reviews_dir.glob("*.json")))
        if not files:
             return _empty_ingest_with_error("No review files found")
        latest = files[-1]
        with open(latest, "r") as f:
            payload = json.load(f)

        res = ingest_market_behavior_review_payload(payload)
        res.source_path = str(latest)
        return res
    except Exception as e:
        return _empty_ingest_with_error(str(e))

def _empty_ingest_with_error(msg: str) -> MarketBehaviorIngestionResult:
    return MarketBehaviorIngestionResult(
        ingestion_id=create_market_behavior_ingestion_id(),
        created_at_utc=_now(),
        source_path=None, source_review_id=None, source_context_id=None,
        available=False, transition_analytics_ingested=False, diagnostics_loaded=False,
        profile_specs_ready=False, behavior_profiles_ready=False, regime_summaries_ready=False,
        diagnostics_interpreted=False, report_built=False, report_qa_passed=False,
        readiness_gate_ready=False, ready_for_phase131=False, metadata_only=True,
        research_data_only=True, activation_allowed=False, strategy_activation_allowed=False,
        deployment_allowed=False, active_paper_enabled=False, broker_execution_enabled=False,
        order_creation_enabled=False, paper_state_mutation_enabled=False, telegram_real_send_enabled=False,
        scraping_enabled=False, html_parse_enabled=False, paid_api_enabled=False,
        dashboard_enabled=False, network_default_enabled=False, model_training_used=False,
        model_prediction_used=False, heavy_ml_dependency_used=False, produces_trade_signal=False,
        produces_order_decision=False, produces_portfolio_weights=False, investment_advice=False,
        network_used=False, paid_api_used=False, scraping_used=False, html_parsing_used=False,
        broker_used=False, order_created=False, paper_state_mutated=False, telegram_real_sent=False,
        dashboard_started=False, valid_for_phase131=False,
        risk_flags=[RegimeAlignmentRiskFlag.MARKET_BEHAVIOR_REVIEW_MISSING],
        warnings=[], errors=[msg], metadata={}
    )

def extract_market_behavior_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_behavior_profiles(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("behavior_profiles", [])

def extract_regime_behavior_summaries(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("regime_summaries", [])

def extract_diagnostics_interpretations(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return payload.get("diagnostics_interpretations", [])

def extract_behavior_report_document(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("report_document")

def market_behavior_supports_phase131(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons = []
    ctx = payload.get("context", {})
    if not ctx.get("ready_for_phase131", False):
        reasons.append("ready_for_phase131 is false")
    if not ctx.get("transition_analytics_computed", False):
        reasons.append("transition_analytics_computed is false")
    if not ctx.get("behavior_profiles_ready", False):
        reasons.append("behavior_profiles_ready is false")

    if ctx.get("activation_allowed", True) or ctx.get("strategy_activation_allowed", True):
        reasons.append("activation allowed in source")
    if ctx.get("produces_trade_signal", True) or ctx.get("investment_advice", True):
        reasons.append("trade signals or investment advice allowed in source")

    return len(reasons) == 0, reasons

def market_behavior_ingestion_to_text(result: MarketBehaviorIngestionResult) -> str:
    return f"Ingestion {result.ingestion_id} - Valid: {result.valid_for_phase131} - Ready: {result.ready_for_phase131}"
