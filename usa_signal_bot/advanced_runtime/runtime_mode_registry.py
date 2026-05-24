from typing import Any
from usa_signal_bot.advanced_runtime.phase102_models import RuntimeModeRecord, RuntimeMode
from usa_signal_bot.core.enums import RuntimeRegistryRiskFlag

def build_phase102_runtime_modes() -> list[RuntimeModeRecord]:
    return [
        RuntimeModeRecord(
            mode=RuntimeMode.OFFLINE_METADATA,
            enabled=True,
            allowed_in_phase102=True,
            description="Offline metadata mode",
            blocked_capabilities=["FETCH_FREE_MARKET_DATA", "PLACE_PAPER_ORDER", "PLACE_LIVE_BROKER_ORDER"],
            allowed_capabilities=["READ_LOCAL_CONFIG"],
            risk_flags=[],
            metadata={}
        ),
        RuntimeModeRecord(
            mode=RuntimeMode.LOCAL_READ_ONLY,
            enabled=True,
            allowed_in_phase102=True,
            description="Local read only mode",
            blocked_capabilities=["PLACE_PAPER_ORDER", "PLACE_LIVE_BROKER_ORDER"],
            allowed_capabilities=["READ_LOCAL_CONFIG"],
            risk_flags=[],
            metadata={}
        ),
        RuntimeModeRecord(
            mode=RuntimeMode.LOCAL_COMPUTE_ONLY,
            enabled=True,
            allowed_in_phase102=True,
            description="Local compute only mode",
            blocked_capabilities=["PLACE_PAPER_ORDER", "PLACE_LIVE_BROKER_ORDER"],
            allowed_capabilities=["READ_LOCAL_CONFIG", "COMPUTE_INDICATORS"],
            risk_flags=[],
            metadata={}
        ),
        RuntimeModeRecord(
            mode=RuntimeMode.PROVIDER_READY_NO_FETCH,
            enabled=True,
            allowed_in_phase102=True,
            description="Provider ready no fetch mode",
            blocked_capabilities=["FETCH_FREE_MARKET_DATA", "PLACE_PAPER_ORDER", "PLACE_LIVE_BROKER_ORDER"],
            allowed_capabilities=["READ_LOCAL_CONFIG"],
            risk_flags=[],
            metadata={}
        ),
        RuntimeModeRecord(
            mode=RuntimeMode.LOCAL_PAPER_SIMULATION_DISABLED,
            enabled=False,
            allowed_in_phase102=False,
            description="Local paper simulation disabled mode",
            blocked_capabilities=[],
            allowed_capabilities=[],
            risk_flags=[],
            metadata={}
        ),
        RuntimeModeRecord(
            mode=RuntimeMode.ACTIVE_PAPER_DISABLED,
            enabled=False,
            allowed_in_phase102=False,
            description="Active paper disabled mode",
            blocked_capabilities=[],
            allowed_capabilities=[],
            risk_flags=[],
            metadata={}
        ),
        RuntimeModeRecord(
            mode=RuntimeMode.BROKER_EXECUTION_DISABLED,
            enabled=False,
            allowed_in_phase102=False,
            description="Broker execution disabled mode",
            blocked_capabilities=[],
            allowed_capabilities=[],
            risk_flags=[],
            metadata={}
        )
    ]

def runtime_mode_by_name(name: str) -> RuntimeModeRecord | None:
    for mode in build_phase102_runtime_modes():
        if mode.mode.value == name:
            return mode
    return None

def validate_runtime_modes(records: list[RuntimeModeRecord]) -> list[str]:
    errors = []
    for r in records:
        if r.mode in [RuntimeMode.ACTIVE_PAPER_DISABLED, RuntimeMode.BROKER_EXECUTION_DISABLED]:
            if r.enabled:
                errors.append(f"{r.mode.value} should not be enabled")
    return errors

def runtime_mode_summary(records: list[RuntimeModeRecord]) -> dict[str, Any]:
    return {
        "total_modes": len(records),
        "enabled_modes": [r.mode.value for r in records if r.enabled],
        "disabled_modes": [r.mode.value for r in records if not r.enabled]
    }

def runtime_mode_registry_to_text(records: list[RuntimeModeRecord]) -> str:
    lines = ["--- Runtime Mode Registry ---"]
    for r in records:
        lines.append(f"Mode: {r.mode.value} | Enabled: {r.enabled} | Allowed in 102: {r.allowed_in_phase102}")
    return "\n".join(lines)
