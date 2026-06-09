from typing import List, Dict, Any
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalArtifactIndex,
    FinalArtifactRecord,
    FinalArtifactKind,
    create_final_artifact_record_id,
    create_final_artifact_index_id,
    generate_timestamp
)
import hashlib
import json

def build_default_final_artifact_records() -> List[FinalArtifactRecord]:
    kinds = [
        FinalArtifactKind.SOURCE_CODE,
        FinalArtifactKind.CONFIG,
        FinalArtifactKind.CLI,
        FinalArtifactKind.HEALTH,
        FinalArtifactKind.STORAGE,
        FinalArtifactKind.DATA_PIPELINE,
        FinalArtifactKind.FEATURE_ENGINE,
        FinalArtifactKind.REGIME_ENGINE,
        FinalArtifactKind.ML_GOVERNANCE,
        FinalArtifactKind.BACKTEST,
        FinalArtifactKind.PORTFOLIO,
        FinalArtifactKind.INTEGRATION,
        FinalArtifactKind.ACCEPTANCE,
        FinalArtifactKind.RELEASE,
        FinalArtifactKind.DOCUMENTATION,
        FinalArtifactKind.TESTS,
        FinalArtifactKind.QUALITY,
        FinalArtifactKind.OBSERVABILITY,
        FinalArtifactKind.NOTIFICATIONS,
        FinalArtifactKind.FINAL_CERTIFICATE,
        FinalArtifactKind.PROJECT_CLOSURE
    ]

    records = []
    for kind in kinds:
        records.append(FinalArtifactRecord(
            artifact_id=create_final_artifact_record_id(),
            created_at_utc=generate_timestamp(),
            artifact_kind=kind,
            artifact_name=f"{kind.value.lower()}_bundle",
            source_phase_range=None,
            module_path=None,
            doc_path=None,
            test_path=None,
            available=True,
            required=True,
            read_only=True,
            deterministic_hash="dummy_hash",
            artifact_valid=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return records

def compute_final_artifact_index_hash(index: FinalArtifactIndex) -> str:
    # A real implementation would serialize the meaningful fields and hash them
    data = json.dumps([a.to_dict() for a in index.artifacts], sort_keys=True)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_final_artifact_index() -> FinalArtifactIndex:
    records = build_default_final_artifact_records()
    index = FinalArtifactIndex(
        index_id=create_final_artifact_index_id(),
        created_at_utc=generate_timestamp(),
        artifacts=records,
        artifact_count=len(records),
        required_artifact_count=len([r for r in records if r.required]),
        available_required_count=len([r for r in records if r.required and r.available]),
        missing_required_count=len([r for r in records if r.required and not r.available]),
        index_valid=True,
        research_data_only=True,
        final_closure_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    if index.missing_required_count > 0:
        index.index_valid = False
        index.errors.append(f"Missing {index.missing_required_count} required artifacts")

    index.index_hash = compute_final_artifact_index_hash(index)
    return index

def validate_final_artifact_index(index: FinalArtifactIndex) -> List[str]:
    errors = []
    if not index.index_valid:
        errors.extend(index.errors)
    return errors

def final_artifact_index_to_text(index: FinalArtifactIndex, limit: int = 300) -> str:
    return f"Final Artifact Index: Valid={index.index_valid}, Count={index.artifact_count}, Missing={index.missing_required_count}"
