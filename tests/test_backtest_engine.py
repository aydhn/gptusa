import pytest
from pathlib import Path
from usa_signal_bot.core.enums import SignalAction, BacktestSignalMode, BacktestExitMode, BacktestOrderSide
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.backtesting.backtest_engine import (
    BacktestEngine, BacktestRunRequest, BacktestRunConfig, MarketReplayData, SignalReplayData, MarketReplayRequest, SignalReplayRequest
)
from usa_signal_bot.backtesting.signal_adapter import default_signal_to_order_config

def test_engine_process_stream():
    # Setup mock data
    req = BacktestRunRequest("test", ["AAPL"], "1d")
    config = BacktestRunConfig(
        10000.0, 0.0, 0.0, default_signal_to_order_config(),
        BacktestExitMode.HOLD_N_BARS, 1, 10, 1000.0, True
    )

    engine = BacktestEngine(Path("data"))

    b1 = OHLCVBar(symbol="AAPL", timestamp_utc="2023-01-01T00:00:00Z", timeframe="1d", open=100.0, high=100.0, low=100.0, close=100.0, volume=100)
    b2 = OHLCVBar(symbol="AAPL", timestamp_utc="2023-01-02T00:00:00Z", timeframe="1d", open=110.0, high=110.0, low=110.0, close=110.0, volume=100)
    m_data = MarketReplayData(MarketReplayRequest(["AAPL"], "1d"), {"AAPL": [b1, b2]}, ["2023-01-01T00:00:00Z", "2023-01-02T00:00:00Z"])

    s1 = StrategySignal("sig1", "s1", "AAPL", "1d", "2023-01-01T00:00:00Z", SignalAction.LONG, 1.0, __import__('usa_signal_bot.core.enums', fromlist=['SignalConfidenceBucket']).SignalConfidenceBucket.HIGH, 100.0, [], {}, [])
    sig_data = SignalReplayData(SignalReplayRequest(symbols=["AAPL"]), [s1])

    stream = engine.build_event_stream(m_data, sig_data)

    portfolio, snapshots, order_intents, fills = engine.process_event_stream(stream, m_data, sig_data, config)

    # Assert
    assert len(order_intents) == 2 # 1 entry, 1 exit
    assert order_intents[0].side == BacktestOrderSide.BUY
    assert order_intents[1].side == BacktestOrderSide.SELL
    assert len(fills) == 2
    assert fills[0].fill_price == 110.0 # Next open from 01-01 is 01-02 open=110

def test_backtest_benchmark_integration():
    from usa_signal_bot.backtesting.backtest_engine import BacktestEngine, BacktestRunConfig, BacktestRunRequest
    from usa_signal_bot.backtesting.order_models import SignalToOrderIntentConfig
    from usa_signal_bot.core.enums import BacktestExitMode
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as td:
        engine = BacktestEngine(Path(td))

        cfg = BacktestRunConfig(
            starting_cash=10000.0,
            fee_rate=0.0,
            slippage_bps=0.0,
            signal_to_order=SignalToOrderIntentConfig(),
            exit_mode=BacktestExitMode.HOLD_N_BARS,
            hold_bars=5,
            max_positions=5,
            max_position_notional=2000.0,
            allow_fractional_quantity=False,
            enable_benchmark_comparison=True,
            enable_attribution=True
        )
        req = BacktestRunRequest(
            run_name="test_bm",
            symbols=["SPY"],
            timeframe="1d",

            config=cfg
        )

        # It shouldn't crash if data is empty, just generate empty metrics/reports or warning
        res = engine.run(req)
        assert res is not None
