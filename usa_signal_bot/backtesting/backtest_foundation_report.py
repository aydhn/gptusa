from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    BacktestFoundationContext,
    BacktestFoundationFullReview,
    create_backtest_foundation_context_id,
    create_backtest_foundation_full_review_id
)
from usa_signal_bot.core.enums import (
    BacktestFoundationStatus,
    BacktestFoundationDecision,
    BacktestFoundationReportType
)

def _build_foundation_components() -> dict[str, Any]:
    from usa_signal_bot.backtesting.advanced_ml_closure_ingestion import _empty_ingestion_result
    from usa_signal_bot.backtesting.backtest_dataset_contract import build_default_backtest_dataset_contract
    from usa_signal_bot.backtesting.research_input_boundary import build_backtest_research_input_contract
    from usa_signal_bot.backtesting.backtest_event_timeline import build_default_backtest_event_timeline
    from usa_signal_bot.backtesting.execution_assumptions import build_default_execution_assumption
    from usa_signal_bot.backtesting.transaction_cost_model import build_default_transaction_cost_model
    from usa_signal_bot.backtesting.commission_model import build_default_commission_model
    from usa_signal_bot.backtesting.spread_model import build_default_spread_model
    from usa_signal_bot.backtesting.slippage_model import build_default_slippage_model
    from usa_signal_bot.backtesting.liquidity_guard import build_default_liquidity_guard
    from usa_signal_bot.backtesting.partial_fill_assumptions import build_default_partial_fill_assumption
    from usa_signal_bot.backtesting.execution_latency_assumptions import build_default_execution_latency_assumption
    from usa_signal_bot.backtesting.market_simulation_contract import build_market_simulation_contract
    from usa_signal_bot.backtesting.backtest_safety_boundary import build_backtest_safety_boundary_rules, build_backtest_safety_boundary_result
    from usa_signal_bot.backtesting.backtest_readiness_gate import build_backtest_readiness_gate

    ingestion = _empty_ingestion_result(["DUMMY INGESTION"])
    inputs = []
    ds_contract = build_default_backtest_dataset_contract(inputs)
    rin_contract = build_backtest_research_input_contract()
    timeline = build_default_backtest_event_timeline()
    exec_asm = build_default_execution_assumption()
    tx_cost = build_default_transaction_cost_model()
    comm = build_default_commission_model()
    spread = build_default_spread_model()
    slip = build_default_slippage_model()
    liq = build_default_liquidity_guard()
    pfill = build_default_partial_fill_assumption()
    lat = build_default_execution_latency_assumption()
    mkt = build_market_simulation_contract(ds_contract, timeline, exec_asm, tx_cost, comm, spread, slip, liq, pfill, lat)

    s_rules = build_backtest_safety_boundary_rules()
    s_bound = build_backtest_safety_boundary_result(s_rules)

    r_gate = build_backtest_readiness_gate(ingestion, ds_contract, rin_contract, mkt, s_bound)

    return {
        "ingestion": ingestion,
        "input_references": inputs,
        "dataset_contract": ds_contract,
        "research_input_contract": rin_contract,
        "event_timeline": timeline,
        "execution_assumption": exec_asm,
        "transaction_cost_model": tx_cost,
        "commission_model": comm,
        "spread_model": spread,
        "slippage_model": slip,
        "liquidity_guard": liq,
        "partial_fill_assumption": pfill,
        "execution_latency_assumption": lat,
        "market_simulation_contract": mkt,
        "safety_boundary": s_bound,
        "readiness_gate": r_gate,
    }

def _get_default_foundation_flags() -> dict[str, Any]:
    return {
        "advanced_ml_closure_ingested": False,
        "artifacts_loaded": False,
        "inputs_resolved": False,
        "dataset_contract_built": False,
        "research_input_boundary_built": False,
        "event_timeline_built": False,
        "execution_assumptions_built": False,
        "transaction_cost_model_built": False,
        "commission_model_built": False,
        "spread_model_built": False,
        "slippage_model_built": False,
        "liquidity_guard_built": False,
        "partial_fill_assumptions_built": False,
        "execution_latency_assumptions_built": False,
        "market_simulation_contract_built": False,
        "safety_boundary_validated": False,
        "readiness_gate_built": False,
        "readiness_gate_passed": False,
        "ready_for_phase147": False,
        "research_data_only": True,
        "offline_backtest_research_only": True,
        "live_trading_enabled": False,
        "paper_trading_enabled": False,
        "broker_execution_enabled": False,
        "order_creation_enabled": False,
        "paper_state_mutation_enabled": False,
        "telegram_real_send_enabled": False,
        "strategy_activation_allowed": False,
        "portfolio_allocation_allowed": False,
        "deployment_allowed": False,
        "network_used": False,
        "paid_api_used": False,
        "scraping_used": False,
        "html_parsing_used": False,
        "dashboard_started": False,
        "daemon_started": False,
        "scheduler_enabled": False,
        "full_backtest_run_executed": False,
        "walk_forward_executed": False,
        "stress_test_executed": False,
        "monte_carlo_executed": False,
        "produces_trade_signal": False,
        "produces_order_decision": False,
        "produces_portfolio_weights": False,
        "investment_advice": False,
        "warnings": [],
        "errors": [],
        "risk_flags": [],
        "metadata": {},
    }

def build_backtest_foundation_context() -> BacktestFoundationContext:
    # Build a stub/empty context. Actual usage will populate this via a workflow.
    # We satisfy imports to show we build it.

    components = _build_foundation_components()
    flags = _get_default_foundation_flags()

    return BacktestFoundationContext(
        context_id=create_backtest_foundation_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=BacktestFoundationStatus.CREATED,
        decision=BacktestFoundationDecision.UNKNOWN,
        source_advanced_ml_closure_review_id=None,
        **components,
        **flags
    )

def build_backtest_foundation_full_review() -> BacktestFoundationFullReview:
    ctx = build_backtest_foundation_context()
    return BacktestFoundationFullReview(
        review_id=create_backtest_foundation_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=BacktestFoundationReportType.FULL_PHASE146_REVIEW,
        ingestion=ctx.ingestion,
        context=ctx,
        dataset_contract=ctx.dataset_contract,
        research_input_contract=ctx.research_input_contract,
        market_simulation_contract=ctx.market_simulation_contract,
        safety_boundary=ctx.safety_boundary,
        readiness_gate=ctx.readiness_gate,
        output_paths={},
        warnings=[],
        errors=[]
    )

def backtest_foundation_full_review_summary(review: BacktestFoundationFullReview) -> dict[str, Any]:
    return {"valid": len(review.errors) == 0, "ready": review.readiness_gate.ready_for_phase147}

def backtest_foundation_limitations_text() -> str:
    return "Phase 146 is a foundation setup only. It does not perform actual backtesting, paper trading, live execution, or deployment."

def backtest_foundation_full_review_to_text(review: BacktestFoundationFullReview, limit: int = 300) -> str:
    return f"BacktestFoundationReview(ready={review.readiness_gate.ready_for_phase147}, errors={len(review.errors)})"
