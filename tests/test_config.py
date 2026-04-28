import pytest
from pathlib import Path
from usa_signal_bot.core.config import load_app_config, config_to_dict
from usa_signal_bot.core.config_schema import AppConfig
from usa_signal_bot.core.exceptions import ConfigError

def test_default_config_load():
    # Will use the project's config/default.yaml
    config = load_app_config()
    assert isinstance(config, AppConfig)
    assert config.runtime.mode == "local_paper_only"
    assert config.runtime.broker_order_routing_enabled is False
    assert config.runtime.web_scraping_allowed is False
    assert config.runtime.dashboard_enabled is False
    assert config.universe.max_symbols_per_scan > 0

    # Test valid risk ratios
    assert 0.0 <= config.risk.max_position_pct <= 1.0
    assert 0.0 <= config.risk.max_daily_loss_pct <= 1.0

def test_invalid_broker_routing_guard(monkeypatch):
    from usa_signal_bot.core.config import validate_raw_config
    bad_config = {
        "runtime": {
            "broker_order_routing_enabled": True
        }
    }
    with pytest.raises(ConfigError, match="broker_order_routing_enabled must be False"):
        validate_raw_config(bad_config)

def test_invalid_web_scraping_guard():
    from usa_signal_bot.core.config import validate_raw_config
    bad_config = {
        "runtime": {
            "web_scraping_allowed": True
        }
    }
    with pytest.raises(ConfigError, match="web_scraping_allowed must be False"):
        validate_raw_config(bad_config)

def test_invalid_dashboard_guard():
    from usa_signal_bot.core.config import validate_raw_config
    bad_config = {
        "runtime": {
            "dashboard_enabled": True
        }
    }
    with pytest.raises(ConfigError, match="dashboard_enabled must be False"):
        validate_raw_config(bad_config)

def test_invalid_runtime_mode():
    from usa_signal_bot.core.config import validate_raw_config
    bad_config = {
        "runtime": {
            "mode": "live_trading"
        }
    }
    with pytest.raises(ConfigError, match="runtime.mode must be 'local_paper_only'"):
        validate_raw_config(bad_config)

def test_invalid_risk_ratio():
    from usa_signal_bot.core.config_schema import RiskConfig
    with pytest.raises(ConfigError, match="max_position_pct"):
        RiskConfig.from_dict({"max_position_pct": 1.5})
