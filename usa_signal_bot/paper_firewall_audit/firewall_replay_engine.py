from typing import Any, List
from datetime import datetime, timezone
from usa_signal_bot.core.enums import FirewallReplayStatus, FirewallReplayOutcome, FirewallAuditRiskFlag
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import FirewallReplayPlan, FirewallReplayResult, create_firewall_replay_result_id

class PaperFirewallReplayEngine:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def replay(self, plan: FirewallReplayPlan, events: List[dict[str, Any]]) -> FirewallReplayResult:
        replayed = 0
        blocked = 0
        unblocked = 0

        for event in events:
            res = self.replay_single_event(event)
            replayed += 1
            if res.get("blocked", False):
                blocked += 1
            elif res.get("is_dangerous", False):
                unblocked += 1

        outcome = self.determine_replay_outcome(plan, events)
        status = FirewallReplayStatus.COMPLETED if outcome != FirewallReplayOutcome.REPLAY_FAILED else FirewallReplayStatus.FAILED
        if outcome == FirewallReplayOutcome.SOME_ATTEMPTS_NOT_BLOCKED:
            status = FirewallReplayStatus.BLOCKED

        flags = self.collect_replay_risk_flags(plan, events)

        return FirewallReplayResult(
            replay_result_id=create_firewall_replay_result_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            replay_plan_id=plan.replay_plan_id,
            status=status,
            outcome=outcome,
            replayed_event_count=replayed,
            blocked_event_count=blocked,
            unblocked_dangerous_event_count=unblocked,
            missing_rule_count=0,
            risk_flags=flags,
            passed=(outcome == FirewallReplayOutcome.ALL_DANGEROUS_ATTEMPTS_BLOCKED),
            warnings=[],
            errors=[]
        )

    def replay_single_event(self, event: dict[str, Any]) -> dict[str, Any]:
        return event

    def validate_replay_coverage(self, plan: FirewallReplayPlan, events: List[dict[str, Any]]) -> List[str]:
        return []

    def determine_replay_outcome(self, plan: FirewallReplayPlan, events: List[dict[str, Any]]) -> FirewallReplayOutcome:
        unblocked = sum(1 for e in events if not e.get("blocked", False) and e.get("is_dangerous", False))
        if unblocked > 0:
            return FirewallReplayOutcome.SOME_ATTEMPTS_NOT_BLOCKED
        return FirewallReplayOutcome.ALL_DANGEROUS_ATTEMPTS_BLOCKED

    def collect_replay_risk_flags(self, plan: FirewallReplayPlan, events: List[dict[str, Any]]) -> List[FirewallAuditRiskFlag]:
        flags = []
        if self.determine_replay_outcome(plan, events) == FirewallReplayOutcome.SOME_ATTEMPTS_NOT_BLOCKED:
            flags.append(FirewallAuditRiskFlag.FIREWALL_BYPASS_RISK)
        return flags

    def replay_summary(self, result: FirewallReplayResult) -> dict[str, Any]:
        return {
            "id": result.replay_result_id,
            "outcome": result.outcome.value,
            "passed": result.passed
        }
