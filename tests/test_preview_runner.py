import pytest
from usa_signal_bot.core.enums import SandboxRuntimeMode, SandboxStatus
from usa_signal_bot.release_sandbox.sandbox_models import SandboxRuntimeContext
from usa_signal_bot.release_sandbox.preview_runner import SafePreviewRunner, preview_run_summary

def test_preview_runner():
    ctx = SandboxRuntimeContext(
        context_id="c1", created_at_utc="now", sandbox_id=None, bundle_id=None, bundle_version=None,
        runtime_mode=SandboxRuntimeMode.FULL_SAFE_PREVIEW, in_memory_config={}, mounted_artifacts=[],
        sandbox_output_path=None, allowed_operations=[], denied_operations=[],
        allowed_to_write_production_config=False, allowed_to_mutate_paper_state=False,
        allowed_to_send_orders=False, allowed_to_send_telegram_real=False, warnings=[], errors=[]
    )

    runner = SafePreviewRunner()
    run = runner.run_preview(ctx)

    assert run.status == SandboxStatus.COMPLETED
    assert len(run.outputs) == 4

    output_types = [o.output_type for o in run.outputs]
    assert "SIGNAL_PREVIEW" in output_types
    assert "PORTFOLIO_PREVIEW" in output_types
    assert "RISK_PREVIEW" in output_types
    assert "NOTIFICATION_PREVIEW" in output_types

    s = preview_run_summary(run)
    assert s["outputs_count"] == 4
