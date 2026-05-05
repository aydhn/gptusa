from usa_signal_bot.risk.candidate_risk import (
    CandidateRiskInput,
    infer_price_from_feature_snapshot,
    infer_volatility_from_feature_snapshot,
    infer_atr_from_feature_snapshot,
    validate_candidate_risk_input,
    build_position_sizing_request
)
from usa_signal_bot.core.enums import SignalAction, RiskCheckStatus
from usa_signal_bot.risk.exposure_guard import create_empty_exposure_snapshot

def test_infer_price():
    assert infer_price_from_feature_snapshot({"close": 150.0}) == 150.0
    assert infer_price_from_feature_snapshot({"price": "100.5"}) == 100.5
    assert infer_price_from_feature_snapshot({}) is None

def test_infer_volatility():
    assert infer_volatility_from_feature_snapshot({"rolling_volatility": 0.05}) == 0.05
    assert infer_volatility_from_feature_snapshot({"normalized_atr": 0.02}) == 0.02

def test_infer_atr():
    assert infer_atr_from_feature_snapshot({"atr": 5.0}) == 5.0
    assert infer_atr_from_feature_snapshot({"average_true_range": 2.5}) == 2.5

def test_validate_candidate_risk_input():
    cand = CandidateRiskInput("c1", "s1", "AAPL", "1d", "strat", SignalAction.LONG, 0.8, 80.0, None, {}, [])
    checks = validate_candidate_risk_input(cand)
    assert any(c.check_name == "missing_price" and c.status == RiskCheckStatus.FAILED for c in checks)

    cand_short = CandidateRiskInput("c2", "s2", "AAPL", "1d", "strat", SignalAction.SHORT, 0.8, 80.0, 100.0, {}, [])
    checks_short = validate_candidate_risk_input(cand_short)
    assert any(c.check_name == "short_action_default_check" and c.status == RiskCheckStatus.WARNING for c in checks_short)

def test_build_position_sizing_request():
    cand = CandidateRiskInput("c1", "s1", "AAPL", "1d", "strat", SignalAction.LONG, 0.8, 80.0, 150.0, {"atr": 5.0}, [])
    snap = create_empty_exposure_snapshot(100000.0, 50000.0)
    req = build_position_sizing_request(cand, snap)
    assert req.price == 150.0
    assert req.portfolio_equity == 100000.0
    assert req.atr_value == 5.0
