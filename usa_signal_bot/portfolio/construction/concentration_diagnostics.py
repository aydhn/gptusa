from typing import Any, Dict, List
from usa_signal_bot.portfolio.construction.phase155_models import (
    PortfolioSandboxDiagnosticRecord,
    PortfolioSandboxDiagnosticKind,
    PrototypeExposureTable,
    PortfolioConstructionPolicy,
    create_portfolio_sandbox_diagnostic_id,
    _now_str
)

def build_concentration_diagnostics(
    table: PrototypeExposureTable,
    policy: PortfolioConstructionPolicy
) -> List[PortfolioSandboxDiagnosticRecord]:

    diags = []

    method_records = {}
    for r in table.records:
        if r.method_kind not in method_records:
            method_records[r.method_kind] = []
        method_records[r.method_kind].append(r)

    for method, recs in method_records.items():
        weights = [r.normalized_sandbox_weight for r in recs if r.normalized_sandbox_weight is not None]

        # Max weight
        max_w = max(weights) if weights else 0.0
        diags.append(PortfolioSandboxDiagnosticRecord(
            diagnostic_id=create_portfolio_sandbox_diagnostic_id(),
            created_at_utc=_now_str(),
            diagnostic_kind=PortfolioSandboxDiagnosticKind.MAX_SANDBOX_WEIGHT,
            value=max_w,
            diagnostic_notes=[f"Max weight for {method.value}"],
            diagnostic_valid=True,
            research_sandbox_only=True,
            not_investment_advice=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={"method": method.value, "policy_max": policy.max_sandbox_weight_fraction}
        ))

        # Top 5 concentration
        top_5 = calculate_top_n_concentration(weights, 5)
        diags.append(PortfolioSandboxDiagnosticRecord(
            diagnostic_id=create_portfolio_sandbox_diagnostic_id(),
            created_at_utc=_now_str(),
            diagnostic_kind=PortfolioSandboxDiagnosticKind.TOP_N_SANDBOX_CONCENTRATION,
            value=top_5,
            diagnostic_notes=[f"Top 5 concentration for {method.value}"],
            diagnostic_valid=True,
            research_sandbox_only=True,
            not_investment_advice=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={"method": method.value, "n": 5}
        ))

    return diags

def calculate_top_n_concentration(weights: List[float], n: int = 5) -> float | None:
    if not weights:
        return None
    sorted_w = sorted(weights, reverse=True)
    return sum(sorted_w[:n])

def validate_concentration_diagnostics(items: List[PortfolioSandboxDiagnosticRecord]) -> List[str]:
    errors = []
    for item in items:
        if not item.research_sandbox_only or not item.not_investment_advice:
            errors.append(f"Diagnostic {item.diagnostic_id} is not marked as research/not-advice.")
    return errors

def concentration_diagnostics_summary(items: List[PortfolioSandboxDiagnosticRecord]) -> Dict[str, Any]:
    return {
        "count": len(items),
        "kinds": list(set(i.diagnostic_kind.value for i in items))
    }
