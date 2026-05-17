import pytest
from usa_signal_bot.core.exceptions import DataValidationError
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    PortfolioPosition, CurrentPortfolioState, TargetPortfolioState,
    DriftMeasurement, RebalanceAction, TurnoverAssessment, RebalancePlan,
    RebalanceReview, validate_portfolio_position, validate_current_portfolio_state,
    validate_target_portfolio_state, validate_drift_measurement,
    validate_rebalance_action, validate_turnover_assessment,
    validate_rebalance_plan, create_portfolio_position_id,
    portfolio_position_to_dict
)
from usa_signal_bot.core.enums import (
    RebalanceMode, RebalanceActionType, RebalanceStatus, DriftType,
    DriftSeverity, TurnoverStatus, RebalanceReportType
)

def test_portfolio_position_valid():
    pos = PortfolioPosition(
        position_id="pos_1", symbol="AAPL", quantity=10.0, market_value_usd=1500.0
    )
    validate_portfolio_position(pos)
    assert pos.symbol == "AAPL"

def test_portfolio_position_invalid_quantity():
    pos = PortfolioPosition(
        position_id="pos_1", symbol="AAPL", quantity=-10.0, market_value_usd=1500.0
    )
    with pytest.raises(DataValidationError, match="quantity cannot be negative"):
        validate_portfolio_position(pos)

def test_portfolio_position_invalid_value():
    pos = PortfolioPosition(
        position_id="pos_1", symbol="AAPL", quantity=10.0, market_value_usd=-1500.0
    )
    with pytest.raises(DataValidationError, match="market_value_usd cannot be negative"):
        validate_portfolio_position(pos)

def test_rebalance_action_invalid_turnover():
    action = RebalanceAction(
        action_id="act_1", symbol="AAPL", action_type=RebalanceActionType.INCREASE,
        status=RebalanceStatus.PROPOSED, estimated_turnover_usd=-100.0
    )
    with pytest.raises(DataValidationError, match="estimated_turnover_usd cannot be negative"):
        validate_rebalance_action(action)

def test_serialization():
    pos = PortfolioPosition(
        position_id="pos_1", symbol="AAPL", quantity=10.0, market_value_usd=1500.0
    )
    d = portfolio_position_to_dict(pos)
    assert d["symbol"] == "AAPL"
    assert d["quantity"] == 10.0

def test_id_creation():
    id_val = create_portfolio_position_id("MSFT")
    assert id_val.startswith("pos_MSFT_")
