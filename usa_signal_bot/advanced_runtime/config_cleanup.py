from typing import Any
import copy

def normalize_config_surface(config: dict[str, Any]) -> dict[str, Any]:
    normalized = copy.deepcopy(config)
    normalized = apply_phase102_config_defaults(normalized)
    normalized = normalize_safety_config(normalized)
    normalized = normalize_provider_config(normalized)
    normalized = normalize_runtime_mode_config(normalized)
    return normalized

def normalize_safety_config(config: dict[str, Any]) -> dict[str, Any]:
    if "safety" not in config:
        config["safety"] = {}

    # Enforce safe defaults
    config["safety"]["allow_broker_execution"] = False
    config["safety"]["allow_paper_state_mutation"] = False
    config["safety"]["allow_telegram_real_send"] = False
    config["safety"]["allow_scraping"] = False
    config["safety"]["allow_dashboard"] = False
    return config

def normalize_provider_config(config: dict[str, Any]) -> dict[str, Any]:
    if "provider" not in config:
        config["provider"] = {}

    config["provider"]["allow_paid_api"] = False
    config["provider"]["allow_scraping"] = False
    return config

def normalize_runtime_mode_config(config: dict[str, Any]) -> dict[str, Any]:
    return config

def apply_phase102_config_defaults(config: dict[str, Any]) -> dict[str, Any]:
    if "advanced_runtime" not in config:
        config["advanced_runtime"] = {}
    config["advanced_runtime"]["current_phase"] = 102
    return config

def config_cleanup_summary(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "normalized",
        "changed_keys": []
    }

def config_cleanup_to_text(summary: dict[str, Any]) -> str:
    return f"Config cleanup complete. Status: {summary['status']}"
