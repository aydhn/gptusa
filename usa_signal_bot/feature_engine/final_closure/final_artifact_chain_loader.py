import hashlib
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import FinalClosureArtifactKind, FinalClosureRiskFlag
from usa_signal_bot.feature_engine.final_closure.phase125_models import (
    FinalClosureArtifactReference,
    create_final_closure_artifact_reference_id
)

def compute_final_artifact_hash(path: Optional[Path]) -> Optional[str]:
    if not path or not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def build_final_artifact_references(data_root: Optional[Path] = None) -> List[FinalClosureArtifactReference]:
    kinds = [
        FinalClosureArtifactKind.FEATURE_FOUNDATION_REVIEW,
        FinalClosureArtifactKind.CORE_INDICATOR_REVIEW,
        FinalClosureArtifactKind.ADVANCED_FEATURE_REVIEW,
        FinalClosureArtifactKind.FEATURE_ENRICHMENT_REVIEW,
        FinalClosureArtifactKind.FACTOR_COMPOSITION_REVIEW,
        FinalClosureArtifactKind.FACTOR_SCORING_REVIEW,
        FinalClosureArtifactKind.FACTOR_VALIDATION_REVIEW,
        FinalClosureArtifactKind.EXPLAINABILITY_REVIEW,
        FinalClosureArtifactKind.FREEZE_PREPARATION_REVIEW
    ]

    refs = []
    for k in kinds:
        refs.append(FinalClosureArtifactReference(
            reference_id=create_final_closure_artifact_reference_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            artifact_kind=k,
            phase_number=None,
            artifact_name=k.value,
            artifact_path=None,
            artifact_hash=None,
            schema_signature=None,
            lineage_reference=None,
            safety_reference=None,
            required=True,
            available=False,
            immutable=True,
            research_data_only=True,
            contains_secret=False,
            contains_forbidden_columns=False,
            contains_execution_language=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return refs

def load_final_artifact_references_from_payload(payload: Dict[str, Any]) -> List[FinalClosureArtifactReference]:
    # Placeholder for test payloads
    return build_final_artifact_references()

def resolve_final_artifact_paths(data_root: Path, references: List[FinalClosureArtifactReference]) -> List[FinalClosureArtifactReference]:
    for ref in references:
        # Dummy resolution logic
        pass
    return references

def validate_final_artifact_references(references: List[FinalClosureArtifactReference]) -> List[str]:
    errors = []
    for ref in references:
        if ref.required and not ref.available:
            errors.append(f"Missing required artifact: {ref.artifact_kind.value}")
    return errors

def final_artifact_chain_loader_summary(references: List[FinalClosureArtifactReference]) -> Dict[str, Any]:
    return {
        "total": len(references),
        "available": sum(1 for r in references if r.available),
        "missing": sum(1 for r in references if r.required and not r.available)
    }

def final_artifact_chain_loader_to_text(references: List[FinalClosureArtifactReference], limit: int = 300) -> str:
    summary = final_artifact_chain_loader_summary(references)
    return f"ArtifactChain: Total {summary['total']}, Available {summary['available']}, Missing {summary['missing']}"
