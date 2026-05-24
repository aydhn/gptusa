from datetime import datetime, timezone
from typing import Any, List
from usa_signal_bot.core.enums import (
    ShadowLaunchReplayStatus,
    ShadowLaunchReplayOutcome,
    ShadowLaunchReplayDecision,
    DryAdmissionGateRiskFlag
)
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import (
    ShadowLaunchReplayItem,
    ShadowLaunchReplayPlan,
    ShadowLaunchReplayResult,
    create_shadow_replay_item_id,
    create_shadow_replay_result_id
)

class ShadowLaunchBlockerReplayEngine:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def replay(self, plan: ShadowLaunchReplayPlan, events: List[dict[str, Any]] | None = None) -> ShadowLaunchReplayResult:
        if events is None:
            events = []

        replay_items = []
        for event in events:
            replay_items.append(self.replay_single_event(event))

        outcome = self.determine_replay_outcome(plan, replay_items)
        risk_flags = self.collect_replay_risk_flags(plan, replay_items)
        coverage_errors = self.validate_replay_coverage(plan, events)

        status = ShadowLaunchReplayStatus.COMPLETED_ALL_BLOCKED
        if coverage_errors:
            status = ShadowLaunchReplayStatus.BLOCKED
            outcome = ShadowLaunchReplayOutcome.BLOCKER_EVENTS_MISSING
            risk_flags.append(DryAdmissionGateRiskFlag.BLOCKER_EVENTS_MISSING)
        elif outcome != ShadowLaunchReplayOutcome.ALL_SHADOW_ATTEMPTS_BLOCKED:
            status = ShadowLaunchReplayStatus.FAILED

        replayed_count = len(replay_items)
        blocked_count = sum(1 for item in replay_items if item.blocked)
        allowed_count = sum(1 for item in replay_items if not item.blocked)

        passed = (status == ShadowLaunchReplayStatus.COMPLETED_ALL_BLOCKED and allowed_count == 0 and len(coverage_errors) == 0)

        return ShadowLaunchReplayResult(
            replay_result_id=create_shadow_replay_result_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            replay_plan_id=plan.replay_plan_id,
            status=status,
            outcome=outcome,
            replayed_attempt_count=replayed_count,
            blocked_attempt_count=blocked_count,
            allowed_attempt_count=allowed_count,
            missing_event_count=len(coverage_errors),
            passed=passed,
            risk_flags=list(set(risk_flags)),
            warnings=[],
            errors=coverage_errors
        )

    def replay_single_event(self, event: dict[str, Any]) -> ShadowLaunchReplayItem:
        blocked = event.get("blocked", True)
        shadow_launch_allowed = event.get("shadow_launch_allowed", False)
        paper_mode_launch_allowed = event.get("paper_mode_launch_allowed", False)

        # Determine decision based on blocked status
        decision = ShadowLaunchReplayDecision.BLOCK
        if not blocked or shadow_launch_allowed or paper_mode_launch_allowed:
            # Replay failed, something was allowed
            decision = ShadowLaunchReplayDecision.UNKNOWN

        risk_flags = []
        if not blocked: risk_flags.append(DryAdmissionGateRiskFlag.SHADOW_ATTEMPT_NOT_BLOCKED)
        if shadow_launch_allowed: risk_flags.append(DryAdmissionGateRiskFlag.SHADOW_LAUNCH_RISK)
        if paper_mode_launch_allowed: risk_flags.append(DryAdmissionGateRiskFlag.PAPER_MODE_LAUNCH_RISK)
        if event.get("active_paper_enabled"): risk_flags.append(DryAdmissionGateRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
        if event.get("order_created"): risk_flags.append(DryAdmissionGateRiskFlag.ORDER_CREATED_RISK)
        if event.get("paper_state_mutated"): risk_flags.append(DryAdmissionGateRiskFlag.PAPER_STATE_MUTATION_RISK)
        if event.get("broker_order_sent"): risk_flags.append(DryAdmissionGateRiskFlag.BROKER_ORDER_RISK)
        if event.get("telegram_real_sent"): risk_flags.append(DryAdmissionGateRiskFlag.TELEGRAM_REAL_SEND_RISK)
        if event.get("config_patched"): risk_flags.append(DryAdmissionGateRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)

        return ShadowLaunchReplayItem(
            replay_item_id=create_shadow_replay_item_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            attempt_type=event.get("attempt_type", "UNKNOWN"),
            source_event_id=event.get("event_id"),
            decision=decision,
            blocked=blocked,
            shadow_launch_allowed=shadow_launch_allowed,
            paper_mode_launch_allowed=paper_mode_launch_allowed,
            admission_allowed=event.get("admission_allowed", False),
            active_paper_enabled=event.get("active_paper_enabled", False),
            order_created=event.get("order_created", False),
            paper_state_mutated=event.get("paper_state_mutated", False),
            broker_order_sent=event.get("broker_order_sent", False),
            telegram_real_sent=event.get("telegram_real_sent", False),
            config_patched=event.get("config_patched", False),
            risk_flags=list(set(risk_flags)),
            warnings=[],
            errors=[]
        )

    def validate_replay_coverage(self, plan: ShadowLaunchReplayPlan, events: List[dict[str, Any]]) -> List[str]:
        event_types = [e.get("attempt_type") for e in events]
        missing = [t for t in plan.required_attempt_types if t not in event_types]
        return [f"Missing required attempt type: {t}" for t in missing]

    def determine_replay_outcome(self, plan: ShadowLaunchReplayPlan, replay_items: List[ShadowLaunchReplayItem]) -> ShadowLaunchReplayOutcome:
        for item in replay_items:
            if not item.blocked or item.shadow_launch_allowed or item.paper_mode_launch_allowed:
                return ShadowLaunchReplayOutcome.SHADOW_ATTEMPT_ALLOWED
            if item.active_paper_enabled or item.order_created or item.paper_state_mutated or item.broker_order_sent or item.telegram_real_sent or item.config_patched:
                return ShadowLaunchReplayOutcome.BLOCKED # Technically a hard fail/block

        if plan.require_all_attempts_blocked:
             return ShadowLaunchReplayOutcome.ALL_SHADOW_ATTEMPTS_BLOCKED

        return ShadowLaunchReplayOutcome.UNKNOWN

    def collect_replay_risk_flags(self, plan: ShadowLaunchReplayPlan, replay_items: List[ShadowLaunchReplayItem]) -> List[DryAdmissionGateRiskFlag]:
        flags = []
        for item in replay_items:
            flags.extend(item.risk_flags)
        return list(set(flags))

    def replay_summary(self, result: ShadowLaunchReplayResult) -> dict[str, Any]:
        return {
            "replay_result_id": result.replay_result_id,
            "status": result.status.value,
            "outcome": result.outcome.value,
            "passed": result.passed,
            "replayed": result.replayed_attempt_count,
            "allowed": result.allowed_attempt_count
        }
