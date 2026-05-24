import pytest
from usa_signal_bot.advanced_runtime.runtime_registry_store import runtime_registry_store_dir
from pathlib import Path

def test_store():
    d = runtime_registry_store_dir(Path("data"))
    assert d.name == "advanced_runtime"
