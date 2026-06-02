import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import json
from .phase147_models import (
    BacktestFoundationIngestionResult, create_backtest_foundation_ingestion_id, BacktestRunRiskFlag
)
from usa_signal_bot.core.exceptions import BacktestFoundationIngestionError

def ingest_backtest_foundation_review_payload(payload: Dict[str, Any]) -> BacktestFoundationIngestionResult:
    import json
    gate = extract_backtest_readiness_gate(payload)
    ready = False
    if gate and gate.get("status") == "PASSED" and gate.get("ready_for_phase147", False):
        ready = True

    valid_phase147, flags = backtest_foundation_supports_phase147(payload)

    return BacktestFoundationIngestionResult(
        ingestion_id=create_backtest_foundation_ingestion_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=None,
        available=True,
        advanced_ml_closure_ingested=True,
        inputs_resolved=True,
        dataset_contract_built=payload.get("dataset_contract_enabled", True),
        research_input_boundary_built=True,
        event_timeline_built=True,
        execution_assumptions_built=True,
        transaction_cost_model_built=True,
        commission_model_built=True,
        spread_model_built=True,
        slippage_model_built=True,
        liquidity_guard_built=True,
        partial_fill_assumptions_built=True,
        execution_latency_assumptions_built=True,
        market_simulation_contract_built=True,
        safety_boundary_validated=True,
        readiness_gate_built=True,
        readiness_gate_passed=ready,
        ready_for_phase147=ready,
        research_data_only=True,
        offline_backtest_research_only=True,
        live_trading_enabled=False,
        paper_trading_enabled=False,
        broker_execution_enabled=False,
        order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        strategy_activation_allowed=False,
        portfolio_allocation_allowed=False,
        deployment_allowed=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        dashboard_started=False,
        daemon_started=False,
        scheduler_enabled=False,
        full_backtest_run_executed=False,
        walk_forward_executed=False,
        stress_test_executed=False,
        monte_carlo_executed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        valid_for_phase147=valid_phase147,
        risk_flags=[BacktestRunRiskFlag(f) for f in flags],
        warnings=[],
        errors=[],
        metadata={}
    )

def ingest_latest_backtest_foundation_review_from_store(data_root: Path) -> BacktestFoundationIngestionResult:
    review_path = data_root / "backtesting/foundation/reviews/latest_review.json"
    if not review_path.exists():
        raise BacktestFoundationIngestionError(f"Review not found at {review_path}")
    with open(review_path, "r") as f:
        payload = json.load(f)
    result = ingest_backtest_foundation_review_payload(payload)
    result.source_path = str(review_path)
    return result

def extract_backtest_foundation_context(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("context")

def extract_backtest_readiness_gate(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("readiness_gate")

def extract_backtest_safety_boundary(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("safety_boundary")

def extract_dataset_contract(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    ctx = extract_backtest_foundation_context(payload)
    if ctx: return ctx.get("dataset_contract")
    return None

def extract_research_input_contract(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    ctx = extract_backtest_foundation_context(payload)
    if ctx: return ctx.get("research_input_boundary")
    return None

def extract_market_simulation_contract(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    ctx = extract_backtest_foundation_context(payload)
    if ctx: return ctx.get("market_simulation_contract")
    return None

def backtest_foundation_supports_phase147(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    flags = []
    ready = True
    gate = extract_backtest_readiness_gate(payload)
    if not gate or not gate.get("ready_for_phase147", False):
        flags.append("PHASE146_NOT_READY")
        ready = False
    saf = extract_backtest_safety_boundary(payload)
    if not saf or not saf.get("boundary_passed", False):
        flags.append("FOUNDATION_SAFETY_BOUNDARY_FAILED")
        ready = False
    if not extract_dataset_contract(payload) or not extract_market_simulation_contract(payload):
        flags.append("BACKTEST_FOUNDATION_REVIEW_INVALID")
        ready = False
    return ready, flags

def backtest_foundation_ingestion_to_text(result: BacktestFoundationIngestionResult) -> str:
    return f"Ingestion {result.ingestion_id} - valid_for_phase147: {result.valid_for_phase147}"
