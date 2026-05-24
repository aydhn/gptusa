import pytest
from usa_signal_bot.advanced_runtime.config_surface import build_config_surface_records

def test_build_records():
    records = build_config_surface_records({})
    assert len(records) > 0
    domains = [r.domain.value for r in records]
    assert "SAFETY" in domains
