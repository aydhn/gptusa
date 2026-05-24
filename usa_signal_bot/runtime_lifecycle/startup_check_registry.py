from typing import Dict, List
from usa_signal_bot.core.enums import StartupCheckType
from usa_signal_bot.core.exceptions import StartupCheckRegistryError

def required_startup_check_types() -> List[StartupCheckType]:
    return [
        StartupCheckType.CORE_CONFIG,
        StartupCheckType.CORE_STORAGE,
        StartupCheckType.CORE_VALIDATION,
        StartupCheckType.CORE_HEALTH,
        StartupCheckType.CORE_LOGGING,
        StartupCheckType.CORE_SERIALIZATION,
        StartupCheckType.RUNTIME_CONTEXT,
        StartupCheckType.SERVICE_GRAPH,
        StartupCheckType.DEPENDENCY_CONTRACTS,
        StartupCheckType.PROVIDER_INTERFACES,
        StartupCheckType.DATA_CACHE,
        StartupCheckType.DATA_QUALITY,
        StartupCheckType.OBSERVABILITY,
        StartupCheckType.NOTIFICATION_PREVIEW,
        StartupCheckType.CLI,
        StartupCheckType.NO_EXECUTION_SAFETY
    ]

def build_startup_check_registry() -> Dict[StartupCheckType, str]:
    return {
        check_type: f"usa_signal_bot.runtime_lifecycle.startup_checks_{check_type.name.lower()}"
        for check_type in required_startup_check_types()
    }

def validate_startup_check_registry(registry: Dict[StartupCheckType, str]) -> List[str]:
    errors = []
    required = required_startup_check_types()
    for req in required:
        if req not in registry:
            errors.append(f"Missing required startup check in registry: {req.name}")
    return errors

def startup_check_registry_to_text(registry: Dict[StartupCheckType, str]) -> str:
    lines = ["=== STARTUP CHECK REGISTRY ==="]
    for k, v in registry.items():
        lines.append(f"{k.name}: {v}")
    return "\n".join(lines)
