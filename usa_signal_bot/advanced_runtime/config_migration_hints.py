from typing import Any

def generate_config_migration_hints(config: dict[str, Any]) -> list[str]:
    hints = []
    hints.extend(provider_config_migration_hints(config))
    hints.extend(runtime_mode_migration_hints(config))
    return hints

def hint_for_unsafe_key(key: str, value: Any) -> str:
    return f"Key '{key}' with value '{value}' is unsafe. Set to False for Phase 102."

def provider_config_migration_hints(config: dict[str, Any]) -> list[str]:
    hints = []
    provider = config.get("provider", {})
    if provider.get("allow_paid_api"):
        hints.append(hint_for_unsafe_key("provider.allow_paid_api", True))
    return hints

def runtime_mode_migration_hints(config: dict[str, Any]) -> list[str]:
    hints = []
    safety = config.get("safety", {})
    if safety.get("allow_broker_execution"):
        hints.append(hint_for_unsafe_key("safety.allow_broker_execution", True))
    return hints

def config_migration_hints_to_text(hints: list[str]) -> str:
    lines = ["--- Config Migration Hints ---"]
    if not hints:
        lines.append("No migration hints.")
    else:
        for h in hints:
            lines.append(f" - {h}")
    return "\n".join(lines)
