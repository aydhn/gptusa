from usa_signal_bot.portfolio.portfolio_candidates import (
    portfolio_candidate_from_risk_decision,
    portfolio_candidate_from_selected_candidate,
    filter_eligible_portfolio_candidates,
    reject_ineligible_portfolio_candidates,
    sort_candidates_for_allocation
)
from usa_signal_bot.core.enums import RiskDecisionStatus, SignalAction, PortfolioCandidateStatus
from usa_signal_bot.risk.risk_models import RiskDecision
from usa_signal_bot.strategies.candidate_selection import SelectedCandidate
from usa_signal_bot.portfolio.portfolio_models import PortfolioCandidate

def test_portfolio_candidate_from_risk_decision():
    from usa_signal_bot.core.enums import PositionSizingMethod, RiskSeverity
    decision = RiskDecision("d1", "c1", "sig1", "AAPL", "Strat1", "1d", RiskDecisionStatus.APPROVED, SignalAction.LONG, 10.0, 1500.0, PositionSizingMethod.FIXED_NOTIONAL, [], [], 50.0, RiskSeverity.LOW, [], "utc")
    decision.price = 150.0
    decision.rank_score = 90
    decision.strategy_name = "Strategy1"
    cand = portfolio_candidate_from_risk_decision(decision)

    assert cand.candidate_id == "d1"
    assert cand.symbol == "AAPL"
    assert cand.status == PortfolioCandidateStatus.ELIGIBLE
    assert cand.approved_quantity == 10
    assert cand.price == 150.0
    assert cand.rank_score == 90

def test_portfolio_candidate_from_selected_candidate():

    from usa_signal_bot.strategies.signal_ranking import RankedSignal
    from usa_signal_bot.strategies.signal_contract import StrategySignal
    from usa_signal_bot.core.enums import CandidateSelectionStatus
    sig = StrategySignal("sig1", "Strat1", "AAPL", "1d", SignalAction.LONG, 150.0, 100.0, 0.8, [], "utc", {}, [])
    rs = RankedSignal(sig, 80.0, 1, CandidateSelectionStatus.SELECTED, {}, {"RISK_PENALTY": 50.0}, {}, [], "utc")
    sel = SelectedCandidate("s1", rs, CandidateSelectionStatus.SELECTED, None, 1, [], "utc")

    cand = portfolio_candidate_from_selected_candidate(sel, default_price=100.0)

    assert cand.symbol == "AAPL"
    assert cand.status == PortfolioCandidateStatus.ELIGIBLE
    assert cand.price == 100.0
    assert cand.approved_quantity == 0

def test_filter_eligible():
    candidates = [
        PortfolioCandidate("1", "AAPL", "1d", SignalAction.LONG, 0, 0, status=PortfolioCandidateStatus.ELIGIBLE),
        PortfolioCandidate("2", "MSFT", "1d", SignalAction.LONG, 0, 0, status=PortfolioCandidateStatus.REJECTED)
    ]
    el = filter_eligible_portfolio_candidates(candidates)
    assert len(el) == 1
    assert el[0].symbol == "AAPL"

def test_sort_candidates():
    candidates = [
        PortfolioCandidate("1", "AAPL", "1d", SignalAction.LONG, 0, 0, rank_score=50, risk_score=20, confidence=0.8),
        PortfolioCandidate("2", "MSFT", "1d", SignalAction.LONG, 0, 0, rank_score=90, risk_score=50, confidence=0.9),
        PortfolioCandidate("3", "NVDA", "1d", SignalAction.LONG, 0, 0, rank_score=90, risk_score=10, confidence=0.9)
    ]
    sorted_cands = sort_candidates_for_allocation(candidates)
    assert sorted_cands[0].symbol == "NVDA"
    assert sorted_cands[1].symbol == "MSFT"
    assert sorted_cands[2].symbol == "AAPL"
