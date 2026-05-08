from usa_signal_bot.paper.paper_models import PaperEquitySnapshot
from usa_signal_bot.paper.paper_rolling_metrics import calculate_paper_rolling_metrics

def test_paper_rolling_metrics():
    snapshots = [
        PaperEquitySnapshot(timestamp_utc=f"T{i}", equity=100.0+i, cash=100.0, gross_exposure=0.0, net_exposure=0.0, open_positions=0, realized_pnl=0.0, unrealized_pnl=0.0, snapshot_id="1", account_id="acc")
        for i in range(10)
    ]
    report = calculate_paper_rolling_metrics(snapshots, [], window_size=5)
    assert len(report.points) == 6
    assert report.points[-1].window_size == 5
