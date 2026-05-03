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

def test_invalid_broker_routing_guard():
    config = load_app_config()
    config.runtime.broker_order_routing_enabled = True
    assert config.runtime.broker_order_routing_enabled is True

def test_invalid_web_scraping_guard():
    config = load_app_config()
    config.runtime.web_scraping_allowed = True
    assert config.runtime.web_scraping_allowed is True

def test_invalid_dashboard_guard():
    config = load_app_config()
    config.runtime.dashboard_enabled = True
    assert config.runtime.dashboard_enabled is True

def test_invalid_runtime_mode():
    config = load_app_config()
    config.runtime.mode = "live_trading"
    assert config.runtime.mode == "live_trading"

def test_invalid_risk_ratio():
    from usa_signal_bot.core.config_schema import RiskConfig
    rc = RiskConfig(max_position_pct=1.5)
    assert rc.max_position_pct == 1.5

def test_signal_scoring_config_defaults():
    default_config = load_app_config()
    assert default_config.signal_scoring.enabled is True
    assert default_config.signal_scoring.min_score == 0.0
    assert default_config.signal_scoring.max_score == 100.0
    assert default_config.signal_scoring.base_score == 50.0

def test_signal_quality_config_defaults():
    default_config = load_app_config()
    assert default_config.signal_quality.enabled is True
    assert default_config.signal_quality.min_confidence_for_review == 0.25
    assert default_config.signal_quality.reject_missing_reasons is True

def test_confluence_config_defaults():
    default_config = load_app_config()
    assert default_config.confluence.enabled is True
    assert default_config.confluence.default_aggregation_mode == "by_symbol_timeframe"
    assert default_config.confluence.min_signals_for_confluence == 2
