from datetime import datetime, timezone
from typing import Any
from usa_signal_bot.core.enums import (
    PaperSandboxRuntimeAdmissionAttemptType,
    PaperSandboxRuntimeAdmissionBlockerStatus,
    PaperSandboxRuntimeAdmissionBlockerDecision,
    PaperSandboxRuntimeAdmissionBlockerAction
)
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import (
    PaperSandboxRuntimeAdmissionBlockerRule,
    PaperSandboxRuntimeAdmissionBlockerEvent,
    create_sandbox_runtime_admission_blocker_event_id
)
from usa_signal_bot.local_paper_admission_simulator_dossier.sandbox_runtime_admission_blocker_rules import default_sandbox_runtime_admission_blocker_rules

class FinalPaperSandboxRuntimeAdmissionBlocker:
    def __init__(self, rules: list[PaperSandboxRuntimeAdmissionBlockerRule] | None = None):
        self.rules = rules if rules is not None else default_sandbox_runtime_admission_blocker_rules()

    def evaluate_attempt(self, attempt_type: PaperSandboxRuntimeAdmissionAttemptType, payload: dict[str, Any] | None = None, source_component: str | None = None) -> PaperSandboxRuntimeAdmissionBlockerEvent:
        return self.deny_sandbox_runtime_admission_attempt(attempt_type, payload, source_component)

    def sandbox_runtime_admission_allowed(self, attempt_type: PaperSandboxRuntimeAdmissionAttemptType) -> bool:
        return False

    def deny_sandbox_runtime_admission_attempt(self, attempt_type: PaperSandboxRuntimeAdmissionAttemptType, payload: dict[str, Any] | None = None, source_component: str | None = None) -> PaperSandboxRuntimeAdmissionBlockerEvent:
        return PaperSandboxRuntimeAdmissionBlockerEvent(
            event_id=create_sandbox_runtime_admission_blocker_event_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            attempt_type=attempt_type,
            status=PaperSandboxRuntimeAdmissionBlockerStatus.SANDBOX_RUNTIME_ADMISSION_ATTEMPT_BLOCKED,
            decision=PaperSandboxRuntimeAdmissionBlockerDecision.BLOCK_SANDBOX_RUNTIME_ADMISSION,
            action=PaperSandboxRuntimeAdmissionBlockerAction.DENY_AND_RECORD,
            blocked=True,
            sandbox_runtime_admission_allowed=False,
            paper_sandbox_runtime_allowed=False,
            simulator_admission_allowed=False,
            local_paper_simulator_allowed=False,
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
            payload_summary={"simulated_attempt": True, "payload": payload},
            risk_flags=[],
            warnings=[],
            errors=[],
            source_component=source_component,
            metadata={}
        )

    def validate_blocker_enabled(self) -> list[str]:
        errors = []
        if not self.rules:
            errors.append("No rules configured")
        return errors

    def blocker_summary(self, events: list[PaperSandboxRuntimeAdmissionBlockerEvent]) -> dict[str, Any]:
        return {
            "total_events": len(events),
            "blocked_events": len([e for e in events if e.blocked])
        }
