import json
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
    p.mkdir(parents=True, exist_ok=True)
    return p

def adjacent_rehearsal_runs_dir(data_root: Path) -> Path:
    p = controlled_planning_store_dir(data_root) / "rehearsals"
    p.mkdir(parents=True, exist_ok=True)
    return p

def approval_queue_dir(data_root: Path) -> Path:
    p = controlled_planning_store_dir(data_root) / "approval_queue"
    p.mkdir(parents=True, exist_ok=True)
    return p

def planning_audit_dir(data_root: Path) -> Path:
    p = controlled_planning_store_dir(data_root) / "audit"
    p.mkdir(parents=True, exist_ok=True)
    return p

def planning_reviews_dir(data_root: Path) -> Path:
    p = controlled_planning_store_dir(data_root) / "reviews"
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_controlled_planning_ticket_json(path: Path, item: ControlledPlanningTicket) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(controlled_planning_ticket_to_dict(item), f, indent=2)
    return path

def write_paper_adjacent_rehearsal_run_json(path: Path, item: PaperAdjacentRehearsalRun) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(paper_adjacent_rehearsal_run_to_dict(item), f, indent=2)
    return path

def write_approval_queue_item_json(path: Path, item: FinalHumanApprovalQueueItem) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(final_human_approval_queue_item_to_dict(item), f, indent=2)
    return path

def write_controlled_planning_audit_jsonl(path: Path, items: List[ControlledPlanningAuditEntry]) -> Path:
    with open(path, "a", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(controlled_planning_audit_entry_to_dict(item)) + "\n")
    return path

def write_controlled_planning_review_json(path: Path, item: ControlledPlanningReview) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(controlled_planning_review_to_dict(item), f, indent=2)
    return path

def read_controlled_planning_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_controlled_planning_reviews(data_root: Path) -> List[Path]:
    dir_path = planning_reviews_dir(data_root)
    return sorted(dir_path.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)

def get_latest_controlled_planning_review(data_root: Path) -> Optional[Path]:
    files = list_controlled_planning_reviews(data_root)
    return files[0] if files else None

def controlled_planning_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "tickets_count": len(list(planning_tickets_dir(data_root).glob("*.json"))),
        "rehearsals_count": len(list(adjacent_rehearsal_runs_dir(data_root).glob("*.json"))),
        "approval_queue_count": len(list(approval_queue_dir(data_root).glob("*.json"))),
        "reviews_count": len(list_controlled_planning_reviews(data_root))
    }
