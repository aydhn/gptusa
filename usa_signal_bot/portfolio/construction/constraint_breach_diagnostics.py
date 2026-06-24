from typing import Any, Dict, List, Tuple
from collections import defaultdict
from usa_signal_bot.portfolio.construction.phase155_models import (
    PortfolioSandboxDiagnosticRecord,
    PortfolioSandboxDiagnosticKind,
    PrototypeExposureTable,
    PortfolioConstructionPolicy,
    create_portfolio_sandbox_diagnostic_id,
    _now_str,
    PrototypeExposureRecord
)

def _evaluate_weight_breach(
    r: PrototypeExposureRecord,
    policy: PortfolioConstructionPolicy
) -> Tuple[int, List[str]]:
    w = r.normalized_sandbox_weight
    if w is None:
        return 0, []

    breaches = 0
    notes = []

    # Due to float rounding, use small epsilon
    if w > policy.max_sandbox_weight_fraction + 1e-5:
        breaches += 1
        notes.append(f"{r.symbol} weight {w:.4f} > max {policy.max_sandbox_weight_fraction}")
    # Don't penalize exactly 0 for min check, min check is for non-zero weights
    elif w > 0 and w < policy.min_sandbox_weight_fraction - 1e-5:
        breaches += 1
        notes.append(f"{r.symbol} weight {w:.4f} < min {policy.min_sandbox_weight_fraction}")

    return breaches, notes

def build_constraint_breach_diagnostics(
    table: PrototypeExposureTable,
    policy: PortfolioConstructionPolicy
) -> List[PortfolioSandboxDiagnosticRecord]:

    diags = []

    method_records = defaultdict(list)
    for r in table.records:
        method_records[r.method_kind].append(r)

    for method, recs in method_records.items():
        breaches = 0
        notes = []

        for r in recs:
            b, n = _evaluate_weight_breach(r, policy)
            breaches += b
            notes.extend(n)

        diags.append(PortfolioSandboxDiagnosticRecord(
            diagnostic_id=create_portfolio_sandbox_diagnostic_id(),
            created_at_utc=_now_str(),
            diagnostic_kind=PortfolioSandboxDiagnosticKind.CONSTRAINT_BREACH_COUNT,
            value=breaches,
            diagnostic_notes=notes,
            diagnostic_valid=True,
            research_sandbox_only=True,
            not_investment_advice=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={"method": method.value}
        ))

    return diags

def count_sandbox_constraint_breaches(table: PrototypeExposureTable, policy: PortfolioConstructionPolicy) -> int:
    diags = build_constraint_breach_diagnostics(table, policy)
    return sum(d.value for d in diags if isinstance(d.value, int))

def validate_constraint_breach_diagnostics(items: List[PortfolioSandboxDiagnosticRecord]) -> List[str]:
    from usa_signal_bot.portfolio.construction.concentration_diagnostics import validate_concentration_diagnostics
    return validate_concentration_diagnostics(items)

def constraint_breach_diagnostics_summary(items: List[PortfolioSandboxDiagnosticRecord]) -> Dict[str, Any]:
    return {
        "count": len(items),
        "total_breaches": sum(d.value for d in items if isinstance(d.value, int))
    }
