from usa_signal_bot.portfolio.concentration_guards import (
    default_concentration_guard_config, build_concentration_report, apply_concentration_caps,
    concentration_report_to_text
)
from usa_signal_bot.portfolio.portfolio_models import AllocationResult
from usa_signal_bot.core.enums import AllocationMethod, AllocationStatus, PortfolioReviewStatus

def get_test_allocations():
    return [
        AllocationResult("1", "AAPL", "1d", AllocationMethod.EQUAL_WEIGHT, AllocationStatus.ALLOCATED, 0.4, 4000, 10, 0.4, 4000, False, [], [], [], "S1"),
        AllocationResult("2", "MSFT", "1d", AllocationMethod.EQUAL_WEIGHT, AllocationStatus.ALLOCATED, 0.5, 5000, 10, 0.5, 5000, False, [], [], [], "S2")
    ]

def test_default_config():
    config = default_concentration_guard_config()
    assert config.max_symbol_weight == 0.15

def test_build_concentration_report_breach():
    allocs = get_test_allocations()
    config = default_concentration_guard_config()
    config.max_symbol_weight = 0.2

    report = build_concentration_report(allocs, config)
    assert report.review_status == PortfolioReviewStatus.NEEDS_REVIEW
    assert report.breach_count > 0

    text = concentration_report_to_text(report)
    assert "BREACHED" in text

def test_apply_caps():
    allocs = get_test_allocations()
    config = default_concentration_guard_config()
    config.max_single_candidate_weight = 0.2
    config.cap_breaches = True

    capped = apply_concentration_caps(allocs, config)
    assert capped[0].target_weight == 0.2
    assert capped[0].status == AllocationStatus.CAPPED
    assert capped[1].target_weight == 0.2
    assert capped[1].status == AllocationStatus.CAPPED
