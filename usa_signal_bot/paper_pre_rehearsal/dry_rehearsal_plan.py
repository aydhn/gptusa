from typing import Any, Dict, List
import datetime
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import (
    PrePaperDryRehearsalPlan,
    create_pre_paper_plan_id,
    validate_pre_paper_dry_rehearsal_plan
)
from usa_signal_bot.core.enums import PrePaperDryRehearsalStatus, PrePaperDryRehearsalDecision
from usa_signal_bot.paper_pre_rehearsal.eligibility_checker import (
    evaluate_pre_paper_rehearsal_eligibility,
    pre_paper_status_from_decision
)
from usa_signal_bot.paper_pre_rehearsal.final_handoff_ingestion import (
    extract_final_handoff_candidate_id,
    extract_pre_paper_checkpoint,
    extract_sealed_archive_manifest
)

def build_pre_paper_dry_rehearsal_plan(final_handoff_payload: Dict[str, Any]) -> PrePaperDryRehearsalPlan:
    decision = evaluate_pre_paper_rehearsal_eligibility(final_handoff_payload)
    status = pre_paper_status_from_decision(decision)

    candidate_id = extract_final_handoff_candidate_id(final_handoff_payload)
    checkpoint = extract_pre_paper_checkpoint(final_handoff_payload)
    archive = extract_sealed_archive_manifest(final_handoff_payload)

    source_checkpoint_id = checkpoint.get("checkpoint_id") if checkpoint else None
    source_archive_id = archive.get("archive_id") if archive else None

    plan = PrePaperDryRehearsalPlan(


        candidate_id=candidate_id,
        source_checkpoint_id=source_checkpoint_id,
        source_archive_id=source_archive_id,
        status=status,
        decision=decision,
        required_inputs=["final_handoff_payload", "read_only_paper_baseline"],
        expected_outputs=["firewall_events", "activation_checkpoint", "zero_mutation_assertion", "pre_paper_review"],
        firewall_required=True,
        activation_denied_required=True,
        execution_enabled=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        telegram_real_send_enabled=False,
        warnings=[],
        errors=[]
    )
    validate_pre_paper_dry_rehearsal_plan(plan)
    return plan

def build_default_pre_paper_dry_rehearsal_plan(candidate_id: str | None = None) -> PrePaperDryRehearsalPlan:
    plan = PrePaperDryRehearsalPlan(


        candidate_id=candidate_id,
        source_checkpoint_id=None,
        source_archive_id=None,
        status=PrePaperDryRehearsalStatus.DRAFT,
        decision=PrePaperDryRehearsalDecision.INCONCLUSIVE,
        required_inputs=["read_only_paper_baseline"],
        expected_outputs=["firewall_events", "activation_checkpoint"],
        firewall_required=True,
        activation_denied_required=True,
        execution_enabled=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        telegram_real_send_enabled=False,
        warnings=[],
        errors=[]
    )
    validate_pre_paper_dry_rehearsal_plan(plan)
    return plan

def validate_pre_paper_plan_safety(plan: PrePaperDryRehearsalPlan) -> List[str]:
    violations = []
    if plan.execution_enabled: violations.append("execution_enabled must be false")
    if plan.active_paper_enabled: violations.append("active_paper_enabled must be false")
    if plan.broker_execution_enabled: violations.append("broker_execution_enabled must be false")
    if plan.paper_state_mutation_enabled: violations.append("paper_state_mutation_enabled must be false")
    if plan.config_patch_enabled: violations.append("config_patch_enabled must be false")
    if plan.telegram_real_send_enabled: violations.append("telegram_real_send_enabled must be false")
    if not plan.firewall_required: violations.append("firewall_required must be true")
    if not plan.activation_denied_required: violations.append("activation_denied_required must be true")
    return violations

def pre_paper_plan_summary(plan: PrePaperDryRehearsalPlan) -> Dict[str, Any]:
    return {
        "plan_id": plan.plan_id,
        "status": plan.status.value,
        "decision": plan.decision.value,
        "safe": len(validate_pre_paper_plan_safety(plan)) == 0
    }

def pre_paper_plan_to_text(plan: PrePaperDryRehearsalPlan) -> str:
    return f"Plan {plan.plan_id} (Status: {plan.status.value}, Decision: {plan.decision.value})"
