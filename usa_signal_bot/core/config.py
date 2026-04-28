"""Configuration loading and validation module."""

from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from dataclasses import asdict

from usa_signal_bot.core.exceptions import ConfigError
from usa_signal_bot.core.paths import CONFIG_DIR
from usa_signal_bot.core.config_schema import AppConfig
from usa_signal_bot.utils.dict_utils import deep_merge_dicts

def load_yaml_file(file_path: Path) -> dict:
    """Loads a YAML file and returns its content as a dictionary."""
    if not file_path.exists():
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ConfigError(f"Failed to parse YAML file {file_path}: {e}")

def validate_raw_config(raw: dict) -> None:
    """Ensures strict architectural boundaries are respected via raw config checks."""
    runtime = raw.get("runtime", {})

    if runtime.get("broker_order_routing_enabled") is True:
        raise ConfigError("Strict Boundary Violation: broker_order_routing_enabled must be False.")

    if runtime.get("web_scraping_allowed") is True:
        raise ConfigError("Strict Boundary Violation: web_scraping_allowed must be False.")

    if runtime.get("dashboard_enabled") is True:
        raise ConfigError("Strict Boundary Violation: dashboard_enabled must be False.")

    mode = runtime.get("mode")
    if mode is not None and mode != "local_paper_only":
        raise ConfigError("Strict Boundary Violation: runtime.mode must be 'local_paper_only'.")

def validate_app_config(config: AppConfig) -> None:
    """Validates the strongly typed AppConfig instance."""
    if config.runtime.broker_order_routing_enabled is True:
        raise ConfigError("Strict Boundary Violation: broker_order_routing_enabled must be False.")

    if config.runtime.web_scraping_allowed is True:
        raise ConfigError("Strict Boundary Violation: web_scraping_allowed must be False.")

    if config.runtime.dashboard_enabled is True:
        raise ConfigError("Strict Boundary Violation: dashboard_enabled must be False.")

    if config.runtime.mode != "local_paper_only":
        raise ConfigError("Strict Boundary Violation: runtime.mode must be 'local_paper_only'.")

    if config.paper.allow_short is True:
        raise ConfigError("Phase 2 Guard: paper.allow_short must be False for now.")

def load_raw_config(config_dir: Optional[Path] = None, local_filename: str = "local.yaml") -> dict:
    """Loads default and local configs, merges them, and validates guardrails on raw dict."""
    config_dir = config_dir or CONFIG_DIR
    default_path = config_dir / "default.yaml"
    local_path = config_dir / local_filename

    if not default_path.exists():
        raise ConfigError(f"Missing required configuration file: {default_path}")

    default_config = load_yaml_file(default_path)
    local_config = load_yaml_file(local_path)

    merged_config = deep_merge_dicts(default_config, local_config)
    validate_raw_config(merged_config)

    return merged_config

def load_app_config(config_dir: Optional[Path] = None) -> AppConfig:
    """Loads raw config, converts to AppConfig, and fully validates it."""
    raw_config = load_raw_config(config_dir)
    app_config = AppConfig.from_dict(raw_config)
    validate_app_config(app_config)
    return app_config

def config_to_dict(config: AppConfig) -> dict:
    """Converts the typed AppConfig to a dictionary."""
    return asdict(config)

# Backward compatibility for existing code in Phase 1
def load_config() -> dict:
    app_config = load_app_config()
    return config_to_dict(app_config)
