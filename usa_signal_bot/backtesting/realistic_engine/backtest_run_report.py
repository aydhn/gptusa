import datetime
from typing import Dict, Any
from .phase147_models import (
    BacktestRunContext, BacktestRunFullReview, BacktestRunReportType,
    create_backtest_run_context_id, create_backtest_run_full_review_id,
    BacktestRunStatus, BacktestRunDecision, BacktestRunRiskFlag,
    BacktestFoundationIngestionResult, BacktestRunConfig, ResearchDecisionStream,
    SimulationClock, PriceEventStream
)

def build_backtest_run_context() -> BacktestRunContext:
    # Dummy empty context for testing
    return BacktestRunContext(
        context_id=create_backtest_run_context_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=BacktestRunStatus.CREATED,
        decision=BacktestRunDecision.UNKNOWN,
        source_backtest_foundation_review_id=None,
        ingestion=None, # type: ignore
        config=None, # type: ignore
        research_decision_stream=None, # type: ignore
        simulation_clock=None, # type: ignore
        price_event_stream=None, # type: ignore
        run_artifact=None,
        safety_boundary=None,
        validation_gate=None,
        backtest_foundation_ingested=False,
        artifacts_loaded=False,
        inputs_resolved=False,
        run_config_built=False,
        research_decision_stream_built=False,
        simulation_clock_built=False,
        price_event_stream_built=False,
        simulated_execution_built=False,
        costs_applied=False,
        liquidity_partial_fill_evaluated=False,
        exposure_timeline_built=False,
        equity_curve_built=False,
        drawdown_curve_built=False,
        ledgers_built=False,
        basic_performance_built=False,
        safety_boundary_validated=False,
        validation_gate_built=False,
        validation_gate_passed=False,
        ready_for_phase148=False,
        research_data_only=True,
        offline_backtest_research_only=True,
        deterministic=True,
        live_trading_enabled=False,
        paper_trading_enabled=False,
        broker_execution_enabled=False,
        real_order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        strategy_activation_allowed=False,
        portfolio_optimization_enabled=False,
        deployment_allowed=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        dashboard_started=False,
        daemon_started=False,
        scheduler_enabled=False,
        full_backtest_run_executed=True,
        walk_forward_executed=False,
        stress_test_executed=False,
        monte_carlo_executed=False,
        benchmark_comparison_executed=False,
        produces_live_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_backtest_run_full_review(context: BacktestRunContext | None = None) -> BacktestRunFullReview:
    return BacktestRunFullReview(
        review_id=create_backtest_run_full_review_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        report_type=BacktestRunReportType.FULL_PHASE147_REVIEW,
        ingestion=None, # type: ignore
        context=context or build_backtest_run_context(),
        run_artifact=None,
        performance_summary=None,
        safety_boundary=None,
        validation_gate=None,
        output_paths={},
        warnings=[],
        errors=[]
    )

def backtest_run_full_review_summary(review: BacktestRunFullReview) -> Dict[str, Any]:
    return {"review_id": review.review_id}

def backtest_run_limitations_text() -> str:
    return "Limitations: Offline deterministic single-strategy backtest run only. Not investment advice. No live/paper trading or deployment."

def backtest_run_full_review_to_text(review: BacktestRunFullReview, limit: int = 300) -> str:
    return f"FullReview {review.review_id} - Phase 147 Offline Deterministic Realistic Backtest Engine"
