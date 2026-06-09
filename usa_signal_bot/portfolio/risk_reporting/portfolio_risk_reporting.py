from typing import Any, Dict, List

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    OptimizerPrototypeIngestionResult,
    PortfolioRiskInputReference,
    SandboxExposureGovernanceRecord,
    PortfolioRiskSummary,
    PortfolioGovernanceReport,
    PortfolioBandLineage,
    PortfolioBandComplianceAudit,
    PortfolioBandFinalReview,
    PortfolioBandClosureCertificate,
    Phase158HandoffContract,
    Phase158HandoffPackage,
    PortfolioRiskSafetyBoundaryResult,
    Phase158ReadinessGate,
    PortfolioRiskContext,
    PortfolioRiskFullReview
)

def optimizer_prototype_ingestion_result_to_text(item: OptimizerPrototypeIngestionResult) -> str:
    return f"IngestionResult(valid={item.valid_for_phase157})"

def portfolio_risk_input_reference_to_text(item: PortfolioRiskInputReference) -> str:
    return f"InputReference({item.source_artifact_name})"

def sandbox_exposure_governance_to_text(items: List[SandboxExposureGovernanceRecord], limit: int = 300) -> str:
    return f"SandboxExposureGovernance(items={len(items)})"

def portfolio_risk_summary_to_text(item: PortfolioRiskSummary, limit: int = 300) -> str:
    return f"PortfolioRiskSummary({item.summary_id})"

def portfolio_governance_report_to_text(item: PortfolioGovernanceReport, limit: int = 300) -> str:
    return f"PortfolioGovernanceReport({item.title})"

def portfolio_band_lineage_to_text(item: PortfolioBandLineage, limit: int = 300) -> str:
    return f"PortfolioBandLineage({item.lineage_id})"

def portfolio_band_compliance_audit_to_text(item: PortfolioBandComplianceAudit, limit: int = 300) -> str:
    return f"PortfolioBandComplianceAudit(passed={item.audit_passed})"

def portfolio_band_final_review_to_text(item: PortfolioBandFinalReview, limit: int = 300) -> str:
    return f"PortfolioBandFinalReview(passed={item.final_review_passed})"

def portfolio_band_closure_certificate_to_text(item: PortfolioBandClosureCertificate, limit: int = 300) -> str:
    return f"PortfolioBandClosureCertificate(closed={item.closed})"

def phase158_handoff_contract_to_text(item: Phase158HandoffContract, limit: int = 300) -> str:
    return f"Phase158HandoffContract(valid={item.contract_valid})"

def phase158_handoff_package_to_text(item: Phase158HandoffPackage, limit: int = 300) -> str:
    return f"Phase158HandoffPackage(valid={item.package_valid})"

def portfolio_risk_safety_boundary_to_text(item: PortfolioRiskSafetyBoundaryResult, limit: int = 300) -> str:
    return f"PortfolioRiskSafetyBoundary(passed={item.boundary_passed})"

def phase158_readiness_gate_to_text(item: Phase158ReadinessGate, limit: int = 300) -> str:
    return f"Phase158ReadinessGate(ready={item.ready_for_phase158})"

def portfolio_risk_context_to_text(item: PortfolioRiskContext, limit: int = 300) -> str:
    return f"PortfolioRiskContext({item.context_id})"

def portfolio_risk_full_review_to_text(item: PortfolioRiskFullReview, limit: int = 300) -> str:
    return f"PortfolioRiskFullReview({item.review_id})"

def portfolio_risk_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store Summary: {summary}"

def portfolio_risk_limitations_text() -> str:
    return "Phase 157 limits: Research only, no actual trading or target weights."
