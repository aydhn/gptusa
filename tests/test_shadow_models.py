import pytest
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext, ShadowPortfolioState, ShadowSignal,
    ShadowOrderIntent, ShadowFill, ShadowLedgerEvent, ShadowPnLSnapshot,
    ShadowRehearsalSession, create_shadow_context_id
)
from usa_signal_bot.core.enums import ShadowRuntimeMode

def test_shadow_simulation_context_valid():
    ctx = ShadowSimulationContext(
        context_id=create_shadow_context_id(),
        created_at_utc="2023-01-01T00:00:00Z",
        source_sandbox_id=None,
        source_bundle_id=None,
        source_bundle_version=None,
        runtime_mode=ShadowRuntimeMode.FULL_PAPER_SHADOW,
        starting_equity_usd=100000.0,
        in_memory_config={},
        isolated_output_path=None,
        allow_real_orders=False,
        allow_broker_calls=False,
        allow_paper_state_mutation=False,
        allow_telegram_real_send=False,
        allow_production_config_write=False,
        warnings=[],
        errors=[]
    )
    assert ctx.starting_equity_usd == 100000.0
    assert not ctx.allow_real_orders
