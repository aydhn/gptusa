from usa_signal_bot.portfolio_construction.exposure_limits import check_gross_exposure_limit
from usa_signal_bot.portfolio_construction.exposure_calculator import calculate_exposure_snapshot

def test_gross_limit_clear():
    snap = calculate_exposure_snapshot([{"final_notional_usd": 50}], 100)
    res = check_gross_exposure_limit(snap, 100.0)
    assert res.decision.value == "CLEAR"

def test_gross_limit_block():
    snap = calculate_exposure_snapshot([{"final_notional_usd": 150}], 100)
    res = check_gross_exposure_limit(snap, 100.0)
    assert res.decision.value == "BLOCK"
