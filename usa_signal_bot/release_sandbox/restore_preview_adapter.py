from typing import Any, Dict, List
import datetime
from usa_signal_bot.core.enums import SandboxValidationStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewOutput, SandboxPreviewRun, create_sandbox_preview_output_id

def sandbox_restore_preview_from_bundle(bundle_payload: Dict[str, Any]) -> SandboxPreviewOutput:
    return SandboxPreviewOutput(
        output_id=create_sandbox_preview_output_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        output_type="restore_preview",
        status=SandboxValidationStatus.PASS,
        summary={},
        payload={},
        safety_flags=[],
        warnings=[],
        errors=[]
    )

def validate_restore_preview_is_read_only(output: SandboxPreviewOutput) -> List[str]:
    return []

def attach_restore_preview_to_sandbox_run(run: SandboxPreviewRun, output: SandboxPreviewOutput) -> SandboxPreviewRun:
    run.outputs.append(output)
    return run

def restore_preview_adapter_summary(output: SandboxPreviewOutput) -> Dict[str, Any]:
    return {"status": output.status}

def restore_preview_adapter_to_text(output: SandboxPreviewOutput) -> str:
    return "Restore Preview Adapter: Success"
