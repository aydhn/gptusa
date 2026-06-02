from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from usa_signal_bot.backtesting.phase146_models import (
    AdvancedMLClosureIngestionResult,
    create_advanced_ml_closure_ingestion_id
)
from usa_signal_bot.core.enums import BacktestFoundationRiskFlag

def ingest_advanced_ml_closure_review_payload(payload: dict[str, Any]) -> AdvancedMLClosureIngestionResult:
    is_valid, warnings = advanced_ml_closure_supports_phase146(payload)

    # We enforce strict defaults from payload.
    activation_allowed = payload.get("activation_allowed", False)
    ready_for_phase146 = payload.get("ready_for_phase146", False)
    phase136_to_145_closed = payload.get("phase136_to_145_closed", False)
    acceptance_gate_passed = payload.get("acceptance_gate_passed", False)
    research_data_only = payload.get("research_data_only", True)
    offline_ml_research_only = payload.get("offline_ml_research_only", True)

    risk_flags = []
    if not ready_for_phase146:
        risk_flags.append(BacktestFoundationRiskFlag.PHASE145_NOT_READY)
    if not acceptance_gate_passed:
        risk_flags.append(BacktestFoundationRiskFlag.ACCEPTANCE_GATE_FAILED)
    if not is_valid:
        risk_flags.append(BacktestFoundationRiskFlag.ADVANCED_ML_CLOSURE_REVIEW_INVALID)

    return AdvancedMLClosureIngestionResult(
        ingestion_id=create_advanced_ml_closure_ingestion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_path=payload.get("source_path"),
        source_review_id=payload.get("review_id"),
        source_context_id=payload.get("context_id"),
        available=True,
        drift_monitoring_ingested=payload.get("drift_monitoring_ingested", False),
        explainability_report_built=payload.get("explainability_report_built", False),
        artifact_lineage_built=payload.get("artifact_lineage_built", False),
        ml_governance_closure_built=payload.get("ml_governance_closure_built", False),
        advanced_ml_final_audit_built=payload.get("advanced_ml_final_audit_built", False),
        non_activation_boundary_validated=payload.get("non_activation_boundary_validated", False),
        final_model_cards_updated=payload.get("final_model_cards_updated", False),
        acceptance_gate_built=payload.get("acceptance_gate_built", False),
        acceptance_gate_passed=acceptance_gate_passed,
        ready_for_phase146=ready_for_phase146,
        phase136_to_145_closed=phase136_to_145_closed,
        research_data_only=research_data_only,
        offline_ml_research_only=offline_ml_research_only,
        activation_allowed=activation_allowed,
        strategy_activation_allowed=payload.get("strategy_activation_allowed", False),
        deployment_allowed=payload.get("deployment_allowed", False),
        broker_execution_enabled=payload.get("broker_execution_enabled", payload.get("paper_trading_enabled", False)),
        order_creation_enabled=payload.get("order_creation_enabled", False),
        paper_state_mutation_enabled=payload.get("paper_state_mutation_enabled", False),
        telegram_real_send_enabled=payload.get("telegram_real_send_enabled", False),
        scraping_enabled=payload.get("scraping_enabled", False),
        html_parse_enabled=payload.get("html_parse_enabled", False),
        paid_api_enabled=payload.get("paid_api_enabled", False),
        dashboard_enabled=payload.get("dashboard_enabled", False),
        network_default_enabled=payload.get("network_default_enabled", False),
        daemon_started=payload.get("daemon_started", False),
        scheduler_enabled=payload.get("scheduler_enabled", False),
        live_inference_enabled=payload.get("live_inference_enabled", payload.get("live_trading_enabled", False)),
        online_inference_enabled=payload.get("online_inference_enabled", False),
        live_monitoring_enabled=payload.get("live_monitoring_enabled", False),
        backtest_executed=payload.get("backtest_executed", False),
        produces_trade_signal=payload.get("produces_trade_signal", False),
        produces_order_decision=payload.get("produces_order_decision", False),
        produces_portfolio_weights=payload.get("produces_portfolio_weights", False),
        investment_advice=payload.get("investment_advice", False),
        valid_for_phase146=is_valid,
        risk_flags=risk_flags,
        warnings=warnings,
        errors=[],
        metadata={"ingested_keys": list(payload.keys())}
    )

