from usa_signal_bot.core.enums import PaperAccountStatus
from usa_signal_bot.paper.paper_models import VirtualAccount
from usa_signal_bot.paper.paper_performance_report import build_paper_performance_report

def test_paper_performance_report():
    account = VirtualAccount(account_id="a", status=PaperAccountStatus.ACTIVE, starting_cash=100.0, cash=100.0, equity=100.0, name="a", realized_pnl=0.0, unrealized_pnl=0.0, created_at_utc="2023-01-01")
    report = build_paper_performance_report(account, [], [], [], [])
    assert report.status.value in ["EMPTY", "WARNING", "INSUFFICIENT_DATA", "OK"]
