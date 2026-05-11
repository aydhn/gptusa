from dataclasses import dataclass, field
from typing import Any
import uuid

from usa_signal_bot.core.enums import ResourceProfileScope, ThrottlingAction
from usa_signal_bot.core.exceptions import ThrottlingPolicyError

@dataclass
class ThrottlingPolicy:
    policy_id: str
    scope: ResourceProfileScope
    enabled: bool
    max_wall_time_seconds: float | None
    max_memory_peak_mb: float | None
    max_output_growth_mb: float | None
    max_file_growth_count: int | None
    action_on_warning: ThrottlingAction
    action_on_critical: ThrottlingAction
    description: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

def default_throttling_policies() -> list[ThrottlingPolicy]:
    policies = []

    policies.append(ThrottlingPolicy(
        policy_id=f"policy_{uuid.uuid4().hex[:8]}",
        scope=ResourceProfileScope.SCAN,
        enabled=True,
        max_wall_time_seconds=1800.0,
        max_memory_peak_mb=4096.0,
        max_output_growth_mb=512.0,
        max_file_growth_count=5000,
        action_on_warning=ThrottlingAction.WARN,
        action_on_critical=ThrottlingAction.REDUCE_SCOPE,
        description="Default policy for SCAN operations"
    ))

    policies.append(ThrottlingPolicy(
        policy_id=f"policy_{uuid.uuid4().hex[:8]}",
        scope=ResourceProfileScope.BACKTEST,
        enabled=True,
        max_wall_time_seconds=7200.0,
        max_memory_peak_mb=6144.0,
        max_output_growth_mb=1024.0,
        max_file_growth_count=10000,
        action_on_warning=ThrottlingAction.WARN,
        action_on_critical=ThrottlingAction.SPLIT,
        description="Default policy for BACKTEST operations"
    ))

    policies.append(ThrottlingPolicy(
        policy_id=f"policy_{uuid.uuid4().hex[:8]}",
        scope=ResourceProfileScope.REGRESSION,
        enabled=True,
        max_wall_time_seconds=3600.0,
        max_memory_peak_mb=4096.0,
        max_output_growth_mb=512.0,
        max_file_growth_count=5000,
        action_on_warning=ThrottlingAction.WARN,
        action_on_critical=ThrottlingAction.DELAY,
        description="Default policy for REGRESSION operations"
    ))

    policies.append(ThrottlingPolicy(
        policy_id=f"policy_{uuid.uuid4().hex[:8]}",
        scope=ResourceProfileScope.RETENTION,
        enabled=True,
        max_wall_time_seconds=600.0,
        max_memory_peak_mb=1024.0,
        max_output_growth_mb=10.0,
        max_file_growth_count=100,
        action_on_warning=ThrottlingAction.WARN,
        action_on_critical=ThrottlingAction.DRY_RUN_ONLY,
        description="Default policy for RETENTION operations"
    ))

    return policies

def policy_for_profile_scope(scope: ResourceProfileScope, policies: list[ThrottlingPolicy] | None = None) -> ThrottlingPolicy:
    if policies is None:
        policies = default_throttling_policies()

    for p in policies:
        if p.scope == scope:
            return p

    return ThrottlingPolicy(
        policy_id=f"policy_fallback_{uuid.uuid4().hex[:8]}",
        scope=scope,
        enabled=True,
        max_wall_time_seconds=300.0,
        max_memory_peak_mb=1024.0,
        max_output_growth_mb=100.0,
        max_file_growth_count=1000,
        action_on_warning=ThrottlingAction.WARN,
        action_on_critical=ThrottlingAction.REVIEW,
        description="Fallback policy"
    )

def load_throttling_policies_from_config(config_dict: dict[str, Any] | None = None) -> list[ThrottlingPolicy]:
    return default_throttling_policies()

def throttling_policy_to_dict(policy: ThrottlingPolicy) -> dict:
    return {
        "policy_id": policy.policy_id,
        "scope": policy.scope.value,
        "enabled": policy.enabled,
        "max_wall_time_seconds": policy.max_wall_time_seconds,
        "max_memory_peak_mb": policy.max_memory_peak_mb,
        "max_output_growth_mb": policy.max_output_growth_mb,
        "max_file_growth_count": policy.max_file_growth_count,
        "action_on_warning": policy.action_on_warning.value,
        "action_on_critical": policy.action_on_critical.value,
        "description": policy.description,
        "metadata": policy.metadata
    }

def validate_throttling_policy(policy: ThrottlingPolicy) -> None:
    if policy.max_wall_time_seconds is not None and policy.max_wall_time_seconds < 0:
        raise ThrottlingPolicyError("max_wall_time_seconds cannot be negative")
    if policy.max_memory_peak_mb is not None and policy.max_memory_peak_mb < 0:
        raise ThrottlingPolicyError("max_memory_peak_mb cannot be negative")
    if policy.max_output_growth_mb is not None and policy.max_output_growth_mb < 0:
        raise ThrottlingPolicyError("max_output_growth_mb cannot be negative")
    if policy.max_file_growth_count is not None and policy.max_file_growth_count < 0:
        raise ThrottlingPolicyError("max_file_growth_count cannot be negative")

def throttling_policies_to_text(policies: list[ThrottlingPolicy]) -> str:
    lines = []
    for p in policies:
        lines.append(f"Policy: {p.scope.value} (Enabled: {p.enabled})")
        lines.append(f"  Max Wall Time: {p.max_wall_time_seconds}s")
        lines.append(f"  Max Memory Peak: {p.max_memory_peak_mb}MB")
        lines.append(f"  Critical Action: {p.action_on_critical.value}")
    return "\n".join(lines)
