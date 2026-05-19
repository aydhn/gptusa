import datetime
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import SandboxValidationStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewOutput, SandboxRuntimeContext, create_sandbox_preview_output_id

def sample_notification_preview_payload(context: SandboxRuntimeContext) -> Dict[str, Any]:
    return {
        "channel": "DRY_RUN",
        "mock_message": "This is a dry-run preview of a notification. No actual telegram message sent.",
        "note": "Sandbox preview report generated."
    }

def build_sandbox_notification_preview(
    context: SandboxRuntimeContext,
    outputs: Optional[List[SandboxPreviewOutput]] = None
) -> SandboxPreviewOutput:
    payload = sample_notification_preview_payload(context)
    if outputs:
        payload["dependent_outputs"] = [o.output_id for o in outputs]

    return SandboxPreviewOutput(
        output_id=create_sandbox_preview_output_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        output_type="NOTIFICATION_PREVIEW",
        status=SandboxValidationStatus.PASS,
        summary={"mock_message_length": len(payload.get("mock_message", ""))},
        payload=payload,
        safety_flags=[],
        warnings=[],
        errors=[]
    )

def validate_notification_preview_safe(output: SandboxPreviewOutput) -> List[str]:
    warnings = []
    payload_str = str(output.payload).lower()
    unsafe_terms = ["telegram real send", "gönderildi"]
    for term in unsafe_terms:
        if term in payload_str:
            warnings.append(f"Unsafe term detected in notification preview: {term}")
    return warnings

def sandbox_notification_preview_to_text(output: SandboxPreviewOutput) -> str:
    summary = output.summary
    return f"Notification Preview [{output.output_id}]: Message length {summary.get('mock_message_length', 0)}."
