import pytest
from usa_signal_bot.core.enums import ParameterGridType, SensitivityRunStatus, StabilityBucket, OverfitRiskHint
from usa_signal_bot.backtesting.backtest_engine import BacktestRunRequest
from usa_signal_bot.backtesting.parameter_sensitivity_models import (
    ParameterSensitivityConfig, ParameterGridSpec, ParameterSensitivityRunResult
)
from usa_signal_bot.backtesting.sensitivity_validation import (
    validate_sensitivity_run_request, validate_no_optimizer_behavior, assert_sensitivity_valid
)
from usa_signal_bot.core.exceptions import SensitivityValidationError

def test_validate_sensitivity_run_request():
    req = BacktestRunRequest("test", ["AAPL"], "1d", signal_file="sigs.jsonl")
    grid = ParameterGridSpec("g1", "strat", ParameterGridType.SINGLE_PARAMETER, [], 200)
    config = ParameterSensitivityConfig(
        max_cells=100, continue_on_cell_error=True, run_backtest=True,
        include_benchmark=False, include_monte_carlo=False, include_walk_forward=False,
        primary_metric=None, stability_metric=None, min_completed_cells=1
    )

    rep = validate_sensitivity_run_request(req, grid, config)
    # We expect a warning for max_cells (200 > 100)
    assert rep.warning_count == 1
    assert "exceeds config max_cells" in rep.warnings[0]

def test_validate_no_optimizer_behavior():
    grid = ParameterGridSpec("g1", "strat", ParameterGridType.SINGLE_PARAMETER, [], 10)
    config = ParameterSensitivityConfig(10, True, True, False, False, False, None, None, 1)

    # Valid result
    res = ParameterSensitivityRunResult(
        "run1", "", SensitivityRunStatus.COMPLETED, "strat", grid, config, [], [],
        {"return_pct": 10.0}, StabilityBucket.STABLE, OverfitRiskHint.LOW, [], [], {}, [], []
    )

    rep = validate_no_optimizer_behavior(res)
    assert rep.valid

    # Invalid result with 'best_params' dynamically added
    res.best_params = {"a": 1}
    rep2 = validate_no_optimizer_behavior(res)
    assert not rep2.valid
    assert rep2.error_count == 1

    # Invalid result with 'optimal_xyz' in aggregate metrics
    del res.best_params
    res.aggregate_metrics["optimal_return"] = 50.0
    rep3 = validate_no_optimizer_behavior(res)
    assert not rep3.valid

def test_assert_sensitivity_valid():
    grid = ParameterGridSpec("g1", "strat", ParameterGridType.SINGLE_PARAMETER, [], 10)
    config = ParameterSensitivityConfig(10, True, True, False, False, False, None, None, 1)
    res = ParameterSensitivityRunResult(
        "run1", "", SensitivityRunStatus.COMPLETED, "strat", grid, config, [], [],
        {"return_pct": 10.0}, StabilityBucket.STABLE, OverfitRiskHint.LOW, [], [], {}, [], []
    )
    res.best_params = {"a": 1}
    rep = validate_no_optimizer_behavior(res)

    with pytest.raises(SensitivityValidationError, match="Optimizer behavior"):
        assert_sensitivity_valid(rep)
