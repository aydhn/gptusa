import pytest
from usa_signal_bot.advanced_runtime.config_conflict_detector import detect_config_conflicts

def test_conflict():
    config = {"safety": {"allow_broker_execution": True}}
    conflicts = detect_config_conflicts(config)
    assert len(conflicts) > 0
