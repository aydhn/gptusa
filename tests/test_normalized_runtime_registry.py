import pytest
from usa_signal_bot.advanced_runtime.normalized_runtime_registry import build_normalized_runtime_registry

def test_build_registry():
    reg = build_normalized_runtime_registry(None, {})
    assert reg.registry_normalized is True
    assert reg.safety_policy_valid is True
    assert reg.activation_allowed is False
