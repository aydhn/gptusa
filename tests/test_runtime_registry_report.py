import pytest
from usa_signal_bot.advanced_runtime.runtime_registry_report import build_runtime_registry_full_review

def test_review():
    r = build_runtime_registry_full_review()
    assert r.registry.registry_normalized is True
