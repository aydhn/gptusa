import pytest
from usa_signal_bot.portfolio_construction.portfolio_models import PortfolioConstructionPlan, PortfolioAllocation, ExposureSnapshot, ConcentrationAssessment
from usa_signal_bot.portfolio_construction.conflict_resolver import detect_symbol_overlap_conflicts, resolve_portfolio_conflicts
from usa_signal_bot.core.enums import PortfolioConstructionMode, PortfolioAllocationStatus

def test_conflict_symbol_overlap():
    plan = PortfolioConstructionPlan("p1", "time", PortfolioConstructionMode.HYBRID, [], [
        PortfolioAllocation("a1", "AAPL", None, "LONG", 100, 100, 1, 10.0, PortfolioAllocationStatus.APPROVED, [], [], [], []),
        PortfolioAllocation("a2", "AAPL", None, "SHORT", 50, 50, 1, 5.0, PortfolioAllocationStatus.APPROVED, [], [], [], [])
    ], None, [], [], 0, 0, 0, 0, 0, 0, [], [], {})

    conflicts = detect_symbol_overlap_conflicts(plan)
    assert len(conflicts) == 1
    assert conflicts[0]["type"] == "SIDE_CONFLICT"

def test_resolve_conflicts():
    plan = PortfolioConstructionPlan("p1", "time", PortfolioConstructionMode.HYBRID, [], [
        PortfolioAllocation("a1", "AAPL", None, "LONG", 100, 100, 1, 10.0, PortfolioAllocationStatus.APPROVED, [], [], [], []),
        PortfolioAllocation("a2", "AAPL", None, "SHORT", 50, 50, 1, 5.0, PortfolioAllocationStatus.APPROVED, [], [], [], [])
    ], None, [], [], 0, 0, 0, 0, 0, 0, [], [], {})

    plan = resolve_portfolio_conflicts(plan)
    assert len(plan.conflicts) == 1

    aapl_allocs = [a for a in plan.allocations if a.symbol == "AAPL"]
    long_alloc = next(a for a in aapl_allocs if a.side == "LONG")
    short_alloc = next(a for a in aapl_allocs if a.side == "SHORT")

    assert long_alloc.status == PortfolioAllocationStatus.APPROVED
    assert short_alloc.status == PortfolioAllocationStatus.SUPPRESSED

def test_storage(tmp_path):
    from usa_signal_bot.portfolio_construction.construction_store import write_portfolio_construction_plan_json
    plan = PortfolioConstructionPlan("p1", "time", PortfolioConstructionMode.HYBRID, [], [], None, [], [], 0, 0, 0, 0, 0, 0, [], [], {})
    p = tmp_path / "plan.json"
    write_portfolio_construction_plan_json(p, plan)
    assert p.exists()

def test_validation():
    from usa_signal_bot.portfolio_construction.construction_validation import validate_no_live_execution_language_in_portfolio
    res = validate_no_live_execution_language_in_portfolio("This is live approved and sent to broker")
    assert not res.valid

    res2 = validate_no_live_execution_language_in_portfolio("This is local metadata")
    assert res2.valid
