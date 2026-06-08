import pytest
from usa_signal_bot.portfolio.sizing.phase154_models import (
    SizingPrototypeContext, SizingCandidate, SizingPolicy,
    SizingMethodContract, SizingPrototypeResult, SizingComparisonMatrix,
    SizingDiagnosticRecord, SizingSensitivityReport, RiskBudgetAdherenceReport,
    SizingSafetyBoundaryResult, Phase155ReadinessGate
)
from usa_signal_bot.portfolio.sizing.sizing_schema_validator import validate_sizing_comparison_matrix_schema
from usa_signal_bot.portfolio.sizing.sizing_safety_validator import validate_sizing_context_safety

def test_comparison_matrix_schema():
    matrix = SizingComparisonMatrix(no_actual_position_size=True)
    errors = validate_sizing_comparison_matrix_schema(matrix)
    assert not errors

    matrix_bad = SizingComparisonMatrix(no_actual_position_size=False)
    errors_bad = validate_sizing_comparison_matrix_schema(matrix_bad)
    assert errors_bad

def test_context_safety():
    context = SizingPrototypeContext()
    context.actual_position_sizing_executed = True
    errors = validate_sizing_context_safety(context)
    assert errors
    assert any("actual position sizing" in e.lower() for e in errors)

def test_context_safety_clean():
    context = SizingPrototypeContext()
    errors = validate_sizing_context_safety(context)
    assert not errors
