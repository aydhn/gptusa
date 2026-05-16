from usa_signal_bot.allocation.risk_budget import default_risk_budget, modulate_risk_budget
from usa_signal_bot.core.enums import RiskBudgetStatus

def test_default_risk_budget():
    rb = default_risk_budget()
    assert rb.portfolio_risk_budget_pct == 10.0

def test_modulate_risk_budget():
    rb = default_risk_budget()
    mod = modulate_risk_budget(rb, execution_payload={"illiquid": True})
    assert mod.status == RiskBudgetStatus.BLOCKED
    assert mod.per_trade_risk_budget_pct == 0.0
