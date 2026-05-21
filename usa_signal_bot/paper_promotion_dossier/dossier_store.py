import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from .dossier_models import (
    ObserverPromotionDossier,
    PromotionEvidenceIndex,
    FinalSafetyBoardReview,
    PromotionRiskRegisterItem,
    StagedPaperReadinessPackage,
    PromotionDossierAuditEntry,
    PromotionDossierReview,
    observer_promotion_dossier_to_dict,
    promotion_evidence_index_to_dict,
    final_safety_board_review_to_dict,
    promotion_risk_register_item_to_dict,
    staged_paper_readiness_package_to_dict,
    promotion_dossier_audit_entry_to_dict,
    promotion_dossier_review_to_dict
)

def promotion_dossier_store_dir(data_root: Path) -> Path:
    p = data_root / "paper_promotion_dossier"
    p.mkdir(parents=True, exist_ok=True)
    return p

def promotion_dossiers_dir(data_root: Path) -> Path:
    p = promotion_dossier_store_dir(data_root) / "dossiers"
    p.mkdir(exist_ok=True)
    return p

def evidence_indexes_dir(data_root: Path) -> Path:
    p = promotion_dossier_store_dir(data_root) / "evidence_indexes"
    p.mkdir(exist_ok=True)
    return p

def safety_board_reviews_dir(data_root: Path) -> Path:
    p = promotion_dossier_store_dir(data_root) / "safety_board"
    p.mkdir(exist_ok=True)
    return p

def risk_registers_dir(data_root: Path) -> Path:
    p = promotion_dossier_store_dir(data_root) / "risk_registers"
    p.mkdir(exist_ok=True)
    return p

def readiness_packages_dir(data_root: Path) -> Path:
    p = promotion_dossier_store_dir(data_root) / "readiness_packages"
    p.mkdir(exist_ok=True)
    return p

def promotion_dossier_audit_dir(data_root: Path) -> Path:
    p = promotion_dossier_store_dir(data_root) / "audit"
    p.mkdir(exist_ok=True)
    return p

def promotion_dossier_reviews_dir(data_root: Path) -> Path:
    p = promotion_dossier_store_dir(data_root) / "reviews"
    p.mkdir(exist_ok=True)
    return p

def write_promotion_dossier_json(path: Path, item: ObserverPromotionDossier) -> Path:
    with open(path, "w") as f:
        json.dump(observer_promotion_dossier_to_dict(item), f, indent=2)
    return path

def write_promotion_evidence_index_json(path: Path, item: PromotionEvidenceIndex) -> Path:
    with open(path, "w") as f:
        json.dump(promotion_evidence_index_to_dict(item), f, indent=2)
    return path

def write_safety_board_review_json(path: Path, item: FinalSafetyBoardReview) -> Path:
    with open(path, "w") as f:
        json.dump(final_safety_board_review_to_dict(item), f, indent=2)
    return path

def write_promotion_risk_register_jsonl(path: Path, items: List[PromotionRiskRegisterItem]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(promotion_risk_register_item_to_dict(item)) + "\n")
    return path

def write_readiness_package_json(path: Path, item: StagedPaperReadinessPackage) -> Path:
    with open(path, "w") as f:
        json.dump(staged_paper_readiness_package_to_dict(item), f, indent=2)
    return path

def write_promotion_dossier_audit_jsonl(path: Path, items: List[PromotionDossierAuditEntry]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(promotion_dossier_audit_entry_to_dict(item)) + "\n")
    return path

def write_promotion_dossier_review_json(path: Path, item: PromotionDossierReview) -> Path:
    with open(path, "w") as f:
        json.dump(promotion_dossier_review_to_dict(item), f, indent=2)
    return path

def read_promotion_dossier_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_promotion_dossier_reviews(data_root: Path) -> List[Path]:
    p = promotion_dossier_reviews_dir(data_root)
    return sorted(list(p.glob("*.json")))

def get_latest_promotion_dossier_review(data_root: Path) -> Optional[Path]:
    files = list_promotion_dossier_reviews(data_root)
    return files[-1] if files else None

def promotion_dossier_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "dossiers": len(list(promotion_dossiers_dir(data_root).glob("*.json"))),
        "safety_boards": len(list(safety_board_reviews_dir(data_root).glob("*.json"))),
        "readiness_packages": len(list(readiness_packages_dir(data_root).glob("*.json"))),
        "reviews": len(list_promotion_dossier_reviews(data_root))
    }
