from usa_signal_bot.portfolio.risk_reporting.portfolio_band_closure_certificate import (
    build_portfolio_band_closure_certificate
)
from usa_signal_bot.portfolio.risk_reporting.portfolio_band_final_review import build_portfolio_band_final_review
from usa_signal_bot.portfolio.risk_reporting.portfolio_band_lineage import build_portfolio_band_lineage
from usa_signal_bot.portfolio.risk_reporting.portfolio_risk_summary import build_portfolio_risk_summary
from usa_signal_bot.portfolio.risk_reporting.portfolio_band_compliance_audit import build_portfolio_band_compliance_audit

def test_build_portfolio_band_closure_certificate():
    lineage = build_portfolio_band_lineage({})
    summary = build_portfolio_risk_summary([])
    audit = build_portfolio_band_compliance_audit(lineage, summary, [])
    review = build_portfolio_band_final_review(lineage, audit, summary, [])
    cert = build_portfolio_band_closure_certificate(review)
    assert cert.start_phase == 153
    assert cert.end_phase == 157
    assert cert.next_phase == 158
    assert cert.closed is True
    assert cert.not_deployment_approval is True
