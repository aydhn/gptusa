import datetime
from typing import Any, Dict, List
from usa_signal_bot.core.enums import SandboxValidationStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewOutput, SandboxRuntimeContext, create_sandbox_preview_output_id

def sample_portfolio_preview_payload(context: SandboxRuntimeContext) -> Dict[str, Any]:
    return {
        "mock_exposures": {"SPY": 0.4, "AAPL": 0.2},
        "cash_weight": 0.4,
        "note": "Mock exposures for local research. No paper state mutated. No order routing."
    }

def build_portfolio_preview(context: SandboxRuntimeContext) -> SandboxPreviewOutput:
    payload = sample_portfolio_preview_payload(context)
    return SandboxPreviewOutput(
        output_id=create_sandbox_preview_output_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        output_type="PORTFOLIO_PREVIEW",
        status=SandboxValidationStatus.PASS,
        summary={"mock_positions": len(payload.get("mock_exposures", {}))},
        payload=payload,
        safety_flags=[],
        warnings=[],
        errors=[]
    )

def validate_portfolio_preview_safe(output: SandboxPreviewOutput) -> List[str]:
    warnings = []
    payload_str = str(output.payload).lower()
    unsafe_terms = ["paper_state_committed", "portfolio_state_mutated", "real_fill_id", "execution_venue"]
    for term in unsafe_terms:
        if term in payload_str:
            warnings.append(f"Unsafe term detected in portfolio preview: {term}")
    return warnings

def portfolio_preview_to_text(output: SandboxPreviewOutput) -> str:
    summary = output.summary
    return f"Portfolio Preview [{output.output_id}]: {summary.get('mock_positions', 0)} mock positions."
