from pathlib import Path
from typing import Dict, Any, List, Optional
import json

from usa_signal_bot.core_runtime_acceptance.phase105_models import (
    LifecycleReviewIngestionResult,
    ConsolidationEvidenceItem,
    CoreRuntimeAcceptanceReport,
    AdvancedFoundationFreezeBundle,
    DataProviderExpansionKickoffGate,
    CoreRuntimeAcceptanceFullReview,
    lifecycle_review_ingestion_result_to_dict,
    consolidation_evidence_item_to_dict,
    core_runtime_acceptance_report_to_dict,
    advanced_foundation_freeze_bundle_to_dict,
    data_provider_expansion_kickoff_gate_to_dict,
    core_runtime_acceptance_full_review_to_dict
)

def acceptance_store_dir(data_root: Path) -> Path:
    d = data_root / "core_runtime_acceptance"
    d.mkdir(parents=True, exist_ok=True)
    return d

def lifecycle_ingestions_dir(data_root: Path) -> Path:
    d = acceptance_store_dir(data_root) / "lifecycle_ingestions"
    d.mkdir(parents=True, exist_ok=True)
    return d

def evidence_dir(data_root: Path) -> Path:
    d = acceptance_store_dir(data_root) / "evidence"
    d.mkdir(parents=True, exist_ok=True)
    return d

def acceptance_reports_dir(data_root: Path) -> Path:
    d = acceptance_store_dir(data_root) / "acceptance_reports"
    d.mkdir(parents=True, exist_ok=True)
    return d

def foundation_freezes_dir(data_root: Path) -> Path:
    d = acceptance_store_dir(data_root) / "foundation_freezes"
    d.mkdir(parents=True, exist_ok=True)
    return d

def kickoff_gates_dir(data_root: Path) -> Path:
    d = acceptance_store_dir(data_root) / "kickoff_gates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def full_reviews_dir(data_root: Path) -> Path:
    d = acceptance_store_dir(data_root) / "full_reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_lifecycle_ingestion_json(path: Path, item: LifecycleReviewIngestionResult) -> Path:
    path.write_text(json.dumps(lifecycle_review_ingestion_result_to_dict(item), indent=2))
    return path

def write_consolidation_evidence_jsonl(path: Path, items: List[ConsolidationEvidenceItem]) -> Path:
    with path.open('w') as f:
        for item in items:
            f.write(json.dumps(consolidation_evidence_item_to_dict(item)) + "\n")
    return path

def write_core_runtime_acceptance_report_json(path: Path, item: CoreRuntimeAcceptanceReport) -> Path:
    path.write_text(json.dumps(core_runtime_acceptance_report_to_dict(item), indent=2))
    return path

def write_advanced_foundation_freeze_json(path: Path, item: AdvancedFoundationFreezeBundle) -> Path:
    path.write_text(json.dumps(advanced_foundation_freeze_bundle_to_dict(item), indent=2))
    return path

def write_data_provider_kickoff_gate_json(path: Path, item: DataProviderExpansionKickoffGate) -> Path:
    path.write_text(json.dumps(data_provider_expansion_kickoff_gate_to_dict(item), indent=2))
    return path

def write_core_runtime_acceptance_full_review_json(path: Path, item: CoreRuntimeAcceptanceFullReview) -> Path:
    path.write_text(json.dumps(core_runtime_acceptance_full_review_to_dict(item), indent=2))
    return path

def read_core_runtime_acceptance_full_review_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def list_core_runtime_acceptance_reviews(data_root: Path) -> List[Path]:
    d = full_reviews_dir(data_root)
    return sorted(d.glob("*.json"))

def get_latest_core_runtime_acceptance_review(data_root: Path) -> Optional[Path]:
    files = list_core_runtime_acceptance_reviews(data_root)
    return files[-1] if files else None

def acceptance_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews": len(list_core_runtime_acceptance_reviews(data_root))
    }
