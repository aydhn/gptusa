from usa_signal_bot.risk.exposure_guard import (
    create_empty_exposure_snapshot,
    evaluate_exposure_for_candidate,
    update_exposure_snapshot_with_decision
)
from usa_signal_bot.risk.risk_models import PositionSizingRequest, PositionSizingResult, RiskDecision
from usa_signal_bot.risk.risk_limits import default_risk_limit_config
from usa_signal_bot.core.enums import SignalAction, PositionSizingMethod, RiskDecisionStatus, RiskSeverity

def test_create_empty_snapshot():
    snap = create_empty_exposure_snapshot(100000.0, 50000.0)
    assert snap.portfolio_equity == 100000.0
    assert snap.available_cash == 50000.0
    assert snap.total_exposure == 0.0

def test_evaluate_exposure_for_candidate():
    snap = create_empty_exposure_snapshot(100000.0, 100000.0)
    req = PositionSizingRequest("cand1", "AAPL", "strat1", "1d", SignalAction.LONG, 0.8, 80.0, 100.0, 100000.0, 100000.0)
    sz = PositionSizingResult("cand1", PositionSizingMethod.FIXED_NOTIONAL, 10, 1000, 10, 1000, False, [], [], [])

    cfg = default_risk_limit_config()
    cfg.max_symbol_exposure_pct = 0.05 # 5k limit

    res = evaluate_exposure_for_candidate(req, sz, snap, cfg)
    assert res.approved == True

    sz2 = PositionSizingResult("cand1", PositionSizingMethod.FIXED_NOTIONAL, 100, 10000, 100, 10000, False, [], [], [])
    res2 = evaluate_exposure_for_candidate(req, sz2, snap, cfg)
    assert res2.approved == False
    assert any(c.check_name == "symbol_exposure" for c in res2.checks)

def test_update_exposure_snapshot():
    snap = create_empty_exposure_snapshot(100000.0, 100000.0)
    dec = RiskDecision("dec1", "cand1", "sig1", "AAPL", "strat1", "1d", RiskDecisionStatus.APPROVED, SignalAction.LONG, 10, 1000, PositionSizingMethod.FIXED_NOTIONAL, [], [], 10.0, RiskSeverity.INFO, [], "2023-01-01T00:00:00Z")

    new_snap = update_exposure_snapshot_with_decision(snap, dec)
    assert new_snap.total_exposure == 1000.0
    assert new_snap.available_cash == 99000.0
    assert new_snap.exposure_by_symbol["AAPL"] == 1000.0
    assert new_snap.open_positions == 1
