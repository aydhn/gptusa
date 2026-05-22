from typing import Any
from usa_signal_bot.paper_dry_admission.dry_admission_models import (
    PaperModeDryAdmissionPlan,
    PaperModeDryAdmissionRun,
    RuntimeWriteLockProofRefresh,
    HumanApprovalLedger,
    DryAdmissionFullReview
)
from usa_signal_bot.paper_dry_admission.dry_admission_report import build_dry_admission_full_review

def dry_admission_plan_from_no_write(payload: dict[str, Any]) -> PaperModeDryAdmissionPlan:
    review = build_dry_admission_full_review(payload)
    return review.plans[-1] if review.plans else None

def dry_admission_run_from_no_write(payload: dict[str, Any]) -> PaperModeDryAdmissionRun:
    review = build_dry_admission_full_review(payload)
    return review.runs[-1] if review.runs else None

def write_lock_refresh_from_no_write(payload: dict[str, Any]) -> RuntimeWriteLockProofRefresh:
    review = build_dry_admission_full_review(payload)
    return review.write_lock_refreshes[-1] if review.write_lock_refreshes else None

def human_ledger_from_no_write(payload: dict[str, Any]) -> HumanApprovalLedger:
    review = build_dry_admission_full_review(payload)
    return review.human_ledgers[-1] if review.human_ledgers else None

def dry_admission_full_review_from_no_write(payload: dict[str, Any]) -> DryAdmissionFullReview:
    return build_dry_admission_full_review(payload)

def attach_dry_admission_metadata_to_no_write_payload(payload: dict[str, Any], review: DryAdmissionFullReview) -> dict[str, Any]:
    new_payload = payload.copy()
    new_payload["dry_admission_metadata"] = {
        "review_id": review.review_id,
        "report_type": review.report_type.value,
        "run_status": review.runs[-1].status.value if review.runs else "UNKNOWN"
    }
    return new_payload

def no_write_dry_admission_summary(payload: dict[str, Any]) -> dict[str, Any]:
    metadata = payload.get("dry_admission_metadata", {})
    return {
        "has_metadata": bool(metadata),
        "review_id": metadata.get("review_id"),
        "run_status": metadata.get("run_status")
    }

def no_write_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = no_write_dry_admission_summary(payload)
    lines = [
        f"Has Metadata: {summary['has_metadata']}",
        f"Review ID: {summary.get('review_id')}",
        f"Run Status: {summary.get('run_status')}"
    ]
    return "\n".join(lines)
