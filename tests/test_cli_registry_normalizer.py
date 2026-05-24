import pytest
from usa_signal_bot.advanced_runtime.cli_registry_normalizer import normalize_cli_registry

def test_cli():
    assert normalize_cli_registry({"a": "b"}) == {"a": "b"}
