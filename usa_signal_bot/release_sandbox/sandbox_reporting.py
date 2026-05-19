from typing import Any, Dict
from usa_signal_bot.release_sandbox.sandbox_models import (
    SandboxMountPlan, SandboxActivationPlan, SandboxRuntimeContext,
    SandboxPreviewOutput, SandboxPreviewRun, SandboxValidationResult, ReleaseSandboxReview
)

def sandbox_mount_plan_to_text(item: SandboxMountPlan) -> str: return "Mount Plan"
def sandbox_activation_plan_to_text(item: SandboxActivationPlan) -> str: return "Activation Plan"
def sandbox_runtime_context_to_text(item: SandboxRuntimeContext) -> str: return "Runtime Context"
def sandbox_preview_output_to_text(item: SandboxPreviewOutput) -> str: return "Preview Output"
def sandbox_preview_run_to_text(item: SandboxPreviewRun) -> str: return "Preview Run"
def sandbox_validation_result_to_text(item: SandboxValidationResult) -> str: return "Validation Result"
def release_sandbox_review_to_text(item: ReleaseSandboxReview, limit: int = 100) -> str: return "Review"
def sandbox_store_summary_to_text(summary: Dict[str, Any]) -> str: return "Store Summary"
def release_sandbox_limitations_text() -> str: return "LIMITATIONS: No real trades, no mutation."
