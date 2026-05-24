import pytest
from usa_signal_bot.advanced_runtime.observability_registry_normalizer import normalize_observability_registry

def test_obs():
    assert normalize_observability_registry({"a": "b"}) == {"a": "b"}
