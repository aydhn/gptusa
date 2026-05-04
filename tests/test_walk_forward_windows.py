import pytest
from usa_signal_bot.backtesting.walk_forward_windows import (
    generate_rolling_windows,
    generate_anchored_windows,
    generate_expanding_windows,
    split_window_dates
)

def test_generate_rolling_windows():
    windows = generate_rolling_windows(
        "2020-01-01", "2021-01-01",
        train_window_days=100, test_window_days=30, step_days=30, max_windows=10
    )
    assert len(windows) > 0
    assert windows[0].train_start == "2020-01-01"
    assert windows[0].test_end <= "2021-01-01"

def test_generate_anchored_windows():
    windows = generate_anchored_windows(
        "2020-01-01", "2021-01-01",
        min_train_days=100, test_window_days=30, step_days=30, max_windows=10
    )
    assert len(windows) > 0
    for w in windows:
        assert w.train_start == "2020-01-01"

def test_generate_expanding_windows():
    windows = generate_expanding_windows(
        "2020-01-01", "2021-01-01",
        min_train_days=100, test_window_days=30, step_days=30, max_windows=10
    )
    assert len(windows) > 0
    assert windows[0].mode.value == "EXPANDING"

def test_split_window_dates():
    w = generate_rolling_windows("2020-01-01", "2021-01-01", 100, 30, 30, 1)[0]
    res = split_window_dates(w)
    assert "train" in res
    assert "test" in res
    assert res["train"][0] == "2020-01-01"
