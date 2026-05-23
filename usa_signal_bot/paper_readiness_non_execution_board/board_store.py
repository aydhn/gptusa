import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import (
    PaperReadinessNonExecutionBoard,
    RuntimeMapReplayPlan,
    RuntimeMapReplayResult,
    RuntimeRouteReplayItem,
    NonExecutionSealIntegrityAudit,
    NonExecutionBoardGate,
    NonExecutionBoardAssertion,
    NonExecutionBoardAuditEntry,
    NonExecutionBoardFullReview,
    paper_readiness_non_execution_board_to_dict,
    runtime_map_replay_plan_to_dict,
    runtime_map_replay_result_to_dict,
    runtime_route_replay_item_to_dict,
    non_execution_seal_integrity_audit_to_dict,
    non_execution_board_gate_to_dict,
    non_execution_board_assertion_to_dict,
    non_execution_board_audit_entry_to_dict,
    non_execution_board_full_review_to_dict
)

def non_execution_board_store_dir(data_root: Path) -> Path:
    p = data_root / "paper_readiness_non_execution_board"
    p.mkdir(parents=True, exist_ok=True)
    return p

def non_execution_boards_dir(data_root: Path) -> Path:
    p = non_execution_board_store_dir(data_root) / "boards"
    p.mkdir(parents=True, exist_ok=True)
    return p

def runtime_map_replay_plans_dir(data_root: Path) -> Path:
    p = non_execution_board_store_dir(data_root) / "runtime_map_replay_plans"
    p.mkdir(parents=True, exist_ok=True)
    return p

def runtime_map_replay_results_dir(data_root: Path) -> Path:
    p = non_execution_board_store_dir(data_root) / "runtime_map_replay_results"
    p.mkdir(parents=True, exist_ok=True)
    return p

def runtime_route_replay_items_dir(data_root: Path) -> Path:
    p = non_execution_board_store_dir(data_root) / "runtime_route_replay_items"
    p.mkdir(parents=True, exist_ok=True)
    return p

def seal_integrity_audits_dir(data_root: Path) -> Path:
    p = non_execution_board_store_dir(data_root) / "seal_integrity_audits"
    p.mkdir(parents=True, exist_ok=True)
    return p

def non_execution_board_gates_dir(data_root: Path) -> Path:
    p = non_execution_board_store_dir(data_root) / "gates"
    p.mkdir(parents=True, exist_ok=True)
    return p

def non_execution_board_assertions_dir(data_root: Path) -> Path:
    p = non_execution_board_store_dir(data_root) / "assertions"
    p.mkdir(parents=True, exist_ok=True)
    return p

def non_execution_board_audit_dir(data_root: Path) -> Path:
    p = non_execution_board_store_dir(data_root) / "audit"
    p.mkdir(parents=True, exist_ok=True)
    return p

def non_execution_board_full_reviews_dir(data_root: Path) -> Path:
    p = non_execution_board_store_dir(data_root) / "full_reviews"
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_non_execution_board_json(path: Path, item: PaperReadinessNonExecutionBoard) -> Path:
    with open(path, "w") as f:
        json.dump(paper_readiness_non_execution_board_to_dict(item), f, indent=2)
    return path

def write_runtime_map_replay_plan_json(path: Path, item: RuntimeMapReplayPlan) -> Path:
    with open(path, "w") as f:
        json.dump(runtime_map_replay_plan_to_dict(item), f, indent=2)
    return path

def write_runtime_map_replay_result_json(path: Path, item: RuntimeMapReplayResult) -> Path:
    with open(path, "w") as f:
        json.dump(runtime_map_replay_result_to_dict(item), f, indent=2)
    return path

def write_runtime_route_replay_items_jsonl(path: Path, items: List[RuntimeRouteReplayItem]) -> Path:
    with open(path, "a") as f:
        for item in items:
            f.write(json.dumps(runtime_route_replay_item_to_dict(item)) + "\n")
    return path

def write_seal_integrity_audit_json(path: Path, item: NonExecutionSealIntegrityAudit) -> Path:
    with open(path, "w") as f:
        json.dump(non_execution_seal_integrity_audit_to_dict(item), f, indent=2)
    return path

def write_non_execution_board_gates_jsonl(path: Path, items: List[NonExecutionBoardGate]) -> Path:
    with open(path, "a") as f:
        for item in items:
            f.write(json.dumps(non_execution_board_gate_to_dict(item)) + "\n")
    return path

def write_non_execution_board_assertions_jsonl(path: Path, items: List[NonExecutionBoardAssertion]) -> Path:
    with open(path, "a") as f:
        for item in items:
            f.write(json.dumps(non_execution_board_assertion_to_dict(item)) + "\n")
    return path

def write_non_execution_board_audit_jsonl(path: Path, items: List[NonExecutionBoardAuditEntry]) -> Path:
    with open(path, "a") as f:
        for item in items:
            f.write(json.dumps(non_execution_board_audit_entry_to_dict(item)) + "\n")
    return path

def write_non_execution_board_full_review_json(path: Path, item: NonExecutionBoardFullReview) -> Path:
    with open(path, "w") as f:
        json.dump(non_execution_board_full_review_to_dict(item), f, indent=2)
    return path

def read_non_execution_board_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_non_execution_board_full_reviews(data_root: Path) -> List[Path]:
    d = non_execution_board_full_reviews_dir(data_root)
    return sorted(d.glob("*.json"))

def get_latest_non_execution_board_full_review(data_root: Path) -> Optional[Path]:
    files = list_non_execution_board_full_reviews(data_root)
    return files[-1] if files else None

def non_execution_board_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "boards": len(list(non_execution_boards_dir(data_root).glob("*.json"))),
        "replay_plans": len(list(runtime_map_replay_plans_dir(data_root).glob("*.json"))),
        "replay_results": len(list(runtime_map_replay_results_dir(data_root).glob("*.json"))),
        "seal_audits": len(list(seal_integrity_audits_dir(data_root).glob("*.json"))),
        "full_reviews": len(list_non_execution_board_full_reviews(data_root))
    }
