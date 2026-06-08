from typing import Any, Dict
from usa_signal_bot.portfolio.construction.phase155_models import (
    PortfolioConstructionContext,
    PortfolioConstructionFullReview,
    PortfolioConstructionReportType,
    PortfolioConstructionStatus,
    PortfolioConstructionDecision,
    create_portfolio_construction_context_id,
    create_portfolio_construction_full_review_id,
    _now_str
)

def build_portfolio_construction_context() -> PortfolioConstructionContext:
    from usa_signal_bot.portfolio.construction.sizing_prototype_ingestion import ingest_sizing_prototype_review_payload

    return PortfolioConstructionContext(
        context_id=create_portfolio_construction_context_id(),
        created_at_utc=_now_str(),
        status=PortfolioConstructionStatus.CREATED,
        decision=PortfolioConstructionDecision.UNKNOWN,
        source_sizing_prototype_review_id=None,
        ingestion=ingest_sizing_prototype_review_payload({}),
        input_references=[],
        candidates=[],
        policy=None,
        method_contracts=[],
        scores=[],
        allocation_results=[],
        exposure_table=None,
        diagnostics=[],
        comparison_report=None,
        validation_report=None,
        safety_boundary=None,
        phase156_readiness_gate=None,
        sizing_prototype_ingested=False,
        artifacts_loaded=False,
        inputs_resolved=False,
        sandbox_candidates_built=False,
        construction_policy_built=False,
        method_contracts_built=False,
        constraint_aware_scores_built=False,
        equal_sandbox_allocation_built=False,
        sizing_score_sandbox_allocation_built=False,
        risk_budget_sandbox_allocation_built=False,
        robustness_sandbox_allocation_built=False,
        constraint_normalization_built=False,
        prototype_exposure_table_built=False,
        diversification_diagnostics_built=False,
        concentration_diagnostics_built=False,
        turnover_diagnostics_built=False,
        constraint_breach_diagnostics_built=False,
        risk_budget_sandbox_diagnostics_built=False,
        allocation_comparison_report_built=False,
        construction_validation_report_built=False,
        safety_boundary_validated=False,
        phase156_readiness_gate_built=False,
        phase156_readiness_gate_passed=False,
        ready_for_phase156=False,
        research_data_only=True,
        allocation_sandbox_only=True,
        deterministic=True,
        live_trading_enabled=False,
        paper_trading_enabled=False,
        broker_execution_enabled=False,
        real_order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        strategy_activation_allowed=False,
        actual_target_weights_produced=False,
        actual_portfolio_weights_produced=False,
        actual_allocation_produced=False,
        actual_position_size_produced=False,
        order_size_produced=False,
        capital_deployment_allowed=False,
        portfolio_optimization_enabled=False,
        rebalancing_execution_enabled=False,
        deployment_allowed=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        dashboard_started=False,
        daemon_started=False,
        scheduler_enabled=False,
        produces_live_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_portfolio_construction_full_review(context: PortfolioConstructionContext) -> PortfolioConstructionFullReview:
    return PortfolioConstructionFullReview(
        review_id=create_portfolio_construction_full_review_id(),
        created_at_utc=_now_str(),
        report_type=PortfolioConstructionReportType.FULL_PHASE155_REVIEW,
        ingestion=context.ingestion,
        context=context,
        policy=context.policy,
        comparison_report=context.comparison_report,
        validation_report=context.validation_report,
        safety_boundary=context.safety_boundary,
        phase156_readiness_gate=context.phase156_readiness_gate,
        output_paths={},
        warnings=context.warnings,
        errors=context.errors
    )

def portfolio_construction_full_review_summary(review: PortfolioConstructionFullReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "context_id": review.context.context_id,
        "ready_for_phase156": review.context.ready_for_phase156,
        "errors": len(review.errors)
    }

def portfolio_construction_limitations_text() -> str:
    return (
        "Phase 155 is a research-only constraint-aware portfolio construction prototype "
        "and allocation sandbox. It does not produce actual target weights, actual allocations, "
        "or capital deployments. It does not perform actual portfolio optimization. "
        "It operates fully offline and does not integrate with brokers or live execution."
    )

def portfolio_construction_full_review_to_text(review: PortfolioConstructionFullReview, limit: int = 300) -> str:
    summary = portfolio_construction_full_review_summary(review)
    return (
        f"Portfolio Construction Full Review: {summary['review_id']}\n"
        f"Ready for Phase 156: {summary['ready_for_phase156']}\n"
        f"Errors: {summary['errors']}\n\n"
        f"{portfolio_construction_limitations_text()}"
    )
