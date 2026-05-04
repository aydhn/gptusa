from usa_signal_bot.backtesting.walk_forward_validation import (
    validate_walk_forward_run_request, validate_walk_forward_windows,
    validate_no_walk_forward_optimization
)
from usa_signal_bot.backtesting.walk_forward_models import WalkForwardRunRequest, WalkForwardRunResult

def test_validate_walk_forward_run_request():
    req = WalkForwardRunRequest("test", [], "1d", signal_file="test.json")
    rep = validate_walk_forward_run_request(req)
    assert not rep.valid # no symbols

    req2 = WalkForwardRunRequest("test", ["AAPL"], "1d", signal_file="test.json")
    rep2 = validate_walk_forward_run_request(req2)
    assert rep2.valid

def test_validate_walk_forward_windows_empty():
    rep = validate_walk_forward_windows([])
    assert not rep.valid

def test_validate_no_optimization():
    res = WalkForwardRunResult(
        "id", "name", "COMPLETED", None, [], [], {"optimization": True}, "UNKNOWN", "UNKNOWN", {}, [], [], ""
    )
    rep = validate_no_walk_forward_optimization(res)
    assert not rep.valid
