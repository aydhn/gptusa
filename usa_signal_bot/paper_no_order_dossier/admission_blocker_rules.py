from typing import Any
import json
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    PaperAdmissionAttemptType,
    PaperAdmissionBlockerAction
)
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import (
    PaperAdmissionBlockerRule,
    create_admission_blocker_rule_id,
    paper_admission_blocker_rule_to_dict
)

def dangerous_paper_admission_attempt_types() -> list[PaperAdmissionAttemptType]:
    return [
        PaperAdmissionAttemptType.ENABLE_ACTIVE_PAPER,
        PaperAdmissionAttemptType.ENABLE_PAPER_RUNTIME,
        PaperAdmissionAttemptType.ADMIT_CANDIDATE_TO_PAPER,
        PaperAdmissionAttemptType.CREATE_PAPER_SESSION,
        PaperAdmissionAttemptType.CREATE_PAPER_ORDER,
        PaperAdmissionAttemptType.COMMIT_PAPER_STATE,
        PaperAdmissionAttemptType.PATCH_PAPER_CONFIG,
        PaperAdmissionAttemptType.SEND_BROKER_ORDER,
        PaperAdmissionAttemptType.SEND_TELEGRAM_REAL,
        PaperAdmissionAttemptType.UNLOCK_PAPER_GATE
    ]

def rule_for_paper_admission_attempt(attempt_type: PaperAdmissionAttemptType) -> PaperAdmissionBlockerRule:
    return PaperAdmissionBlockerRule(
        rule_id=create_admission_blocker_rule_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        attempt_type=attempt_type,
        enabled=True,
        blocking=True,
        action=PaperAdmissionBlockerAction.DENY_AND_RECORD,
        description=f"Blocks {attempt_type} unconditionally to prevent active paper execution",
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def default_paper_admission_blocker_rules() -> list[PaperAdmissionBlockerRule]:
    return [rule_for_paper_admission_attempt(t) for t in dangerous_paper_admission_attempt_types()]

def validate_paper_admission_blocker_rules_complete(rules: list[PaperAdmissionBlockerRule]) -> list[str]:
    reasons = []
    covered_types = {r.attempt_type for r in rules if r.enabled and r.blocking}
    for t in dangerous_paper_admission_attempt_types():
        if t not in covered_types:
            reasons.append(f"Missing active/blocking rule for {t}")
    return reasons

def paper_admission_blocker_rules_summary(rules: list[PaperAdmissionBlockerRule]) -> dict[str, Any]:
    return {
        "total_rules": len(rules),
        "blocking_rules": len([r for r in rules if r.blocking]),
        "enabled_rules": len([r for r in rules if r.enabled]),
        "complete": len(validate_paper_admission_blocker_rules_complete(rules)) == 0
    }

def paper_admission_blocker_rules_to_text(rules: list[PaperAdmissionBlockerRule], limit: int = 100) -> str:
    return json.dumps([paper_admission_blocker_rule_to_dict(r) for r in rules[:limit]], indent=2)
