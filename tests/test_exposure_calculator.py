from usa_signal_bot.portfolio_construction.exposure_calculator import calculate_exposure_snapshot
from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioAllocation

def test_calculate_exposure():
    allocs = [
        PortfolioAllocation("1", "AAPL", "T", "LONG", 100, 100, 1, 10, "APPROVED", [], [], [], []),
        PortfolioAllocation("2", "TSLA", "T", "SHORT", 50, 50, 1, 5, "APPROVED", [], [], [], [])
    ]
    snap = calculate_exposure_snapshot(allocs, 1000)
    assert snap.gross_exposure_usd == 150
    assert snap.long_exposure_usd == 100
    assert snap.short_exposure_usd == -50
    assert snap.net_exposure_usd == 50
