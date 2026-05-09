from typing import Any
from usa_signal_bot.core.enums import RetentionArtifactType, RetentionPolicyAction
from usa_signal_bot.retention.retention_models import RetentionPolicy, create_retention_policy_id

def default_retention_policies() -> list[RetentionPolicy]:
    return [
        RetentionPolicy(
            policy_id=create_retention_policy_id("DATA_CACHE"),
            artifact_type=RetentionArtifactType.DATA_CACHE,
            name="Data Cache Policy",
            enabled=True,
            keep_latest=5,
            max_age_days=180,
            action=RetentionPolicyAction.REVIEW
        ),
        RetentionPolicy(
            policy_id=create_retention_policy_id("RUNTIME_SCAN"),
            artifact_type=RetentionArtifactType.RUNTIME_SCAN,
            name="Runtime Scan Policy",
            enabled=True,
            keep_latest=50,
            max_age_days=90,
            action=RetentionPolicyAction.DELETE
        ),
        RetentionPolicy(
            policy_id=create_retention_policy_id("BACKTEST_RUN"),
            artifact_type=RetentionArtifactType.BACKTEST_RUN,
            name="Backtest Run Policy",
            enabled=True,
            keep_latest=30,
            max_age_days=180,
            action=RetentionPolicyAction.REVIEW
        ),
        RetentionPolicy(
            policy_id=create_retention_policy_id("PAPER_RUN"),
            artifact_type=RetentionArtifactType.PAPER_RUN,
            name="Paper Run Policy",
            enabled=True,
            keep_latest=50,
            max_age_days=180,
            action=RetentionPolicyAction.REVIEW
        ),
        RetentionPolicy(
            policy_id=create_retention_policy_id("PAPER_ANALYTICS"),
            artifact_type=RetentionArtifactType.PAPER_ANALYTICS,
            name="Paper Analytics Policy",
            enabled=True,
            keep_latest=50,
            max_age_days=180,
            action=RetentionPolicyAction.DELETE
        ),
        RetentionPolicy(
            policy_id=create_retention_policy_id("COMPARISON_RUN"),
            artifact_type=RetentionArtifactType.COMPARISON_RUN,
            name="Comparison Run Policy",
            enabled=True,
            keep_latest=30,
            max_age_days=180,
            action=RetentionPolicyAction.DELETE
        ),
        RetentionPolicy(
            policy_id=create_retention_policy_id("QUALITY_RUN"),
            artifact_type=RetentionArtifactType.QUALITY_RUN,
            name="Quality Run Policy",
            enabled=True,
            keep_latest=30,
            max_age_days=180,
            action=RetentionPolicyAction.DELETE
        ),
        RetentionPolicy(
            policy_id=create_retention_policy_id("REGRESSION_RUN"),
            artifact_type=RetentionArtifactType.REGRESSION_RUN,
            name="Regression Run Policy",
            enabled=True,
            keep_latest=30,
            max_age_days=180,
            action=RetentionPolicyAction.DELETE
        ),
        RetentionPolicy(
            policy_id=create_retention_policy_id("RELEASE_BUILD"),
            artifact_type=RetentionArtifactType.RELEASE_BUILD,
            name="Release Build Policy",
            enabled=True,
            keep_latest=10,
            max_age_days=365,
            action=RetentionPolicyAction.REVIEW,
            protected=True
        ),
        RetentionPolicy(
            policy_id=create_retention_policy_id("BACKUP"),
            artifact_type=RetentionArtifactType.BACKUP,
            name="Backup Policy",
            enabled=True,
            keep_latest=10,
            max_age_days=365,
            action=RetentionPolicyAction.REVIEW,
            protected=True
        ),
        RetentionPolicy(
            policy_id=create_retention_policy_id("OBSERVABILITY_LOG"),
            artifact_type=RetentionArtifactType.OBSERVABILITY_LOG,
            name="Observability Log Policy",
            enabled=True,
            keep_latest=10,
            max_age_days=60,
            action=RetentionPolicyAction.DELETE
        ),
        RetentionPolicy(
            policy_id=create_retention_policy_id("TEMP_FILE"),
            artifact_type=RetentionArtifactType.TEMP_FILE,
            name="Temp File Policy",
            enabled=True,
            keep_latest=0,
            max_age_days=7,
            action=RetentionPolicyAction.DELETE
        )
    ]

def policy_for_artifact_type(policies: list[RetentionPolicy], artifact_type: RetentionArtifactType) -> RetentionPolicy | None:
    for p in policies:
        if p.artifact_type == artifact_type and p.enabled:
            return p
    return None

def load_retention_policies_from_config(config_dict: dict[str, Any] | None = None) -> list[RetentionPolicy]:
    return default_retention_policies()

def retention_policies_to_text(policies: list[RetentionPolicy]) -> str:
    lines = []
    for p in policies:
        lines.append(f"[{p.artifact_type.value}] {p.name}: Action={p.action.value}, Keep={p.keep_latest}, MaxAge={p.max_age_days}")
    return "\n".join(lines)
