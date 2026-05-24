from typing import Any
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    ShadowLaunchAttemptType,
    ShadowLaunchBlockerAction,
    ShadowLaunchBlockerStatus,
    ShadowLaunchBlockerDecision,
    BoardDossierRiskFlag
)
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import (
    ShadowLaunchBlockerRule,
    ShadowLaunchBlockerEvent,
    create_shadow_launch_blocker_event_id
)
from usa_signal_bot.paper_readiness_board_dossier.shadow_launch_blocker_rules import (
    default_shadow_launch_blocker_rules,
    rule_for_shadow_launch_attempt,
    validate_shadow_launch_blocker_rules_complete
)

class FinalPaperModeShadowLaunchBlocker:
    def __init__(self, rules: list[ShadowLaunchBlockerRule] | None = None):
        self.rules = rules or default_shadow_launch_blocker_rules()

    def evaluate_attempt(self, attempt_type: ShadowLaunchAttemptType, payload: dict[str, Any] | None = None, source_component: str | None = None) -> ShadowLaunchBlockerEvent:
        # Check rules
        rule = next((r for r in self.rules if r.attempt_type == attempt_type and r.enabled and r.blocking), None)
        if not rule:
            # Fallback to unconditional deny
            rule = rule_for_shadow_launch_attempt(attempt_type)

        return self.deny_shadow_launch_attempt(attempt_type, payload, source_component)

    def shadow_launch_allowed(self, attempt_type: ShadowLaunchAttemptType) -> bool:
        return False

    def deny_shadow_launch_attempt(self, attempt_type: ShadowLaunchAttemptType, payload: dict[str, Any] | None = None, source_component: str | None = None) -> ShadowLaunchBlockerEvent:
        rule = rule_for_shadow_launch_attempt(attempt_type)
        return ShadowLaunchBlockerEvent(
            event_id=create_shadow_launch_blocker_event_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            attempt_type=attempt_type,
            status=ShadowLaunchBlockerStatus.SHADOW_LAUNCH_ATTEMPT_BLOCKED,
            decision=ShadowLaunchBlockerDecision.BLOCK_SHADOW_LAUNCH,
            action=ShadowLaunchBlockerAction.DENY_AND_RECORD,
            blocked=True,
            shadow_launch_allowed=False,
            paper_mode_launch_allowed=False,
            admission_allowed=False,
            active_paper_enabled=False,
            order_created=False,
            paper_state_mutated=False,
            broker_order_sent=False,
            telegram_real_sent=False,
            config_patched=False,
            payload_summary={"payload_keys": list(payload.keys())} if payload else {},
            risk_flags=rule.risk_flags,
            warnings=[],
            errors=[],
            source_component=source_component
        )

    def validate_blocker_enabled(self) -> list[str]:
        return validate_shadow_launch_blocker_rules_complete(self.rules)

    def blocker_summary(self, events: list[ShadowLaunchBlockerEvent]) -> dict[str, Any]:
        return {
            "total_events": len(events),
            "blocked_events": sum(1 for e in events if e.blocked),
            "unblocked_events": sum(1 for e in events if not e.blocked),
            "all_shadow_launch_allowed_false": all(not e.shadow_launch_allowed for e in events)
        }
