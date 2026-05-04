from usa_signal_bot.backtesting.walk_forward_metrics import (
    calculate_degradation, calculate_stability_score,
    classify_walk_forward_stability, classify_out_of_sample_result,
    calculate_walk_forward_aggregate_metrics
)
from usa_signal_bot.backtesting.walk_forward_models import WalkForwardWindowResult, WalkForwardWindow
from usa_signal_bot.core.enums import WalkForwardMode, WalkForwardWindowStatus

def test_calculate_degradation():
    assert calculate_degradation(10.0, 5.0) == -5.0
    assert calculate_degradation(-5.0, 5.0) == 10.0

def test_calculate_stability_score():
    w1 = WalkForwardWindow("w1", 1, WalkForwardMode.ROLLING, "x", "x", "x", "x", "x", "x", WalkForwardWindowStatus.COMPLETED)
    w2 = WalkForwardWindow("w2", 2, WalkForwardMode.ROLLING, "x", "x", "x", "x", "x", "x", WalkForwardWindowStatus.COMPLETED)

    r1 = WalkForwardWindowResult(w1, "is1", "oos1", {"total_return_pct": 10}, {"total_return_pct": 5}, {}, {}, [], [])
    r2 = WalkForwardWindowResult(w2, "is2", "oos2", {"total_return_pct": 10}, {"total_return_pct": -5}, {}, {}, [], [])

    score = calculate_stability_score([r1, r2])
    assert score is not None
    assert 0 <= score <= 100

def test_classify_buckets():
    assert classify_walk_forward_stability(80.0).value == "STABLE"
    assert classify_walk_forward_stability(10.0).value == "SEVERELY_UNSTABLE"

def test_calculate_walk_forward_aggregate_metrics_empty():
    res = calculate_walk_forward_aggregate_metrics([])
    assert res.status.value == "EMPTY"
    assert res.total_windows == 0
