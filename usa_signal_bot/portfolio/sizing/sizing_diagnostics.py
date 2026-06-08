from typing import Any
from usa_signal_bot.portfolio.sizing.phase154_models import SizingDiagnosticRecord, SizingComparisonMatrix, SizingCapFloorRule, SizingDiagnosticKind

def build_sizing_diagnostics(matrix: SizingComparisonMatrix, cap_floor_rules: list[SizingCapFloorRule]) -> list[SizingDiagnosticRecord]:
    diagnostics = []

    # Method disagreement
    disagreement = calculate_method_disagreement(matrix)
    d1 = SizingDiagnosticRecord(
        diagnostic_kind=SizingDiagnosticKind.METHOD_DISAGREEMENT,
        value=disagreement,
        diagnostic_notes=["Disagreement calculated as max diff between methods per symbol"],
        diagnostic_valid=True
    )
    diagnostics.append(d1)

    # Cap floor binding count
    binding_count = calculate_cap_floor_binding_count(cap_floor_rules)
    d2 = SizingDiagnosticRecord(
        diagnostic_kind=SizingDiagnosticKind.CAP_FLOOR_BINDING_COUNT,
        value=binding_count,
        diagnostic_notes=["Count of rules that were binding (capped or floored)"],
        diagnostic_valid=True
    )
    diagnostics.append(d2)

    return diagnostics

def calculate_method_disagreement(matrix: SizingComparisonMatrix) -> dict[str, Any]:
    # Dummy implementation for method disagreement
    disagreements = {}
    from collections import defaultdict
    by_symbol = defaultdict(list)
    for r in matrix.results:
        if r.capped_prototype_fraction is not None:
            by_symbol[r.symbol].append(r.capped_prototype_fraction)

    for sym, fractions in by_symbol.items():
        if fractions:
            disagreements[sym] = max(fractions) - min(fractions)
        else:
            disagreements[sym] = 0.0

    avg_disagreement = sum(disagreements.values()) / len(disagreements) if disagreements else 0.0
    return {"average_disagreement": avg_disagreement, "symbol_disagreements": disagreements}

def calculate_cap_floor_binding_count(cap_floor_rules: list[SizingCapFloorRule]) -> int:
    return sum(1 for r in cap_floor_rules if not r.passed)

def validate_sizing_diagnostics(items: list[SizingDiagnosticRecord]) -> list[str]:
    errors = []
    for i, d in enumerate(items):
        if not d.research_prototype_only:
            errors.append(f"Diagnostic {i} is not research prototype only.")
    return errors

def sizing_diagnostics_summary(items: list[SizingDiagnosticRecord]) -> dict[str, Any]:
    return {"count": len(items), "valid": len(validate_sizing_diagnostics(items)) == 0}

def sizing_diagnostics_to_text(items: list[SizingDiagnosticRecord], limit: int = 300) -> str:
    return f"Sizing Diagnostics: {len(items)}"[:limit]
