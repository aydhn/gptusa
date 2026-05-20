import datetime
from typing import Any

from usa_signal_bot.core.enums import BridgePlanStatus, BridgeMode
from usa_signal_bot.paper_quarantine.quarantine_models import (
    SupervisedDryRunBridgePlan,
    QuarantinedPaperCandidate,
    ReadOnlyPromotionTicket,
    QuarantinePolicy,
    create_bridge_plan_id,
    validate_supervised_dry_run_bridge_plan,
)
from usa_signal_bot.paper_quarantine.quarantine_policy import allowed_quarantine_bridge_operations, denied_quarantine_bridge_operations
from usa_signal_bot.paper_quarantine.eligibility_checker import quarantine_safety_flags_from_shadow_governance

def build_supervised_dry_run_bridge_plan(
    candidate: QuarantinedPaperCandidate,
    ticket: ReadOnlyPromotionTicket,
    policy: QuarantinePolicy | None = None
) -> SupervisedDryRunBridgePlan:

    allowed = policy.allowed_bridge_operations if policy else allowed_quarantine_bridge_operations()
    denied = policy.denied_bridge_operations if policy else denied_quarantine_bridge_operations()

    plan = SupervisedDryRunBridgePlan(
        bridge_plan_id=create_bridge_plan_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        status=BridgePlanStatus.READY,
        mode=BridgeMode.SUPERVISED_DRY_RUN_PLANNING,
        candidate_id=candidate.candidate_id,
        ticket_id=ticket.ticket_id,
        paper_snapshot_ref_id=candidate.paper_snapshot_ref.snapshot_ref_id if candidate.paper_snapshot_ref else None,
        quarantine_output_path=f"data/paper_quarantine/outputs/{candidate.candidate_id}",
        allowed_operations=allowed,
        denied_operations=denied,
        manual_review_required=True,
        bridge_execution_enabled=False,
        paper_state_mutation_enabled=False,
        paper_order_enabled=False,
        broker_order_enabled=False,
        telegram_real_send_enabled=False,
        production_config_write_enabled=False,
        safety_flags=candidate.risk_flags.copy(),
        warnings=[],
        errors=[]
    )
    validate_supervised_dry_run_bridge_plan(plan)
    return plan

def bridge_plan_from_shadow_governance_payload(payload: dict[str, Any], paper_snapshot: dict[str, Any] | None = None) -> SupervisedDryRunBridgePlan:
    allowed = allowed_quarantine_bridge_operations()
    denied = denied_quarantine_bridge_operations()
    flags = quarantine_safety_flags_from_shadow_governance(payload)

    plan = SupervisedDryRunBridgePlan(
        bridge_plan_id=create_bridge_plan_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        status=BridgePlanStatus.DRAFT,
        mode=BridgeMode.SUPERVISED_DRY_RUN_PLANNING,
        candidate_id=None,
        ticket_id=None,
        paper_snapshot_ref_id=None,
        quarantine_output_path="data/paper_quarantine/outputs/shadow_payload",
        allowed_operations=allowed,
        denied_operations=denied,
        manual_review_required=True,
        bridge_execution_enabled=False,
        paper_state_mutation_enabled=False,
        paper_order_enabled=False,
        broker_order_enabled=False,
        telegram_real_send_enabled=False,
        production_config_write_enabled=False,
        safety_flags=flags,
        warnings=[],
        errors=[]
    )
    validate_supervised_dry_run_bridge_plan(plan)
    return plan

def validate_bridge_plan_safety(plan: SupervisedDryRunBridgePlan) -> list[str]:
    errors = []
    if plan.bridge_execution_enabled:
        errors.append("bridge_execution_enabled must be False")
    if plan.paper_state_mutation_enabled:
        errors.append("paper_state_mutation_enabled must be False")
    if plan.paper_order_enabled:
        errors.append("paper_order_enabled must be False")
    if plan.broker_order_enabled:
        errors.append("broker_order_enabled must be False")
    if plan.telegram_real_send_enabled:
        errors.append("telegram_real_send_enabled must be False")
    if plan.production_config_write_enabled:
        errors.append("production_config_write_enabled must be False")
    return errors

def bridge_plan_summary(plan: SupervisedDryRunBridgePlan) -> dict[str, Any]:
    return {
        "bridge_plan_id": plan.bridge_plan_id,
        "status": plan.status.value,
        "mode": plan.mode.value,
        "paper_state_mutation_enabled": plan.paper_state_mutation_enabled,
    }

def bridge_plan_to_text(plan: SupervisedDryRunBridgePlan) -> str:
    lines = [
        f"Bridge Plan: {plan.bridge_plan_id}",
        f"Status: {plan.status.value}",
        f"Mode: {plan.mode.value}",
        f"Candidate ID: {plan.candidate_id}",
        f"Ticket ID: {plan.ticket_id}",
        f"Paper Mutation Enabled: {plan.paper_state_mutation_enabled}",
        f"Broker Order Enabled: {plan.broker_order_enabled}",
    ]
    return "\n".join(lines)
