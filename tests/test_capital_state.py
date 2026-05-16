from usa_signal_bot.allocation.capital_state import default_capital_state, available_risk_capital_usd
from usa_signal_bot.allocation.risk_budget import default_risk_budget

def test_default_capital_state():
    cs = default_capital_state()
    assert cs.total_equity_usd == 100000.0
    assert cs.available_cash_usd == 100000.0

def test_available_risk_capital():
    cs = default_capital_state(1000.0)
    rb = default_risk_budget()
    # 10% portfolio risk budget by default
    assert available_risk_capital_usd(cs, rb) == 100.0
