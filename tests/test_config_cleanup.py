import pytest
from usa_signal_bot.advanced_runtime.config_cleanup import normalize_config_surface

def test_normalize():
    config = {"safety": {"allow_broker_execution": True}}
    norm = normalize_config_surface(config)
    assert norm["safety"]["allow_broker_execution"] is False
