import pytest
from usa_signal_bot.advanced_runtime.capability_policy import build_phase102_capability_policies

def test_build_policies():
    policies = build_phase102_capability_policies()
    assert len(policies) > 0
    names = [p.capability_name for p in policies]
    assert "READ_LOCAL_CONFIG" in names
    assert "PLACE_LIVE_BROKER_ORDER" in names
