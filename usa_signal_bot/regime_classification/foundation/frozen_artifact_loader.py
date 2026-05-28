import json
from pathlib import Path
from typing import Any, Dict, List

from usa_signal_bot.core.exceptions import FrozenArtifactLoaderError
from usa_signal_bot.core.enums import RegimeFoundationRiskFlag
from usa_signal_bot.regime_classification.foundation.phase126_models import (
    FrozenArtifactReference,
    RegimeResearchInputBundle,
    create_frozen_artifact_reference_id,
    create_regime_research_input_bundle_id,
    _now
)

def build_frozen_artifact_references_from_final_closure(payload: dict[str, Any]) -> List[FrozenArtifactReference]:
    refs = []

    # Try to extract paths from the final closure payload's output paths
    paths = payload.get("output_paths", {})
    if not paths:
        return refs

    for key, path_val in paths.items():
        refs.append(
            FrozenArtifactReference(
                reference_id=create_frozen_artifact_reference_id(),
                created_at_utc=_now(),
                artifact_name=key,
                artifact_kind=key.split("_")[0].upper() if "_" in key else "UNKNOWN",
                source_phase=125,
                path=path_val,
                artifact_hash=None,
                schema_signature=None,
                lineage_reference=None,
                safety_reference=None,
                required_for_regime_foundation=True,
                available=True,
                immutable=True,
                research_data_only=True,
                warnings=[],
                errors=[],
                risk_flags=[],
                metadata={}
            )
        )

    return refs

def load_frozen_artifact_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FrozenArtifactLoaderError(f"Manifest path not found: {path}")

    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise FrozenArtifactLoaderError(f"Error loading artifact manifest from {path}: {e}")

def validate_frozen_artifact_references(references: List[FrozenArtifactReference]) -> List[str]:
    errors = []
    for ref in references:
        if ".." in (ref.path or ""):
            errors.append(f"Path traversal detected in reference path: {ref.path}")
        if not ref.available:
            errors.append(f"Artifact {ref.artifact_name} is marked as not available.")
    return errors

def frozen_artifact_refs_by_kind(references: List[FrozenArtifactReference], kind: str) -> List[FrozenArtifactReference]:
    return [ref for ref in references if ref.artifact_kind == kind]

def build_regime_research_input_bundle(source_review_id: str | None, references: List[FrozenArtifactReference]) -> RegimeResearchInputBundle:
    bundle_id = create_regime_research_input_bundle_id()
    created_at_utc = _now()

    warnings = []
    errors = validate_frozen_artifact_references(references)
    risk_flags = []

    if not references:
        errors.append("No frozen artifact references provided.")
        risk_flags.append(RegimeFoundationRiskFlag.FROZEN_ARTIFACTS_MISSING)

    valid = len(errors) == 0

    return RegimeResearchInputBundle(
        bundle_id=bundle_id,
        created_at_utc=created_at_utc,
        source_final_closure_review_id=source_review_id,
        frozen_artifacts=references,
        factor_table_refs=[r.reference_id for r in references if "factor" in r.artifact_name.lower()],
        factor_diagnostics_refs=[r.reference_id for r in references if "diagnostics" in r.artifact_name.lower()],
        schema_contract_refs=[r.reference_id for r in references if "schema" in r.artifact_name.lower()],
        lineage_contract_refs=[r.reference_id for r in references if "lineage" in r.artifact_name.lower()],
        safety_contract_refs=[r.reference_id for r in references if "safety" in r.artifact_name.lower()],
        research_report_refs=[r.reference_id for r in references if "report" in r.artifact_name.lower()],
        bundle_valid=valid,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=warnings,
        errors=errors,
        risk_flags=risk_flags,
        metadata={"artifact_count": len(references)}
    )

def frozen_artifact_loader_summary(bundle: RegimeResearchInputBundle) -> dict[str, Any]:
    return {
        "bundle_id": bundle.bundle_id,
        "valid": bundle.bundle_valid,
        "artifact_count": len(bundle.frozen_artifacts),
        "factor_tables": len(bundle.factor_table_refs),
        "reports": len(bundle.research_report_refs)
    }

def frozen_artifact_loader_to_text(bundle: RegimeResearchInputBundle, limit: int = 300) -> str:
    lines = [
        f"Regime Input Bundle ID: {bundle.bundle_id}",
        f"Valid: {bundle.bundle_valid}",
        f"Artifacts: {len(bundle.frozen_artifacts)}"
    ]
    if bundle.errors:
        lines.append("Errors:")
        for err in bundle.errors[:limit]:
            lines.append(f"  - {err}")
    return "\n".join(lines)
