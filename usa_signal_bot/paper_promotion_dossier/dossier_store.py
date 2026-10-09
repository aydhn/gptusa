"""Local JSON/JSONL store for promotion dossier artifacts (metadata only)."""
from pathlib import Path
from typing import Any, Dict, List, Optional

from usa_signal_bot.paper_common.io import (
    count_files, ensure_dir, list_files, read_json, write_json, write_jsonl,
)
from .dossier_models import (
    FinalSafetyBoardReview, ObserverPromotionDossier, PromotionDossierAuditEntry,
    PromotionDossierReview, PromotionEvidenceIndex, StagedPaperReadinessPackage,
    final_safety_board_review_to_dict, observer_promotion_dossier_to_dict,
    promotion_dossier_audit_entry_to_dict, promotion_dossier_review_to_dict,
    promotion_evidence_index_to_dict, staged_paper_readiness_package_to_dict,
)


def promotion_dossier_store_dir(data_root: Path) -> Path:
    return ensure_dir(Path(data_root) / "paper_promotion_dossier")


def _sub(data_root: Path, name: str) -> Path:
    return ensure_dir(promotion_dossier_store_dir(data_root) / name)


def promotion_dossiers_dir(data_root: Path) -> Path:
    return _sub(data_root, "dossiers")


def promotion_evidence_indexes_dir(data_root: Path) -> Path:
    return _sub(data_root, "evidence_indexes")


def final_safety_board_reviews_dir(data_root: Path) -> Path:
    return _sub(data_root, "board_reviews")


def staged_readiness_packages_dir(data_root: Path) -> Path:
    return _sub(data_root, "readiness_packages")


def promotion_dossier_audit_dir(data_root: Path) -> Path:
    return _sub(data_root, "audit")


def promotion_dossier_full_reviews_dir(data_root: Path) -> Path:
    return _sub(data_root, "full_reviews")


def write_promotion_dossier_json(path: Path, item: ObserverPromotionDossier) -> Path:
    return write_json(path, observer_promotion_dossier_to_dict(item), ensure_parent=False)


def write_promotion_evidence_index_json(path: Path, item: PromotionEvidenceIndex) -> Path:
    return write_json(path, promotion_evidence_index_to_dict(item), ensure_parent=False)


def write_final_safety_board_review_json(path: Path, item: FinalSafetyBoardReview) -> Path:
    return write_json(path, final_safety_board_review_to_dict(item), ensure_parent=False)


def write_staged_readiness_package_json(path: Path, item: StagedPaperReadinessPackage) -> Path:
    return write_json(path, staged_paper_readiness_package_to_dict(item), ensure_parent=False)


def write_promotion_dossier_audit_jsonl(path: Path, items: List[PromotionDossierAuditEntry]) -> Path:
    return write_jsonl(path, (promotion_dossier_audit_entry_to_dict(i) for i in items), ensure_parent=False)


def write_promotion_dossier_full_review_json(path: Path, item: PromotionDossierReview) -> Path:
    return write_json(path, promotion_dossier_review_to_dict(item), ensure_parent=False)


def read_promotion_dossier_full_review_json(path: Path) -> Dict[str, Any]:
    return read_json(path)


def list_promotion_dossier_full_reviews(data_root: Path) -> List[Path]:
    return list_files(promotion_dossier_full_reviews_dir(data_root), "*.json", sort=True)


def get_latest_promotion_dossier_full_review(data_root: Path) -> Optional[Path]:
    files = list_promotion_dossier_full_reviews(data_root)
    return files[-1] if files else None


def promotion_dossier_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "dossiers": count_files(promotion_dossiers_dir(data_root), "*.json"),
        "evidence_indexes": count_files(promotion_evidence_indexes_dir(data_root), "*.json"),
        "board_reviews": count_files(final_safety_board_reviews_dir(data_root), "*.json"),
        "readiness_packages": count_files(staged_readiness_packages_dir(data_root), "*.json"),
        "full_reviews": count_files(promotion_dossier_full_reviews_dir(data_root), "*.json"),
    }
