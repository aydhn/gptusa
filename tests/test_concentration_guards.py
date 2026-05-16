from usa_signal_bot.portfolio_construction.concentration_guards import assess_symbol_concentration
from usa_signal_bot.portfolio_construction.exposure_calculator import calculate_exposure_snapshot

def test_symbol_concentration_clear():
    snap = calculate_exposure_snapshot([{"symbol": "AAPL", "final_notional_usd": 5}], 100)
    res = assess_symbol_concentration(snap, 10.0)
    assert res[0].decision.value == "CLEAR"

def test_symbol_concentration_cap():
    snap = calculate_exposure_snapshot([{"symbol": "AAPL", "final_notional_usd": 15}], 100)
    res = assess_symbol_concentration(snap, 10.0)
    assert res[0].decision.value == "BLOCK"
