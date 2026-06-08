from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.construction.phase155_models import (
    PortfolioSandboxDiagnosticRecord,
    PortfolioSandboxDiagnosticKind,
    PrototypeExposureTable,
    PortfolioConstructionPolicy,
    create_portfolio_sandbox_diagnostic_id,
    _now_str
)

def build_turnover_sandbox_diagnostics(
    current_table: PrototypeExposureTable,
    previous_table: Optional[PrototypeExposureTable] = None,
    policy: Optional[PortfolioConstructionPolicy] = None
) -> List[PortfolioSandboxDiagnosticRecord]:

    diags = []

    if not previous_table:
        diags.append(PortfolioSandboxDiagnosticRecord(
            diagnostic_id=create_portfolio_sandbox_diagnostic_id(),
            created_at_utc=_now_str(),
            diagnostic_kind=PortfolioSandboxDiagnosticKind.TURNOVER_SANDBOX_ESTIMATE,
            value=0.0,
            diagnostic_notes=["No previous table for turnover comparison. Defaulting to 0.0"],
            diagnostic_valid=True,
            research_sandbox_only=True,
            not_investment_advice=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={"comparison": "none"}
        ))
        return diags

    # Turnover is computed per method
    methods = set(r.method_kind for r in current_table.records)

    for method in methods:
        curr_map = {r.symbol: (r.normalized_sandbox_weight or 0.0) for r in current_table.records if r.method_kind == method}
        prev_map = {r.symbol: (r.normalized_sandbox_weight or 0.0) for r in previous_table.records if r.method_kind == method}

        symbols = set(curr_map.keys()) | set(prev_map.keys())
        turnover = sum(abs(curr_map.get(s, 0.0) - prev_map.get(s, 0.0)) for s in symbols) / 2.0

        diags.append(PortfolioSandboxDiagnosticRecord(
            diagnostic_id=create_portfolio_sandbox_diagnostic_id(),
            created_at_utc=_now_str(),
            diagnostic_kind=PortfolioSandboxDiagnosticKind.TURNOVER_SANDBOX_ESTIMATE,
            value=turnover,
            diagnostic_notes=[f"Sandbox turnover for {method.value}"],
            diagnostic_valid=True,
            research_sandbox_only=True,
            not_investment_advice=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={"method": method.value}
        ))

    return diags

def estimate_sandbox_turnover(
    current_table: PrototypeExposureTable,
    previous_table: Optional[PrototypeExposureTable] = None
) -> float | None:
    if not previous_table:
        return None

    # Overall average turnover across all methods
    diags = build_turnover_sandbox_diagnostics(current_table, previous_table)
    vals = [d.value for d in diags if isinstance(d.value, (int, float))]
    return sum(vals) / len(vals) if vals else None

def validate_turnover_sandbox_diagnostics(items: List[PortfolioSandboxDiagnosticRecord]) -> List[str]:
    from usa_signal_bot.portfolio.construction.concentration_diagnostics import validate_concentration_diagnostics
    return validate_concentration_diagnostics(items)

def turnover_sandbox_diagnostics_summary(items: List[PortfolioSandboxDiagnosticRecord]) -> Dict[str, Any]:
    return {
        "count": len(items),
        "kinds": list(set(i.diagnostic_kind.value for i in items))
    }
