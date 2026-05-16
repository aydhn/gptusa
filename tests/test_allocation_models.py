import pytest
from usa_signal_bot.allocation.allocation_models import CapitalState, RiskBudget, SizingInput, PositionSizeResult, create_capital_state_id, validate_capital_state
from usa_signal_bot.core.enums import CapitalStateSource, RiskBudgetStatus, CapitalAllocationMode, PositionSizeStatus

def test_capital_state_valid():
    cs = CapitalState(
        capital_state_id=create_capital_state_id(),
        created_at_utc="2024-01-01T00:00:00Z",
        source=CapitalStateSource.SIMULATED,
        total_equity_usd=1000.0,
        available_cash_usd=1000.0,
        reserved_cash_usd=0.0,
        open_exposure_usd=0.0,
        max_gross_exposure_usd=1000.0,
        max_net_exposure_usd=1000.0,
        currency="USD",
        warnings=[],
        errors=[]
    )
    validate_capital_state(cs)
    assert cs.total_equity_usd == 1000.0

def test_capital_state_invalid_equity():
    cs = CapitalState(
        capital_state_id=create_capital_state_id(),
        created_at_utc="2024-01-01T00:00:00Z",
        source=CapitalStateSource.SIMULATED,
        total_equity_usd=-1000.0,
        available_cash_usd=1000.0,
        reserved_cash_usd=0.0,
        open_exposure_usd=0.0,
        max_gross_exposure_usd=1000.0,
        max_net_exposure_usd=1000.0,
        currency="USD",
        warnings=[],
        errors=[]
    )
    with pytest.raises(Exception):
        validate_capital_state(cs)
