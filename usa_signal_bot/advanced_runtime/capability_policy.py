from typing import Any
from usa_signal_bot.advanced_runtime.phase102_models import CapabilityPolicyRecord
from usa_signal_bot.core.enums import RuntimeRegistryRiskFlag, RuntimeCapability

def build_phase102_capability_policies() -> list[CapabilityPolicyRecord]:
    policies = []

    allowed_capabilities = [
        "READ_LOCAL_CONFIG",
        "READ_LOCAL_STORAGE",
        "WRITE_METADATA_ARTIFACT",
        "WRITE_TEST_ARTIFACT",
        "COMPUTE_INDICATORS",
        "COMPUTE_FEATURES"
    ]

    blocked_capabilities = [
        "PLACE_LIVE_BROKER_ORDER",
        "PLACE_PAPER_ORDER",
        "PLACE_DEMO_BROKER_ORDER",
        "MUTATE_PAPER_STATE",
        "SEND_TELEGRAM_REAL",
        "WEB_SCRAPE",
        "START_DASHBOARD",
        "PATCH_PRODUCTION_CONFIG"
    ]

    for cap in allowed_capabilities:
        policies.append(CapabilityPolicyRecord(
            capability_name=cap,
            status="ALLOWED",
            allowed=True,
            metadata_only=True,
            read_only=True,
            future_phase_allowed=True,
            blocked_reason=None,
            risk_flags=[],
            metadata={}
        ))

    for cap in blocked_capabilities:
        policies.append(CapabilityPolicyRecord(
            capability_name=cap,
            status="BLOCKED",
            allowed=False,
            metadata_only=False,
            read_only=False,
            future_phase_allowed=False,
            blocked_reason="Blocked in Phase 102",
            risk_flags=[],
            metadata={}
        ))

    return policies

def resolve_capability_policy(capability_name: str) -> CapabilityPolicyRecord:
    for policy in build_phase102_capability_policies():
        if policy.capability_name == capability_name:
            return policy
    return CapabilityPolicyRecord(
        capability_name=capability_name,
        status="BLOCKED",
        allowed=False,
        metadata_only=False,
        read_only=False,
        future_phase_allowed=False,
        blocked_reason="Unknown capability",
        risk_flags=[RuntimeRegistryRiskFlag.UNSAFE_CAPABILITY_ENABLED],
        metadata={}
    )

def capability_allowed(capability_name: str) -> bool:
    return resolve_capability_policy(capability_name).allowed

def capability_metadata_only(capability_name: str) -> bool:
    return resolve_capability_policy(capability_name).metadata_only

def capability_read_only(capability_name: str) -> bool:
    return resolve_capability_policy(capability_name).read_only

def validate_capability_policies(records: list[CapabilityPolicyRecord]) -> list[str]:
    errors = []
    for r in records:
        if r.allowed and r.capability_name in [
            "PLACE_LIVE_BROKER_ORDER", "PLACE_PAPER_ORDER", "MUTATE_PAPER_STATE", "SEND_TELEGRAM_REAL", "WEB_SCRAPE"
        ]:
            errors.append(f"Unsafe capability {r.capability_name} is allowed")
    return errors

def capability_policy_summary(records: list[CapabilityPolicyRecord]) -> dict[str, Any]:
    return {
        "total_policies": len(records),
        "allowed": [r.capability_name for r in records if r.allowed],
        "blocked": [r.capability_name for r in records if not r.allowed]
    }

def capability_policy_to_text(records: list[CapabilityPolicyRecord]) -> str:
    lines = ["--- Capability Policies ---"]
    for r in records:
        lines.append(f"Capability: {r.capability_name} | Allowed: {r.allowed} | Status: {r.status}")
    return "\n".join(lines)
