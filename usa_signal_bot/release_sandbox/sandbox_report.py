import datetime
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import SandboxReportType
from usa_signal_bot.release_sandbox.sandbox_models import (
    SandboxActivationPlan, SandboxPreviewRun, SandboxValidationResult,
    ReleaseSandboxReview, create_release_sandbox_review_id
)

def build_sandbox_review(
    activation_plan: SandboxActivationPlan,
    preview_run: Optional[SandboxPreviewRun] = None,
    validation_result: Optional[SandboxValidationResult] = None
) -> ReleaseSandboxReview:

    return ReleaseSandboxReview(
        review_id=create_release_sandbox_review_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
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
    return {
        "review_id": review.review_id,
        "activation_plans_count": len(review.activation_plans),
        "preview_runs_count": len(review.preview_runs),
        "validation_results_count": len(review.validation_results)
    }

def sandbox_review_limitations_text() -> str:
    return (
        "LIMITATIONS:\n"
        "- Sandbox is a local preview environment only.\n"
        "- No broker/live/demo orders are generated.\n"
        "- No paper state is mutated.\n"
        "- No Telegram real sends occur.\n"
        "- No production configs are patched.\n"
        "- Results do not guarantee future performance and are not investment advice.\n"
        "- PASS is not a live trading approval."
    )

def sandbox_report_to_text(review: ReleaseSandboxReview, limit: int = 100) -> str:
    summary = sandbox_review_summary(review)
    return f"Sandbox Review [{summary['review_id']}]: Plans={summary['activation_plans_count']}, Runs={summary['preview_runs_count']}\n{sandbox_review_limitations_text()}"
