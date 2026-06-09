from usa_signal_bot.portfolio.risk_reporting.phase158_handoff_package import (
    build_phase158_handoff_package
)
from usa_signal_bot.portfolio.risk_reporting.phase158_handoff_contract import build_phase158_handoff_contract
from usa_signal_bot.portfolio.risk_reporting.portfolio_band_closure_certificate import build_portfolio_band_closure_certificate
from usa_signal_bot.portfolio.risk_reporting.portfolio_band_final_review import build_portfolio_band_final_review
from usa_signal_bot.portfolio.risk_reporting.portfolio_band_lineage import build_portfolio_band_lineage
from usa_signal_bot.portfolio.risk_reporting.portfolio_risk_summary import build_portfolio_risk_summary
from usa_signal_bot.portfolio.risk_reporting.portfolio_band_compliance_audit import build_portfolio_band_compliance_audit

def test_build_phase158_handoff_package():
    lineage = build_portfolio_band_lineage({})
    summary = build_portfolio_risk_summary([])
    audit = build_portfolio_band_compliance_audit(lineage, summary, [])
    review = build_portfolio_band_final_review(lineage, audit, summary, [])
    cert = build_portfolio_band_closure_certificate(review)
    contract = build_phase158_handoff_contract(cert, review)
    package = build_phase158_handoff_package(contract, cert, review, summary, [], lineage)
    assert package.package_valid is True
    assert package.read_only is True
    assert package.deployment_allowed is False
