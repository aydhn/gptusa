import pytest
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext,
    ShadowPortfolioState,
    ShadowSignal,
    ShadowOrderIntent,
    ShadowFill,
    ShadowLedgerEvent,
    ShadowPnLSnapshot,
    ShadowRehearsalSession,
    validate_shadow_simulation_context,
    validate_shadow_order_intent,
    validate_shadow_fill,
    create_shadow_context_id
)
from usa_signal_bot.core.enums import ShadowRuntimeMode, ShadowOrderIntentStatus, ShadowFillStatus, ShadowLedgerEventType, ShadowSessionStatus
from datetime import datetime, timezone

def test_shadow_simulation_context_valid():
    ctx = ShadowSimulationContext(
        context_id=create_shadow_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        runtime_mode=ShadowRuntimeMode.FULL_PAPER_SHADOW,
        starting_equity_usd=100000.0,
        in_memory_config={},
        allow_real_orders=False,
        allow_broker_calls=False,
        allow_paper_state_mutation=False,
        allow_telegram_real_send=False,
        allow_production_config_write=False,
        warnings=[],
        errors=[]
    )
    validate_shadow_simulation_context(ctx)

def test_shadow_simulation_context_invalid_allow_real_orders():
    ctx = ShadowSimulationContext(
        context_id="test",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        runtime_mode=ShadowRuntimeMode.FULL_PAPER_SHADOW,
        starting_equity_usd=100000.0,
        in_memory_config={},
        allow_real_orders=True,
        allow_broker_calls=False,
        allow_paper_state_mutation=False,
        allow_telegram_real_send=False,
        allow_production_config_write=False,
        warnings=[],
        errors=[]
    )
    with pytest.raises(ValueError, match="allow_real_orders must be False"):
        validate_shadow_simulation_context(ctx)

def test_shadow_order_intent_invalid_real_order():
    intent = ShadowOrderIntent(
        intent_id="test",
        created_at_utc="test",
        symbol="AAPL",
        side="BUY",
        quantity=10,
        notional_usd=1000,
        status=ShadowOrderIntentStatus.DRAFT,
        is_real_order=True,
        warnings=[],
        errors=[]
    )
    with pytest.raises(ValueError, match="is_real_order must be False"):
        validate_shadow_order_intent(intent)

def test_shadow_fill_invalid_real_fill():
    fill = ShadowFill(
        fill_id="test",
        created_at_utc="test",
        intent_id="test",
        symbol="AAPL",
        side="BUY",
        requested_quantity=10,
        filled_quantity=10,
        simulated_cost_usd=1000,
        simulated_slippage_usd=10,
        status=ShadowFillStatus.SIMULATED_FILLED,
        is_real_fill=True,
        warnings=[],
        errors=[]
    )
    with pytest.raises(ValueError, match="is_real_fill must be False"):
        validate_shadow_fill(fill)
