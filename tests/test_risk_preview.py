import pytest
from usa_signal_bot.core.enums import SandboxRuntimeMode
from usa_signal_bot.release_sandbox.sandbox_models import SandboxRuntimeContext
from usa_signal_bot.release_sandbox.risk_preview import (
    build_risk_preview, validate_risk_preview_safe, risk_preview_to_text
)

def test_risk_preview():
    ctx = SandboxRuntimeContext(
        context_id="c1", created_at_utc="now", sandbox_id=None, bundle_id=None, bundle_version=None,
        runtime_mode=SandboxRuntimeMode.DRY_RUN_PREVIEW, in_memory_config={}, mounted_artifacts=[],
        sandbox_output_path=None, allowed_operations=[], denied_operations=[],
        allowed_to_write_production_config=False, allowed_to_mutate_paper_state=False,
        allowed_to_send_orders=False, allowed_to_send_telegram_real=False, warnings=[], errors=[]
    )

    out = build_risk_preview(ctx)
    assert out.output_type == "RISK_PREVIEW"
    assert out.payload["mock_drawdown"] == 0.05

    warns = validate_risk_preview_safe(out)
    assert not warns

    out.payload["note"] = "kesin kâr"
    warns = validate_risk_preview_safe(out)
    assert len(warns) == 1
    assert "kesin kâr" in warns[0].lower()

    txt = risk_preview_to_text(out)
    assert "concentration clusters" in txt
