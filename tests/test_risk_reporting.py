from usa_signal_bot.risk.risk_reporting import (
    risk_limit_config_to_text,
    position_sizing_config_to_text,
    risk_decision_to_text,
    risk_run_result_to_text,
    risk_limitations_text
)
from usa_signal_bot.risk.risk_limits import default_risk_limit_config
from usa_signal_bot.risk.position_sizing import default_position_sizing_config
from usa_signal_bot.risk.risk_models import RiskDecision, RiskRunResult
from usa_signal_bot.core.enums import RiskDecisionStatus, SignalAction, PositionSizingMethod, RiskSeverity, RiskRunStatus

def test_risk_reporting_text_gen():
    lcfg = default_risk_limit_config()
    scfg = default_position_sizing_config()

    assert "Max Position Notional" in risk_limit_config_to_text(lcfg)
    assert "FIXED_NOTIONAL" in position_sizing_config_to_text(scfg)

    dec = RiskDecision("d1", "c1", "s1", "AAPL", "strat", "1d", RiskDecisionStatus.APPROVED, SignalAction.LONG, 10, 1000, PositionSizingMethod.FIXED_NOTIONAL, [], [], 10.0, RiskSeverity.INFO, [], "2023-01-01T00:00:00Z")
    dec_text = risk_decision_to_text(dec)
    assert "AAPL" in dec_text
    assert "APPROVED" in dec_text

    run = RiskRunResult("run1", "2023-01-01T00:00:00Z", RiskRunStatus.COMPLETED, 1, 1, 0, 0, 0, [dec], [], [])
    run_text = risk_run_result_to_text(run)
    assert "run1" in run_text
    assert "DISCLAIMER" in run_text
