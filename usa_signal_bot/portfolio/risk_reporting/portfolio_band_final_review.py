from typing import Any, Dict, List
import datetime
import hashlib
import json

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    PortfolioBandFinalReview,
    PortfolioBandLineage,
    PortfolioBandComplianceAudit,
    PortfolioRiskSummary,
    PortfolioGovernanceReport,
    create_portfolio_band_final_review_id
)

def build_portfolio_band_final_review(lineage: PortfolioBandLineage, compliance_audit: PortfolioBandComplianceAudit, risk_summary: PortfolioRiskSummary, governance_reports: List[PortfolioGovernanceReport]) -> PortfolioBandFinalReview:
    review = PortfolioBandFinalReview(
        review_id=create_portfolio_band_final_review_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        lineage=lineage,
        compliance_audit=compliance_audit,
        risk_summary=risk_summary,
        governance_reports=governance_reports,
        review_hash=None,
        review_valid=True,
        final_review_passed=compliance_audit.audit_passed,
        research_data_only=True,
        portfolio_risk_governance_only=True,
        no_actual_target_weights=True,
        no_actual_allocation=True,
        no_order_output=True,
        no_broker_execution=True,
        not_investment_advice=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    review.review_hash = compute_portfolio_band_final_review_hash(review)
    return review

def compute_portfolio_band_final_review_hash(review: PortfolioBandFinalReview) -> str:
    from usa_signal_bot.portfolio.risk_reporting.phase157_models import portfolio_band_final_review_to_dict
    d = portfolio_band_final_review_to_dict(review)
    d.pop("review_hash", None)
    return hashlib.sha256(json.dumps(d, sort_keys=True).encode('utf-8')).hexdigest()

def validate_portfolio_band_final_review(review: PortfolioBandFinalReview) -> List[str]:
    return []

def portfolio_band_final_review_to_text(review: PortfolioBandFinalReview, limit: int = 300) -> str:
    return f"Final Review {review.review_id}: passed={review.final_review_passed}"
