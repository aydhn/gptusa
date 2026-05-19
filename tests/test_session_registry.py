import pytest
from usa_signal_bot.core.enums import SandboxRuntimeMode, SandboxStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewRun
from usa_signal_bot.release_sandbox.session_registry import (
    register_sandbox_preview_run, find_sandbox_run_by_id, find_sandbox_runs_by_bundle_id,
    latest_sandbox_run_for_bundle, sandbox_session_registry_to_text
)

def test_session_registry():
    run1 = SandboxPreviewRun("r1", "now", None, "b1", None, SandboxRuntimeMode.DRY_RUN_PREVIEW, SandboxStatus.COMPLETED, None, [], [], [], None, None, [], [])
    run2 = SandboxPreviewRun("r2", "now", None, "b1", None, SandboxRuntimeMode.DRY_RUN_PREVIEW, SandboxStatus.COMPLETED, None, [], [], [], None, None, [], [])

    registry = register_sandbox_preview_run(run1)
    assert len(registry) == 1

    registry = register_sandbox_preview_run(run2, registry)
    assert len(registry) == 2

    found = find_sandbox_run_by_id(registry, "r1")
    assert found.run_id == "r1"

    runs = find_sandbox_runs_by_bundle_id(registry, "b1")
    assert len(runs) == 2

    latest = latest_sandbox_run_for_bundle(registry, "b1")
    assert latest.run_id == "r2"

    txt = sandbox_session_registry_to_text(registry)
    assert "2 runs registered" in txt
