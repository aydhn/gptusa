from typing import Any, Dict, List
from usa_signal_bot.core.enums import (
    ResearchFreezeArtifactKind,
    ResearchFreezeQuality,
    ResearchFreezeRiskFlag
)
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import (
    RegimeMonitoringIngestionResult,
    MonitoringValidationResult,
    DriftReportDocument,
    ResearchFreezeArtifactReference,
    ResearchFreezePackage,
    create_research_freeze_artifact_reference_id,
    create_research_freeze_package_id,
    _now_utc_str
)
from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_hashing import (
    compute_research_freeze_package_hash,
    compute_research_freeze_manifest_hash
)

def build_required_research_freeze_artifact_kinds() -> List[ResearchFreezeArtifactKind]:
    return [
        ResearchFreezeArtifactKind.REGIME_FOUNDATION_REVIEW,
        ResearchFreezeArtifactKind.REGIME_FEATURE_ENGINEERING_REVIEW,
        ResearchFreezeArtifactKind.REGIME_LABELING_REVIEW,
        ResearchFreezeArtifactKind.REGIME_TRANSITION_REVIEW,
        ResearchFreezeArtifactKind.MARKET_BEHAVIOR_REVIEW,
        ResearchFreezeArtifactKind.REGIME_ALIGNMENT_REVIEW,
        ResearchFreezeArtifactKind.CONTEXT_VALIDATION_REVIEW,
        ResearchFreezeArtifactKind.REGIME_MONITORING_REVIEW,
        ResearchFreezeArtifactKind.DRIFT_REPORT,
        ResearchFreezeArtifactKind.SAFETY_BOUNDARY_REPORT
    ]

def build_research_freeze_artifact_references(source_review_id: str | None, drift_report: DriftReportDocument) -> List[ResearchFreezeArtifactReference]:
    kinds = build_required_research_freeze_artifact_kinds()
    refs = []
    for k in kinds:
        avail = False
        if k == ResearchFreezeArtifactKind.REGIME_MONITORING_REVIEW and source_review_id:
            avail = True
        elif k == ResearchFreezeArtifactKind.DRIFT_REPORT and drift_report:
            avail = True

        ref = ResearchFreezeArtifactReference(
            reference_id=create_research_freeze_artifact_reference_id(),
            created_at_utc=_now_utc_str(),
            artifact_kind=k,
            artifact_name=k.value if hasattr(k, 'value') else k,
            source_phase=134 if k == ResearchFreezeArtifactKind.DRIFT_REPORT else 133,
            source_path=None,
            source_review_id=source_review_id if k == ResearchFreezeArtifactKind.REGIME_MONITORING_REVIEW else drift_report.document_id if k == ResearchFreezeArtifactKind.DRIFT_REPORT else None,
            artifact_hash=None,
            required=True,
            available=avail,
            immutable=True,
            research_metadata_only=True,
            activation_allowed=False,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
            warnings=[],
            errors=[],
            risk_flags=[]
        )
        if not avail:
            ref.errors.append("Artifact not available")
            ref.risk_flags.append(ResearchFreezeRiskFlag.REQUIRED_ARTIFACT_MISSING)

        refs.append(ref)
    return refs

def validate_required_artifact_coverage(references: List[ResearchFreezeArtifactReference]) -> List[str]:
    errors = []
    req_kinds = set(build_required_research_freeze_artifact_kinds())
    obs_kinds = set(r.artifact_kind for r in references if r.available)
    missing = req_kinds - obs_kinds
    for m in missing:
        errors.append(f"Missing required artifact kind: {m}")
    return errors

def build_research_freeze_package(ingestion: RegimeMonitoringIngestionResult, monitoring_validation: MonitoringValidationResult, drift_report: DriftReportDocument) -> ResearchFreezePackage:
    refs = build_research_freeze_artifact_references(ingestion.source_review_id, drift_report)
    req_count = len([r for r in refs if r.required])
    avail_count = len([r for r in refs if r.required and r.available])
    missing_count = req_count - avail_count

    pkg = ResearchFreezePackage(
        package_id=create_research_freeze_package_id(),
        created_at_utc=_now_utc_str(),
        package_name="regime_research_freeze_package",
        package_version="phase134.v1",
        artifact_references=refs,
        drift_report=drift_report,
        monitoring_validation=monitoring_validation,
        required_artifact_count=req_count,
        available_required_artifact_count=avail_count,
        missing_required_artifact_count=missing_count,
        package_hash=None,
        manifest_hash=None,
        package_valid=missing_count == 0,
        quality=ResearchFreezeQuality.HIGH if missing_count == 0 else ResearchFreezeQuality.INVALID,
        research_metadata_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        model_training_used=False,
        model_prediction_used=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[]
    )

    if not pkg.package_valid:
        pkg.errors.append("Missing required artifacts")
        pkg.risk_flags.append(ResearchFreezeRiskFlag.FREEZE_PACKAGE_INVALID)

    pkg.package_hash = compute_research_freeze_package_hash(pkg)
    pkg.manifest_hash = compute_research_freeze_manifest_hash(pkg)

    return pkg

def research_freeze_package_summary(package: ResearchFreezePackage) -> Dict[str, Any]:
    return {
        "package_id": package.package_id,
        "valid": package.package_valid,
        "missing_count": package.missing_required_artifact_count
    }

def research_freeze_package_to_text(package: ResearchFreezePackage, limit: int = 300) -> str:
    s = f"Freeze Package {package.package_id} ({package.package_version})\n"
    s += f"Valid: {package.package_valid}, Missing: {package.missing_required_artifact_count}\n"
    return s[:limit]
