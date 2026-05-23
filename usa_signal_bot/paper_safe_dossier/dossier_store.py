from typing import Any, Dict, List, Optional
from pathlib import Path
import json
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
    d = data_root / "paper_safe_dossier"
    d.mkdir(parents=True, exist_ok=True)
    return d

def paper_safe_dossiers_dir(data_root: Path) -> Path:
    d = paper_safe_dossier_store_dir(data_root) / "dossiers"
    d.mkdir(parents=True, exist_ok=True)
    return d

def paper_safe_dossier_evidence_dir(data_root: Path) -> Path:
    d = paper_safe_dossier_store_dir(data_root) / "evidence"
    d.mkdir(parents=True, exist_ok=True)
    return d

def non_execution_seals_dir(data_root: Path) -> Path:
    d = paper_safe_dossier_store_dir(data_root) / "non_execution_seals"
    d.mkdir(parents=True, exist_ok=True)
    return d

def pre_paper_runtime_maps_dir(data_root: Path) -> Path:
    d = paper_safe_dossier_store_dir(data_root) / "pre_paper_runtime_maps"
    d.mkdir(parents=True, exist_ok=True)
    return d

def runtime_components_dir(data_root: Path) -> Path:
    d = paper_safe_dossier_store_dir(data_root) / "runtime_components"
    d.mkdir(parents=True, exist_ok=True)
    return d

def runtime_routes_dir(data_root: Path) -> Path:
    d = paper_safe_dossier_store_dir(data_root) / "runtime_routes"
    d.mkdir(parents=True, exist_ok=True)
    return d

def paper_safe_dossier_audit_dir(data_root: Path) -> Path:
    d = paper_safe_dossier_store_dir(data_root) / "audit"
    d.mkdir(parents=True, exist_ok=True)
    return d

def paper_safe_dossier_full_reviews_dir(data_root: Path) -> Path:
    d = paper_safe_dossier_store_dir(data_root) / "full_reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_paper_safe_dossier_json(path: Path, item: PaperSafeGateDossier) -> Path:
    path.write_text(json.dumps(paper_safe_gate_dossier_to_dict(item), indent=2))
    return path

def write_paper_safe_dossier_evidence_jsonl(path: Path, items: List[PaperSafeDossierEvidenceItem]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(paper_safe_dossier_evidence_item_to_dict(i)) + "\n")
    return path

def write_non_execution_seal_json(path: Path, item: NonExecutionAcceptanceSeal) -> Path:
    path.write_text(json.dumps(non_execution_acceptance_seal_to_dict(item), indent=2))
    return path

def write_pre_paper_runtime_map_json(path: Path, item: PrePaperLocalRuntimeMap) -> Path:
    path.write_text(json.dumps(pre_paper_local_runtime_map_to_dict(item), indent=2))
    return path

def write_runtime_components_jsonl(path: Path, items: List[RuntimeComponentMapItem]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(runtime_component_map_item_to_dict(i)) + "\n")
    return path

def write_runtime_routes_jsonl(path: Path, items: List[RuntimeRouteMapItem]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(runtime_route_map_item_to_dict(i)) + "\n")
    return path

def write_paper_safe_dossier_audit_jsonl(path: Path, items: List[PaperSafeDossierAuditEntry]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(paper_safe_dossier_audit_entry_to_dict(i)) + "\n")
    return path

def write_paper_safe_dossier_full_review_json(path: Path, item: PaperSafeDossierFullReview) -> Path:
    path.write_text(json.dumps(paper_safe_dossier_full_review_to_dict(item), indent=2))
    return path

def read_paper_safe_dossier_full_review_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def list_paper_safe_dossier_full_reviews(data_root: Path) -> List[Path]:
    d = paper_safe_dossier_full_reviews_dir(data_root)
    return sorted(d.glob("*.json"))

def get_latest_paper_safe_dossier_full_review(data_root: Path) -> Optional[Path]:
    files = list_paper_safe_dossier_full_reviews(data_root)
    return files[-1] if files else None

def paper_safe_dossier_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "dossiers": len(list(paper_safe_dossiers_dir(data_root).glob("*.json"))),
        "seals": len(list(non_execution_seals_dir(data_root).glob("*.json"))),
        "runtime_maps": len(list(pre_paper_runtime_maps_dir(data_root).glob("*.json"))),
        "full_reviews": len(list(paper_safe_dossier_full_reviews_dir(data_root).glob("*.json")))
    }
