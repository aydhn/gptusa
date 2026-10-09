from usa_signal_bot.paper_common.io import ensure_dir, write_json, write_jsonl, read_json, count_files
from pathlib import Path
from typing import Any, List, Optional
from usa_signal_bot.paper_controlled_planning.planning_models import (
    ControlledPlanningTicket,
    PaperAdjacentRehearsalRun,
    FinalHumanApprovalQueueItem,
    ControlledPlanningAuditEntry,
    ControlledPlanningReview,
    controlled_planning_ticket_to_dict,
    paper_adjacent_rehearsal_run_to_dict,
    final_human_approval_queue_item_to_dict,
    controlled_planning_audit_entry_to_dict,
    controlled_planning_review_to_dict
)

def controlled_planning_store_dir(data_root: Path) -> Path:
    return data_root / "paper_controlled_planning"

def planning_tickets_dir(data_root: Path) -> Path:
    p = controlled_planning_store_dir(data_root) / "tickets"
    ensure_dir(p)
    return p

def adjacent_rehearsal_runs_dir(data_root: Path) -> Path:
    p = controlled_planning_store_dir(data_root) / "rehearsals"
    ensure_dir(p)
    return p

def approval_queue_dir(data_root: Path) -> Path:
    p = controlled_planning_store_dir(data_root) / "approval_queue"
    ensure_dir(p)
    return p

def planning_audit_dir(data_root: Path) -> Path:
    p = controlled_planning_store_dir(data_root) / "audit"
    ensure_dir(p)
    return p

def planning_reviews_dir(data_root: Path) -> Path:
    p = controlled_planning_store_dir(data_root) / "reviews"
    ensure_dir(p)
    return p

def write_controlled_planning_ticket_json(path: Path, item: ControlledPlanningTicket) -> Path:
    return write_json(path, controlled_planning_ticket_to_dict(item), ensure_parent=False)

def write_paper_adjacent_rehearsal_run_json(path: Path, item: PaperAdjacentRehearsalRun) -> Path:
    return write_json(path, paper_adjacent_rehearsal_run_to_dict(item), ensure_parent=False)

def write_approval_queue_item_json(path: Path, item: FinalHumanApprovalQueueItem) -> Path:
    return write_json(path, final_human_approval_queue_item_to_dict(item), ensure_parent=False)

def write_controlled_planning_audit_jsonl(path: Path, items: List[ControlledPlanningAuditEntry]) -> Path:
    return write_jsonl(path, (controlled_planning_audit_entry_to_dict(item) for item in items), mode="a", ensure_parent=False)

def write_controlled_planning_review_json(path: Path, item: ControlledPlanningReview) -> Path:
    return write_json(path, controlled_planning_review_to_dict(item), ensure_parent=False)

def read_controlled_planning_review_json(path: Path) -> dict[str, Any]:
    return read_json(path)

def list_controlled_planning_reviews(data_root: Path) -> List[Path]:
    dir_path = planning_reviews_dir(data_root)
    return sorted(dir_path.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)

def get_latest_controlled_planning_review(data_root: Path) -> Optional[Path]:
    files = list_controlled_planning_reviews(data_root)
    return files[0] if files else None

def controlled_planning_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "tickets_count": count_files(planning_tickets_dir(data_root), "*.json"),
        "rehearsals_count": count_files(adjacent_rehearsal_runs_dir(data_root), "*.json"),
        "approval_queue_count": count_files(approval_queue_dir(data_root), "*.json"),
        "reviews_count": len(list_controlled_planning_reviews(data_root))
    }
