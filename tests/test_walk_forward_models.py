import pytest
from usa_signal_bot.core.enums import WalkForwardMode, WalkForwardWindowStatus
from usa_signal_bot.backtesting.walk_forward_models import (
    WalkForwardWindow, WalkForwardConfig,
    validate_walk_forward_window, validate_walk_forward_config,
    create_walk_forward_run_id, walk_forward_run_result_to_dict
)
from usa_signal_bot.core.exceptions import WalkForwardWindowError, WalkForwardError

def test_walk_forward_window_valid():
    w = WalkForwardWindow(
        window_id="win_01",
        index=1,
        mode=WalkForwardMode.ROLLING,
        train_start="2020-01-01",
        train_end="2021-01-01",
        test_start="2021-01-01",
        test_end="2021-04-01",
        full_start="2020-01-01",
        full_end="2021-04-01"
    )
    validate_walk_forward_window(w)
    assert w.status == WalkForwardWindowStatus.CREATED

def test_walk_forward_window_invalid_dates():
    w = WalkForwardWindow(
        window_id="win_01",
        index=1,
        mode=WalkForwardMode.ROLLING,
        train_start="2021-01-01",
        train_end="2020-01-01", # invalid
        test_start="2021-01-01",
        test_end="2021-04-01",
        full_start="2020-01-01",
        full_end="2021-04-01"
    )
    with pytest.raises(WalkForwardWindowError):
        validate_walk_forward_window(w)

def test_walk_forward_config_valid():
    c = WalkForwardConfig(
        mode=WalkForwardMode.ROLLING,
        train_window_days=100,
        test_window_days=30,
        step_days=30,
        min_train_days=50,
        max_windows=10,
        anchored_start=False,
        include_partial_last_window=True
    )
    validate_walk_forward_config(c)

def test_walk_forward_config_invalid():
    c = WalkForwardConfig(
        mode=WalkForwardMode.ROLLING,
        train_window_days=-10, # invalid
        test_window_days=30,
        step_days=30,
        min_train_days=50,
        max_windows=10,
        anchored_start=False,
        include_partial_last_window=True
    )
    with pytest.raises(WalkForwardError):
        validate_walk_forward_config(c)

def test_create_walk_forward_run_id():
    rid = create_walk_forward_run_id("test_run")
    assert "test_run" in rid
    assert rid.startswith("wf_")
