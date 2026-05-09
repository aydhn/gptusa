from usa_signal_bot.core.enums import RecoveryActionType, RecoveryActionStatus, IncidentCategory
from usa_signal_bot.incident.incident_models import IncidentRecord
from usa_signal_bot.incident.recovery_models import RecoveryAction, create_recovery_action_id

def recovery_action_validate_config() -> RecoveryAction:
    return RecoveryAction(
        action_id=create_recovery_action_id("validate_config"),
        action_type=RecoveryActionType.VALIDATE_CONFIG,
        name="Validate Configuration",
        description="Run config validation checks.",
        command="python -m usa_signal_bot validate-config",
        dry_run=True,
        required=True,
        status=RecoveryActionStatus.PENDING,
        safety_note="Safe read-only operation."
    )

def recovery_action_health_check() -> RecoveryAction:
    return RecoveryAction(
        action_id=create_recovery_action_id("health_check"),
        action_type=RecoveryActionType.RUN_HEALTH_CHECK,
        name="Run Health Check",
        description="Run local system health check.",
        command="python -m usa_signal_bot health",
        dry_run=True,
        required=True,
        status=RecoveryActionStatus.PENDING,
        safety_note="Safe read-only operation."
    )

def recovery_action_regression_smoke() -> RecoveryAction:
    return RecoveryAction(
        action_id=create_recovery_action_id("regression_smoke"),
        action_type=RecoveryActionType.RUN_REGRESSION_SMOKE,
        name="Regression Smoke Test",
        description="Run regression tests to verify core logic.",
        command="python -m usa_signal_bot regression-run --smoke",
        dry_run=True,
        required=True,
        status=RecoveryActionStatus.PENDING,
        safety_note="Safe operation. May take some time."
    )

def recovery_action_backup_create() -> RecoveryAction:
    return RecoveryAction(
        action_id=create_recovery_action_id("backup_create"),
        action_type=RecoveryActionType.BACKUP_CREATE,
        name="Create Backup",
        description="Create a backup before attempting recovery.",
        command="python -m usa_signal_bot backup-create",
        dry_run=False,
        required=True,
        status=RecoveryActionStatus.PENDING,
        safety_note="Write operation but non-destructive."
    )

def recovery_action_backup_validate() -> RecoveryAction:
    return RecoveryAction(
        action_id=create_recovery_action_id("backup_validate"),
        action_type=RecoveryActionType.BACKUP_VALIDATE,
        name="Validate Backup",
        description="Verify backup integrity.",
        command="python -m usa_signal_bot backup-validate",
        dry_run=True,
        required=True,
        status=RecoveryActionStatus.PENDING,
        safety_note="Safe read-only operation."
    )

def recovery_action_restore_dry_run() -> RecoveryAction:
    return RecoveryAction(
        action_id=create_recovery_action_id("restore_dry_run"),
        action_type=RecoveryActionType.RESTORE_DRY_RUN,
        name="Restore Dry Run",
        description="Simulate restore operation.",
        command="python -m usa_signal_bot restore-dry-run",
        dry_run=True,
        required=True,
        status=RecoveryActionStatus.PENDING,
        safety_note="Dry run operation. Modifies no files."
    )

def recovery_action_cleanup_dry_run() -> RecoveryAction:
    return RecoveryAction(
        action_id=create_recovery_action_id("cleanup_dry_run"),
        action_type=RecoveryActionType.CLEANUP_DRY_RUN,
        name="Cleanup Dry Run",
        description="Simulate disk cleanup to recover space.",
        command="python -m usa_signal_bot cleanup-dry-run",
        dry_run=True,
        required=True,
        status=RecoveryActionStatus.PENDING,
        safety_note="Dry run operation. Modifies no files."
    )

def recovery_action_rollback_dry_run() -> RecoveryAction:
    return RecoveryAction(
        action_id=create_recovery_action_id("rollback_dry_run"),
        action_type=RecoveryActionType.ROLLBACK_DRY_RUN,
        name="Rollback Dry Run",
        description="Simulate rollback from latest source.",
        command="python -m usa_signal_bot rollback-dry-run",
        dry_run=True,
        required=True,
        status=RecoveryActionStatus.PENDING,
        safety_note="Dry run operation. Modifies no files."
    )

def recovery_action_manual_review(reason: str) -> RecoveryAction:
    return RecoveryAction(
        action_id=create_recovery_action_id("manual_review"),
        action_type=RecoveryActionType.MANUAL_REVIEW,
        name="Manual Review Required",
        description=f"Manual intervention required due to: {reason}",
        command=None,
        dry_run=True,
        required=True,
        status=RecoveryActionStatus.BLOCKED,
        safety_note="Human review needed. No automated action available."
    )

def recovery_actions_for_category(category: IncidentCategory) -> list[RecoveryAction]:
    if category == IncidentCategory.CONFIG_ERROR:
        return [recovery_action_validate_config(), recovery_action_health_check()]
    if category == IncidentCategory.DISK_QUOTA:
        return [recovery_action_cleanup_dry_run(), recovery_action_backup_create()]
    if category == IncidentCategory.REGRESSION_FAILURE:
        return [recovery_action_regression_smoke(), recovery_action_health_check()]
    if category in [IncidentCategory.SAFETY_VIOLATION, IncidentCategory.SECRET_LEAK_RISK]:
        return [recovery_action_manual_review("Safety/Secret incident requires manual review")]

    # default generic
    return [recovery_action_health_check(), recovery_action_rollback_dry_run()]

def default_recovery_actions_for_incident(incident: IncidentRecord) -> list[RecoveryAction]:
    actions = recovery_actions_for_category(incident.category)
    return actions

def recovery_actions_to_text(actions: list[RecoveryAction]) -> str:
    lines = []
    for a in actions:
        req = "[REQUIRED]" if a.required else "[OPTIONAL]"
        lines.append(f"{req} {a.name} ({a.status.name}): {a.description}")
        if a.command:
            lines.append(f"  Command: {a.command}")
    return "\n".join(lines)
