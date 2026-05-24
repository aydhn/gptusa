import json
from pathlib import Path
from typing import Any
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
    with open(path, "r") as f:
        return json.load(f)

def list_board_dossier_full_reviews(data_root: Path) -> list[Path]:
    d = board_dossier_full_reviews_dir(data_root)
    if not d.exists():
        return []
    return sorted(list(d.glob("*.json")), reverse=True)

def get_latest_board_dossier_full_review(data_root: Path) -> Path | None:
    files = list_board_dossier_full_reviews(data_root)
    return files[0] if files else None

def board_dossier_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "dossiers": len(list(board_dossiers_dir(data_root).glob("*.json"))) if board_dossiers_dir(data_root).exists() else 0,
        "acceptance_seals": len(list(acceptance_board_seals_dir(data_root).glob("*.json"))) if acceptance_board_seals_dir(data_root).exists() else 0,
        "full_reviews": len(list(board_dossier_full_reviews_dir(data_root).glob("*.json"))) if board_dossier_full_reviews_dir(data_root).exists() else 0
    }
