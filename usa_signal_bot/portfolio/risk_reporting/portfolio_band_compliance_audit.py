from typing import Any, Dict, List
import datetime

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    PortfolioBandComplianceAudit,
    PortfolioBandLineage,
    PortfolioRiskSummary,
    PortfolioGovernanceReport,
    PortfolioBandComplianceCheck,
    create_portfolio_band_compliance_audit_id,
    create_portfolio_band_compliance_check_id
)
from usa_signal_bot.core.enums import PortfolioBandClosureStatus

def build_portfolio_band_compliance_audit(lineage: PortfolioBandLineage, risk_summary: PortfolioRiskSummary, governance_reports: List[PortfolioGovernanceReport]) -> PortfolioBandComplianceAudit:
    checks = build_portfolio_band_compliance_checks(lineage, risk_summary, governance_reports)

    passed_count = sum(1 for c in checks if c.status == PortfolioBandClosureStatus.PASSED)
    warning_count = sum(1 for c in checks if c.status == PortfolioBandClosureStatus.WARNING)
    failed_count = sum(1 for c in checks if c.status == PortfolioBandClosureStatus.FAILED)
    blocked_count = sum(1 for c in checks if c.status == PortfolioBandClosureStatus.BLOCKED)

    audit_passed = failed_count == 0 and blocked_count == 0

    return PortfolioBandComplianceAudit(
        audit_id=create_portfolio_band_compliance_audit_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        checks=checks,
        audit_passed=audit_passed,
        passed_count=passed_count,
        warning_count=warning_count,
        failed_count=failed_count,
        blocked_count=blocked_count,
        no_live_trading=True,
        no_paper_trading=True,
        no_broker_execution=True,
        no_real_order_creation=True,
        no_actual_target_weights=True,
        no_actual_allocation=True,
        no_capital_deployment=True,
        no_deployment=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_portfolio_band_compliance_checks(lineage: PortfolioBandLineage, risk_summary: PortfolioRiskSummary, governance_reports: List[PortfolioGovernanceReport]) -> List[PortfolioBandComplianceCheck]:
    checks = []
    checks.append(PortfolioBandComplianceCheck(
        check_id=create_portfolio_band_compliance_check_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        name="All Required Artifacts Available",
        status=PortfolioBandClosureStatus.PASSED if lineage.all_required_available else PortfolioBandClosureStatus.BLOCKED,
        required=True,
        passed=lineage.all_required_available,
        expected_value=True,
        observed_value=lineage.all_required_available,
        rationale="All artifacts required for Phase 153-157 closure must be available.",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))
    return checks

def validate_portfolio_band_compliance_audit(audit: PortfolioBandComplianceAudit) -> List[str]:
    return []

def portfolio_band_compliance_audit_to_text(audit: PortfolioBandComplianceAudit, limit: int = 300) -> str:
    return f"Audit {audit.audit_id}: passed={audit.audit_passed}"
