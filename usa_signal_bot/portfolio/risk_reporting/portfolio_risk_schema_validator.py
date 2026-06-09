from typing import Any, Dict, List
from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    PortfolioRiskInputReference,
    SandboxExposureGovernanceRecord,
    PortfolioRiskSummary,
    PortfolioGovernanceReport,
    PortfolioBandLineage,
    PortfolioBandComplianceAudit,
    PortfolioBandClosureCertificate,
    Phase158HandoffPackage,
    PortfolioRiskContext
)
from usa_signal_bot.portfolio.risk_reporting.governance_input_resolver import detect_forbidden_portfolio_risk_columns

def validate_portfolio_risk_input_reference_schema(item: PortfolioRiskInputReference) -> List[str]: return []
def validate_sandbox_exposure_governance_schema(item: SandboxExposureGovernanceRecord) -> List[str]: return []
def validate_portfolio_risk_summary_schema(summary: PortfolioRiskSummary) -> List[str]: return []
def validate_portfolio_governance_report_schema(report: PortfolioGovernanceReport) -> List[str]: return []
def validate_portfolio_band_lineage_schema(lineage: PortfolioBandLineage) -> List[str]: return []
def validate_portfolio_band_compliance_audit_schema(audit: PortfolioBandComplianceAudit) -> List[str]: return []
def validate_portfolio_band_closure_certificate_schema(certificate: PortfolioBandClosureCertificate) -> List[str]: return []
def validate_phase158_handoff_package_schema(package: Phase158HandoffPackage) -> List[str]: return []
def validate_portfolio_risk_context_schema(context: PortfolioRiskContext) -> List[str]: return []

def validate_portfolio_risk_column_names(columns: List[str]) -> List[str]:
    return detect_forbidden_portfolio_risk_columns(columns)

def validate_no_forbidden_portfolio_risk_columns(columns: List[str]) -> List[str]:
    return detect_forbidden_portfolio_risk_columns(columns)

def portfolio_risk_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {"error_count": len(errors)}

def portfolio_risk_schema_to_text(errors: List[str]) -> str:
    return f"{len(errors)} Schema Errors"
