from typing import Any, List
from usa_signal_bot.paper_dry_admission.dry_admission_models import (
    PaperModeDryAdmissionPlan,
    create_dry_admission_plan_id
)
from usa_signal_bot.core.enums import PaperModeDryAdmissionDecision
from usa_signal_bot.paper_dry_admission.no_write_ingestion import (
    extract_no_write_candidate_id,
    extract_no_write_contract,
    extract_paper_mode_preflight
)
from usa_signal_bot.paper_dry_admission.eligibility_checker import evaluate_dry_admission_eligibility

def default_dry_admission_steps() -> List[str]:
    return [
        "no_write_contract_load",
        "read_only_paper_snapshot_refresh",
        "write_lock_proof_refresh",
        "activation_replay_reference_check",
        "human_ledger_prepare",
        "signal_pipeline_no_write_preview",
        "risk_pipeline_no_write_preview",
        "notification_dry_preview",
        "no_write_continuity_assertion",
        "final_dry_admission_summary"
    ]

def required_dry_admission_inputs() -> List[str]:
    return [
        "no_write_contract",
        "activation_replay",
        "paper_mode_preflight"
    ]

def required_dry_admission_outputs() -> List[str]:
    return [
        "dry_admission_run_report",
        "write_lock_proof_refresh_report",
        "human_approval_ledger_report",
        "dry_admission_safety_report"
    ]

def build_default_dry_admission_plan(candidate_id: str | None = None) -> PaperModeDryAdmissionPlan:
    return PaperModeDryAdmissionPlan(
        plan_id=create_dry_admission_plan_id(),
        candidate_id=candidate_id,
        decision=PaperModeDryAdmissionDecision.UNKNOWN,
        planned_steps=default_dry_admission_steps(),
        required_inputs=required_dry_admission_inputs(),
        expected_outputs=required_dry_admission_outputs()
    )

def build_paper_mode_dry_admission_plan(no_write_payload: dict[str, Any]) -> PaperModeDryAdmissionPlan:
    candidate_id = extract_no_write_candidate_id(no_write_payload)
    decision = evaluate_dry_admission_eligibility(no_write_payload)

    contract = extract_no_write_contract(no_write_payload)
    preflight = extract_paper_mode_preflight(no_write_payload)

    plan = build_default_dry_admission_plan(candidate_id)
    plan.decision = decision
    if contract:
        plan.source_contract_id = contract.get("contract_id")
    if preflight:
        plan.source_preflight_id = preflight.get("preflight_id")

    if decision != PaperModeDryAdmissionDecision.RUN_DRY_ADMISSION_REHEARSAL:
        plan.warnings.append(f"Eligibility decision is {decision.value}. Run will likely fail or skip.")

    return plan

def validate_dry_admission_plan_safety(plan: PaperModeDryAdmissionPlan) -> List[str]:
    issues = []
    if plan.execution_enabled: issues.append("execution_enabled is True")
    if plan.active_paper_enabled: issues.append("active_paper_enabled is True")
    if plan.broker_execution_enabled: issues.append("broker_execution_enabled is True")
    if plan.paper_state_mutation_enabled: issues.append("paper_state_mutation_enabled is True")
    if plan.config_patch_enabled: issues.append("config_patch_enabled is True")
    if plan.telegram_real_send_enabled: issues.append("telegram_real_send_enabled is True")
    if not plan.require_write_lock_refresh: issues.append("require_write_lock_refresh is False")
    if not plan.require_human_ledger: issues.append("require_human_ledger is False")
    return issues

def dry_admission_plan_summary(plan: PaperModeDryAdmissionPlan) -> dict[str, Any]:
    return {
        "plan_id": plan.plan_id,
        "candidate_id": plan.candidate_id,
        "decision": plan.decision.value,
        "safety_issues": validate_dry_admission_plan_safety(plan),
        "steps_count": len(plan.planned_steps)
    }

def dry_admission_plan_to_text(plan: PaperModeDryAdmissionPlan) -> str:
    lines = [
        f"Plan ID: {plan.plan_id}",
        f"Candidate: {plan.candidate_id}",
        f"Decision: {plan.decision.value}",
        f"Steps: {len(plan.planned_steps)}",
        f"Safety Issues: {len(validate_dry_admission_plan_safety(plan))}"
    ]
    return "\n".join(lines)
