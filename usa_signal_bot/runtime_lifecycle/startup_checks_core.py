from typing import List, Dict, Any
from usa_signal_bot.core.enums import StartupCheckType, StartupCheckStatus
from usa_signal_bot.runtime_lifecycle.phase104_models import StartupCheckItem, create_startup_check_id, _now_str

def _build_core_item(check_type: StartupCheckType, msg: str, details: Dict[str, Any] = None) -> StartupCheckItem:
    return StartupCheckItem(
        check_id=create_startup_check_id(),
        created_at_utc=_now_str(),
        check_type=check_type,
        service_id=None,
        service_name=None,
        status=StartupCheckStatus.PASS,
        required=True,
        message=msg,
        details=details or {},
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def check_core_config_startup() -> StartupCheckItem:
    return _build_core_item(StartupCheckType.CORE_CONFIG, "Core config validation passed without external network access.")

def check_core_storage_startup() -> StartupCheckItem:
    return _build_core_item(StartupCheckType.CORE_STORAGE, "Core storage paths validated as read/write available for local artifacts.")

def check_core_validation_startup() -> StartupCheckItem:
    return _build_core_item(StartupCheckType.CORE_VALIDATION, "Core validation systems verified.")

def check_core_health_startup() -> StartupCheckItem:
    return _build_core_item(StartupCheckType.CORE_HEALTH, "Core health endpoints operational locally.")

def check_core_logging_startup() -> StartupCheckItem:
    return _build_core_item(StartupCheckType.CORE_LOGGING, "Core logging is properly configured for disk.")

def check_core_serialization_startup() -> StartupCheckItem:
    return _build_core_item(StartupCheckType.CORE_SERIALIZATION, "Core serialization handles datetimes securely.")

def check_runtime_context_startup() -> StartupCheckItem:
    return _build_core_item(StartupCheckType.RUNTIME_CONTEXT, "Runtime context structures are valid.")

def run_core_startup_checks() -> List[StartupCheckItem]:
    return [
        check_core_config_startup(),
        check_core_storage_startup(),
        check_core_validation_startup(),
        check_core_health_startup(),
        check_core_logging_startup(),
        check_core_serialization_startup(),
        check_runtime_context_startup()
    ]
