import pytest
from usa_signal_bot.core.enums import ExposureLimitType, RiskSeverity, SignalAction, PositionSizingMethod
from usa_signal_bot.core.exceptions import RiskLimitError, PositionSizingError
from usa_signal_bot.risk.risk_models import (
    RiskLimit,
    PositionSizingRequest,
    PositionSizingResult,
    RiskDecision,
    RiskRunResult,
    validate_risk_limit,
    validate_position_sizing_request,
    validate_position_sizing_result,
    create_risk_decision_id,
    create_risk_run_id,
    risk_decision_to_dict,
    risk_run_result_to_dict
)
from usa_signal_bot.core.enums import RiskCheckStatus, RiskDecisionStatus, RiskRunStatus

def test_risk_limit_valid():
    limit = RiskLimit("test", ExposureLimitType.PORTFOLIO, 0.5)
    validate_risk_limit(limit)
    assert limit.name == "test"
    assert limit.value == 0.5

def test_risk_limit_invalid():
    limit = RiskLimit("", ExposureLimitType.PORTFOLIO, 0.5)
    with pytest.raises(RiskLimitError):
        validate_risk_limit(limit)

    limit = RiskLimit("test", ExposureLimitType.PORTFOLIO, -0.5)
    with pytest.raises(RiskLimitError):
        validate_risk_limit(limit)

def test_position_sizing_request_valid():
    req = PositionSizingRequest("cand1", "AAPL", "strat1", "1d", SignalAction.LONG, 0.8, 80.0, 150.0, 100000.0, 100000.0)
    validate_position_sizing_request(req)
    assert req.price == 150.0

def test_position_sizing_request_invalid():
    req = PositionSizingRequest("cand1", "AAPL", "strat1", "1d", SignalAction.LONG, 0.8, 80.0, -150.0, 100000.0, 100000.0)
    with pytest.raises(PositionSizingError):
        validate_position_sizing_request(req)

def test_position_sizing_result_serialize():
    res = PositionSizingResult("cand1", PositionSizingMethod.FIXED_NOTIONAL, 10.0, 1500.0, 10.0, 1500.0, False, [], [], [])
    validate_position_sizing_result(res)
    assert res.approved_quantity == 10.0

def test_decision_and_run_serialize():
    dec = RiskDecision("dec1", "cand1", "sig1", "AAPL", "strat", "1d", RiskDecisionStatus.APPROVED, SignalAction.LONG, 10, 1500, PositionSizingMethod.FIXED_NOTIONAL, [], [], 10.0, RiskSeverity.INFO, [], "2023-01-01T00:00:00Z")
    dec_dict = risk_decision_to_dict(dec)
    assert dec_dict["decision_id"] == "dec1"

    run = RiskRunResult("run1", "2023-01-01T00:00:00Z", RiskRunStatus.COMPLETED, 1, 1, 0, 0, 0, [dec], [], [])
    run_dict = risk_run_result_to_dict(run)
    assert run_dict["run_id"] == "run1"

def test_id_generation():
    dec_id = create_risk_decision_id("cand12345678", "AAPL")
    assert dec_id.startswith("dec_AAPL_")

    run_id = create_risk_run_id()
    assert run_id.startswith("risk_")
