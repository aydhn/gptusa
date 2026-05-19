import datetime
from typing import Any, Dict, List
from usa_signal_bot.core.enums import SandboxValidationStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewOutput, SandboxRuntimeContext, create_sandbox_preview_output_id

def sample_signal_preview_payload(context: SandboxRuntimeContext) -> Dict[str, Any]:
    return {
        "symbols": ["SPY", "AAPL"],
        "mock_signals": {
            "SPY": {"direction": "BUY", "confidence": 0.8},
            "AAPL": {"direction": "NEUTRAL", "confidence": 0.0}
        },
        "note": "Dry-run local candidate signals only. Not an order."
    }

def build_signal_preview(context: SandboxRuntimeContext) -> SandboxPreviewOutput:
    payload = sample_signal_preview_payload(context)
    return SandboxPreviewOutput(
        output_id=create_sandbox_preview_output_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        output_type="SIGNAL_PREVIEW",
        status=SandboxValidationStatus.PASS,
        summary={"symbols_evaluated": 2},
        payload=payload,
        safety_flags=[],
        warnings=[],
        errors=[]
    )

def validate_signal_preview_safe(output: SandboxPreviewOutput) -> List[str]:
    warnings = []
    payload_str = str(output.payload).lower()
    unsafe_terms = ["kesin al", "kesin sat", "sent to broker", "broker_order_id"]
    for term in unsafe_terms:
        if term in payload_str:
            warnings.append(f"Unsafe term detected in signal preview: {term}")
    return warnings

def signal_preview_to_text(output: SandboxPreviewOutput) -> str:
    summary = output.summary
    return f"Signal Preview [{output.output_id}]: {summary.get('symbols_evaluated', 0)} symbols evaluated."
