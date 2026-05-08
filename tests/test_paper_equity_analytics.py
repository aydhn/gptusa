from usa_signal_bot.paper.paper_models import PaperEquitySnapshot
from usa_signal_bot.paper.paper_equity_analytics import (
    calculate_paper_equity_metrics,
    calculate_paper_drawdown_series,
    extract_equity_values,
    calculate_equity_total_return_pct,
    paper_equity_metrics_to_text
)
from usa_signal_bot.core.enums import PaperMetricStatus

def test_paper_equity_analytics():
    snapshots = [
        PaperEquitySnapshot(timestamp_utc="2023-01-01T00:00:00Z", equity=100.0, cash=100.0, gross_exposure=0.0, net_exposure=0.0, open_positions=0, realized_pnl=0.0, unrealized_pnl=0.0, snapshot_id="1", account_id="acc"),
        PaperEquitySnapshot(timestamp_utc="2023-01-02T00:00:00Z", equity=110.0, cash=10.0, gross_exposure=100.0, net_exposure=100.0, open_positions=1, realized_pnl=0.0, unrealized_pnl=10.0, snapshot_id="2", account_id="acc"),
        PaperEquitySnapshot(timestamp_utc="2023-01-03T00:00:00Z", equity=105.0, cash=10.0, gross_exposure=95.0, net_exposure=95.0, open_positions=1, realized_pnl=0.0, unrealized_pnl=5.0, snapshot_id="3", account_id="acc")
    ]

    metrics = calculate_paper_equity_metrics(snapshots)
    assert metrics.status == PaperMetricStatus.OK
    assert metrics.starting_equity == 100.0
    assert metrics.ending_equity == 105.0
    assert metrics.total_return_pct == 5.0
    assert metrics.peak_equity == 110.0
    assert metrics.trough_equity == 100.0
    assert metrics.max_drawdown == 5.0
    assert abs(metrics.max_drawdown_pct - (5.0/110.0)*100.0) < 0.001

    txt = paper_equity_metrics_to_text(metrics)
    assert "Ending Equity: 105.00" in txt

def test_paper_equity_analytics_empty():
    metrics = calculate_paper_equity_metrics([])
    assert metrics.status == PaperMetricStatus.EMPTY
