"""Configuration loading and validation module."""

import os
from pathlib import Path
from typing import Dict, Any
import yaml

from usa_signal_bot.core.exceptions import ConfigError
from usa_signal_bot.core.paths import CONFIG_DIR

def load_yaml(file_path: Path) -> Dict[str, Any]:
    """Loads a YAML file and returns its content as a dictionary."""
    if not file_path.exists():
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ConfigError(f"Failed to parse YAML file {file_path}: {e}")

def merge_dicts(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merges two dictionaries."""
    merged = base.copy()
    for key, value in override.items():
        if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
            merged[key] = merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged

def validate_config_guards(config: Dict[str, Any]) -> None:
    """Ensures strict architectural boundaries are respected via config checks."""
    runtime = config.get("runtime", {})

    if runtime.get("broker_order_routing_enabled") is True:
        raise ConfigError("Strict Boundary Violation: broker_order_routing_enabled must be False.")

    if runtime.get("web_scraping_allowed") is True:
        raise ConfigError("Strict Boundary Violation: web_scraping_allowed must be False.")

    if runtime.get("dashboard_enabled") is True:
        raise ConfigError("Strict Boundary Violation: dashboard_enabled must be False.")

    if runtime.get("mode") != "local_paper_only":
        raise ConfigError("Strict Boundary Violation: runtime.mode must be 'local_paper_only'.")

def load_config() -> Dict[str, Any]:
    """Loads default and local configs, merges them, and validates guardrails."""
    default_path = CONFIG_DIR / "default.yaml"
    local_path = CONFIG_DIR / "local.yaml"

    if not default_path.exists():
        raise ConfigError(f"Missing required configuration file: {default_path}")

    default_config = load_yaml(default_path)
    local_config = load_yaml(local_path)

    merged_config = merge_dicts(default_config, local_config)

    validate_config_guards(merged_config)

    return merged_config
