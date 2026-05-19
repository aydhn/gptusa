import pytest
from usa_signal_bot.core.enums import SandboxRuntimeMode
from usa_signal_bot.release_sandbox.sandbox_models import SandboxRuntimeContext
from usa_signal_bot.release_sandbox.portfolio_preview import (
    build_portfolio_preview, validate_portfolio_preview_safe, portfolio_preview_to_text
)

def test_portfolio_preview():
    ctx = SandboxRuntimeContext(
        context_id="c1", created_at_utc="now", sandbox_id=None, bundle_id=None, bundle_version=None,
        runtime_mode=SandboxRuntimeMode.DRY_RUN_PREVIEW, in_memory_config={}, mounted_artifacts=[],
        sandbox_output_path=None, allowed_operations=[], denied_operations=[],
        allowed_to_write_production_config=False, allowed_to_mutate_paper_state=False,
        allowed_to_send_orders=False, allowed_to_send_telegram_real=False, warnings=[], errors=[]
    )

    out = build_portfolio_preview(ctx)
    assert out.output_type == "PORTFOLIO_PREVIEW"
    assert out.payload["mock_exposures"]["SPY"] == 0.4

    warns = validate_portfolio_preview_safe(out)
    assert not warns

    out.payload["note"] = "portfolio_state_mutated"
    warns = validate_portfolio_preview_safe(out)
    assert len(warns) == 1
    assert "portfolio_state_mutated" in warns[0].lower()

    txt = portfolio_preview_to_text(out)
    assert "mock positions" in txt
