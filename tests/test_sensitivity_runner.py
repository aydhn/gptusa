import pytest
from pathlib import Path
from usa_signal_bot.core.enums import (
    ParameterValueType, SensitivityRunStatus, SensitivityMetricName,
    BacktestRunStatus, SensitivityCellStatus
)
from usa_signal_bot.backtesting.backtest_engine import BacktestRunRequest, BacktestRunResult
from usa_signal_bot.backtesting.parameter_sensitivity_models import ParameterSensitivityConfig
from usa_signal_bot.backtesting.parameter_grid import create_single_parameter_grid
from usa_signal_bot.backtesting.sensitivity_runner import ParameterSensitivityRunner

class FakeBacktestMetrics:
    def __init__(self, val):
        self.total_return_pct = val
        self.max_drawdown_pct = 0.0
        self.win_rate = 0.5
        self.profit_factor = 1.0
        self.sharpe_ratio = 1.0

class FakeBacktestEngine:
    def __init__(self, fail_on_val=None):
        self.fail_on_val = fail_on_val
        self.calls = 0

    def run(self, request: BacktestRunRequest):
        self.calls += 1
        # Expecting param in run_name for this fake test
        is_fail = False
        if self.fail_on_val is not None and str(self.fail_on_val) in request.run_name:
            is_fail = True

        if is_fail:
            return BacktestRunResult(
                run_id="fake_fail", run_name=request.run_name,
                status=BacktestRunStatus.FAILED, request=request,
                portfolio=None, snapshots=[], fills=[], order_intents=[],
                equity_curve=None, metrics=None, events=[], warnings=[],
                errors=["Failed!"], created_at_utc=""
            )

        return BacktestRunResult(
            run_id=f"fake_{self.calls}", run_name=request.run_name,
            status=BacktestRunStatus.COMPLETED, request=request,
            portfolio=None, snapshots=[], fills=[], order_intents=[],
            equity_curve=None, metrics=FakeBacktestMetrics(float(self.calls)), events=[], warnings=[],
            errors=[], created_at_utc=""
        )

def test_runner_full_success(tmp_path: Path):
    engine = FakeBacktestEngine()
    runner = ParameterSensitivityRunner(tmp_path, backtest_engine=engine)

    grid = create_single_parameter_grid("test_strat", "a", [1, 2], ParameterValueType.INT)
    req = BacktestRunRequest("test", ["AAPL"], "1d")
    config = ParameterSensitivityConfig(
        max_cells=10, continue_on_cell_error=False, run_backtest=True,
        include_benchmark=False, include_monte_carlo=False, include_walk_forward=False,
        primary_metric=SensitivityMetricName.RETURN_PCT,
        stability_metric=SensitivityMetricName.STABILITY_SCORE,
        min_completed_cells=1
    )

    result = runner.run(req, grid, config)
    assert result.status == SensitivityRunStatus.COMPLETED
    assert engine.calls == 2
    assert len(result.cell_results) == 2
    assert result.cell_results[0].status == SensitivityCellStatus.COMPLETED

def test_runner_continue_on_error(tmp_path: Path):
    engine = FakeBacktestEngine(fail_on_val=2) # fail when param=2? Wait, run_name has cell_id cell_0001
    runner = ParameterSensitivityRunner(tmp_path, backtest_engine=engine)

    grid = create_single_parameter_grid("test_strat", "a", [1, 2, 3], ParameterValueType.INT)
    req = BacktestRunRequest("test", ["AAPL"], "1d")
    config = ParameterSensitivityConfig(
        max_cells=10, continue_on_cell_error=True, run_backtest=True,
        include_benchmark=False, include_monte_carlo=False, include_walk_forward=False,
        primary_metric=SensitivityMetricName.RETURN_PCT,
        stability_metric=SensitivityMetricName.STABILITY_SCORE,
        min_completed_cells=1
    )

    # Actually fake engine fails on '2' in run_name? No run_name is "test_cell_0001" etc.
    engine.fail_on_val = "0001"

    result = runner.run(req, grid, config)
    assert result.status == SensitivityRunStatus.PARTIAL_SUCCESS
    assert engine.calls == 3
    assert result.cell_results[1].status == SensitivityCellStatus.FAILED
    assert result.cell_results[2].status == SensitivityCellStatus.COMPLETED

def test_runner_halt_on_error(tmp_path: Path):
    engine = FakeBacktestEngine(fail_on_val="0001")
    runner = ParameterSensitivityRunner(tmp_path, backtest_engine=engine)

    grid = create_single_parameter_grid("test_strat", "a", [1, 2, 3], ParameterValueType.INT)
    req = BacktestRunRequest("test", ["AAPL"], "1d")
    config = ParameterSensitivityConfig(
        max_cells=10, continue_on_cell_error=False, run_backtest=True,
        include_benchmark=False, include_monte_carlo=False, include_walk_forward=False,
        primary_metric=SensitivityMetricName.RETURN_PCT,
        stability_metric=SensitivityMetricName.STABILITY_SCORE,
        min_completed_cells=1
    )

    result = runner.run(req, grid, config)
    # Fails on index 1, so len should be 2 (idx 0 and 1)
    assert engine.calls == 2
    assert result.status == SensitivityRunStatus.PARTIAL_SUCCESS # Has 1 completed
    assert len(result.cell_results) == 2
