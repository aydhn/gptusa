from typing import Any
import datetime

from usa_signal_bot.core.enums import PaperModeRehearsalAttemptType, PaperModeRehearsalBlockerAction, DryAdmissionDossierRiskFlag
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import PaperModeRehearsalBlockerRule, create_rehearsal_blocker_rule_id

def dangerous_rehearsal_attempt_types() -> list[PaperModeRehearsalAttemptType]:
    return [
        PaperModeRehearsalAttemptType.START_PAPER_MODE_REHEARSAL,
        PaperModeRehearsalAttemptType.START_LOCAL_PAPER_REHEARSAL_RUNTIME,
        PaperModeRehearsalAttemptType.REHEARSE_CANDIDATE,
        PaperModeRehearsalAttemptType.ADMIT_CANDIDATE_TO_REHEARSAL,
        PaperModeRehearsalAttemptType.CREATE_REHEARSAL_SESSION,
        PaperModeRehearsalAttemptType.CREATE_PAPER_SESSION,
        PaperModeRehearsalAttemptType.CREATE_PAPER_ORDER,
        PaperModeRehearsalAttemptType.COMMIT_PAPER_STATE,
        PaperModeRehearsalAttemptType.PATCH_PAPER_CONFIG,
        PaperModeRehearsalAttemptType.SEND_BROKER_ORDER,
        PaperModeRehearsalAttemptType.SEND_TELEGRAM_REAL,
        PaperModeRehearsalAttemptType.UNLOCK_REHEARSAL_GATE
    ]

def rule_for_rehearsal_attempt(attempt_type: PaperModeRehearsalAttemptType) -> PaperModeRehearsalBlockerRule:
    now = datetime.datetime.utcnow().isoformat() + "Z"
    flags = [DryAdmissionDossierRiskFlag.PAPER_MODE_REHEARSAL_RISK]

    if attempt_type == PaperModeRehearsalAttemptType.SEND_BROKER_ORDER:
        flags.append(DryAdmissionDossierRiskFlag.BROKER_ORDER_RISK)
    elif attempt_type == PaperModeRehearsalAttemptType.COMMIT_PAPER_STATE:
        flags.append(DryAdmissionDossierRiskFlag.PAPER_STATE_MUTATION_RISK)
    elif attempt_type == PaperModeRehearsalAttemptType.PATCH_PAPER_CONFIG:
        flags.append(DryAdmissionDossierRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
    elif attempt_type == PaperModeRehearsalAttemptType.SEND_TELEGRAM_REAL:
        flags.append(DryAdmissionDossierRiskFlag.TELEGRAM_REAL_SEND_RISK)

    return PaperModeRehearsalBlockerRule(
        rule_id=create_rehearsal_blocker_rule_id(),
        created_at_utc=now,
        attempt_type=attempt_type,
        enabled=True,
        blocking=True,
        action=PaperModeRehearsalBlockerAction.DENY_AND_RECORD,
        description=f"Block {attempt_type.value}",
        risk_flags=flags,
        warnings=[],
        errors=[],
        metadata={}
    )

def default_rehearsal_blocker_rules() -> list[PaperModeRehearsalBlockerRule]:
    return [rule_for_rehearsal_attempt(t) for t in dangerous_rehearsal_attempt_types()]

def validate_rehearsal_blocker_rules_complete(rules: list[PaperModeRehearsalBlockerRule]) -> list[str]:
    errors = []
    covered = {r.attempt_type for r in rules if r.enabled and r.blocking}
    required = set(dangerous_rehearsal_attempt_types())
    missing = required - covered

    if missing:
        errors.append(f"Missing rules for: {[m.value for m in missing]}")

    return errors

def rehearsal_blocker_rules_summary(rules: list[PaperModeRehearsalBlockerRule]) -> dict[str, Any]:
    return {
        "total": len(rules),
        "enabled": sum(1 for r in rules if r.enabled),
        "blocking": sum(1 for r in rules if r.blocking),
        "complete": len(validate_rehearsal_blocker_rules_complete(rules)) == 0
    }

def rehearsal_blocker_rules_to_text(rules: list[PaperModeRehearsalBlockerRule], limit: int = 100) -> str:
    summary = rehearsal_blocker_rules_summary(rules)
    return f"Rehearsal Blocker Rules (Complete: {summary['complete']}): Total={summary['total']}, Blocking={summary['blocking']}"
