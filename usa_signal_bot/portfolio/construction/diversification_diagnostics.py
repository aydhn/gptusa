from typing import Any, Dict, List
from usa_signal_bot.portfolio.construction.phase155_models import (
    PortfolioSandboxDiagnosticRecord,
    PortfolioSandboxDiagnosticKind,
    PrototypeExposureTable,
    create_portfolio_sandbox_diagnostic_id,
    _now_str
)

def build_diversification_diagnostics(table: PrototypeExposureTable) -> List[PortfolioSandboxDiagnosticRecord]:
    diags = []

    # Calculate per method
    method_records = {}
    for r in table.records:
        if r.method_kind not in method_records:
            method_records[r.method_kind] = []
        method_records[r.method_kind].append(r)

    for method, recs in method_records.items():
        weights = [r.normalized_sandbox_weight for r in recs if r.normalized_sandbox_weight is not None and r.normalized_sandbox_weight > 0]

        # Effective Name Count
        enc = calculate_effective_name_count(weights)
        diags.append(PortfolioSandboxDiagnosticRecord(
            diagnostic_id=create_portfolio_sandbox_diagnostic_id(),
            created_at_utc=_now_str(),
            diagnostic_kind=PortfolioSandboxDiagnosticKind.EFFECTIVE_NAME_COUNT,
            value=enc,
            diagnostic_notes=[f"Calculated for {method.value}"],
            diagnostic_valid=True,
            research_sandbox_only=True,
            not_investment_advice=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={"method": method.value}
        ))

        # Herfindahl Index
        hhi = calculate_herfindahl_index(weights)
        diags.append(PortfolioSandboxDiagnosticRecord(
            diagnostic_id=create_portfolio_sandbox_diagnostic_id(),
            created_at_utc=_now_str(),
            diagnostic_kind=PortfolioSandboxDiagnosticKind.HERFINDAHL_INDEX,
            value=hhi,
            diagnostic_notes=[f"Calculated for {method.value}"],
            diagnostic_valid=True,
            research_sandbox_only=True,
            not_investment_advice=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={"method": method.value}
        ))

        # Diversification Count (non-zero weights)
        diags.append(PortfolioSandboxDiagnosticRecord(
            diagnostic_id=create_portfolio_sandbox_diagnostic_id(),
            created_at_utc=_now_str(),
            diagnostic_kind=PortfolioSandboxDiagnosticKind.DIVERSIFICATION_COUNT,
            value=len(weights),
            diagnostic_notes=[f"Non-zero count for {method.value}"],
            diagnostic_valid=True,
            research_sandbox_only=True,
            not_investment_advice=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={"method": method.value}
        ))

    return diags

def calculate_effective_name_count(weights: List[float]) -> float | None:
    if not weights:
        return None
    hhi = calculate_herfindahl_index(weights)
    if hhi and hhi > 0:
        return 1.0 / hhi
    return None

def calculate_herfindahl_index(weights: List[float]) -> float | None:
    if not weights:
        return None
    return sum(w * w for w in weights)

def validate_diversification_diagnostics(items: List[PortfolioSandboxDiagnosticRecord]) -> List[str]:
    errors = []
    for item in items:
        if not item.research_sandbox_only or not item.not_investment_advice:
            errors.append(f"Diagnostic {item.diagnostic_id} is not marked as research/not-advice.")
    return errors

def diversification_diagnostics_summary(items: List[PortfolioSandboxDiagnosticRecord]) -> Dict[str, Any]:
    return {
        "count": len(items),
        "kinds": list(set(i.diagnostic_kind.value for i in items))
    }
