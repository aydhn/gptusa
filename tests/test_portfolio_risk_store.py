from pathlib import Path
from usa_signal_bot.portfolio.risk_reporting.portfolio_risk_store import (
    portfolio_risk_store_summary
)

def test_portfolio_risk_store_summary(tmp_path: Path):
    res = portfolio_risk_store_summary(tmp_path)
    assert res["reviews"] == 0
