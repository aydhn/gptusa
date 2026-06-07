from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    ResearchBoundaryAudit, ClosureAuditCheck, ClosureAuditKind,
    ClosureComplianceStatus, BacktestClosureRiskFlag
)

def build_research_boundary_checks(payloads: dict[str, dict[str, Any]]) -> list[ClosureAuditCheck]:
    checks = []
    flags_required_true = {
        "research_data_only": "Research data only",
        "offline_backtest_research_only": "Offline backtest research only"
    }
    flags_required_false = {
        "investment_advice": "No investment advice",
        "produces_live_signal": "No live signal produced",
        "produces_order_decision": "No order decision produced",
        "produces_portfolio_weights": "No portfolio weights produced"
    }

    for flag, name in flags_required_true.items():
        found_false = False
        for p_name, payload in payloads.items():
            if not payload.get("context", {}).get(flag, True) and not payload.get(flag, True):
                found_false = True
                break
        chk = ClosureAuditCheck(
            audit_kind=ClosureAuditKind.RESEARCH_BOUNDARY,
            name=name,
            required=True,
            passed=not found_false,
            expected_value=True,
            observed_value=not found_false,
            rationale=f"Check that {flag} is True"
        )
        chk.status = ClosureComplianceStatus.PASSED if chk.passed else ClosureComplianceStatus.FAILED
        checks.append(chk)

    for flag, name in flags_required_false.items():
        found_true = False
        for p_name, payload in payloads.items():
            if payload.get("context", {}).get(flag, False) or payload.get(flag, False):
                found_true = True
                break
        chk = ClosureAuditCheck(
            audit_kind=ClosureAuditKind.RESEARCH_BOUNDARY,
            name=name,
            required=True,
            passed=not found_true,
            expected_value=False,
            observed_value=found_true,
            rationale=f"Check that {flag} is False"
        )
        chk.status = ClosureComplianceStatus.PASSED if chk.passed else ClosureComplianceStatus.FAILED
        checks.append(chk)

    return checks

def build_research_boundary_audit(payloads: dict[str, dict[str, Any]]) -> ResearchBoundaryAudit:
    audit = ResearchBoundaryAudit()
    audit.checks = build_research_boundary_checks(payloads)

    audit.research_data_only = next((c.passed for c in audit.checks if c.name == "Research data only"), False)
    audit.offline_backtest_research_only = next((c.passed for c in audit.checks if c.name == "Offline backtest research only"), False)
    audit.no_investment_advice = next((c.passed for c in audit.checks if c.name == "No investment advice"), False)
    audit.no_live_signal = next((c.passed for c in audit.checks if c.name == "No live signal produced"), False)
    audit.no_order_decision = next((c.passed for c in audit.checks if c.name == "No order decision produced"), False)
    audit.no_portfolio_weights = next((c.passed for c in audit.checks if c.name == "No portfolio weights produced"), False)

    audit.audit_passed = all(c.passed for c in audit.checks)

    if not audit.audit_passed:
        audit.risk_flags.append(BacktestClosureRiskFlag.RESEARCH_BOUNDARY_FAILED)
        audit.errors.append("Research boundary audit failed")

    return audit

def validate_research_boundary_audit(audit: ResearchBoundaryAudit) -> list[str]:
    errors = []
    if not audit.audit_passed:
        errors.append("Research boundary audit failed")
    return errors

def research_boundary_audit_summary(audit: ResearchBoundaryAudit) -> dict[str, Any]:
    return {"passed": audit.audit_passed}

def research_boundary_audit_to_text(audit: ResearchBoundaryAudit, limit: int = 300) -> str:
    return f"ResearchBoundaryAudit(passed={audit.audit_passed})"
