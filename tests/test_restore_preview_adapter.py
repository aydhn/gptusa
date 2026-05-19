import pytest
from usa_signal_bot.core.enums import SandboxRuntimeMode, SandboxStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewRun
from usa_signal_bot.release_sandbox.restore_preview_adapter import (
    sandbox_restore_preview_from_bundle, validate_restore_preview_is_read_only,
    attach_restore_preview_to_sandbox_run, restore_preview_adapter_to_text
)

def test_restore_preview_adapter():
    bundle_payload = {"manifest": {"bundle_id": "b1"}}
    out = sandbox_restore_preview_from_bundle(bundle_payload)

    assert out.output_type == "RESTORE_PREVIEW"
    assert out.summary["bundle_id"] == "b1"

    warns = validate_restore_preview_is_read_only(out)
    assert not warns

    out.payload["note"] = "files were patched"
    warns = validate_restore_preview_is_read_only(out)
    assert len(warns) == 1

    run = SandboxPreviewRun("r1", "now", None, None, None, SandboxRuntimeMode.DRY_RUN_PREVIEW, SandboxStatus.COMPLETED, None, [], [], [], None, None, [], [])
    run = attach_restore_preview_to_sandbox_run(run, out)
    assert len(run.outputs) == 1

    txt = restore_preview_adapter_to_text(out)
    assert "Restore Preview" in txt
