import pytest
from usa_signal_bot.core.enums import SandboxRuntimeMode
from usa_signal_bot.release_sandbox.sandbox_models import SandboxRuntimeContext, SandboxPreviewOutput
from usa_signal_bot.release_sandbox.notification_preview import (
    build_sandbox_notification_preview, validate_notification_preview_safe, sandbox_notification_preview_to_text
)

def test_notification_preview():
    ctx = SandboxRuntimeContext(
        context_id="c1", created_at_utc="now", sandbox_id=None, bundle_id=None, bundle_version=None,
        runtime_mode=SandboxRuntimeMode.DRY_RUN_PREVIEW, in_memory_config={}, mounted_artifacts=[],
        sandbox_output_path=None, allowed_operations=[], denied_operations=[],
        allowed_to_write_production_config=False, allowed_to_mutate_paper_state=False,
        allowed_to_send_orders=False, allowed_to_send_telegram_real=False, warnings=[], errors=[]
    )

    out = build_sandbox_notification_preview(ctx)
    assert out.output_type == "NOTIFICATION_PREVIEW"
    assert out.payload["channel"] == "DRY_RUN"

    warns = validate_notification_preview_safe(out)
    assert not warns

    out.payload["mock_message"] = "telegram real send"
    warns = validate_notification_preview_safe(out)
    assert len(warns) == 1
    assert "telegram real send" in warns[0].lower()

    txt = sandbox_notification_preview_to_text(out)
    assert "Message length" in txt
