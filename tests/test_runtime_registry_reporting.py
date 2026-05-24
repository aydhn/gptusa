import pytest
from usa_signal_bot.advanced_runtime.runtime_registry_reporting import runtime_registry_limitations_text

def test_rep():
    assert "NOT activation" in runtime_registry_limitations_text()
