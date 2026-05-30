from typing import Any, Dict
import hashlib
import json
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import (
    ResearchFreezeArtifactReference,
    ResearchFreezePackage
)

def stable_json_dumps(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(',', ':'))

def compute_payload_hash(payload: Dict[str, Any]) -> str:
    return hashlib.sha256(stable_json_dumps(payload).encode('utf-8')).hexdigest()

def compute_text_hash(text: str) -> str:
    if text is None:
        return hashlib.sha256(b"").hexdigest()
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def compute_artifact_reference_hash(reference: ResearchFreezeArtifactReference) -> str:
    data = {
        "reference_id": reference.reference_id,
        "artifact_kind": reference.artifact_kind.value if hasattr(reference.artifact_kind, 'value') else reference.artifact_kind,
        "artifact_name": reference.artifact_name,
        "source_phase": reference.source_phase,
        "source_path": reference.source_path,
        "source_review_id": reference.source_review_id,
        "required": reference.required,
        "available": reference.available,
        "immutable": reference.immutable
    }
    return compute_payload_hash(data)

def compute_research_freeze_package_hash(package: ResearchFreezePackage) -> str:
    data = {
        "package_id": package.package_id,
        "package_name": package.package_name,
        "package_version": package.package_version,
        "required_artifact_count": package.required_artifact_count,
        "available_required_artifact_count": package.available_required_artifact_count,
        "missing_required_artifact_count": package.missing_required_artifact_count,
        "drift_report_id": package.drift_report.document_id if package.drift_report else None,
        "monitoring_validation_id": package.monitoring_validation.validation_id if package.monitoring_validation else None
    }
    return compute_payload_hash(data)

def compute_research_freeze_manifest_hash(package: ResearchFreezePackage) -> str:
    refs = [compute_artifact_reference_hash(r) for r in package.artifact_references]
    return compute_payload_hash({"refs": refs})

def validate_hash_value(value: str | None) -> bool:
    if not value:
        return False
    return len(value) == 64 and all(c in "0123456789abcdef" for c in value)
