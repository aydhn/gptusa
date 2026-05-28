import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import datetime

from usa_signal_bot.feature_engine.final_closure.phase125_models import (
    FreezePreparationIngestionResult,
    create_freeze_preparation_ingestion_id,
    validate_freeze_preparation_ingestion_result
)

def extract_freeze_preparation_context(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("context")

def extract_freeze_manifest_payload(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("manifest")

def extract_freeze_gate_payload(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("freeze_readiness_gate")

def freeze_preparation_supports_phase125(payload: dict[str, Any]) -> Tuple[bool, list[str]]:
    ctx = extract_freeze_preparation_context(payload)
    if not ctx:
        return False, ["Missing context in freeze preparation payload"]
    return ctx.get("ready_for_phase125", False), []

def ingest_freeze_preparation_review_payload(payload: dict[str, Any]) -> FreezePreparationIngestionResult:
    ctx = extract_freeze_preparation_context(payload) or {}

    res = FreezePreparationIngestionResult(
        ingestion_id=create_freeze_preparation_ingestion_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=ctx.get("context_id"),
        available=bool(payload),
        artifact_chain_ready=ctx.get("artifact_chain_ready", False),
        integration_rehearsal_ready=ctx.get("integration_rehearsal_ready", False),
        report_qa_accepted=ctx.get("report_qa_accepted", False),
        freeze_candidate_ready=ctx.get("freeze_candidate_ready", False),
        freeze_readiness_gate_ready=ctx.get("freeze_readiness_gate_ready", False),
        ready_for_phase125=ctx.get("ready_for_phase125", False),
        metadata_only=True,
        research_data_only=ctx.get("research_data_only", True),
        activation_allowed=ctx.get("activation_allowed", False),
        strategy_activation_allowed=ctx.get("strategy_activation_allowed", False),
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
        produces_trade_signal=ctx.get("produces_trade_signal", False),
        produces_order_decision=ctx.get("produces_order_decision", False),
        produces_portfolio_weights=ctx.get("produces_portfolio_weights", False),
        investment_advice=ctx.get("investment_advice", False),
        deployment_allowed=ctx.get("deployment_allowed", False),
        network_used=ctx.get("network_used", False),
        paid_api_used=ctx.get("paid_api_used", False),
        scraping_used=ctx.get("scraping_used", False),
        html_parsing_used=ctx.get("html_parsing_used", False),
        broker_used=ctx.get("broker_used", False),
        order_created=ctx.get("order_created", False),
        paper_state_mutated=ctx.get("paper_state_mutated", False),
        telegram_real_sent=ctx.get("telegram_real_sent", False),
        dashboard_started=ctx.get("dashboard_started", False),
        valid_for_phase125=True,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata=payload
    )

    try:
        validate_freeze_preparation_ingestion_result(res)
    except Exception as e:
        res.valid_for_phase125 = False
        res.errors.append(str(e))

    if not payload:
        res.valid_for_phase125 = False

    return res

def ingest_latest_freeze_preparation_review_from_store(data_root: Path) -> FreezePreparationIngestionResult:
    # Since Phase 124 freeze prep doesn't exist yet, we return a mock payload for test continuity if store is empty
    target_dir = data_root / "feature_engine" / "integration_freeze" / "reviews"
    if target_dir.exists():
        files = sorted([f for f in target_dir.glob("*.json")])
        if files:
            latest = files[-1]
            with open(latest, 'r') as f:
                data = json.load(f)
            res = ingest_freeze_preparation_review_payload(data)
            res.source_path = str(latest)
            return res

    return ingest_freeze_preparation_review_payload({})

def freeze_preparation_ingestion_to_text(result: FreezePreparationIngestionResult) -> str:
    return f"FreezePrepIngestion({result.ingestion_id}): Valid={result.valid_for_phase125}"
