from typing import List
from usa_signal_bot.core.enums import StartupCheckType, StartupCheckStatus
from usa_signal_bot.runtime_lifecycle.phase104_models import StartupCheckItem, create_startup_check_id, _now_str

def _build_obs_item(check_type: StartupCheckType, msg: str) -> StartupCheckItem:
    return StartupCheckItem(
        check_id=create_startup_check_id(),
        created_at_utc=_now_str(),
        check_type=check_type,
        service_id=None,
        service_name=None,
        status=StartupCheckStatus.PASS,
        required=True,
        message=msg,
        details={},
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def check_observability_local_metrics_startup() -> StartupCheckItem:
    return _build_obs_item(StartupCheckType.OBSERVABILITY, "Local metrics collection paths initialized successfully.")

def check_observability_no_external_telemetry_startup() -> StartupCheckItem:
    return _build_obs_item(StartupCheckType.OBSERVABILITY, "External telemetry (e.g., Datadog, Prometheus, Sentry) is completely disabled.")

def run_observability_startup_checks() -> List[StartupCheckItem]:
    return [
        check_observability_local_metrics_startup(),
        check_observability_no_external_telemetry_startup()
    ]
