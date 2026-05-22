from typing import Any, List
from usa_signal_bot.paper_dry_admission.dry_admission_models import (
    DryAdmissionFullReview,
    PaperModeDryAdmissionPlan,
    PaperModeDryAdmissionRun,
    RuntimeWriteLockProofRefresh,
    HumanApprovalLedger,
    DryAdmissionAuditEntry,
    create_dry_admission_full_review_id
)
from usa_signal_bot.core.enums import DryAdmissionReportType
from usa_signal_bot.paper_dry_admission.dry_admission_plan import build_paper_mode_dry_admission_plan
from usa_signal_bot.paper_dry_admission.dry_admission_runner import PaperModeDryAdmissionRunner
from usa_signal_bot.paper_dry_admission.dry_admission_audit import (
    audit_entry_from_dry_admission_run,
    audit_entry_from_write_lock_refresh,
    audit_entry_from_human_ledger
)
from usa_signal_bot.paper_dry_admission.dry_admission_safety_validator import validate_dry_admission_safety

def dry_admission_limitations_text() -> str:
    return (
        "LIMITATIONS AND DISCLAIMERS:\n"
        "- This dry admission rehearsal is local metadata only.\n"
        "- It does NOT constitute active paper or live trading approval.\n"
        "- Runtime write-lock proof refresh is NOT a real write attempt, it is metadata validation.\n"
        "- Human approval ledger is NOT an activation approval.\n"
        "- No broker API calls, demo or live orders are generated.\n"
        "- No real paper state mutation occurs.\n"
        "- No Telegram real sends occur.\n"
        "- No production configuration patches are applied.\n"
        "- This output does NOT contain investment advice."
    )

def build_dry_admission_review_from_parts(
    plan: PaperModeDryAdmissionPlan,
    run: PaperModeDryAdmissionRun | None = None,
    refresh: RuntimeWriteLockProofRefresh | None = None,
    ledger: HumanApprovalLedger | None = None
) -> DryAdmissionFullReview:

    review = DryAdmissionFullReview(
        review_id=create_dry_admission_full_review_id(),
        report_type=DryAdmissionReportType.FULL_DRY_ADMISSION_REVIEW,
        plans=[plan],
        runs=[run] if run else [],
        write_lock_refreshes=[refresh] if refresh else [],
        human_ledgers=[ledger] if ledger else [],
        audit_entries=[]
    )

    if run:
        review.audit_entries.append(audit_entry_from_dry_admission_run(run))
    if refresh:
        review.audit_entries.append(audit_entry_from_write_lock_refresh(refresh))
    if ledger:
        review.audit_entries.append(audit_entry_from_human_ledger(ledger))

    safety_issues = validate_dry_admission_safety(plan, run, refresh, ledger)
    if safety_issues:
        review.warnings.extend(safety_issues)

    return review

def build_dry_admission_full_review(no_write_payload: dict[str, Any]) -> DryAdmissionFullReview:
    plan = build_paper_mode_dry_admission_plan(no_write_payload)
    runner = PaperModeDryAdmissionRunner()
    run = runner.run_dry_admission(plan, no_write_payload)

    return build_dry_admission_review_from_parts(
        plan=plan,
        run=run,
        refresh=run.write_lock_refresh,
        ledger=run.human_ledger
    )

def dry_admission_full_review_summary(review: DryAdmissionFullReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "report_type": review.report_type.value,
        "plans_count": len(review.plans),
        "runs_count": len(review.runs),
        "write_lock_refreshes_count": len(review.write_lock_refreshes),
        "human_ledgers_count": len(review.human_ledgers),
        "audit_entries_count": len(review.audit_entries),
        "safety_issues_count": len(review.warnings)
    }

def dry_admission_full_review_to_text(review: DryAdmissionFullReview, limit: int = 100) -> str:
    lines = [
        f"Review ID: {review.review_id}",
        f"Report Type: {review.report_type.value}",
        f"Plans: {len(review.plans)}",
        f"Runs: {len(review.runs)}",
        f"Write-Lock Refreshes: {len(review.write_lock_refreshes)}",
        f"Human Ledgers: {len(review.human_ledgers)}",
        f"Safety Issues: {len(review.warnings)}",
        "",
        dry_admission_limitations_text()
    ]
    return "\n".join(lines)
