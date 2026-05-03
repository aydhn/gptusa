import pytest
from usa_signal_bot.app.cli import handle_backtest_info

def test_handle_backtest_info(capsys):
    class DummyConfig:
        class BT:
            enabled = True
            store_dir = "x"
            default_starting_cash = 100
            default_signal_mode = "watch"
            default_exit_mode = "hold"
            default_hold_bars = 5
        backtesting = BT()
        historical_replay = BT()

    class DummyContext:
        config = DummyConfig()

    import logging
    from usa_signal_bot.core import logging_config
    logging_config._LOGGING_CONFIGURED = True
    handle_backtest_info(DummyContext(), None)
    out, err = capsys.readouterr()
    assert "Backtesting Enabled: True" in out
