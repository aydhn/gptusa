import datetime
from typing import Any, Dict, List
from usa_signal_bot.core.enums import SandboxValidationStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewOutput, SandboxRuntimeContext, create_sandbox_preview_output_id

def sample_signal_preview_payload(context: SandboxRuntimeContext) -> Dict[str, Any]:
    return {"mock_signal": "BUY", "confidence": 0.8}

def build_signal_preview(context: SandboxRuntimeContext) -> SandboxPreviewOutput:
    return SandboxPreviewOutput(
        output_id=create_sandbox_preview_output_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        output_type="signal_preview",
        status=SandboxValidationStatus.PASS,
        summary={"signals": 1},
        payload=sample_signal_preview_payload(context),
        safety_flags=[],
        warnings=[],
        errors=[]
    )

def validate_signal_preview_safe(output: SandboxPreviewOutput) -> List[str]:
    return []

def signal_preview_to_text(output: SandboxPreviewOutput) -> str:
    return "Signal Preview: PASS"
