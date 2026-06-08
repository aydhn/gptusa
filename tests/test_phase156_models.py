import pytest
from usa_signal_bot.portfolio.optimization.phase156_models import (
    PortfolioConstructionIngestionResult,
    OptimizerSandboxResult,
    Phase157ReadinessGate,
    validate_portfolio_construction_ingestion,
    validate_optimizer_sandbox_result,
    validate_phase157_readiness_gate,
    OptimizerSafetyBoundaryResult
)

def test_portfolio_construction_ingestion_valid():
    r = PortfolioConstructionIngestionResult(
        ready_for_phase156=True,
        research_data_only=True,
        allocation_sandbox_only=True,
        deterministic=True
    )
    assert not validate_portfolio_construction_ingestion(r)

def test_portfolio_construction_ingestion_invalid():
    r = PortfolioConstructionIngestionResult(
        ready_for_phase156=False,
        actual_target_weights_produced=True,
        live_trading_enabled=True
    )
    errs = validate_portfolio_construction_ingestion(r)
    assert len(errs) > 0
    assert "Ingestion not ready for Phase 156" in errs
    assert "Actual target weights produced" in errs
    assert "Live trading enabled" in errs

def test_optimizer_sandbox_result():
    r = OptimizerSandboxResult(
        symbol="AAPL",
        actual_target_weight=0.1
    )
    errs = validate_optimizer_sandbox_result(r)
    assert "AAPL: actual target weight must be None" in errs

def test_phase157_readiness_gate():
    b = OptimizerSafetyBoundaryResult(boundary_passed=False)
    gate = Phase157ReadinessGate(ready_for_phase157=True, safety_boundary=b)
    errs = validate_phase157_readiness_gate(gate)
    assert len(errs) > 0
    assert "ready_for_phase157 true but safety_boundary failed" in errs
