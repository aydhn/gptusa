from usa_signal_bot.portfolio.risk_reporting.portfolio_band_compliance_audit import (
    build_portfolio_band_compliance_audit
)
from usa_signal_bot.portfolio.risk_reporting.portfolio_band_lineage import build_portfolio_band_lineage
from usa_signal_bot.portfolio.risk_reporting.portfolio_risk_summary import build_portfolio_risk_summary

def test_build_portfolio_band_compliance_audit():
    lineage = build_portfolio_band_lineage({})
    summary = build_portfolio_risk_summary([])
    audit = build_portfolio_band_compliance_audit(lineage, summary, [])
    assert audit.audit_passed is True
    assert audit.no_live_trading is True
