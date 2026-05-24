import pytest
from usa_signal_bot.advanced_runtime.safety_policy_validator import validate_runtime_registry_safety
from usa_signal_bot.advanced_runtime.normalized_runtime_registry import build_default_normalized_runtime_registry

def test_safety_policy():
    reg = build_default_normalized_runtime_registry()
    assert len(validate_runtime_registry_safety(reg)) == 0
