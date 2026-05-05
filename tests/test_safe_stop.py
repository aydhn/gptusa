import pytest
from pathlib import Path
from usa_signal_bot.runtime.safe_stop import SafeStopManager
from usa_signal_bot.core.exceptions import SafeStopError

def test_safe_stop(tmp_path):
    mgr = SafeStopManager(tmp_path / "stop.json")

    assert not mgr.is_stop_requested()
    mgr.check_or_raise() # Should not raise

    mgr.request_stop(reason="test reason")
    assert mgr.is_stop_requested()

    state = mgr.read_state()
    assert state.stop_requested
    assert state.reason == "test reason"

    with pytest.raises(SafeStopError, match="test reason"):
        mgr.check_or_raise()

    mgr.clear_stop()
    assert not mgr.is_stop_requested()
