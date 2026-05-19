import datetime
from typing import Any, Dict, List
from usa_signal_bot.core.enums import SandboxValidationStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewOutput, SandboxPreviewRun, create_sandbox_preview_output_id

def sandbox_restore_preview_from_bundle(bundle_payload: Dict[str, Any]) -> SandboxPreviewOutput:
    manifest = bundle_payload.get("manifest", {})
    return SandboxPreviewOutput(
        output_id=create_sandbox_preview_output_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        output_type="RESTORE_PREVIEW",
        status=SandboxValidationStatus.PASS,
        summary={"bundle_id": manifest.get("bundle_id")},
        payload={"note": "Dry run preview of restore operation. No files patched."},
        safety_flags=[],
        warnings=[],
        errors=[]
    )

def validate_restore_preview_is_read_only(output: SandboxPreviewOutput) -> List[str]:
    warnings = []
    payload_str = str(output.payload).lower()
    if "patched" in payload_str and "no files patched" not in payload_str:
         warnings.append("Restore preview seems to imply files were patched.")
    return warnings

def attach_restore_preview_to_sandbox_run(run: SandboxPreviewRun, output: SandboxPreviewOutput) -> SandboxPreviewRun:
    run.outputs.append(output)
    return run

def restore_preview_adapter_summary(output: SandboxPreviewOutput) -> Dict[str, Any]:
    return {
        "output_id": output.output_id,
        "bundle_id": output.summary.get("bundle_id")
    }

def restore_preview_adapter_to_text(output: SandboxPreviewOutput) -> str:
    summary = restore_preview_adapter_summary(output)
    return f"Restore Preview [{summary['output_id']}] for Bundle: {summary['bundle_id']}"
