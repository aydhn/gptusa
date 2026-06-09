from usa_signal_bot.portfolio.risk_reporting.portfolio_band_final_review import (
    build_portfolio_band_final_review
)
from usa_signal_bot.portfolio.risk_reporting.portfolio_band_lineage import build_portfolio_band_lineage
from usa_signal_bot.portfolio.risk_reporting.portfolio_risk_summary import build_portfolio_risk_summary
from usa_signal_bot.portfolio.risk_reporting.portfolio_band_compliance_audit import build_portfolio_band_compliance_audit

def test_build_portfolio_band_final_review():
    lineage = build_portfolio_band_lineage({})
    summary = build_portfolio_risk_summary([])
    audit = build_portfolio_band_compliance_audit(lineage, summary, [])
    review = build_portfolio_band_final_review(lineage, audit, summary, [])
    assert review.final_review_passed is True
    assert review.review_valid is True
