from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import AdmissionBlockerReplayPlan, AdmissionBlockerReplayResult, create_blocker_replay_result_id
from usa_signal_bot.core.enums import AdmissionBlockerReplayStatus, AdmissionBlockerReplayOutcome, PaperSandboxBoundaryRiskFlag

class PaperAdmissionBlockerReplayEngine:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def replay(self, plan: AdmissionBlockerReplayPlan, events: list[dict[str, Any]] | None = None) -> AdmissionBlockerReplayResult:
        events = events or []
        allowed = 0
        blocked = 0
        missing = 0
        risk_flags = self.collect_replay_risk_flags(plan, events)

        for ev in events:
            res = self.replay_single_event(ev)
            if res.get("blocked", True):
                blocked += 1
            else:
                allowed += 1

        outcome = self.determine_replay_outcome(plan, events)
        passed = outcome == AdmissionBlockerReplayOutcome.ALL_ADMISSION_ATTEMPTS_BLOCKED
        status = AdmissionBlockerReplayStatus.COMPLETED_ALL_BLOCKED if passed else AdmissionBlockerReplayStatus.BLOCKED

        return AdmissionBlockerReplayResult(
            replay_result_id=create_blocker_replay_result_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            replay_plan_id=plan.replay_plan_id,
            status=status,
            outcome=outcome,
            replayed_attempt_count=len(events),
            blocked_attempt_count=blocked,
            allowed_attempt_count=allowed,
            missing_rule_count=missing,
            passed=passed,
            risk_flags=risk_flags,
            warnings=[],
            errors=[]
        )

    def replay_single_event(self, event: dict[str, Any]) -> dict[str, Any]:
        return {"blocked": event.get("blocked", True)}

    def validate_replay_coverage(self, plan: AdmissionBlockerReplayPlan, events: list[dict[str, Any]]) -> list[str]:
        return []

    def determine_replay_outcome(self, plan: AdmissionBlockerReplayPlan, events: list[dict[str, Any]]) -> AdmissionBlockerReplayOutcome:
        for ev in events:
            if not ev.get("blocked", True):
                return AdmissionBlockerReplayOutcome.SOME_ADMISSION_ATTEMPTS_ALLOWED
        if not events and self.conservative:
            return AdmissionBlockerReplayOutcome.BLOCKER_EVENTS_MISSING
        return AdmissionBlockerReplayOutcome.ALL_ADMISSION_ATTEMPTS_BLOCKED

    def collect_replay_risk_flags(self, plan: AdmissionBlockerReplayPlan, events: list[dict[str, Any]]) -> list[PaperSandboxBoundaryRiskFlag]:
        flags = []
        for ev in events:
            if not ev.get("blocked", True):
                flags.append(PaperSandboxBoundaryRiskFlag.BLOCKER_ATTEMPT_NOT_BLOCKED)
        if not events:
            flags.append(PaperSandboxBoundaryRiskFlag.BLOCKER_RULES_INCOMPLETE)
        return flags

    def replay_summary(self, result: AdmissionBlockerReplayResult) -> dict[str, Any]:
        return {"id": result.replay_result_id, "passed": result.passed, "allowed": result.allowed_attempt_count}
