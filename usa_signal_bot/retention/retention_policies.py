from typing import Any
from usa_signal_bot.core.enums import RetentionArtifactType, RetentionPolicyAction
from usa_signal_bot.retention.retention_models import (
    RetentionPolicy,
    create_retention_policy_id,
)

_DEFAULT_POLICY_SPECS = [
    {
        "id_prefix": "DATA_CACHE",
        "artifact_type": RetentionArtifactType.DATA_CACHE,
        "name": "Data Cache Policy",
        "keep_latest": 5,
        "max_age_days": 180,
        "action": RetentionPolicyAction.REVIEW,
    },
    {
        "id_prefix": "RUNTIME_SCAN",
        "artifact_type": RetentionArtifactType.RUNTIME_SCAN,
        "name": "Runtime Scan Policy",
        "keep_latest": 50,
        "max_age_days": 90,
        "action": RetentionPolicyAction.DELETE,
    },
    {
        "id_prefix": "BACKTEST_RUN",
        "artifact_type": RetentionArtifactType.BACKTEST_RUN,
        "name": "Backtest Run Policy",
        "keep_latest": 30,
        "max_age_days": 180,
        "action": RetentionPolicyAction.REVIEW,
    },
    {
        "id_prefix": "PAPER_RUN",
        "artifact_type": RetentionArtifactType.PAPER_RUN,
        "name": "Paper Run Policy",
        "keep_latest": 50,
        "max_age_days": 180,
        "action": RetentionPolicyAction.REVIEW,
    },
    {
        "id_prefix": "PAPER_ANALYTICS",
        "artifact_type": RetentionArtifactType.PAPER_ANALYTICS,
        "name": "Paper Analytics Policy",
        "keep_latest": 50,
        "max_age_days": 180,
        "action": RetentionPolicyAction.DELETE,
    },
    {
        "id_prefix": "COMPARISON_RUN",
        "artifact_type": RetentionArtifactType.COMPARISON_RUN,
        "name": "Comparison Run Policy",
        "keep_latest": 30,
        "max_age_days": 180,
        "action": RetentionPolicyAction.DELETE,
    },
    {
        "id_prefix": "QUALITY_RUN",
        "artifact_type": RetentionArtifactType.QUALITY_RUN,
        "name": "Quality Run Policy",
        "keep_latest": 30,
        "max_age_days": 180,
        "action": RetentionPolicyAction.DELETE,
    },
    {
        "id_prefix": "REGRESSION_RUN",
        "artifact_type": RetentionArtifactType.REGRESSION_RUN,
        "name": "Regression Run Policy",
        "keep_latest": 30,
        "max_age_days": 180,
        "action": RetentionPolicyAction.DELETE,
    },
    {
        "id_prefix": "RELEASE_BUILD",
        "artifact_type": RetentionArtifactType.RELEASE_BUILD,
        "name": "Release Build Policy",
        "keep_latest": 10,
        "max_age_days": 365,
        "action": RetentionPolicyAction.REVIEW,
        "protected": True,
    },
    {
        "id_prefix": "BACKUP",
        "artifact_type": RetentionArtifactType.BACKUP,
        "name": "Backup Policy",
        "keep_latest": 10,
        "max_age_days": 365,
        "action": RetentionPolicyAction.REVIEW,
        "protected": True,
    },
    {
        "id_prefix": "OBSERVABILITY_LOG",
        "artifact_type": RetentionArtifactType.OBSERVABILITY_LOG,
        "name": "Observability Log Policy",
        "keep_latest": 10,
        "max_age_days": 60,
        "action": RetentionPolicyAction.DELETE,
    },
    {
        "id_prefix": "TEMP_FILE",
        "artifact_type": RetentionArtifactType.TEMP_FILE,
        "name": "Temp File Policy",
        "keep_latest": 0,
        "max_age_days": 7,
        "action": RetentionPolicyAction.DELETE,
    },
]


def default_retention_policies() -> list[RetentionPolicy]:
    policies = []
    for spec in _DEFAULT_POLICY_SPECS:
        kwargs = spec.copy()
        id_prefix = kwargs.pop("id_prefix")
        kwargs["policy_id"] = create_retention_policy_id(id_prefix)
        kwargs["enabled"] = True
        policies.append(RetentionPolicy(**kwargs))
    return policies


def policy_for_artifact_type(
    policies: list[RetentionPolicy], artifact_type: RetentionArtifactType
) -> RetentionPolicy | None:
    for p in policies:
        if p.artifact_type == artifact_type and p.enabled:
            return p
    return None


def load_retention_policies_from_config(
    config_dict: dict[str, Any] | None = None,
) -> list[RetentionPolicy]:
    return default_retention_policies()


def retention_policies_to_text(policies: list[RetentionPolicy]) -> str:
    lines = []
    for p in policies:
        lines.append(
            f"[{p.artifact_type.value}] {p.name}: Action={p.action.value}, Keep={p.keep_latest}, MaxAge={p.max_age_days}"
        )
    return "\n".join(lines)
