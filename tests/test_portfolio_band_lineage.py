from usa_signal_bot.portfolio.risk_reporting.portfolio_band_lineage import (
    build_portfolio_band_lineage
)

def test_build_portfolio_band_lineage():
    lineage = build_portfolio_band_lineage({})
    assert lineage.lineage_valid is True
    assert lineage.deterministic_hashes_available is True
