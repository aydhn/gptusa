from typing import Any
import datetime

from usa_signal_bot.core.enums import PaperModeRehearsalAttemptType, PaperModeRehearsalBlockerAction, PaperModeRehearsalBlockerStatus, PaperModeRehearsalBlockerDecision
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import PaperModeRehearsalBlockerEvent, PaperModeRehearsalBlockerRule, create_rehearsal_blocker_event_id
from usa_signal_bot.paper_mode_dry_admission_dossier.rehearsal_blocker_rules import default_rehearsal_blocker_rules

class FinalPaperModeRehearsalBlocker:
    def __init__(self, rules: list[PaperModeRehearsalBlockerRule] | None = None):
        self.rules = rules or default_rehearsal_blocker_rules()

    def validate_blocker_enabled(self) -> list[str]:
        errors = []
        if not self.rules:
            errors.append("No rules configured")
        for rule in self.rules:
            if not rule.enabled or not rule.blocking:
                errors.append(f"Rule {rule.rule_id} is not blocking")
        return errors

    def evaluate_attempt(self, attempt_type: PaperModeRehearsalAttemptType, payload: dict[str, Any] | None = None, source_component: str | None = None) -> PaperModeRehearsalBlockerEvent:
        return self.deny_rehearsal_attempt(attempt_type, payload, source_component)

    def deny_rehearsal_attempt(self, attempt_type: PaperModeRehearsalAttemptType, payload: dict[str, Any] | None = None, source_component: str | None = None) -> PaperModeRehearsalBlockerEvent:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        rule = next((r for r in self.rules if r.attempt_type == attempt_type), None)

        flags = rule.risk_flags if rule else []
        action = rule.action if rule else PaperModeRehearsalBlockerAction.DENY

        return PaperModeRehearsalBlockerEvent(
            event_id=create_rehearsal_blocker_event_id(),
            created_at_utc=now,
            attempt_type=attempt_type,
            status=PaperModeRehearsalBlockerStatus.REHEARSAL_ATTEMPT_BLOCKED,
            decision=PaperModeRehearsalBlockerDecision.BLOCK_REHEARSAL,
            action=action,
            blocked=True,
            rehearsal_allowed=False,
            paper_mode_rehearsal_allowed=False,
            shadow_launch_allowed=False,
            paper_mode_launch_allowed=False,
            admission_allowed=False,
            active_paper_enabled=False,
            order_created=False,
            paper_state_mutated=False,
            broker_order_sent=False,
            telegram_real_sent=False,
            config_patched=False,
            source_component=source_component,
            payload_summary={"blocked_payload_keys": list(payload.keys())} if payload else {},
            risk_flags=flags,
            warnings=[],
            errors=[],
            metadata={"rule_applied": rule.rule_id if rule else "default_deny"}
        )

    def rehearsal_allowed(self, attempt_type: PaperModeRehearsalAttemptType) -> bool:
        return False

    def blocker_summary(self, events: list[PaperModeRehearsalBlockerEvent]) -> dict[str, Any]:
        return {
            "events_evaluated": len(events),
            "events_blocked": sum(1 for e in events if e.blocked),
            "all_blocked": all(e.blocked for e in events) if events else True
        }
