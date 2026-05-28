import datetime
from typing import Any, Dict, List
from usa_signal_bot.core.enums import EngineReadinessCertificateStatus
from usa_signal_bot.feature_engine.final_closure.phase125_models import (
    FinalClosureManifest,
    FreezeSealMetadata,
    EngineReadinessCertificate,
    create_engine_readiness_certificate_id
)

def build_engine_readiness_certificate(manifest: FinalClosureManifest, seal: FreezeSealMetadata) -> EngineReadinessCertificate:
    valid = manifest.final_manifest_valid and seal.sealed
    return EngineReadinessCertificate(
        certificate_id=create_engine_readiness_certificate_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=EngineReadinessCertificateStatus.CERTIFIED if valid else EngineReadinessCertificateStatus.BLOCKED,
        certificate_version="phase125.v1",
        source_seal_id=seal.seal_id,
        feature_factor_engine_closed=valid,
        freeze_seal_valid=seal.sealed,
        final_manifest_valid=manifest.final_manifest_valid,
        schema_contract_available=valid,
        lineage_contract_available=valid,
        safety_contract_available=valid,
        factor_tables_available=valid,
        factor_diagnostics_available=valid,
        research_reports_available=valid,
        ready_for_phase126=valid,
        certified_for_research_handoff=valid,
        certified_for_trading_activation=False,
        certified_for_deployment=False,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[] if valid else ["Manifest or seal invalid"],
        risk_flags=[],
        metadata={}
    )

def validate_engine_readiness_certificate(certificate: EngineReadinessCertificate) -> List[str]:
    errs = []
    if certificate.certified_for_trading_activation: errs.append("certified_for_trading_activation is true")
    if certificate.certified_for_deployment: errs.append("certified_for_deployment is true")
    if not certificate.research_data_only: errs.append("research_data_only is false")
    if certificate.activation_allowed: errs.append("activation_allowed is true")
    return errs

def engine_certificate_valid(certificate: EngineReadinessCertificate) -> bool:
    return len(validate_engine_readiness_certificate(certificate)) == 0

def engine_readiness_certificate_summary(certificate: EngineReadinessCertificate) -> Dict[str, Any]:
    return {
        "certified": certificate.status == EngineReadinessCertificateStatus.CERTIFIED,
        "valid": engine_certificate_valid(certificate)
    }

def engine_readiness_certificate_to_text(certificate: EngineReadinessCertificate, limit: int = 300) -> str:
    return f"EngineCertificate({certificate.certificate_id}): Status={certificate.status.value}"
