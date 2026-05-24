import pytest
from usa_signal_bot.advanced_runtime.provider_safety_manifest import build_provider_safety_manifest

def test_safety_manifest():
    m = build_provider_safety_manifest("test")
    assert m.safe_for_phase102 is True
