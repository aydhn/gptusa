"""Freeze Preparation Store."""
import json
from pathlib import Path
from typing import Any

from .phase124_models import (
    FreezePreparationContext,
    FreezePreparationFullReview,
    ArtifactChainIntegrityResult,
    IntegrationRehearsalResult,
    ReportQaAcceptanceGate,
    FreezeCandidateManifest,
    FreezePreparationGate,
    freeze_preparation_context_to_dict,
    freeze_preparation_full_review_to_dict,
    artifact_chain_integrity_result_to_dict,
    integration_rehearsal_result_to_dict,
    report_qa_acceptance_gate_to_dict,
    freeze_candidate_manifest_to_dict,
    freeze_preparation_gate_to_dict
)

def freeze_preparation_store_dir(data_root: Path) -> Path:
    d = data_root / "feature_engine" / "integration_freeze"
    d.mkdir(parents=True, exist_ok=True)
    return d

def freeze_preparation_contexts_dir(data_root: Path) -> Path:
    d = freeze_preparation_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def freeze_preparation_reviews_dir(data_root: Path) -> Path:
    d = freeze_preparation_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def artifact_chain_dir(data_root: Path) -> Path:
    d = freeze_preparation_store_dir(data_root) / "artifact_chain"
    d.mkdir(parents=True, exist_ok=True)
    return d

def integration_rehearsal_dir(data_root: Path) -> Path:
    d = freeze_preparation_store_dir(data_root) / "rehearsal"
    d.mkdir(parents=True, exist_ok=True)
    return d

def report_qa_acceptance_dir(data_root: Path) -> Path:
    d = freeze_preparation_store_dir(data_root) / "report_qa"
    d.mkdir(parents=True, exist_ok=True)
    return d

def freeze_manifests_dir(data_root: Path) -> Path:
    d = freeze_preparation_store_dir(data_root) / "freeze_manifests"
    d.mkdir(parents=True, exist_ok=True)
    return d

def freeze_gates_dir(data_root: Path) -> Path:
    d = freeze_preparation_store_dir(data_root) / "freeze_gates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_freeze_preparation_context_json(path: Path, item: FreezePreparationContext) -> Path:
    with open(path, "w") as f:
        json.dump(freeze_preparation_context_to_dict(item), f, indent=2)
    return path

def write_freeze_preparation_full_review_json(path: Path, item: FreezePreparationFullReview) -> Path:
    with open(path, "w") as f:
        json.dump(freeze_preparation_full_review_to_dict(item), f, indent=2)
    return path

def write_artifact_chain_integrity_json(path: Path, item: ArtifactChainIntegrityResult) -> Path:
    with open(path, "w") as f:
        json.dump(artifact_chain_integrity_result_to_dict(item), f, indent=2)
    return path

def write_integration_rehearsal_result_json(path: Path, item: IntegrationRehearsalResult) -> Path:
    with open(path, "w") as f:
        json.dump(integration_rehearsal_result_to_dict(item), f, indent=2)
    return path

def write_report_qa_acceptance_gate_json(path: Path, item: ReportQaAcceptanceGate) -> Path:
    with open(path, "w") as f:
        json.dump(report_qa_acceptance_gate_to_dict(item), f, indent=2)
    return path

def write_freeze_candidate_manifest_json(path: Path, item: FreezeCandidateManifest) -> Path:
    with open(path, "w") as f:
        json.dump(freeze_candidate_manifest_to_dict(item), f, indent=2)
    return path

def write_freeze_preparation_gate_json(path: Path, item: FreezePreparationGate) -> Path:
    with open(path, "w") as f:
        json.dump(freeze_preparation_gate_to_dict(item), f, indent=2)
    return path

def read_freeze_preparation_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_freeze_preparation_reviews(data_root: Path) -> list[Path]:
    d = freeze_preparation_reviews_dir(data_root)
    return list(d.glob("*.json"))

def get_latest_freeze_preparation_review(data_root: Path) -> Path | None:
    files = list_freeze_preparation_reviews(data_root)
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_mtime)

def freeze_preparation_store_summary(data_root: Path) -> dict[str, Any]:
    return {"review_count": len(list_freeze_preparation_reviews(data_root))}
