import pytest
from usa_signal_bot.core.enums import SensitivityMetricName, StabilityBucket, OverfitRiskHint, SensitivityCellStatus
from usa_signal_bot.backtesting.parameter_sensitivity_models import ParameterGridCell, SensitivityCellResult
from usa_signal_bot.backtesting.sensitivity_metrics import (
    extract_cell_metric, calculate_std_like, calculate_stability_score_from_values,
    calculate_fragility_score_from_values, calculate_sensitivity_aggregate_metrics,
    classify_stability_bucket, classify_overfit_risk_hint, sensitivity_aggregate_metrics_to_text
)

def create_fake_result(return_pct, status=SensitivityCellStatus.COMPLETED):
    cell = ParameterGridCell("c", 0, "s", {})
    return SensitivityCellResult(cell, status, None, {"total_return_pct": return_pct})

def test_extract_cell_metric():
    r = create_fake_result(15.5)
    assert extract_cell_metric(r, SensitivityMetricName.RETURN_PCT) == 15.5
    assert extract_cell_metric(r, SensitivityMetricName.MAX_DRAWDOWN_PCT) is None

def test_calculate_std_like():
    assert calculate_std_like([1.0]) is None
    assert calculate_std_like([1.0, 1.0, 1.0]) == 0.0

def test_calculate_stability_score_from_values():
    assert calculate_stability_score_from_values([]) is None
    assert calculate_stability_score_from_values([1.0]) == 100.0 # stdev is None -> 100

    # zero stdev
    assert calculate_stability_score_from_values([10.0, 10.0]) == 100.0

    # high variance
    score = calculate_stability_score_from_values([10.0, 100.0, -50.0])
    assert score == 0.0 # because cv will be huge -> 100 - (huge) -> 0.0

def test_aggregate_metrics_calculation():
    r1 = create_fake_result(10.0)
    r2 = create_fake_result(12.0)
    r3 = create_fake_result(0.0, SensitivityCellStatus.FAILED)

    agg = calculate_sensitivity_aggregate_metrics([r1, r2, r3], SensitivityMetricName.RETURN_PCT)
    assert agg.completed_cells == 2
    assert agg.failed_cells == 1
    assert agg.primary_metric_mean == 11.0
    assert agg.primary_metric_min == 10.0
    assert agg.primary_metric_max == 12.0

def test_classify_stability_bucket():
    assert classify_stability_bucket(None, 0) == StabilityBucket.INSUFFICIENT_DATA
    assert classify_stability_bucket(85.0, 5) == StabilityBucket.VERY_STABLE
    assert classify_stability_bucket(50.0, 5) == StabilityBucket.MODERATE

def test_classify_overfit_risk_hint():
    # insufficient data
    agg = calculate_sensitivity_aggregate_metrics([create_fake_result(10.0)], SensitivityMetricName.RETURN_PCT)
    assert classify_overfit_risk_hint(agg) == OverfitRiskHint.INSUFFICIENT_DATA

    # high risk due to outlier max
    r1 = create_fake_result(1.0)
    r2 = create_fake_result(2.0)
    r3 = create_fake_result(100.0) # outlier
    agg2 = calculate_sensitivity_aggregate_metrics([r1, r2, r3], SensitivityMetricName.RETURN_PCT)
    assert classify_overfit_risk_hint(agg2) == OverfitRiskHint.HIGH

def test_metrics_to_text():
    r1 = create_fake_result(10.0)
    agg = calculate_sensitivity_aggregate_metrics([r1], SensitivityMetricName.RETURN_PCT)
    txt = sensitivity_aggregate_metrics_to_text(agg)
    assert "Cells: 1 completed" in txt
