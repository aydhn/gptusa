from typing import Any, Dict, List
from usa_signal_bot.portfolio.construction.phase155_models import (
    PortfolioSandboxDiagnosticRecord,
    PortfolioSandboxDiagnosticKind,
    SandboxAllocationResult,
    PortfolioSandboxCandidate,
    create_portfolio_sandbox_diagnostic_id,
    _now_str
)

def build_risk_budget_sandbox_diagnostics(
    results: List[SandboxAllocationResult],
    candidates: List[PortfolioSandboxCandidate]
) -> List[PortfolioSandboxDiagnosticRecord]:

    diags = []

    cand_map = {c.symbol: c for c in candidates}

    method_results = {}
    for r in results:
        if r.method_kind not in method_results:
            method_results[r.method_kind] = []
        method_results[r.method_kind].append(r)

    for method, recs in method_results.items():
        used_budget = 0.0
        total_budget = 0.0

        for r in recs:
            cand = cand_map.get(r.symbol)
            if not cand or cand.risk_budget_score is None:
                continue

            w = r.normalized_sandbox_weight or 0.0
            used_budget += w * cand.risk_budget_score
            total_budget += cand.risk_budget_score

        ratio = used_budget / total_budget if total_budget > 0 else 0.0

        diags.append(PortfolioSandboxDiagnosticRecord(
            diagnostic_id=create_portfolio_sandbox_diagnostic_id(),
            created_at_utc=_now_str(),
            diagnostic_kind=PortfolioSandboxDiagnosticKind.RISK_BUDGET_USAGE,
            value=ratio,
            diagnostic_notes=[f"Risk budget usage for {method.value}"],
            diagnostic_valid=True,
            research_sandbox_only=True,
            not_investment_advice=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={"method": method.value, "used": used_budget, "total": total_budget}
        ))

    return diags

def estimate_sandbox_risk_budget_usage(
    results: List[SandboxAllocationResult],
    candidates: List[PortfolioSandboxCandidate]
) -> Dict[str, Any]:
    diags = build_risk_budget_sandbox_diagnostics(results, candidates)
    res = {}
    for d in diags:
        if d.metadata.get("method"):
            res[d.metadata["method"]] = d.value
    return res

def validate_risk_budget_sandbox_diagnostics(items: List[PortfolioSandboxDiagnosticRecord]) -> List[str]:
    from usa_signal_bot.portfolio.construction.concentration_diagnostics import validate_concentration_diagnostics
    return validate_concentration_diagnostics(items)

def risk_budget_sandbox_diagnostics_summary(items: List[PortfolioSandboxDiagnosticRecord]) -> Dict[str, Any]:
    return {
        "count": len(items),
        "kinds": list(set(i.diagnostic_kind.value for i in items))
    }
