import os
import textwrap

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(textwrap.dedent(content).lstrip())


# 9. SAFETY COMPLIANCE AUDIT
write_file("usa_signal_bot/backtesting/closure/safety_compliance_audit.py", """
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    SafetyComplianceAudit, ClosureAuditCheck, ClosureAuditKind,
    ClosureComplianceStatus, BacktestClosureRiskFlag
)

def build_safety_compliance_checks(payloads: dict[str, dict[str, Any]]) -> list[ClosureAuditCheck]:
    checks = []
    flags = {
        "live_trading_enabled": (ClosureAuditKind.NO_LIVE_TRADING, "No live trading enabled"),
        "paper_trading_enabled": (ClosureAuditKind.NO_PAPER_TRADING, "No paper trading enabled"),
        "broker_execution_enabled": (ClosureAuditKind.NO_BROKER_EXECUTION, "No broker execution enabled"),
        "real_order_creation_enabled": (ClosureAuditKind.NO_REAL_ORDER_CREATION, "No real order creation"),
        "paper_state_mutation_enabled": (ClosureAuditKind.UNKNOWN, "No paper state mutation"),
        "telegram_real_send_enabled": (ClosureAuditKind.UNKNOWN, "No telegram real send"),
        "strategy_activation_allowed": (ClosureAuditKind.UNKNOWN, "No strategy activation allowed"),
        "portfolio_optimization_enabled": (ClosureAuditKind.NO_PORTFOLIO_OUTPUT, "No portfolio optimization"),
        "portfolio_allocation_output_enabled": (ClosureAuditKind.NO_PORTFOLIO_OUTPUT, "No portfolio allocation"),
        "target_weights_produced": (ClosureAuditKind.NO_PORTFOLIO_OUTPUT, "No target weights produced"),
        "deployment_allowed": (ClosureAuditKind.NO_DEPLOYMENT, "No deployment allowed"),
        "network_used": (ClosureAuditKind.UNKNOWN, "No network used")
    }

    for flag, (kind, name) in flags.items():
        # check all payloads for this flag
        found_true = False
        for p_name, payload in payloads.items():
            if payload.get("context", {}).get(flag, False) or payload.get(flag, False):
                found_true = True
                break

        chk = ClosureAuditCheck(
            audit_kind=kind,
            name=name,
            required=True,
            passed=not found_true,
            expected_value=False,
            observed_value=found_true,
            rationale=f"Check that {flag} is False"
        )
        if not found_true:
            chk.status = ClosureComplianceStatus.PASSED
        else:
            chk.status = ClosureComplianceStatus.FAILED
            chk.errors.append(f"{flag} is True")
        checks.append(chk)

    return checks

def build_safety_compliance_audit(payloads: dict[str, dict[str, Any]]) -> SafetyComplianceAudit:
    audit = SafetyComplianceAudit()
    audit.checks = build_safety_compliance_checks(payloads)

    audit.no_live_trading = next((c.passed for c in audit.checks if c.name == "No live trading enabled"), False)
    audit.no_paper_trading = next((c.passed for c in audit.checks if c.name == "No paper trading enabled"), False)
    audit.no_broker_execution = next((c.passed for c in audit.checks if c.name == "No broker execution enabled"), False)
    audit.no_real_order_creation = next((c.passed for c in audit.checks if c.name == "No real order creation"), False)
    audit.no_paper_state_mutation = next((c.passed for c in audit.checks if c.name == "No paper state mutation"), False)
    audit.no_telegram_real_send = next((c.passed for c in audit.checks if c.name == "No telegram real send"), False)
    audit.no_strategy_activation = next((c.passed for c in audit.checks if c.name == "No strategy activation allowed"), False)
    audit.no_portfolio_output = next((c.passed for c in audit.checks if c.name == "No portfolio allocation"), False)
    audit.no_deployment = next((c.passed for c in audit.checks if c.name == "No deployment allowed"), False)
    audit.no_network = next((c.passed for c in audit.checks if c.name == "No network used"), False)

    audit.audit_passed = all(c.passed for c in audit.checks)

    if not audit.audit_passed:
        audit.risk_flags.append(BacktestClosureRiskFlag.SAFETY_COMPLIANCE_FAILED)
        audit.errors.append("Safety compliance audit failed")

    return audit

def validate_safety_compliance_audit(audit: SafetyComplianceAudit) -> list[str]:
    errors = []
    if not audit.audit_passed:
        errors.append("Safety audit failed")
    return errors

def safety_compliance_audit_summary(audit: SafetyComplianceAudit) -> dict[str, Any]:
    return {"passed": audit.audit_passed}

def safety_compliance_audit_to_text(audit: SafetyComplianceAudit, limit: int = 300) -> str:
    return f"SafetyComplianceAudit(passed={audit.audit_passed})"
""")

# 10. RESEARCH BOUNDARY AUDIT
write_file("usa_signal_bot/backtesting/closure/research_boundary_audit.py", """
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
""")
