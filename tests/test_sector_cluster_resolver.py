from usa_signal_bot.portfolio_construction.sector_cluster_resolver import SectorClusterResolver
from usa_signal_bot.portfolio_construction.portfolio_models import SectorClusterRecord
from usa_signal_bot.core.enums import SectorClusterSource

def test_resolver_etf_proxy():
    resolver = SectorClusterResolver([])
    rec = resolver.resolve("SPY")
    assert rec.sector == "broad_market"
    assert rec.source == SectorClusterSource.ETF_PROXY_HEURISTIC

def test_resolver_unknown():
    resolver = SectorClusterResolver([])
    rec = resolver.resolve("UNKNOWN_TICKER")
    assert rec.sector == "unknown_sector"
    assert rec.source == SectorClusterSource.UNKNOWN
