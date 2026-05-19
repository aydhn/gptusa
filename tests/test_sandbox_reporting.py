import pytest
from usa_signal_bot.core.enums import SandboxActivationStatus, SandboxRuntimeMode, SandboxStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewRun, SandboxPreviewOutput
from usa_signal_bot.release_sandbox.sandbox_reporting import (
    sandbox_preview_run_to_text, release_sandbox_limitations_text, sandbox_preview_output_to_text
)

def test_sandbox_reporting_text():
    run = SandboxPreviewRun("r1", "now", None, None, None, SandboxRuntimeMode.DRY_RUN_PREVIEW, SandboxStatus.COMPLETED, None, [], [], [], None, None, [], [])

    txt = sandbox_preview_run_to_text(run)
    assert "r1" in txt
    assert "COMPLETED" in txt

    lim = release_sandbox_limitations_text()
    assert "No broker/live/demo orders" in lim
    assert "No Telegram real sends" in lim

    out = SandboxPreviewOutput("o1", "now", "UNKNOWN_TYPE", SandboxActivationStatus.VALIDATED, {}, {}, [], [], [])
    txt2 = sandbox_preview_output_to_text(out)
    assert "UNKNOWN_TYPE" in txt2
