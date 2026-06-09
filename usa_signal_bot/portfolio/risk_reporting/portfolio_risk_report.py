from typing import Any, Dict
import datetime

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    PortfolioRiskContext,
    PortfolioRiskFullReview,
    create_portfolio_risk_context_id,
    create_portfolio_risk_full_review_id,
    PortfolioRiskReportType,
    PortfolioRiskReportingStatus,
    PortfolioRiskReportingDecision
)

def build_portfolio_risk_context() -> PortfolioRiskContext:
    return PortfolioRiskContext(
        context_id=create_portfolio_risk_context_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        status=PortfolioRiskReportingStatus.CREATED,
        decision=PortfolioRiskReportingDecision.INCONCLUSIVE,
        source_optimizer_review_id=None,
        ingestion=None,
        input_references=[],
        exposure_records=[],
        risk_summary=None,
        governance_reports=[],
        band_lineage=None,
        compliance_audit=None,
        band_final_review=None,
        closure_certificate=None,
        phase158_handoff_contract=None,
        phase158_handoff_package=None,
        safety_boundary=None,
        phase158_readiness_gate=None,
        optimizer_prototype_ingested=False,
        artifacts_loaded=False,
        inputs_resolved=False,
        sandbox_exposure_governance_built=False,
        portfolio_risk_summary_built=False,
        concentration_risk_report_built=False,
        diversification_governance_report_built=False,
        risk_budget_governance_report_built=False,
        turnover_governance_report_built=False,
        optimizer_objective_governance_report_built=False,
        constraint_governance_report_built=False,
        portfolio_limitations_report_built=False,
        portfolio_band_lineage_built=False,
        portfolio_band_compliance_audit_built=False,
        portfolio_band_final_review_built=False,
        portfolio_band_closure_certificate_built=False,
        phase158_handoff_contract_built=False,
        phase158_handoff_package_built=False,
        safety_boundary_validated=False,
        phase158_readiness_gate_built=False,
        phase158_readiness_gate_passed=False,
        ready_for_phase158=False,
        research_data_only=True,
        portfolio_risk_governance_only=True,
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
        actual_portfolio_optimization_enabled=False,
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

def build_portfolio_risk_full_review() -> PortfolioRiskFullReview:
    return PortfolioRiskFullReview(
        review_id=create_portfolio_risk_full_review_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        report_type=PortfolioRiskReportType.FULL_PHASE157_REVIEW,
        ingestion=None,
        context=build_portfolio_risk_context(),
        risk_summary=None,
        band_final_review=None,
        closure_certificate=None,
        phase158_handoff_package=None,
        safety_boundary=None,
        phase158_readiness_gate=None,
        output_paths={},
        warnings=[],
        errors=[]
    )

def portfolio_risk_full_review_summary(review: PortfolioRiskFullReview) -> Dict[str, Any]:
    return {"review_id": review.review_id}

def portfolio_risk_limitations_text() -> str:
    return "Phase 157 Portfolio Risk limitations: No actual targets, allocations or deployment. Research only."

def portfolio_risk_full_review_to_text(review: PortfolioRiskFullReview, limit: int = 300) -> str:
    return f"Full Review {review.review_id}"
