from typing import Any, Dict, List
import datetime
import hashlib
import json

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    PortfolioBandClosureCertificate,
    PortfolioBandFinalReview,
    create_portfolio_band_closure_certificate_id
)
from usa_signal_bot.core.enums import PortfolioBandClosureStatus

def build_portfolio_band_closure_certificate(final_review: PortfolioBandFinalReview) -> PortfolioBandClosureCertificate:
    passed = final_review.final_review_passed
    cert = PortfolioBandClosureCertificate(
        certificate_id=create_portfolio_band_closure_certificate_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        band_name="Phase 153-157 Portfolio Construction and Risk Governance",
        start_phase=153,
        end_phase=157,
        closed=passed,
        closure_status=PortfolioBandClosureStatus.PASSED if passed else PortfolioBandClosureStatus.BLOCKED,
        final_review_id=final_review.review_id,
        compliance_audit_id=final_review.compliance_audit.audit_id,
        closure_hash=None,
        limitations=[
            "Sandbox optimizer output is not an actual target weight.",
            "Risk report is not investment advice.",
            "Live/paper/broker trading is explicitly disabled.",
            "Actual capital allocation is not allowed.",
            "Capital deployment is not allowed.",
            "Backtest/optimizer artifacts are restricted to historical/research-only contexts.",
            "Phase 158 integration handoff is not a deployment approval."
        ],
        next_phase=158,
        ready_for_phase158=passed,
        not_deployment_approval=True,
        not_strategy_activation=True,
        not_investment_advice=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    cert.closure_hash = compute_portfolio_band_closure_certificate_hash(cert)
    return cert

def compute_portfolio_band_closure_certificate_hash(certificate: PortfolioBandClosureCertificate) -> str:
    from usa_signal_bot.portfolio.risk_reporting.phase157_models import portfolio_band_closure_certificate_to_dict
    d = portfolio_band_closure_certificate_to_dict(certificate)
    d.pop("closure_hash", None)
    return hashlib.sha256(json.dumps(d, sort_keys=True).encode('utf-8')).hexdigest()

def validate_portfolio_band_closure_certificate(certificate: PortfolioBandClosureCertificate) -> List[str]:
    return []

def portfolio_band_closure_certificate_to_text(certificate: PortfolioBandClosureCertificate, limit: int = 300) -> str:
    return f"Closure Certificate {certificate.certificate_id}: closed={certificate.closed}"
