import datetime
from typing import Any, Dict, List
from usa_signal_bot.core.enums import SandboxValidationStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewOutput, SandboxRuntimeContext, create_sandbox_preview_output_id

def sample_portfolio_preview_payload(context: SandboxRuntimeContext) -> Dict[str, Any]:
    return {"mock_portfolio": "balanced"}

def build_portfolio_preview(context: SandboxRuntimeContext) -> SandboxPreviewOutput:
    return SandboxPreviewOutput(
        output_id=create_sandbox_preview_output_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        output_type="portfolio_preview",
        status=SandboxValidationStatus.PASS,
        summary={"exposure": 0.5},
        payload=sample_portfolio_preview_payload(context),
        safety_flags=[],
        warnings=[],
        errors=[]
    )

def validate_portfolio_preview_safe(output: SandboxPreviewOutput) -> List[str]:
    return []

def portfolio_preview_to_text(output: SandboxPreviewOutput) -> str:
    return "Portfolio Preview: PASS"
