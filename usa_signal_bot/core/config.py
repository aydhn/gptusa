"""Configuration management for USA Signal Bot."""

import yaml
from pathlib import Path
from dataclasses import asdict
from typing import Optional

from usa_signal_bot.core.config_schema import AppConfig
from usa_signal_bot.core.exceptions import ConfigError
from usa_signal_bot.utils.dict_utils import deep_merge_dicts
from usa_signal_bot.core import paths

def validate_config(config: AppConfig) -> None:
    """Validates the application configuration to ensure core restrictions are respected."""
    # Enforce safe mode constraints
    if config.runtime.broker_order_routing_enabled:
        raise ConfigError("CRITICAL: broker_order_routing_enabled MUST be False in this project.")

    if config.runtime.web_scraping_allowed:
        raise ConfigError("CRITICAL: web_scraping_allowed MUST be False. Web scraping is strictly forbidden.")

    if config.runtime.dashboard_enabled:
        raise ConfigError("CRITICAL: dashboard_enabled MUST be False. UI components are forbidden.")

    if config.runtime.mode != "local_paper_only":
        raise ConfigError(f"CRITICAL: runtime mode must be 'local_paper_only', got '{config.runtime.mode}'.")
    # Validate logging config
    if config.logging.max_bytes <= 0:
        raise ConfigError("logging.max_bytes must be positive")
    if config.logging.backup_count < 0:
        raise ConfigError("logging.backup_count cannot be negative")

    if config.universe.symbol_max_length <= 1:
        raise ConfigError("universe.symbol_max_length must be > 1")
    if not config.universe.default_currency:
        raise ConfigError("universe.default_currency cannot be empty")
    if config.universe.max_symbols_per_scan <= 0:
        raise ConfigError("universe.max_symbols_per_scan must be positive")
    if not config.universe.include_stocks and not config.universe.include_etfs:
        raise ConfigError("Both include_stocks and include_etfs cannot be False")
    for at in config.universe.asset_types:
        if at.lower() not in ("stock", "etf"):
            raise ConfigError(f"Invalid asset_type in config: {at}")


    if config.universe.symbol_max_length <= 1:
        raise ConfigError("universe.symbol_max_length must be > 1")
    if not config.universe.default_currency:
        raise ConfigError("universe.default_currency cannot be empty")
    if config.universe.max_symbols_per_scan <= 0:
        raise ConfigError("universe.max_symbols_per_scan must be positive")
    if not config.universe.include_stocks and not config.universe.include_etfs:
        raise ConfigError("Both include_stocks and include_etfs cannot be False")
    for at in config.universe.asset_types:
        if at.lower() not in ("stock", "etf"):
            raise ConfigError(f"Invalid asset_type in config: {at}")

    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if config.logging.level.upper() not in valid_levels:
        raise ConfigError(f"Invalid logging level: {config.logging.level}")

    # Validate storage config
    if not config.storage.enabled:
        raise ConfigError("CRITICAL: storage.enabled MUST be True.")
    if config.storage.parquet_enabled:
        raise ConfigError("CRITICAL: storage.parquet_enabled MUST be False in this phase.")
    if not (0 <= config.storage.default_json_indent <= 8):
        raise ConfigError("storage.default_json_indent must be between 0 and 8.")
    if not config.storage.manifests_dir:
        raise ConfigError("storage.manifests_dir cannot be empty.")
    if not config.storage.features_dir:
        raise ConfigError("storage.features_dir cannot be empty.")
    if not config.storage.models_dir:
        raise ConfigError("storage.models_dir cannot be empty.")


def _load_yaml(file_path: Path) -> dict:
    """Loads a YAML file and returns its content as a dictionary."""
    if not file_path.exists():
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if data is not None else {}
    except yaml.YAMLError as e:
        raise ConfigError(f"Error parsing YAML file {file_path}: {e}")

def load_app_config(config_dir: Optional[Path] = None) -> AppConfig:
    """
    Loads and merges the application configuration.
    It reads default.yaml and overrides it with local.yaml if present.
    """
    cfg_dir = config_dir or paths.CONFIG_DIR
    default_path = cfg_dir / "default.yaml"
    local_path = cfg_dir / "local.yaml"

    if not default_path.exists():
        raise ConfigError(f"Default configuration file not found at {default_path}")

    default_cfg = _load_yaml(default_path)
    local_cfg = _load_yaml(local_path)

    merged_cfg_dict = deep_merge_dicts(default_cfg, local_cfg)

    # Simple manual deserialization mapping nested dicts to dataclasses
    try:
        config = AppConfig()

        if "project" in merged_cfg_dict:
            for k, v in merged_cfg_dict["project"].items():
                setattr(config.project, k, v)

        if "runtime" in merged_cfg_dict:
            for k, v in merged_cfg_dict["runtime"].items():
                setattr(config.runtime, k, v)

        if "data" in merged_cfg_dict:
            for k, v in merged_cfg_dict["data"].items():
                setattr(config.data, k, v)

        if "logging" in merged_cfg_dict:
            for k, v in merged_cfg_dict["logging"].items():
                setattr(config.logging, k, v)

        if "telegram" in merged_cfg_dict:
            for k, v in merged_cfg_dict["telegram"].items():
                setattr(config.telegram, k, v)

        if "universe" in merged_cfg_dict:
            for k, v in merged_cfg_dict["universe"].items():
                setattr(config.universe, k, v)

        if "paper" in merged_cfg_dict:
            for k, v in merged_cfg_dict["paper"].items():
                setattr(config.paper, k, v)

        if "risk" in merged_cfg_dict:
            for k, v in merged_cfg_dict["risk"].items():
                setattr(config.risk, k, v)

        if "backtest" in merged_cfg_dict:
            for k, v in merged_cfg_dict["backtest"].items():
                setattr(config.backtest, k, v)

        if "optimization" in merged_cfg_dict:
            for k, v in merged_cfg_dict["optimization"].items():
                setattr(config.optimization, k, v)

        if "regime" in merged_cfg_dict:
            for k, v in merged_cfg_dict["regime"].items():
                setattr(config.regime, k, v)


        if "ml" in merged_cfg_dict:
            for k, v in merged_cfg_dict["ml"].items():
                setattr(config.ml, k, v)

        if "storage" in merged_cfg_dict:
            for k, v in merged_cfg_dict["storage"].items():
                setattr(config.storage, k, v)


        validate_config(config)
        return config

    except Exception as e:
        if isinstance(e, ConfigError):
            raise
        raise ConfigError(f"Error mapping configuration to schema: {e}")

def config_to_dict(config: AppConfig) -> dict:
    """Converts the active configuration back to a dictionary."""
    return asdict(config)
