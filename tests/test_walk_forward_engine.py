from usa_signal_bot.backtesting.walk_forward_engine import WalkForwardEngine
from usa_signal_bot.backtesting.walk_forward_models import WalkForwardRunRequest, WalkForwardConfig
from usa_signal_bot.core.enums import WalkForwardMode

class FakeBacktestEngine:
    def run(self, request):
        from usa_signal_bot.backtesting.backtest_engine import BacktestRunResult
        return BacktestRunResult(
            run_id="fake_id", run_name="fake_name", status="COMPLETED", request=request,
            portfolio=None, snapshots=[], fills=[], order_intents=[], equity_curve=[],
            metrics={"total_return_pct": 5.0, "win_rate_pct": 60.0, "max_drawdown_pct": -2.0},
            events=[], warnings=[], errors=[], created_at_utc=""
        )

def test_walk_forward_engine(tmp_path):
    eng = WalkForwardEngine(tmp_path, backtest_engine=FakeBacktestEngine())

    c = WalkForwardConfig(WalkForwardMode.ROLLING, 100, 30, 30, 50, 2, False, False)
    req = WalkForwardRunRequest(
        "test_run", ["AAPL"], "1d", signal_file="fake.jsonl",
        start_date="2020-01-01", end_date="2020-06-01", config=c
    )

    res = eng.run(req)
    assert res.status.value == "COMPLETED"
    assert len(res.windows) > 0
    assert len(res.window_results) > 0
    assert res.aggregate_metrics["average_out_of_sample_return_pct"] == 5.0
