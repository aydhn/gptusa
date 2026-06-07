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
