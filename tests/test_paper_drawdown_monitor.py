from usa_signal_bot.paper.paper_models import PaperEquitySnapshot
from usa_signal_bot.paper.paper_drawdown_monitor import (
    monitor_paper_drawdown,
    default_paper_drawdown_thresholds,
    paper_drawdown_report_to_text,
    classify_paper_drawdown
)
from usa_signal_bot.core.enums import PaperDrawdownStatus

def test_paper_drawdown_monitor():
    thresholds = default_paper_drawdown_thresholds()
    assert classify_paper_drawdown(0.0, thresholds) == PaperDrawdownStatus.NORMAL
    assert classify_paper_drawdown(6.0, thresholds) == PaperDrawdownStatus.WARNING
    assert classify_paper_drawdown(15.0, thresholds) == PaperDrawdownStatus.BREACH
    assert classify_paper_drawdown(25.0, thresholds) == PaperDrawdownStatus.CRITICAL

    snapshots = [
        PaperEquitySnapshot(timestamp_utc="T1", equity=100.0, cash=100.0, gross_exposure=0.0, net_exposure=0.0, open_positions=0, realized_pnl=0.0, unrealized_pnl=0.0, snapshot_id="1", account_id="acc"),
        PaperEquitySnapshot(timestamp_utc="T2", equity=90.0, cash=90.0, gross_exposure=0.0, net_exposure=0.0, open_positions=0, realized_pnl=0.0, unrealized_pnl=0.0, snapshot_id="1", account_id="acc"), # 10% dd
        PaperEquitySnapshot(timestamp_utc="T3", equity=80.0, cash=80.0, gross_exposure=0.0, net_exposure=0.0, open_positions=0, realized_pnl=0.0, unrealized_pnl=0.0, snapshot_id="1", account_id="acc")  # 20% dd
    ]

    report = monitor_paper_drawdown(snapshots)
    assert report.status in [PaperDrawdownStatus.BREACH, PaperDrawdownStatus.CRITICAL]
    assert report.max_drawdown_pct == 20.0
    assert len(report.events) > 0

    txt = paper_drawdown_report_to_text(report)
    assert "Max Drawdown" in txt
