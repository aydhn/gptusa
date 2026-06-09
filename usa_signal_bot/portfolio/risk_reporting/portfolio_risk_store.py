import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    PortfolioRiskContext,
    PortfolioRiskFullReview,
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
    portfolio_risk_context_to_dict,
    portfolio_risk_full_review_to_dict,
    portfolio_risk_input_reference_to_dict,
    sandbox_exposure_governance_record_to_dict,
    portfolio_risk_summary_to_dict,
    portfolio_governance_report_to_dict,
    portfolio_band_lineage_to_dict,
    portfolio_band_compliance_audit_to_dict,
    portfolio_band_final_review_to_dict,
    portfolio_band_closure_certificate_to_dict,
    phase158_handoff_contract_to_dict,
    phase158_handoff_package_to_dict,
    portfolio_risk_safety_boundary_result_to_dict,
    phase158_readiness_gate_to_dict
)

def portfolio_risk_store_dir(data_root: Path) -> Path:
    p = data_root / "portfolio" / "risk_reporting"
    p.mkdir(parents=True, exist_ok=True)
    return p

def portfolio_risk_contexts_dir(data_root: Path) -> Path:
    p = portfolio_risk_store_dir(data_root) / "contexts"
    p.mkdir(parents=True, exist_ok=True)
    return p

def portfolio_risk_reviews_dir(data_root: Path) -> Path:
    p = portfolio_risk_store_dir(data_root) / "reviews"
    p.mkdir(parents=True, exist_ok=True)
    return p

def portfolio_risk_inputs_dir(data_root: Path) -> Path:
    p = portfolio_risk_store_dir(data_root) / "inputs"
    p.mkdir(parents=True, exist_ok=True)
    return p

def exposure_governance_dir(data_root: Path) -> Path:
    p = portfolio_risk_store_dir(data_root) / "exposure_governance"
    p.mkdir(parents=True, exist_ok=True)
    return p

def risk_summaries_dir(data_root: Path) -> Path:
    p = portfolio_risk_store_dir(data_root) / "risk_summaries"
    p.mkdir(parents=True, exist_ok=True)
    return p

def governance_reports_dir(data_root: Path) -> Path:
    p = portfolio_risk_store_dir(data_root) / "governance_reports"
    p.mkdir(parents=True, exist_ok=True)
    return p

def band_lineage_dir(data_root: Path) -> Path:
    p = portfolio_risk_store_dir(data_root) / "band_lineage"
    p.mkdir(parents=True, exist_ok=True)
    return p

def band_compliance_audits_dir(data_root: Path) -> Path:
    p = portfolio_risk_store_dir(data_root) / "band_compliance_audits"
    p.mkdir(parents=True, exist_ok=True)
    return p

def band_final_reviews_dir(data_root: Path) -> Path:
    p = portfolio_risk_store_dir(data_root) / "band_final_reviews"
    p.mkdir(parents=True, exist_ok=True)
    return p

def band_closure_certificates_dir(data_root: Path) -> Path:
    p = portfolio_risk_store_dir(data_root) / "band_closure_certificates"
    p.mkdir(parents=True, exist_ok=True)
    return p

def phase158_handoff_contracts_dir(data_root: Path) -> Path:
    p = portfolio_risk_store_dir(data_root) / "phase158_handoff_contracts"
    p.mkdir(parents=True, exist_ok=True)
    return p

def phase158_handoff_packages_dir(data_root: Path) -> Path:
    p = portfolio_risk_store_dir(data_root) / "phase158_handoff_packages"
    p.mkdir(parents=True, exist_ok=True)
    return p

def safety_boundaries_dir(data_root: Path) -> Path:
    p = portfolio_risk_store_dir(data_root) / "safety_boundaries"
    p.mkdir(parents=True, exist_ok=True)
    return p

def phase158_gates_dir(data_root: Path) -> Path:
    p = portfolio_risk_store_dir(data_root) / "phase158_gates"
    p.mkdir(parents=True, exist_ok=True)
    return p

def _write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path

def _write_jsonl(path: Path, items: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(i) + "\n")
    return path

def write_portfolio_risk_context_json(path: Path, item: PortfolioRiskContext) -> Path:
    return _write_json(path, portfolio_risk_context_to_dict(item))

def write_portfolio_risk_full_review_json(path: Path, item: PortfolioRiskFullReview) -> Path:
    return _write_json(path, portfolio_risk_full_review_to_dict(item))

def write_portfolio_risk_input_refs_jsonl(path: Path, items: List[PortfolioRiskInputReference]) -> Path:
    return _write_jsonl(path, [portfolio_risk_input_reference_to_dict(i) for i in items])

def write_sandbox_exposure_governance_jsonl(path: Path, items: List[SandboxExposureGovernanceRecord]) -> Path:
    return _write_jsonl(path, [sandbox_exposure_governance_record_to_dict(i) for i in items])

def write_portfolio_risk_summary_json(path: Path, item: PortfolioRiskSummary) -> Path:
    return _write_json(path, portfolio_risk_summary_to_dict(item))

def write_governance_reports_jsonl(path: Path, items: List[PortfolioGovernanceReport]) -> Path:
    return _write_jsonl(path, [portfolio_governance_report_to_dict(i) for i in items])

def write_portfolio_band_lineage_json(path: Path, item: PortfolioBandLineage) -> Path:
    return _write_json(path, portfolio_band_lineage_to_dict(item))

def write_portfolio_band_compliance_audit_json(path: Path, item: PortfolioBandComplianceAudit) -> Path:
    return _write_json(path, portfolio_band_compliance_audit_to_dict(item))

def write_portfolio_band_final_review_json(path: Path, item: PortfolioBandFinalReview) -> Path:
    return _write_json(path, portfolio_band_final_review_to_dict(item))

def write_portfolio_band_closure_certificate_json(path: Path, item: PortfolioBandClosureCertificate) -> Path:
    return _write_json(path, portfolio_band_closure_certificate_to_dict(item))

def write_phase158_handoff_contract_json(path: Path, item: Phase158HandoffContract) -> Path:
    return _write_json(path, phase158_handoff_contract_to_dict(item))

def write_phase158_handoff_package_json(path: Path, item: Phase158HandoffPackage) -> Path:
    return _write_json(path, phase158_handoff_package_to_dict(item))

def write_portfolio_risk_safety_boundary_json(path: Path, item: PortfolioRiskSafetyBoundaryResult) -> Path:
    return _write_json(path, portfolio_risk_safety_boundary_result_to_dict(item))

def write_phase158_readiness_gate_json(path: Path, item: Phase158ReadinessGate) -> Path:
    return _write_json(path, phase158_readiness_gate_to_dict(item))

def read_portfolio_risk_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_portfolio_risk_reviews(data_root: Path) -> List[Path]:
    p = portfolio_risk_reviews_dir(data_root)
    if not p.exists(): return []
    return sorted(list(p.glob("*.json")))

def get_latest_portfolio_risk_review(data_root: Path) -> Optional[Path]:
    reviews = list_portfolio_risk_reviews(data_root)
    return reviews[-1] if reviews else None

def portfolio_risk_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"reviews": len(list_portfolio_risk_reviews(data_root))}
