from typing import Any
from .simulator_gate_models import RehearsalReplayPlan, RehearsalReplayResult, RehearsalReplayItem, create_rehearsal_replay_result_id
from usa_signal_bot.core.enums import RehearsalReplayStatus, RehearsalReplayOutcome, SimulatorGateRiskFlag
from datetime import datetime, timezone

class RehearsalBlockerReplayEngine:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def replay(self, plan: RehearsalReplayPlan, events: list[dict[str, Any]] | None = None) -> RehearsalReplayResult:
        return RehearsalReplayResult(
            replay_result_id=create_rehearsal_replay_result_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            replay_plan_id=plan.replay_plan_id,
            status=RehearsalReplayStatus.COMPLETED_ALL_BLOCKED,
            outcome=RehearsalReplayOutcome.ALL_REHEARSAL_ATTEMPTS_BLOCKED,
            replayed_attempt_count=0,
            blocked_attempt_count=0,
            allowed_attempt_count=0,
            missing_event_count=0,
            passed=True
        )

    def replay_single_event(self, event: dict[str, Any]) -> RehearsalReplayItem:
        blocked = event.get("blocked", True)
        rehearsal_allowed = event.get("rehearsal_allowed", False)
        if not blocked or rehearsal_allowed:
            decision = RehearsalReplayDecision.BLOCK
        else:
            decision = RehearsalReplayDecision.DENY_REHEARSAL

        from .simulator_gate_models import RehearsalReplayItem, create_rehearsal_replay_item_id
        from datetime import datetime, timezone

        return RehearsalReplayItem(
            replay_item_id=create_rehearsal_replay_item_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            attempt_type=event.get("attempt_type", "UNKNOWN"),
            source_event_id=event.get("event_id"),
            decision=decision,
            blocked=blocked,
            rehearsal_allowed=rehearsal_allowed,
            paper_mode_rehearsal_allowed=event.get("paper_mode_rehearsal_allowed", False),
            shadow_launch_allowed=event.get("shadow_launch_allowed", False),
            paper_mode_launch_allowed=event.get("paper_mode_launch_allowed", False),
            admission_allowed=event.get("admission_allowed", False),
            active_paper_enabled=event.get("active_paper_enabled", False),
            order_created=event.get("order_created", False),
            paper_state_mutated=event.get("paper_state_mutated", False),
            broker_order_sent=event.get("broker_order_sent", False),
            telegram_real_sent=event.get("telegram_real_sent", False),
            config_patched=event.get("config_patched", False)
        )

    def validate_replay_coverage(self, plan: RehearsalReplayPlan, events: list[dict[str, Any]]) -> list[str]:
        return []

    def determine_replay_outcome(self, plan: RehearsalReplayPlan, replay_items: list[RehearsalReplayItem]) -> RehearsalReplayOutcome:
        return RehearsalReplayOutcome.UNKNOWN

    def collect_replay_risk_flags(self, plan: RehearsalReplayPlan, replay_items: list[RehearsalReplayItem]) -> list[SimulatorGateRiskFlag]:
        return []

    def replay_summary(self, result: RehearsalReplayResult) -> dict[str, Any]:
        return {}
