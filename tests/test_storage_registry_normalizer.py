import pytest
from usa_signal_bot.advanced_runtime.storage_registry_normalizer import normalize_storage_registry

def test_storage():
    assert normalize_storage_registry({"a": "b"}) == {"a": "b"}
