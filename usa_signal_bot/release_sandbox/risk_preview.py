import datetime
from typing import Any, Dict, List
from usa_signal_bot.core.enums import SandboxValidationStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewOutput, SandboxRuntimeContext, create_sandbox_preview_output_id

def sample_risk_preview_payload(context: SandboxRuntimeContext) -> Dict[str, Any]:
    return {"mock_risk": "low"}

def build_risk_preview(context: SandboxRuntimeContext) -> SandboxPreviewOutput:
    return SandboxPreviewOutput(
        output_id=create_sandbox_preview_output_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        output_type="risk_preview",
        status=SandboxValidationStatus.PASS,
        summary={"risk": "low"},
        payload=sample_risk_preview_payload(context),
        safety_flags=[],
        warnings=[],
        errors=[]
    )

def validate_risk_preview_safe(output: SandboxPreviewOutput) -> List[str]:
    return []

def risk_preview_to_text(output: SandboxPreviewOutput) -> str:
    return "Risk Preview: PASS"
