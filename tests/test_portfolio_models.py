import pytest
from usa_signal_bot.portfolio_construction.portfolio_models import (
    SectorClusterRecord,
    PortfolioCandidate,
    validate_sector_cluster_record,
)
from usa_signal_bot.core.enums import SectorClusterSource


def test_sector_cluster_record_valid():
    rec = SectorClusterRecord(
        "id1", "AAPL", "tech", "hw", "mega", SectorClusterSource.MANUAL_REGISTRY, 100.0
    )
    assert rec.symbol == "AAPL"


def test_sector_cluster_record_invalid():
    rec = SectorClusterRecord(
        "id1", "", "tech", "hw", "mega", SectorClusterSource.MANUAL_REGISTRY, 100.0
    )
    with pytest.raises(ValueError):
        validate_sector_cluster_record(rec)


def test_validate_portfolio_candidate():
    from usa_signal_bot.portfolio.portfolio_models import (
        PortfolioCandidate,
        validate_portfolio_candidate,
    )
    from usa_signal_bot.core.exceptions import PortfolioCandidateError

    class DummyEnum:
        def __init__(self, value):
            self.value = value

    action_long = DummyEnum("LONG")

    # Happy path
    valid_candidate = PortfolioCandidate(
        candidate_id="c1",
        symbol="AAPL",
        timeframe="1d",
        action=action_long,
        approved_quantity=10,
        approved_notional=1500,
        rank_score=50,
        confidence=0.5,
        risk_score=50,
    )
    validate_portfolio_candidate(valid_candidate)  # Should not raise

    # Empty candidate_id
    with pytest.raises(PortfolioCandidateError, match="candidate_id is empty."):
        c = PortfolioCandidate(
            candidate_id="",
            symbol="AAPL",
            timeframe="1d",
            action=action_long,
            approved_quantity=10,
            approved_notional=1500,
        )
        validate_portfolio_candidate(c)

    # Empty symbol
    with pytest.raises(PortfolioCandidateError, match="symbol is empty."):
        c = PortfolioCandidate(
            candidate_id="c1",
            symbol="",
            timeframe="1d",
            action=action_long,
            approved_quantity=10,
            approved_notional=1500,
        )
        validate_portfolio_candidate(c)

    # Empty timeframe
    with pytest.raises(PortfolioCandidateError, match="timeframe is empty."):
        c = PortfolioCandidate(
            candidate_id="c1",
            symbol="AAPL",
            timeframe="",
            action=action_long,
            approved_quantity=10,
            approved_notional=1500,
        )
        validate_portfolio_candidate(c)

    # Negative approved_quantity
    with pytest.raises(
        PortfolioCandidateError, match="approved_quantity cannot be negative."
    ):
        c = PortfolioCandidate(
            candidate_id="c1",
            symbol="AAPL",
            timeframe="1d",
            action=action_long,
            approved_quantity=-10,
            approved_notional=1500,
        )
        validate_portfolio_candidate(c)

    # Negative approved_notional
    with pytest.raises(
        PortfolioCandidateError, match="approved_notional cannot be negative."
    ):
        c = PortfolioCandidate(
            candidate_id="c1",
            symbol="AAPL",
            timeframe="1d",
            action=action_long,
            approved_quantity=10,
            approved_notional=-1500,
        )
        validate_portfolio_candidate(c)

    # Invalid rank_score
    with pytest.raises(
        PortfolioCandidateError, match="rank_score must be between 0 and 100."
    ):
        c = PortfolioCandidate(
            candidate_id="c1",
            symbol="AAPL",
            timeframe="1d",
            action=action_long,
            approved_quantity=10,
            approved_notional=1500,
            rank_score=-1,
        )
        validate_portfolio_candidate(c)

    with pytest.raises(
        PortfolioCandidateError, match="rank_score must be between 0 and 100."
    ):
        c = PortfolioCandidate(
            candidate_id="c1",
            symbol="AAPL",
            timeframe="1d",
            action=action_long,
            approved_quantity=10,
            approved_notional=1500,
            rank_score=101,
        )
        validate_portfolio_candidate(c)

    # Invalid confidence
    with pytest.raises(
        PortfolioCandidateError, match="confidence must be between 0 and 1."
    ):
        c = PortfolioCandidate(
            candidate_id="c1",
            symbol="AAPL",
            timeframe="1d",
            action=action_long,
            approved_quantity=10,
            approved_notional=1500,
            confidence=-0.1,
        )
        validate_portfolio_candidate(c)

    with pytest.raises(
        PortfolioCandidateError, match="confidence must be between 0 and 1."
    ):
        c = PortfolioCandidate(
            candidate_id="c1",
            symbol="AAPL",
            timeframe="1d",
            action=action_long,
            approved_quantity=10,
            approved_notional=1500,
            confidence=1.1,
        )
        validate_portfolio_candidate(c)

    # Invalid risk_score
    with pytest.raises(
        PortfolioCandidateError, match="risk_score must be between 0 and 100."
    ):
        c = PortfolioCandidate(
            candidate_id="c1",
            symbol="AAPL",
            timeframe="1d",
            action=action_long,
            approved_quantity=10,
            approved_notional=1500,
            risk_score=-1,
        )
        validate_portfolio_candidate(c)

    with pytest.raises(
        PortfolioCandidateError, match="risk_score must be between 0 and 100."
    ):
        c = PortfolioCandidate(
            candidate_id="c1",
            symbol="AAPL",
            timeframe="1d",
            action=action_long,
            approved_quantity=10,
            approved_notional=1500,
            risk_score=101,
        )
        validate_portfolio_candidate(c)
