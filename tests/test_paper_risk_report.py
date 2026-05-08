from usa_signal_bot.core.enums import PaperAccountStatus
from usa_signal_bot.paper.paper_models import VirtualAccount, PaperPosition
from usa_signal_bot.paper.paper_analytics_models import PaperEquityMetrics, PaperExposureMetrics
from usa_signal_bot.core.enums import PaperMetricStatus, PaperPositionSide, PaperRiskLevel
from usa_signal_bot.paper.paper_risk_report import build_paper_risk_report, default_paper_risk_limit_config

def test_paper_risk_report():
    account = VirtualAccount(account_id="a", status=PaperAccountStatus.ACTIVE, starting_cash=5.0, cash=5.0, equity=5.0, name="a", realized_pnl=0.0, unrealized_pnl=0.0, created_at_utc="2023-01-01")
    account._total_equity_cache = 100.0

    eq = PaperEquityMetrics(PaperMetricStatus.OK, 100, 100, 0, 0, 100, 100, 25, 25.0, 25, 25.0, 1)
    ex = PaperExposureMetrics(PaperMetricStatus.OK, 90, 90, 90, 90, 1, 1, 1, 0.9, 0.9)
    positions = [PaperPosition(symbol="A", side=PaperPositionSide.LONG, quantity=1.0, average_price=90.0, market_price=90.0, market_value=90.0, realized_pnl=0.0, unrealized_pnl=0.0, opened_at_utc="", updated_at_utc="")]

    report = build_paper_risk_report(account, eq, ex, positions)

    # max drawdown (25) > breach (20) -> HIGH
    # exposure (0.9) > max (0.8) -> HIGH
    # cash (0.05) >= min (0.05) -> OK
    # largest pos (0.9) > max (0.15) -> HIGH

    assert report.risk_level in [PaperRiskLevel.HIGH, PaperRiskLevel.CRITICAL]
