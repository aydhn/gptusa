import pytest
from usa_signal_bot.core.enums import TransactionSide, LiquidityStatus
from usa_signal_bot.transaction_costs.cost_models import (
    TransactionCostInput,
    TransactionCostBreakdown,
    validate_transaction_cost_input,
    create_transaction_cost_input_id
)

def test_transaction_cost_input_valid():
    inp = TransactionCostInput(
        input_id=create_transaction_cost_input_id("SPY"),
        symbol="SPY",
        side=TransactionSide.BUY,
        quantity=10,
        notional_usd=1000,
        price=100,
        avg_dollar_volume=1000000,
        atr_pct=1.5,
        spread_proxy_bps=5.0,
        participation_rate_pct=0.1,
        liquidity_status=LiquidityStatus.GOOD
    )
    validate_transaction_cost_input(inp)

def test_negative_notional_validation():
    inp = TransactionCostInput(
        input_id=create_transaction_cost_input_id("SPY"),
        symbol="SPY",
        side=TransactionSide.BUY,
        quantity=10,
        notional_usd=-1000,
        price=100,
        avg_dollar_volume=1000000,
        atr_pct=1.5,
        spread_proxy_bps=5.0,
        participation_rate_pct=0.1,
        liquidity_status=LiquidityStatus.GOOD
    )
    with pytest.raises(ValueError):
        validate_transaction_cost_input(inp)
