from usa_signal_bot.paper_dry_admission.dry_admission_models import (
    DryAdmissionStep, PaperModeDryAdmissionPlan, RuntimeWriteLockProofRefresh,
    HumanApprovalLedgerEntry, HumanApprovalLedger, PaperModeDryAdmissionRun,
    DryAdmissionAuditEntry, DryAdmissionFullReview,
    validate_dry_admission_step, validate_paper_mode_dry_admission_plan,
    validate_runtime_write_lock_proof_refresh, validate_human_approval_ledger_entry,
    validate_human_approval_ledger, validate_paper_mode_dry_admission_run,
    validate_dry_admission_full_review,
    dry_admission_step_to_dict, paper_mode_dry_admission_plan_to_dict,
    runtime_write_lock_proof_refresh_to_dict, human_approval_ledger_entry_to_dict,
    human_approval_ledger_to_dict, paper_mode_dry_admission_run_to_dict,
    dry_admission_audit_entry_to_dict, dry_admission_full_review_to_dict
)
from usa_signal_bot.core.enums import HumanApprovalScope, DryAdmissionReportType
import pytest

def test_dry_admission_step():
    step = DryAdmissionStep(step_id="test1", step_name="test_step")
    validate_dry_admission_step(step)

    step.write_attempted = True
    with pytest.raises(ValueError):
        validate_dry_admission_step(step)

def test_paper_mode_dry_admission_plan():
    plan = PaperModeDryAdmissionPlan(plan_id="test1")
    validate_paper_mode_dry_admission_plan(plan)

    plan.execution_enabled = True
    with pytest.raises(ValueError):
        validate_paper_mode_dry_admission_plan(plan)

def test_runtime_write_lock_proof_refresh():
    refresh = RuntimeWriteLockProofRefresh(refresh_id="test1")
    validate_runtime_write_lock_proof_refresh(refresh)

    refresh.unblocked_write_attempt_count = 1
    with pytest.raises(ValueError):
        validate_runtime_write_lock_proof_refresh(refresh)

def test_human_approval_ledger_entry():
    entry = HumanApprovalLedgerEntry(
        ledger_entry_id="test1",
        scope=HumanApprovalScope.NOT_ACTIVATION_APPROVAL,
        note="acknowledged no activation"
    )
    validate_human_approval_ledger_entry(entry)

    entry.note = "aktif et"
    with pytest.raises(ValueError):
        validate_human_approval_ledger_entry(entry)

def test_human_approval_ledger():
    ledger = HumanApprovalLedger(ledger_id="test1")
    validate_human_approval_ledger(ledger)

    ledger.activation_allowed = True
    with pytest.raises(ValueError):
        validate_human_approval_ledger(ledger)

def test_paper_mode_dry_admission_run():
    run = PaperModeDryAdmissionRun(run_id="test1")
    validate_paper_mode_dry_admission_run(run)

    run.activation_allowed = True
    with pytest.raises(ValueError):
        validate_paper_mode_dry_admission_run(run)

def test_dry_admission_full_review():
    review = DryAdmissionFullReview(review_id="test1", report_type=DryAdmissionReportType.FULL_DRY_ADMISSION_REVIEW)
    validate_dry_admission_full_review(review)
    d = dry_admission_full_review_to_dict(review)
    assert d["review_id"] == "test1"
