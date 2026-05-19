import datetime
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import SandboxValidationStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewOutput, SandboxRuntimeContext, create_sandbox_preview_output_id

def sample_notification_preview_payload(context: SandboxRuntimeContext) -> Dict[str, Any]:
    return {"mock_message": "Preview Run completed. No real send."}

def build_sandbox_notification_preview(context: SandboxRuntimeContext, outputs: Optional[List[SandboxPreviewOutput]] = None) -> SandboxPreviewOutput:
    return SandboxPreviewOutput(
        output_id=create_sandbox_preview_output_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        output_type="notification_preview",
        status=SandboxValidationStatus.PASS,
        summary={"notifications": 1},
        payload=sample_notification_preview_payload(context),
        safety_flags=[],
        warnings=[],
        errors=[]
    )

def validate_notification_preview_safe(output: SandboxPreviewOutput) -> List[str]:
    return []

def sandbox_notification_preview_to_text(output: SandboxPreviewOutput) -> str:
    return "Notification Preview: DRY RUN"
