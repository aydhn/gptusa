"""Tests for configuration boundaries and loading."""

import pytest
from usa_signal_bot.core.config import load_config, validate_config_guards
from usa_signal_bot.core.exceptions import ConfigError

def test_default_config_loading():
    """Verify the default config is loaded with correct baseline values."""
    config = load_config()

    assert config["runtime"]["broker_order_routing_enabled"] is False
    assert config["runtime"]["web_scraping_allowed"] is False
    assert config["runtime"]["dashboard_enabled"] is False
    assert config["runtime"]["mode"] == "local_paper_only"

def test_broker_routing_guard():
    """Verify that enabling broker routing raises an error."""
    bad_config = {
        "runtime": {
            "mode": "local_paper_only",
            "broker_order_routing_enabled": True,
            "web_scraping_allowed": False,
            "dashboard_enabled": False
        }
    }
    with pytest.raises(ConfigError, match="broker_order_routing_enabled must be False"):
        validate_config_guards(bad_config)

def test_web_scraping_guard():
    """Verify that enabling web scraping raises an error."""
    bad_config = {
        "runtime": {
            "mode": "local_paper_only",
            "broker_order_routing_enabled": False,
            "web_scraping_allowed": True,
            "dashboard_enabled": False
        }
    }
    with pytest.raises(ConfigError, match="web_scraping_allowed must be False"):
        validate_config_guards(bad_config)

def test_dashboard_guard():
    """Verify that enabling dashboard raises an error."""
    bad_config = {
        "runtime": {
            "mode": "local_paper_only",
            "broker_order_routing_enabled": False,
            "web_scraping_allowed": False,
            "dashboard_enabled": True
        }
    }
    with pytest.raises(ConfigError, match="dashboard_enabled must be False"):
        validate_config_guards(bad_config)

def test_mode_guard():
    """Verify that an invalid mode raises an error."""
    bad_config = {
        "runtime": {
            "mode": "live_trading",
            "broker_order_routing_enabled": False,
            "web_scraping_allowed": False,
            "dashboard_enabled": False
        }
    }
    with pytest.raises(ConfigError, match="runtime.mode must be 'local_paper_only'"):
        validate_config_guards(bad_config)
