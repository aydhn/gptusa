from usa_signal_bot.portfolio.portfolio_reporting import (
    allocation_config_to_text, risk_budget_config_to_text,
    concentration_guard_config_to_text, portfolio_candidate_to_text,
    allocation_result_to_text, portfolio_basket_to_text,
    portfolio_construction_result_to_text, allocations_to_text,
    portfolio_limitations_text
)
from usa_signal_bot.portfolio.allocation_methods import default_allocation_config
from usa_signal_bot.portfolio.risk_budgeting import default_risk_budget_config
from usa_signal_bot.portfolio.concentration_guards import default_concentration_guard_config
from usa_signal_bot.portfolio.portfolio_models import PortfolioCandidate, AllocationResult
from usa_signal_bot.core.enums import SignalAction, PortfolioCandidateStatus, AllocationMethod, AllocationStatus

def test_reporting_formats():
    assert "Method:" in allocation_config_to_text(default_allocation_config())
    assert "Max Total Budget:" in risk_budget_config_to_text(default_risk_budget_config())
    assert "Max Symbol Weight:" in concentration_guard_config_to_text(default_concentration_guard_config())

    cand = PortfolioCandidate("1", "AAPL", "1d", SignalAction.LONG, 0, 0, risk_score=20, status=PortfolioCandidateStatus.ELIGIBLE)
    assert "AAPL" in portfolio_candidate_to_text(cand)
    assert "ELIGIBLE" in portfolio_candidate_to_text(cand)

    alloc = AllocationResult("1", "AAPL", "1d", AllocationMethod.EQUAL_WEIGHT, AllocationStatus.ALLOCATED, 0.1, 100, 10, 0.1, 100, False, [], [], [])
    assert "AAPL" in allocation_result_to_text(alloc)
    assert "ALLOCATED" in allocation_result_to_text(alloc)

    assert "LIMITATIONS" in portfolio_limitations_text()
