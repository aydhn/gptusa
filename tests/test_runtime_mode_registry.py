import pytest
from usa_signal_bot.advanced_runtime.runtime_mode_registry import build_phase102_runtime_modes

def test_build_modes():
    modes = build_phase102_runtime_modes()
    assert len(modes) > 0
    names = [m.mode.value for m in modes]
    assert "PROVIDER_READY_NO_FETCH" in names
    assert "ACTIVE_PAPER_DISABLED" in names
