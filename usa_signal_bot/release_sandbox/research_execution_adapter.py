from typing import Any, Dict
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewOutput
from usa_signal_bot.release_sandbox.restore_preview_adapter import sandbox_restore_preview_from_bundle

def sandbox_preview_from_research_execution_payload(execution_payload: Dict[str, Any]) -> SandboxPreviewOutput:
    return sandbox_restore_preview_from_bundle(execution_payload)

def attach_sandbox_preview_to_execution_payload(execution_payload: Dict[str, Any], output: SandboxPreviewOutput) -> Dict[str, Any]:
    execution_payload["sandbox_preview"] = output.output_id
    return execution_payload

def research_execution_sandbox_summary(execution_payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"execution_adapted": True}

def research_execution_adapter_to_text(payload: Dict[str, Any]) -> str:
    return "Research Execution Adapter: OK"
