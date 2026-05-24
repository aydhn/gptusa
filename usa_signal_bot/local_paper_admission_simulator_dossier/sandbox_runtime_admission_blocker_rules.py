from datetime import datetime, timezone
from typing import Any
from usa_signal_bot.core.enums import (
    PaperSandboxRuntimeAdmissionAttemptType,
    PaperSandboxRuntimeAdmissionBlockerAction
)
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import (
    PaperSandboxRuntimeAdmissionBlockerRule,
    create_sandbox_runtime_admission_blocker_rule_id
)

def dangerous_sandbox_runtime_admission_attempt_types() -> list[PaperSandboxRuntimeAdmissionAttemptType]:
    return [
        PaperSandboxRuntimeAdmissionAttemptType.START_PAPER_SANDBOX_RUNTIME,
        PaperSandboxRuntimeAdmissionAttemptType.ADMIT_CANDIDATE_TO_SANDBOX_RUNTIME,
        PaperSandboxRuntimeAdmissionAttemptType.START_SANDBOX_PAPER_SESSION,
        PaperSandboxRuntimeAdmissionAttemptType.CREATE_SANDBOX_PAPER_SESSION,
        PaperSandboxRuntimeAdmissionAttemptType.CREATE_SANDBOX_PAPER_ORDER,
        PaperSandboxRuntimeAdmissionAttemptType.COMMIT_SANDBOX_PAPER_STATE,
        PaperSandboxRuntimeAdmissionAttemptType.PATCH_SANDBOX_RUNTIME_CONFIG,
        PaperSandboxRuntimeAdmissionAttemptType.SEND_SANDBOX_BROKER_ORDER,
        PaperSandboxRuntimeAdmissionAttemptType.SEND_SANDBOX_TELEGRAM_REAL,
        PaperSandboxRuntimeAdmissionAttemptType.UNLOCK_SANDBOX_RUNTIME_ADMISSION_GATE
    ]

def rule_for_sandbox_runtime_admission_attempt(attempt_type: PaperSandboxRuntimeAdmissionAttemptType) -> PaperSandboxRuntimeAdmissionBlockerRule:
    return PaperSandboxRuntimeAdmissionBlockerRule(
        rule_id=create_sandbox_runtime_admission_blocker_rule_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        attempt_type=attempt_type,
        enabled=True,
        blocking=True,
        action=PaperSandboxRuntimeAdmissionBlockerAction.DENY_AND_RECORD,
        description=f"Blocks {attempt_type.value}",
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def default_sandbox_runtime_admission_blocker_rules() -> list[PaperSandboxRuntimeAdmissionBlockerRule]:
    return [rule_for_sandbox_runtime_admission_attempt(t) for t in dangerous_sandbox_runtime_admission_attempt_types()]

def validate_sandbox_runtime_admission_blocker_rules_complete(rules: list[PaperSandboxRuntimeAdmissionBlockerRule]) -> list[str]:
    errors = []
    types_covered = {r.attempt_type for r in rules if r.enabled and r.blocking}
    for t in dangerous_sandbox_runtime_admission_attempt_types():
        if t not in types_covered:
            errors.append(f"Missing active rule for {t.value}")
    return errors

def sandbox_runtime_admission_blocker_rules_summary(rules: list[PaperSandboxRuntimeAdmissionBlockerRule]) -> dict[str, Any]:
    return {
        "total": len(rules),
        "enabled": len([r for r in rules if r.enabled]),
        "blocking": len([r for r in rules if r.blocking]),
        "errors": validate_sandbox_runtime_admission_blocker_rules_complete(rules)
    }

def sandbox_runtime_admission_blocker_rules_to_text(rules: list[PaperSandboxRuntimeAdmissionBlockerRule], limit: int = 100) -> str:
    summary = sandbox_runtime_admission_blocker_rules_summary(rules)
    lines = [
        "--- Sandbox Runtime Admission Blocker Rules ---",
        f"Total: {summary['total']}, Enabled: {summary['enabled']}, Blocking: {summary['blocking']}",
        "Errors:"
    ]
    if summary["errors"]:
        lines.extend([f"  - {e}" for e in summary["errors"]])
    else:
        lines.append("  - None")
    return "\n".join(lines)
