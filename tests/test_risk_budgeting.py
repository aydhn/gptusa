from usa_signal_bot.portfolio.risk_budgeting import (
    default_risk_budget_config, build_risk_budget_report,
    calculate_weight_by_symbol, calculate_weight_by_strategy,
    calculate_weight_by_timeframe, check_budget_items, risk_budget_report_to_text
)
from usa_signal_bot.portfolio.portfolio_models import AllocationResult
from usa_signal_bot.core.enums import AllocationMethod, AllocationStatus, RiskBudgetType, RiskBudgetStatus

def get_test_allocations():
    return [
        AllocationResult("1", "AAPL", "1d", AllocationMethod.EQUAL_WEIGHT, AllocationStatus.ALLOCATED, 0.4, 4000, 10, 0.4, 4000, False, [], [], [], "S1"),
        AllocationResult("2", "MSFT", "1d", AllocationMethod.EQUAL_WEIGHT, AllocationStatus.ALLOCATED, 0.5, 5000, 10, 0.5, 5000, False, [], [], [], "S2")
    ]

def test_default_config():
    config = default_risk_budget_config()
    assert config.max_total_budget_pct == 0.80

def test_calculate_weights():
    allocs = get_test_allocations()
    assert calculate_weight_by_symbol(allocs)["AAPL"] == 0.4
    assert calculate_weight_by_strategy(allocs)["S1"] == 0.4
    assert calculate_weight_by_timeframe(allocs)["1d"] == 0.9

def test_build_report_breach():
    allocs = get_test_allocations()
    config = default_risk_budget_config()
    config.max_total_budget_pct = 0.50 # Less than 0.9

    report = build_risk_budget_report(allocs, 10000, config)
    assert report.status == RiskBudgetStatus.BREACHED
    assert report.total_allocated_weight == 0.9

    text = risk_budget_report_to_text(report)
    assert "BREACHED" in text

def test_build_report_ok():
    allocs = get_test_allocations()
    config = default_risk_budget_config()
    config.max_total_budget_pct = 1.0
    config.max_symbol_budget_pct = 1.0
    config.max_strategy_budget_pct = 1.0
    config.max_timeframe_budget_pct = 1.0

    report = build_risk_budget_report(allocs, 10000, config)
    assert report.status == RiskBudgetStatus.WITHIN_BUDGET
