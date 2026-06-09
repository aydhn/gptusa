from typing import Any, Dict, List
import datetime
import hashlib
import json

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    Phase158HandoffPackage,
    Phase158HandoffContract,
    PortfolioBandClosureCertificate,
    PortfolioBandFinalReview,
    PortfolioRiskSummary,
    PortfolioGovernanceReport,
    PortfolioBandLineage,
    create_phase158_handoff_package_id
)

def build_phase158_handoff_package(contract: Phase158HandoffContract, certificate: PortfolioBandClosureCertificate, final_review: PortfolioBandFinalReview, risk_summary: PortfolioRiskSummary, governance_reports: List[PortfolioGovernanceReport], lineage: PortfolioBandLineage) -> Phase158HandoffPackage:
    package = Phase158HandoffPackage(
        package_id=create_phase158_handoff_package_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        contract=contract,
        closure_certificate=certificate,
        risk_summary=risk_summary,
        governance_reports=governance_reports,
        band_lineage=lineage,
        package_hash=None,
        package_valid=True,
        read_only=True,
        research_data_only=True,
        integration_handoff_only=True,
        live_trading_enabled=False,
        paper_trading_enabled=False,
        broker_execution_enabled=False,
        actual_target_weights_produced=False,
        actual_allocation_produced=False,
        order_size_produced=False,
        capital_deployment_allowed=False,
        deployment_allowed=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    package.package_hash = compute_phase158_handoff_package_hash(package)
    return package

def compute_phase158_handoff_package_hash(package: Phase158HandoffPackage) -> str:
    from usa_signal_bot.portfolio.risk_reporting.phase157_models import phase158_handoff_package_to_dict
    d = phase158_handoff_package_to_dict(package)
    d.pop("package_hash", None)
    return hashlib.sha256(json.dumps(d, sort_keys=True).encode('utf-8')).hexdigest()

def validate_phase158_handoff_package(package: Phase158HandoffPackage) -> List[str]:
    return []

def phase158_handoff_package_to_text(package: Phase158HandoffPackage, limit: int = 300) -> str:
    return f"Handoff Package {package.package_id}: valid={package.package_valid}"
