from usa_signal_bot.paper.paper_models import PaperEquitySnapshot, PaperPosition, PaperFill
from usa_signal_bot.core.enums import PaperMetricStatus, PaperPositionSide
from usa_signal_bot.paper.paper_exposure_analytics import (
    calculate_paper_exposure_metrics,
    calculate_paper_turnover_proxy,
    paper_exposure_metrics_to_text
)

def test_paper_exposure_analytics():
    snapshots = [
        PaperEquitySnapshot(timestamp_utc="T1", equity=100.0, cash=100.0, gross_exposure=0.0, net_exposure=0.0, open_positions=0, realized_pnl=0.0, unrealized_pnl=0.0, snapshot_id="1", account_id="acc"),
        PaperEquitySnapshot(timestamp_utc="T2", equity=100.0, cash=50.0, gross_exposure=50.0, net_exposure=50.0, open_positions=1, realized_pnl=0.0, unrealized_pnl=0.0, snapshot_id="2", account_id="acc")
    ]
    positions = [
        PaperPosition(symbol="A", side=PaperPositionSide.LONG, quantity=1.0, average_price=50.0, market_price=50.0, market_value=50.0, realized_pnl=0.0, unrealized_pnl=0.0, opened_at_utc="", updated_at_utc="")
    ]

    metrics = calculate_paper_exposure_metrics(snapshots, positions)
    assert metrics.status == PaperMetricStatus.OK
    assert metrics.max_gross_exposure == 50.0
    assert metrics.exposure_to_equity_max == 0.5
    assert metrics.final_open_positions == 1

    txt = paper_exposure_metrics_to_text(metrics)
    assert "Max Exposure/Equity:" in txt
