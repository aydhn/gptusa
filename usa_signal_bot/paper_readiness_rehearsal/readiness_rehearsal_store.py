import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import (
    StageRehearsalPlan, StageRehearsalResult, ReadinessRehearsalRun, FinalReviewLock,
    GuardedHandoffRegistryEntry, HandoffEvidenceIndex, ReadinessRehearsalAuditEntry,
    ReadinessRehearsalReview, stage_rehearsal_plan_to_dict, stage_rehearsal_result_to_dict,
    readiness_rehearsal_run_to_dict, final_review_lock_to_dict, guarded_handoff_registry_entry_to_dict,
    handoff_evidence_index_to_dict, readiness_rehearsal_audit_entry_to_dict, readiness_rehearsal_review_to_dict
)

def readiness_rehearsal_store_dir(data_root: Path) -> Path:
    p = data_root / "paper_readiness_rehearsal"
    p.mkdir(parents=True, exist_ok=True)
    return p

def stage_plans_dir(data_root: Path) -> Path:
    p = readiness_rehearsal_store_dir(data_root) / "stage_plans"
    p.mkdir(parents=True, exist_ok=True)
    return p

def stage_results_dir(data_root: Path) -> Path:
    p = readiness_rehearsal_store_dir(data_root) / "stage_results"
    p.mkdir(parents=True, exist_ok=True)
    return p

def rehearsal_runs_dir(data_root: Path) -> Path:
    p = readiness_rehearsal_store_dir(data_root) / "runs"
    p.mkdir(parents=True, exist_ok=True)
    return p

def final_locks_dir(data_root: Path) -> Path:
    p = readiness_rehearsal_store_dir(data_root) / "final_locks"
    p.mkdir(parents=True, exist_ok=True)
    return p

def handoff_registry_dir(data_root: Path) -> Path:
    p = readiness_rehearsal_store_dir(data_root) / "handoff_registry"
    p.mkdir(parents=True, exist_ok=True)
    return p

def handoff_evidence_indexes_dir(data_root: Path) -> Path:
    p = readiness_rehearsal_store_dir(data_root) / "evidence_indexes"
    p.mkdir(parents=True, exist_ok=True)
    return p

def readiness_rehearsal_audit_dir(data_root: Path) -> Path:
    p = readiness_rehearsal_store_dir(data_root) / "audit"
    p.mkdir(parents=True, exist_ok=True)
    return p

def readiness_rehearsal_reviews_dir(data_root: Path) -> Path:
    p = readiness_rehearsal_store_dir(data_root) / "reviews"
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_stage_rehearsal_plans_jsonl(path: Path, items: List[StageRehearsalPlan]) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(stage_rehearsal_plan_to_dict(item)) + "\n")
    return path

def write_stage_rehearsal_results_jsonl(path: Path, items: List[StageRehearsalResult]) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(stage_rehearsal_result_to_dict(item)) + "\n")
    return path

def write_readiness_rehearsal_run_json(path: Path, item: ReadinessRehearsalRun) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(readiness_rehearsal_run_to_dict(item), f, indent=2)
    return path

def write_final_review_lock_json(path: Path, item: FinalReviewLock) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(final_review_lock_to_dict(item), f, indent=2)
    return path

def write_guarded_handoff_entry_json(path: Path, item: GuardedHandoffRegistryEntry) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(guarded_handoff_registry_entry_to_dict(item), f, indent=2)
    return path

def write_handoff_evidence_index_json(path: Path, item: HandoffEvidenceIndex) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(handoff_evidence_index_to_dict(item), f, indent=2)
    return path

def write_readiness_rehearsal_audit_jsonl(path: Path, items: List[ReadinessRehearsalAuditEntry]) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(readiness_rehearsal_audit_entry_to_dict(item)) + "\n")
    return path

def write_readiness_rehearsal_review_json(path: Path, item: ReadinessRehearsalReview) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(readiness_rehearsal_review_to_dict(item), f, indent=2)
    return path

def read_readiness_rehearsal_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_readiness_rehearsal_reviews(data_root: Path) -> List[Path]:
    p = readiness_rehearsal_reviews_dir(data_root)
    return sorted(list(p.glob("*.json")))

def get_latest_readiness_rehearsal_review(data_root: Path) -> Optional[Path]:
    files = list_readiness_rehearsal_reviews(data_root)
    return files[-1] if files else None

def readiness_rehearsal_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "stage_plans_files": len(list(stage_plans_dir(data_root).glob("*.jsonl"))),
        "stage_results_files": len(list(stage_results_dir(data_root).glob("*.jsonl"))),
        "rehearsal_runs": len(list(rehearsal_runs_dir(data_root).glob("*.json"))),
        "final_locks": len(list(final_locks_dir(data_root).glob("*.json"))),
        "handoff_registry_entries": len(list(handoff_registry_dir(data_root).glob("*.json"))),
        "evidence_indexes": len(list(handoff_evidence_indexes_dir(data_root).glob("*.json"))),
        "audit_files": len(list(readiness_rehearsal_audit_dir(data_root).glob("*.jsonl"))),
        "reviews": len(list(readiness_rehearsal_reviews_dir(data_root).glob("*.json")))
    }