def ingest_latest_advanced_ml_closure_review_from_store(data_root: Path) -> AdvancedMLClosureIngestionResult:
    # Example logic matching requirements.
    # Read the latest json from data/ml_research/ml_governance_closure/reviews/
    store_dir = data_root / "data" / "ml_research" / "ml_governance_closure" / "reviews"
    if not store_dir.exists():
        return _empty_ingestion_result(["No ML closure reviews directory found."])

    files = list(store_dir.glob("*.json"))
    if not files:
        return _empty_ingestion_result(["No ML closure reviews found in store."])

    latest_file = max(files, key=lambda f: f.stat().st_mtime)
    try:
        with open(latest_file, "r") as f:
            payload = json.load(f)
        payload["source_path"] = str(latest_file)
        return ingest_advanced_ml_closure_review_payload(payload)
    except Exception as e:
        return _empty_ingestion_result([f"Failed to load ML closure review: {str(e)}"])

def _empty_ingestion_result(errors: list[str]) -> AdvancedMLClosureIngestionResult:
    return AdvancedMLClosureIngestionResult(
        ingestion_id=create_advanced_ml_closure_ingestion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_path=None, source_review_id=None, source_context_id=None,
        available=False, drift_monitoring_ingested=False, explainability_report_built=False,
        artifact_lineage_built=False, ml_governance_closure_built=False, advanced_ml_final_audit_built=False,
        non_activation_boundary_validated=False, final_model_cards_updated=False, acceptance_gate_built=False,
        acceptance_gate_passed=False, ready_for_phase146=False, phase136_to_145_closed=False,
        research_data_only=False, offline_ml_research_only=False, activation_allowed=True,
        strategy_activation_allowed=True, deployment_allowed=True, broker_execution_enabled=True,
        order_creation_enabled=True, paper_state_mutation_enabled=True, telegram_real_send_enabled=True,
        scraping_enabled=True, html_parse_enabled=True, paid_api_enabled=True, dashboard_enabled=True,
        network_default_enabled=True, daemon_started=True, scheduler_enabled=True, live_inference_enabled=True,
        online_inference_enabled=True, live_monitoring_enabled=True, backtest_executed=True,
        produces_trade_signal=True, produces_order_decision=True, produces_portfolio_weights=True,
        investment_advice=True, valid_for_phase146=False, risk_flags=[BacktestFoundationRiskFlag.ADVANCED_ML_CLOSURE_REVIEW_MISSING],
        warnings=[], errors=errors, metadata={}
    )

def extract_advanced_ml_closure_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_advanced_ml_acceptance_gate(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("acceptance_gate")

def extract_advanced_ml_final_audit(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("final_audit")

def extract_non_activation_ml_boundary(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("non_activation_boundary")

def advanced_ml_closure_supports_phase146(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    warnings = []
    if not payload.get("ready_for_phase146", False):
        warnings.append("ready_for_phase146 is False or missing.")
    if not payload.get("phase136_to_145_closed", False):
        warnings.append("phase136_to_145_closed is False or missing.")
    if not payload.get("acceptance_gate_passed", False):
        warnings.append("acceptance_gate_passed is False or missing.")
    if not payload.get("research_data_only", False):
        warnings.append("research_data_only is False or missing.")
    if not payload.get("offline_ml_research_only", False):
        warnings.append("offline_ml_research_only is False or missing.")

    # Check violations
    violations = [
        "activation_allowed", "strategy_activation_allowed", "deployment_allowed",
        "paper_trading_enabled", "broker_execution_enabled", "order_creation_enabled", "paper_state_mutation_enabled",
        "telegram_real_send_enabled", "scraping_enabled", "html_parse_enabled",
        "paid_api_enabled", "dashboard_enabled", "network_default_enabled",
        "daemon_started", "scheduler_enabled", "live_trading_enabled", "live_inference_enabled",
        "online_inference_enabled", "live_monitoring_enabled", "backtest_executed",
        "produces_trade_signal", "produces_order_decision", "produces_portfolio_weights",
        "investment_advice"
    ]
    for v in violations:
        if payload.get(v, False):
            warnings.append(f"{v} is True, which violates Phase 146 policies.")

    is_valid = len(warnings) == 0
    return is_valid, warnings

def advanced_ml_closure_ingestion_to_text(result: AdvancedMLClosureIngestionResult) -> str:
    return f"AdvancedMLClosureIngestionResult(valid={result.valid_for_phase146}, ready_for_phase146={result.ready_for_phase146})"
