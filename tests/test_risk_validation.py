from usa_signal_bot.risk.risk_validation import (
    validate_risk_decision,
    validate_risk_run_result,
    validate_exposure_snapshot,
    validate_position_sizing_result_for_decision
)
from usa_signal_bot.risk.risk_models import RiskDecision, RiskRunResult
from usa_signal_bot.core.enums import RiskDecisionStatus, SignalAction, PositionSizingMethod, RiskSeverity, RiskRunStatus
from usa_signal_bot.risk.exposure_guard import create_empty_exposure_snapshot

def test_validate_risk_decision():
    dec = RiskDecision("d1", "c1", "s1", "AAPL", "strat", "1d", RiskDecisionStatus.REJECTED, SignalAction.LONG, 10, 1000, PositionSizingMethod.FIXED_NOTIONAL, [], [], 10.0, RiskSeverity.INFO, [], "2023-01-01T00:00:00Z")
    rep = validate_risk_decision(dec)
    assert not rep.valid
    assert any("Rejected decision has >0 approved quantity" in e for e in rep.errors)

def test_validate_risk_run_result():
    dec = RiskDecision("d1", "c1", "s1", "AAPL", "strat", "1d", RiskDecisionStatus.APPROVED, SignalAction.LONG, 10, 1000, PositionSizingMethod.FIXED_NOTIONAL, [], [], 10.0, RiskSeverity.INFO, [], "2023-01-01T00:00:00Z")
    run = RiskRunResult("r1", "2023-01-01T00:00:00Z", RiskRunStatus.COMPLETED, 1, 0, 0, 0, 0, [dec], [], [])
    rep = validate_risk_run_result(run)
    assert not rep.valid
    assert any("Mismatch in approved count" in e for e in rep.errors)

def test_validate_exposure_snapshot():
    snap = create_empty_exposure_snapshot(-10000.0, -5000.0)
    rep = validate_exposure_snapshot(snap)
    assert not rep.valid
    assert rep.error_count == 2
