from typing import Any, Dict
from usa_signal_bot.release_sandbox.sandbox_models import (
    SandboxMountPlan, SandboxActivationPlan, SandboxRuntimeContext,
    SandboxPreviewOutput, SandboxPreviewRun, SandboxValidationResult, ReleaseSandboxReview
)
from usa_signal_bot.release_sandbox.mount_planner import mount_plan_to_text
from usa_signal_bot.release_sandbox.activation_planner import activation_plan_to_text
from usa_signal_bot.release_sandbox.runtime_context import runtime_context_to_text
from usa_signal_bot.release_sandbox.signal_preview import signal_preview_to_text
from usa_signal_bot.release_sandbox.portfolio_preview import portfolio_preview_to_text
from usa_signal_bot.release_sandbox.risk_preview import risk_preview_to_text
from usa_signal_bot.release_sandbox.notification_preview import sandbox_notification_preview_to_text
from usa_signal_bot.release_sandbox.preview_runner import preview_run_summary
from usa_signal_bot.release_sandbox.safety_validator import sandbox_safety_validation_to_text
from usa_signal_bot.release_sandbox.sandbox_report import sandbox_report_to_text, sandbox_review_limitations_text

def sandbox_mount_plan_to_text(item: SandboxMountPlan) -> str:
    return mount_plan_to_text(item)

def sandbox_activation_plan_to_text(item: SandboxActivationPlan) -> str:
    return activation_plan_to_text(item)

def sandbox_runtime_context_to_text(item: SandboxRuntimeContext) -> str:
    return runtime_context_to_text(item)

def sandbox_preview_output_to_text(item: SandboxPreviewOutput) -> str:
    if item.output_type == "SIGNAL_PREVIEW":
        return signal_preview_to_text(item)
    elif item.output_type == "PORTFOLIO_PREVIEW":
        return portfolio_preview_to_text(item)
    elif item.output_type == "RISK_PREVIEW":
        return risk_preview_to_text(item)
    elif item.output_type == "NOTIFICATION_PREVIEW":
        return sandbox_notification_preview_to_text(item)
    return f"Preview Output [{item.output_id}]: {item.output_type}"

def sandbox_preview_run_to_text(item: SandboxPreviewRun) -> str:
    s = preview_run_summary(item)
    return f"Sandbox Preview Run [{s['run_id']}]: Status={s['status']}, Mode={s['runtime_mode']}"

def sandbox_validation_result_to_text(item: SandboxValidationResult) -> str:
    return sandbox_safety_validation_to_text(item)

def release_sandbox_review_to_text(item: ReleaseSandboxReview, limit: int = 100) -> str:
    return sandbox_report_to_text(item, limit)

def sandbox_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Sandbox Store: {summary.get('reviews_count', 0)} reviews stored."

def release_sandbox_limitations_text() -> str:
    return sandbox_review_limitations_text()
