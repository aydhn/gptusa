from typing import Any, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import FirewallReplayStatus, FirewallReplayDecision
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import (
    FirewallReplayPlan, create_firewall_replay_plan_id, validate_firewall_replay_plan
)
from usa_signal_bot.paper_firewall_audit.pre_rehearsal_ingestion import (
    extract_pre_paper_candidate_id, extract_firewall_events
)

def required_firewall_replay_attempt_types() -> List[str]:
    return [
        "PAPER_STATE_WRITE",
        "PAPER_ORDER_CREATE",
        "PAPER_POSITION_MUTATION",
        "PAPER_PORTFOLIO_MUTATION",
        "PAPER_CASH_MUTATION",
        "PAPER_EQUITY_MUTATION",
        "PAPER_FILL_CREATE",
        "BROKER_ORDER_SEND",
        "TELEGRAM_REAL_SEND",
        "PRODUCTION_CONFIG_PATCH",
        "ACTIVE_PAPER_ENABLE",
        "OBSERVER_UNLOCK",
        "ARCHIVE_UNLOCK",
        "FINAL_LOCK_UNLOCK"
    ]

def build_firewall_replay_plan(pre_rehearsal_payload: dict[str, Any]) -> FirewallReplayPlan:
    candidate_id = extract_pre_paper_candidate_id(pre_rehearsal_payload)
    events = extract_firewall_events(pre_rehearsal_payload)

    plan = FirewallReplayPlan(
        replay_plan_id=create_firewall_replay_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id=candidate_id,
        source_pre_rehearsal_review_id=pre_rehearsal_payload.get("review_id"),
        source_pre_paper_run_id=pre_rehearsal_payload.get("run_id"),
        status=FirewallReplayStatus.READY,
        decision=FirewallReplayDecision.REPLAY_FIREWALL_EVENTS,
        required_attempt_types=required_firewall_replay_attempt_types(),
        replay_event_count=len(events),
        require_all_dangerous_attempts_blocked=True,
        execution_enabled=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        telegram_real_send_enabled=False,
        warnings=[],
        errors=[]
    )
    validate_firewall_replay_plan(plan)
    return plan

def build_default_firewall_replay_plan(candidate_id: Optional[str] = None) -> FirewallReplayPlan:
    plan = FirewallReplayPlan(
        replay_plan_id=create_firewall_replay_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id=candidate_id,
        source_pre_rehearsal_review_id=None,
        source_pre_paper_run_id=None,
        status=FirewallReplayStatus.READY,
        decision=FirewallReplayDecision.REPLAY_FIREWALL_EVENTS,
        required_attempt_types=required_firewall_replay_attempt_types(),
        replay_event_count=0,
        require_all_dangerous_attempts_blocked=True,
        execution_enabled=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        telegram_real_send_enabled=False,
        warnings=[],
        errors=[]
    )
    validate_firewall_replay_plan(plan)
    return plan

def validate_firewall_replay_plan_safety(plan: FirewallReplayPlan) -> List[str]:
    errors = []
    if plan.execution_enabled: errors.append("Execution must be disabled")
    if plan.active_paper_enabled: errors.append("Active paper must be disabled")
    if plan.broker_execution_enabled: errors.append("Broker execution must be disabled")
    if plan.paper_state_mutation_enabled: errors.append("Paper state mutation must be disabled")
    if plan.config_patch_enabled: errors.append("Config patch must be disabled")
    if plan.telegram_real_send_enabled: errors.append("Telegram real send must be disabled")
    return errors

def firewall_replay_plan_summary(plan: FirewallReplayPlan) -> dict[str, Any]:
    return {
        "id": plan.replay_plan_id,
        "status": plan.status.value,
        "events": plan.replay_event_count
    }

def firewall_replay_plan_to_text(plan: FirewallReplayPlan) -> str:
    return f"FirewallReplayPlan {plan.replay_plan_id} ({plan.status.value}) - {plan.replay_event_count} events"
