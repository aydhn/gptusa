import json
from pathlib import Path
from typing import Any
from usa_signal_bot.paper_common.io import read_json, list_files, count_files
from usa_signal_bot.core.serialization import dataclass_to_dict
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import (
    PaperReadinessBoardDossier,
    BoardDossierEvidenceItem,
    AcceptanceBoardSeal,
    ShadowLaunchBlockerRule,
    ShadowLaunchBlockerEvent,
    BoardDossierAuditEntry,
    BoardDossierFullReview
)

def board_dossier_store_dir(data_root: Path) -> Path:
    return data_root / "paper_readiness_board_dossier"

def board_dossiers_dir(data_root: Path) -> Path:
    return board_dossier_store_dir(data_root) / "dossiers"

def board_dossier_evidence_dir(data_root: Path) -> Path:
    return board_dossier_store_dir(data_root) / "evidence"

def acceptance_board_seals_dir(data_root: Path) -> Path:
    return board_dossier_store_dir(data_root) / "acceptance_board_seals"

def shadow_launch_blocker_rules_dir(data_root: Path) -> Path:
    return board_dossier_store_dir(data_root) / "shadow_launch_blocker_rules"

def shadow_launch_blocker_events_dir(data_root: Path) -> Path:
    return board_dossier_store_dir(data_root) / "shadow_launch_blocker_events"

def board_dossier_audit_dir(data_root: Path) -> Path:
    return board_dossier_store_dir(data_root) / "audit"

def board_dossier_full_reviews_dir(data_root: Path) -> Path:
    return board_dossier_store_dir(data_root) / "full_reviews"

def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def write_board_dossier_json(path: Path, item: PaperReadinessBoardDossier) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        json.dump(dataclass_to_dict(item), f, indent=2, cls=type())
    return path

def write_board_dossier_evidence_jsonl(path: Path, items: list[BoardDossierEvidenceItem]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dataclass_to_dict(item), cls=type()) + "\n")
    return path

def write_acceptance_board_seal_json(path: Path, item: AcceptanceBoardSeal) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        json.dump(dataclass_to_dict(item), f, indent=2, cls=type())
    return path

def write_shadow_launch_blocker_rules_jsonl(path: Path, items: list[ShadowLaunchBlockerRule]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dataclass_to_dict(item), cls=type()) + "\n")
    return path

def write_shadow_launch_blocker_events_jsonl(path: Path, items: list[ShadowLaunchBlockerEvent]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dataclass_to_dict(item), cls=type()) + "\n")
    return path

def write_board_dossier_audit_jsonl(path: Path, items: list[BoardDossierAuditEntry]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dataclass_to_dict(item), cls=type()) + "\n")
    return path

def write_board_dossier_full_review_json(path: Path, item: BoardDossierFullReview) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        json.dump(dataclass_to_dict(item), f, indent=2, cls=type())
    return path

def read_board_dossier_full_review_json(path: Path) -> dict[str, Any]:
    return read_json(path)

def list_board_dossier_full_reviews(data_root: Path) -> list[Path]:
    return list_files(board_dossier_full_reviews_dir(data_root), "*.json", sort=True, reverse=True)

def get_latest_board_dossier_full_review(data_root: Path) -> Path | None:
    files = list_board_dossier_full_reviews(data_root)
    return files[0] if files else None

def board_dossier_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "dossiers": count_files(board_dossiers_dir(data_root), "*.json"),
        "acceptance_seals": count_files(acceptance_board_seals_dir(data_root), "*.json"),
        "full_reviews": count_files(board_dossier_full_reviews_dir(data_root), "*.json")
    }
