"""Explainability Review Ingestion."""
import json
import uuid
from pathlib import Path
from typing import Any
from datetime import datetime, timezone

from .phase124_models import (
    ExplainabilityIngestionResult,
    FreezePreparationRiskFlag,
    create_explainability_ingestion_id
)

def ingest_explainability_review_payload(payload: dict[str, Any]) -> ExplainabilityIngestionResult:
    warnings = []
    risk_flags = []

    if not payload:
        return ExplainabilityIngestionResult(
            ingestion_id=create_explainability_ingestion_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            source_path=None,
            source_review_id=None,
            source_context_id=None,
            available=False,
            attribution_ready=False,
            contribution_ready=False,
            interpretation_ready=False,
            research_report_ready=False,
            report_qa_passed=False,
            ready_for_phase124=False,
            metadata_only=True,
            research_data_only=True,
            activation_allowed=False,
            strategy_activation_allowed=False,
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
            valid_for_phase124=False,
            risk_flags=[FreezePreparationRiskFlag.EXPLAINABILITY_REVIEW_MISSING],
            warnings=["Explainability review payload is empty."],
            errors=["Missing payload."]
        )

    source_review_id = payload.get("review_id")
    context = payload.get("context", {})
    source_context_id = context.get("context_id")

    ready_for_phase124 = True
    errors = []

    attribution_ready = payload.get("attribution_ready", False)
    if not attribution_ready:
        ready_for_phase124 = False
        errors.append("attribution_ready is False")

    contribution_ready = payload.get("contribution_ready", False)
    if not contribution_ready:
        ready_for_phase124 = False
        errors.append("contribution_ready is False")

    interpretation_ready = payload.get("interpretation_ready", False)
    if not interpretation_ready:
        ready_for_phase124 = False
        errors.append("interpretation_ready is False")

    research_report_ready = payload.get("research_report_ready", False)
    if not research_report_ready:
        ready_for_phase124 = False
        errors.append("research_report_ready is False")

    report_qa_passed = payload.get("report_qa_passed", False)
    if not report_qa_passed:
        ready_for_phase124 = False
        errors.append("report_qa_passed is False")

    research_data_only = payload.get("research_data_only", True)
    if not research_data_only:
        ready_for_phase124 = False
        errors.append("research_data_only is False")
        risk_flags.append(FreezePreparationRiskFlag.EXPLAINABILITY_REVIEW_INVALID)

    forbidden_true_fields = [
        "activation_allowed", "strategy_activation_allowed", "active_paper_enabled",
        "broker_execution_enabled", "order_creation_enabled", "paper_state_mutation_enabled",
        "telegram_real_send_enabled", "scraping_enabled", "html_parse_enabled",
        "paid_api_enabled", "dashboard_enabled", "network_default_enabled",
        "produces_trade_signal", "produces_order_decision", "produces_portfolio_weights",
        "investment_advice"
    ]

    for f in forbidden_true_fields:
        if payload.get(f, False):
            ready_for_phase124 = False
            errors.append(f"{f} is True")
            risk_flags.append(FreezePreparationRiskFlag.EXPLAINABILITY_REVIEW_INVALID)

    return ExplainabilityIngestionResult(
        ingestion_id=create_explainability_ingestion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_path=None,
        source_review_id=source_review_id,
        source_context_id=source_context_id,
        available=True,
        attribution_ready=attribution_ready,
        contribution_ready=contribution_ready,
        interpretation_ready=interpretation_ready,
        research_report_ready=research_report_ready,
        report_qa_passed=report_qa_passed,
        ready_for_phase124=ready_for_phase124,
        metadata_only=True,
        research_data_only=research_data_only,
        activation_allowed=payload.get("activation_allowed", False),
        strategy_activation_allowed=payload.get("strategy_activation_allowed", False),
        active_paper_enabled=payload.get("active_paper_enabled", False),
        broker_execution_enabled=payload.get("broker_execution_enabled", False),
        order_creation_enabled=payload.get("order_creation_enabled", False),
        paper_state_mutation_enabled=payload.get("paper_state_mutation_enabled", False),
        telegram_real_send_enabled=payload.get("telegram_real_send_enabled", False),
        scraping_enabled=payload.get("scraping_enabled", False),
        html_parse_enabled=payload.get("html_parse_enabled", False),
        paid_api_enabled=payload.get("paid_api_enabled", False),
        dashboard_enabled=payload.get("dashboard_enabled", False),
        network_default_enabled=payload.get("network_default_enabled", False),
        produces_trade_signal=payload.get("produces_trade_signal", False),
        produces_order_decision=payload.get("produces_order_decision", False),
        produces_portfolio_weights=payload.get("produces_portfolio_weights", False),
        investment_advice=payload.get("investment_advice", False),
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        valid_for_phase124=ready_for_phase124,
        risk_flags=risk_flags,
        warnings=warnings,
        errors=errors
    )

def ingest_latest_explainability_review_from_store(data_root: Path) -> ExplainabilityIngestionResult:
    # Phase 123 store is assumed to be in data/feature_engine/factor_explainability/reviews
    reviews_dir = data_root / "feature_engine" / "factor_explainability" / "reviews"
    if not reviews_dir.exists():
        return ingest_explainability_review_payload({})

    try:
        files = list(reviews_dir.glob("*.json"))
        if not files:
            return ingest_explainability_review_payload({})

        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        with open(latest_file, "r") as f:
            payload = json.load(f)

        res = ingest_explainability_review_payload(payload)
        res.source_path = str(latest_file)
        return res
    except Exception as e:
        res = ingest_explainability_review_payload({})
        res.errors.append(f"Failed to read store: {str(e)}")
        return res

def extract_explainability_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_research_report_payload(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("research_report")

def extract_report_qa_payload(payload: dict[str, Any]) -> list[dict[str, Any]]:
    qa = payload.get("report_qa", {})
    return qa.get("results", [])

def explainability_supports_phase124(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    res = ingest_explainability_review_payload(payload)
    return res.valid_for_phase124, res.errors

def explainability_ingestion_to_text(result: ExplainabilityIngestionResult) -> str:
    return f"Explainability Ingestion {result.ingestion_id} - Valid: {result.valid_for_phase124}"
