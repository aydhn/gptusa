from typing import List, Dict, Any
from usa_signal_bot.core.enums import RuntimeCapability, RuntimeCapabilityStatus, AdvancedTransitionRiskFlag
from usa_signal_bot.advanced_transition.phase101_models import RuntimeCapabilityRecord

def allowed_phase101_capabilities() -> List[RuntimeCapability]:
    return [
        RuntimeCapability.READ_LOCAL_CONFIG,
        RuntimeCapability.READ_LOCAL_STORAGE,
        RuntimeCapability.WRITE_METADATA_ARTIFACT,
        RuntimeCapability.WRITE_TEST_ARTIFACT,
        RuntimeCapability.READ_MARKET_DATA_CACHE,
        RuntimeCapability.FETCH_FREE_MARKET_DATA,
        RuntimeCapability.COMPUTE_INDICATORS,
        RuntimeCapability.COMPUTE_FEATURES
    ]

def blocked_phase101_capabilities() -> List[RuntimeCapability]:
    return [
        RuntimeCapability.SEND_TELEGRAM_REAL,
        RuntimeCapability.PLACE_PAPER_ORDER,
        RuntimeCapability.PLACE_DEMO_BROKER_ORDER,
        RuntimeCapability.PLACE_LIVE_BROKER_ORDER,
        RuntimeCapability.MUTATE_PAPER_STATE,
        RuntimeCapability.PATCH_PRODUCTION_CONFIG,
        RuntimeCapability.START_DASHBOARD,
        RuntimeCapability.WEB_SCRAPE
    ]

def build_phase101_capability_matrix() -> List[RuntimeCapabilityRecord]:
    records = []
    for cap in allowed_phase101_capabilities():
        records.append(RuntimeCapabilityRecord(
            capability=cap,
            status=RuntimeCapabilityStatus.ALLOWED_METADATA_ONLY,
            reason="Safe local read or metadata generation",
            allowed_in_phase_101=True,
            requires_future_phase=False,
            risk_flags=[],
            metadata={}
        ))
    for cap in blocked_phase101_capabilities():
        records.append(RuntimeCapabilityRecord(
            capability=cap,
            status=RuntimeCapabilityStatus.BLOCKED,
            reason="Blocked to prevent live actions",
            allowed_in_phase_101=False,
            requires_future_phase=False,
            risk_flags=[AdvancedTransitionRiskFlag.PAPER_ORDER_RISK],
            metadata={}
        ))
    return records

def validate_capability_matrix(records: List[RuntimeCapabilityRecord]) -> List[str]:
    errors = []
    blocked_caps = set(blocked_phase101_capabilities())
    for record in records:
        if record.capability in blocked_caps and record.status != RuntimeCapabilityStatus.BLOCKED:
            errors.append(f"{record.capability.name} must be BLOCKED")
    return errors

def capability_matrix_summary(records: List[RuntimeCapabilityRecord]) -> Dict[str, Any]:
    return {"total": len(records), "blocked": sum(1 for r in records if r.status == RuntimeCapabilityStatus.BLOCKED)}

def capability_matrix_to_text(records: List[RuntimeCapabilityRecord]) -> str:
    return "\n".join([f"{r.capability.name}: {r.status.name}" for r in records])
