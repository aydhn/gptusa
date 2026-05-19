import datetime
from typing import Any, Dict
from usa_signal_bot.core.enums import SandboxValidationStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewOutput, create_sandbox_preview_output_id

def sandbox_preview_from_research_execution_payload(execution_payload: Dict[str, Any]) -> SandboxPreviewOutput:
    return SandboxPreviewOutput(
        output_id=create_sandbox_preview_output_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        output_type="RESEARCH_EXECUTION_PREVIEW",
        status=SandboxValidationStatus.PASS,
        summary={"execution_id": execution_payload.get("execution_id", "unknown")},
        payload={"note": "Dry run preview of research execution. No real backtest run."},
        safety_flags=[],
        warnings=[],
        errors=[]
    )

def attach_sandbox_preview_to_execution_payload(execution_payload: Dict[str, Any], output: SandboxPreviewOutput) -> Dict[str, Any]:
    execution_payload["sandbox_preview_id"] = output.output_id
    return execution_payload

def research_execution_sandbox_summary(execution_payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "has_sandbox_preview": "sandbox_preview_id" in execution_payload
    }

def research_execution_adapter_to_text(payload: Dict[str, Any]) -> str:
    summary = research_execution_sandbox_summary(payload)
    return f"Research Execution Adapter: Has Sandbox Preview = {summary['has_sandbox_preview']}"
