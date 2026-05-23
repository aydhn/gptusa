from typing import Any
import json
from datetime import datetime, timezone
from usa_signal_bot.core.enums import (
    PaperAdmissionAttemptType,
    PaperAdmissionBlockerAction,
    PaperAdmissionBlockerStatus,
    PaperAdmissionBlockerDecision
)
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import (
    PaperAdmissionBlockerRule,
    PaperAdmissionBlockerEvent,
    create_admission_blocker_event_id
)
from usa_signal_bot.paper_no_order_dossier.admission_blocker_rules import (
    default_paper_admission_blocker_rules,
    validate_paper_admission_blocker_rules_complete
)

class FinalPaperAdmissionBlocker:
    def __init__(self, rules: list[PaperAdmissionBlockerRule] | None = None):
        self.rules = rules if rules is not None else default_paper_admission_blocker_rules()

    def validate_blocker_enabled(self) -> list[str]:
        return validate_paper_admission_blocker_rules_complete(self.rules)

    def admission_allowed(self, attempt_type: PaperAdmissionAttemptType) -> bool:
        # Final paper admission blocker NEVER allows admission
        return False

    def deny_admission_attempt(self, attempt_type: PaperAdmissionAttemptType, payload: dict[str, Any] | None = None, source_component: str | None = None) -> PaperAdmissionBlockerEvent:
        payload = payload or {}

        # Find matching rule or use default deny
        rule = next((r for r in self.rules if r.attempt_type == attempt_type), None)
        action = rule.action if rule else PaperAdmissionBlockerAction.DENY_AND_RECORD

        return PaperAdmissionBlockerEvent(
            event_id=create_admission_blocker_event_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            attempt_type=attempt_type,
            status=PaperAdmissionBlockerStatus.ADMISSION_ATTEMPT_BLOCKED,
            decision=PaperAdmissionBlockerDecision.BLOCK_PAPER_ADMISSION,
            action=action,
            blocked=True,
            admission_allowed=False,
            active_paper_enabled=False,
            order_created=False,
            paper_state_mutated=False,
            broker_order_sent=False,
            telegram_real_sent=False,
            config_patched=False,
            source_component=source_component,
            payload_summary={"payload_keys": list(payload.keys())},
            risk_flags=[],
            warnings=[],
            errors=[],
            metadata={}
        )

    def evaluate_attempt(self, attempt_type: PaperAdmissionAttemptType, payload: dict[str, Any] | None = None, source_component: str | None = None) -> PaperAdmissionBlockerEvent:
        # Always deny
        return self.deny_admission_attempt(attempt_type, payload, source_component)

    def blocker_summary(self, events: list[PaperAdmissionBlockerEvent]) -> dict[str, Any]:
        return {
            "total_attempts": len(events),
            "blocked_attempts": len([e for e in events if e.blocked]),
            "allowed_attempts": len([e for e in events if not e.blocked])  # Should always be 0
        }
