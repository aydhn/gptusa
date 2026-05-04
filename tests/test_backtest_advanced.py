import pytest
from usa_signal_bot.backtesting.backtest_engine import BacktestEngine, BacktestRunRequest, BacktestRunConfig
from usa_signal_bot.backtesting.order_models import SignalToOrderIntentConfig
from usa_signal_bot.core.enums import BacktestExitMode, TransactionCostModelType, SlippageModelType, BacktestMetricStatus, AdvancedMetricStatus
from usa_signal_bot.backtesting.transaction_costs import TransactionCostConfig
from usa_signal_bot.backtesting.slippage_models import SlippageConfig
from usa_signal_bot.backtesting.backtest_metrics import BacktestMetrics, merge_basic_and_advanced_metrics, backtest_metrics_summary_text
from usa_signal_bot.backtesting.advanced_metrics import AdvancedBacktestMetrics
import tempfile
from pathlib import Path

def test_engine_advanced_integration():
    with tempfile.TemporaryDirectory() as td:
        data_root = Path(td)
        tc_cfg = TransactionCostConfig(model_type=TransactionCostModelType.BPS, fee_bps=1.0)
        sl_cfg = SlippageConfig(model_type=SlippageModelType.FIXED_BPS, fixed_bps=2.0)
        config = BacktestRunConfig(
            starting_cash=100000.0, fee_rate=0.0, slippage_bps=0.0,
            signal_to_order=SignalToOrderIntentConfig(allow_short=False),
            exit_mode=BacktestExitMode.HOLD_N_BARS, hold_bars=5,
            max_positions=10, max_position_notional=10000.0, allow_fractional_quantity=True,
            transaction_cost_config=tc_cfg, slippage_config=sl_cfg,
            enable_advanced_metrics=True, build_trade_ledger=True
        )
        req = BacktestRunRequest(run_name="adv_test", symbols=["AAPL"], timeframe="1d", provider_name="mock", signal_file="signals.jsonl", config=config)
        engine = BacktestEngine(data_root)
        assert engine is not None
        assert req.config.transaction_cost_config.model_type == TransactionCostModelType.BPS

@pytest.fixture
def basic_metrics():
    return BacktestMetrics(
        status=BacktestMetricStatus.OK, starting_cash=100000.0, ending_equity=110000.0,
        total_return=10000.0, total_return_pct=0.1, max_drawdown=5000.0, max_drawdown_pct=0.05,
        total_fills=10, total_trades=5, winning_trades=3, losing_trades=2, win_rate=0.6, average_trade_pnl=2000.0
    )

@pytest.fixture
def adv_metrics():
    return AdvancedBacktestMetrics(
        status=AdvancedMetricStatus.OK, total_return=10000.0, total_return_pct=0.1, annualized_return_pct=0.15,
        max_drawdown_pct=0.05, calmar_ratio=3.0, exposure_ratio=0.5, average_equity=105000.0, equity_volatility=2000.0,
        daily_return_mean=0.001, daily_return_std=0.01, sharpe_like_ratio=1.5, sortino_like_ratio=2.0, trade_analytics=None, drawdown_analytics=None
    )

def test_merge_basic_and_advanced_metrics(basic_metrics, adv_metrics):
    merged = merge_basic_and_advanced_metrics(basic_metrics, adv_metrics)
    assert merged["starting_cash"] == 100000.0
    assert "advanced" in merged
    assert merged["advanced"]["calmar_ratio"] == 3.0

def test_backtest_metrics_summary_text(basic_metrics, adv_metrics):
    txt = backtest_metrics_summary_text(basic_metrics, adv_metrics)
    assert "Ending Equity:      $110000.00" in txt
    assert "Sharpe-like Ratio:  1.50" in txt
