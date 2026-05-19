from typing import Any, Dict, Optional
import datetime
from usa_signal_bot.core.enums import SandboxReportType
from usa_signal_bot.release_sandbox.sandbox_models import (
    ReleaseSandboxReview, SandboxActivationPlan, SandboxPreviewRun,
    SandboxValidationResult, create_release_sandbox_review_id
)

def build_sandbox_review(activation_plan: SandboxActivationPlan, preview_run: Optional[SandboxPreviewRun] = None, validation_result: Optional[SandboxValidationResult] = None) -> ReleaseSandboxReview:
    return ReleaseSandboxReview(
        review_id=create_release_sandbox_review_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        report_type=SandboxReportType.FULL_SANDBOX_REVIEW,
        activation_plans=[activation_plan],
        mount_plans=[activation_plan.mount_plan] if activation_plan.mount_plan else [],
        preview_runs=[preview_run] if preview_run else [],
        validation_results=[validation_result] if validation_result else [],
        output_paths={},
        warnings=[],
        errors=[]
    )

def sandbox_review_summary(review: ReleaseSandboxReview) -> Dict[str, Any]:
    return {"review_id": review.review_id}

def sandbox_review_limitations_text() -> str:
    return "LIMITATIONS: No real orders, no paper state mutation, no telegram real sends."

def sandbox_report_to_text(review: ReleaseSandboxReview, limit: int = 100) -> str:
    return f"Sandbox Report {review.review_id}\n{sandbox_review_limitations_text()}"
