
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_safe_gate.paper_safe_gate_models import (
    BoundaryCertificateReplayPlan, create_boundary_replay_plan_id, utcnow_iso
)

def required_boundary_replay_rule_names() -> List[str]:
    return [
        "activation_denied",
        "activation_allowed_false",
        "admission_allowed_false",
        "transition_allowed_false",
        "all_writes_blocked",
        "order_created_false",
        "mutation_detected_false",
        "blocker_replay_passed",
        "evidence_freeze_valid"
    ]

def required_boundary_replay_assertion_names() -> List[str]:
    return [
        "read_only_metadata_boundary",
        "no_order_boundary",
        "no_write_boundary",
        "no_broker_boundary",
        "no_activation_boundary",
        "no_telegram_real_send_boundary",
        "no_config_patch_boundary"
    ]

def build_default_boundary_replay_plan(candidate_id: Optional[str] = None) -> BoundaryCertificateReplayPlan:
    return BoundaryCertificateReplayPlan(
        replay_plan_id=create_boundary_replay_plan_id(),
        created_at_utc=utcnow_iso(),
        candidate_id=candidate_id,
        source_boundary_certificate_id=None,
        source_boundary_review_id=None,
        required_rule_names=required_boundary_replay_rule_names(),
        required_assertion_names=required_boundary_replay_assertion_names(),
        require_all_rules_pass=True,
        require_all_assertions_pass=True,
        execution_enabled=False,
        active_paper_enabled=False,
        paper_admission_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        telegram_real_send_enabled=False,
        warnings=[],
        errors=[]
    )

def build_boundary_certificate_replay_plan(boundary_payload: Dict[str, Any]) -> BoundaryCertificateReplayPlan:
    plan = build_default_boundary_replay_plan(boundary_payload.get("candidate_id"))
    plan.source_boundary_certificate_id = boundary_payload.get("boundary_certificate_id")
    plan.source_boundary_review_id = boundary_payload.get("boundary_review_id")
    return plan

def validate_boundary_replay_plan_safety(plan: BoundaryCertificateReplayPlan) -> List[str]:
    errors = []
    if plan.execution_enabled: errors.append("execution_enabled must be false")
    if plan.active_paper_enabled: errors.append("active_paper_enabled must be false")
    if plan.paper_admission_enabled: errors.append("paper_admission_enabled must be false")
    if plan.broker_execution_enabled: errors.append("broker_execution_enabled must be false")
    if plan.paper_state_mutation_enabled: errors.append("paper_state_mutation_enabled must be false")
    if plan.config_patch_enabled: errors.append("config_patch_enabled must be false")
    if plan.telegram_real_send_enabled: errors.append("telegram_real_send_enabled must be false")
    return errors

def boundary_replay_plan_summary(plan: BoundaryCertificateReplayPlan) -> Dict[str, Any]:
    return {
        "replay_plan_id": plan.replay_plan_id,
        "candidate_id": plan.candidate_id,
        "required_rules": len(plan.required_rule_names),
        "required_assertions": len(plan.required_assertion_names)
    }

def boundary_replay_plan_to_text(plan: BoundaryCertificateReplayPlan) -> str:
    return f"Boundary Replay Plan {plan.replay_plan_id} for candidate {plan.candidate_id}"
