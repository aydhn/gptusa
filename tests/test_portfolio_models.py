import pytest
from usa_signal_bot.portfolio_construction.portfolio_models import SectorClusterRecord, PortfolioCandidate, validate_sector_cluster_record
from usa_signal_bot.core.enums import SectorClusterSource

def test_sector_cluster_record_valid():
    rec = SectorClusterRecord("id1", "AAPL", "tech", "hw", "mega", SectorClusterSource.MANUAL_REGISTRY, 100.0)
    assert rec.symbol == "AAPL"

def test_sector_cluster_record_invalid():
    rec = SectorClusterRecord("id1", "", "tech", "hw", "mega", SectorClusterSource.MANUAL_REGISTRY, 100.0)
    with pytest.raises(ValueError):
        validate_sector_cluster_record(rec)
