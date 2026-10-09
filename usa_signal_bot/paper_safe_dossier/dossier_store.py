from typing import Any, Dict, List, Optional
from pathlib import Path
from usa_signal_bot.paper_common.io import (
    ensure_dir, write_json, write_jsonl, read_json, list_files, count_files,
)
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import (
    PaperSafeGateDossier, PaperSafeDossierEvidenceItem, NonExecutionAcceptanceSeal,
    PrePaperLocalRuntimeMap, RuntimeComponentMapItem, RuntimeRouteMapItem,
    PaperSafeDossierAuditEntry, PaperSafeDossierFullReview,
    paper_safe_gate_dossier_to_dict, paper_safe_dossier_evidence_item_to_dict,
    non_execution_acceptance_seal_to_dict, pre_paper_local_runtime_map_to_dict,
    runtime_component_map_item_to_dict, runtime_route_map_item_to_dict,
    paper_safe_dossier_audit_entry_to_dict, paper_safe_dossier_full_review_to_dict
)

def paper_safe_dossier_store_dir(data_root: Path) -> Path:
    return ensure_dir(data_root / "paper_safe_dossier")

def paper_safe_dossiers_dir(data_root: Path) -> Path:
    return ensure_dir(paper_safe_dossier_store_dir(data_root) / "dossiers")

def paper_safe_dossier_evidence_dir(data_root: Path) -> Path:
    return ensure_dir(paper_safe_dossier_store_dir(data_root) / "evidence")

def non_execution_seals_dir(data_root: Path) -> Path:
    return ensure_dir(paper_safe_dossier_store_dir(data_root) / "non_execution_seals")

def pre_paper_runtime_maps_dir(data_root: Path) -> Path:
    return ensure_dir(paper_safe_dossier_store_dir(data_root) / "pre_paper_runtime_maps")

def runtime_components_dir(data_root: Path) -> Path:
    return ensure_dir(paper_safe_dossier_store_dir(data_root) / "runtime_components")

def runtime_routes_dir(data_root: Path) -> Path:
    return ensure_dir(paper_safe_dossier_store_dir(data_root) / "runtime_routes")

def paper_safe_dossier_audit_dir(data_root: Path) -> Path:
    return ensure_dir(paper_safe_dossier_store_dir(data_root) / "audit")

def paper_safe_dossier_full_reviews_dir(data_root: Path) -> Path:
    return ensure_dir(paper_safe_dossier_store_dir(data_root) / "full_reviews")

def write_paper_safe_dossier_json(path: Path, item: PaperSafeGateDossier) -> Path:
    return write_json(path, paper_safe_gate_dossier_to_dict(item), ensure_parent=False)

def write_paper_safe_dossier_evidence_jsonl(path: Path, items: List[PaperSafeDossierEvidenceItem]) -> Path:
    return write_jsonl(path, (paper_safe_dossier_evidence_item_to_dict(i) for i in items), ensure_parent=False)

def write_non_execution_seal_json(path: Path, item: NonExecutionAcceptanceSeal) -> Path:
    return write_json(path, non_execution_acceptance_seal_to_dict(item), ensure_parent=False)

def write_pre_paper_runtime_map_json(path: Path, item: PrePaperLocalRuntimeMap) -> Path:
    return write_json(path, pre_paper_local_runtime_map_to_dict(item), ensure_parent=False)

def write_runtime_components_jsonl(path: Path, items: List[RuntimeComponentMapItem]) -> Path:
    return write_jsonl(path, (runtime_component_map_item_to_dict(i) for i in items), ensure_parent=False)

def write_runtime_routes_jsonl(path: Path, items: List[RuntimeRouteMapItem]) -> Path:
    return write_jsonl(path, (runtime_route_map_item_to_dict(i) for i in items), ensure_parent=False)

def write_paper_safe_dossier_audit_jsonl(path: Path, items: List[PaperSafeDossierAuditEntry]) -> Path:
    return write_jsonl(path, (paper_safe_dossier_audit_entry_to_dict(i) for i in items), ensure_parent=False)

def write_paper_safe_dossier_full_review_json(path: Path, item: PaperSafeDossierFullReview) -> Path:
    return write_json(path, paper_safe_dossier_full_review_to_dict(item), ensure_parent=False)

def read_paper_safe_dossier_full_review_json(path: Path) -> Dict[str, Any]:
    return read_json(path)

def list_paper_safe_dossier_full_reviews(data_root: Path) -> List[Path]:
    d = paper_safe_dossier_full_reviews_dir(data_root)
    return list_files(d, "*.json", sort=True)

def get_latest_paper_safe_dossier_full_review(data_root: Path) -> Optional[Path]:
    files = list_paper_safe_dossier_full_reviews(data_root)
    return files[-1] if files else None

def paper_safe_dossier_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "dossiers": count_files(paper_safe_dossiers_dir(data_root), "*.json"),
        "seals": count_files(non_execution_seals_dir(data_root), "*.json"),
        "runtime_maps": count_files(pre_paper_runtime_maps_dir(data_root), "*.json"),
        "full_reviews": count_files(paper_safe_dossier_full_reviews_dir(data_root), "*.json")
    }
