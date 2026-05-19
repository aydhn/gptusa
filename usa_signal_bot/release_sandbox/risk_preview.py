import datetime
from typing import Any, Dict, List
from usa_signal_bot.core.enums import SandboxValidationStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewOutput, SandboxRuntimeContext, create_sandbox_preview_output_id

def sample_risk_preview_payload(context: SandboxRuntimeContext) -> Dict[str, Any]:
    return {
        "mock_drawdown": 0.05,
        "concentration": {"TECH": 0.2},
        "note": "Mock risk summary. Not investment advice."
    }

def build_risk_preview(context: SandboxRuntimeContext) -> SandboxPreviewOutput:
    payload = sample_risk_preview_payload(context)
    return SandboxPreviewOutput(
        output_id=create_sandbox_preview_output_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        output_type="RISK_PREVIEW",
        status=SandboxValidationStatus.PASS,
        summary={"concentration_clusters": len(payload.get("concentration", {}))},
        payload=payload,
        safety_flags=[],
        warnings=[],
        errors=[]
    )

def validate_risk_preview_safe(output: SandboxPreviewOutput) -> List[str]:
    warnings = []
    payload_str = str(output.payload).lower()
    unsafe_terms = ["kesin kâr", "garanti"]
    for term in unsafe_terms:
        if term in payload_str:
            warnings.append(f"Unsafe term detected in risk preview: {term}")
    return warnings

def risk_preview_to_text(output: SandboxPreviewOutput) -> str:
    summary = output.summary
    return f"Risk Preview [{output.output_id}]: {summary.get('concentration_clusters', 0)} concentration clusters evaluated."
