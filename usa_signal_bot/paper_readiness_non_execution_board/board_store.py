from usa_signal_bot.paper_common.io import (
    ensure_dir, write_json, write_jsonl, read_json, list_files, count_files,
)
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
    return ensure_dir(data_root / "paper_readiness_non_execution_board")

def non_execution_boards_dir(data_root: Path) -> Path:
    return ensure_dir(non_execution_board_store_dir(data_root) / "boards")

def runtime_map_replay_plans_dir(data_root: Path) -> Path:
    return ensure_dir(non_execution_board_store_dir(data_root) / "runtime_map_replay_plans")

def runtime_map_replay_results_dir(data_root: Path) -> Path:
    return ensure_dir(non_execution_board_store_dir(data_root) / "runtime_map_replay_results")

def runtime_route_replay_items_dir(data_root: Path) -> Path:
    return ensure_dir(non_execution_board_store_dir(data_root) / "runtime_route_replay_items")

def seal_integrity_audits_dir(data_root: Path) -> Path:
    return ensure_dir(non_execution_board_store_dir(data_root) / "seal_integrity_audits")

def non_execution_board_gates_dir(data_root: Path) -> Path:
    return ensure_dir(non_execution_board_store_dir(data_root) / "gates")

def non_execution_board_assertions_dir(data_root: Path) -> Path:
    return ensure_dir(non_execution_board_store_dir(data_root) / "assertions")

def non_execution_board_audit_dir(data_root: Path) -> Path:
    return ensure_dir(non_execution_board_store_dir(data_root) / "audit")

def non_execution_board_full_reviews_dir(data_root: Path) -> Path:
    return ensure_dir(non_execution_board_store_dir(data_root) / "full_reviews")

def write_non_execution_board_json(path: Path, item: PaperReadinessNonExecutionBoard) -> Path:
    return write_json(path, paper_readiness_non_execution_board_to_dict(item), ensure_parent=False)

def write_runtime_map_replay_plan_json(path: Path, item: RuntimeMapReplayPlan) -> Path:
    return write_json(path, runtime_map_replay_plan_to_dict(item), ensure_parent=False)

def write_runtime_map_replay_result_json(path: Path, item: RuntimeMapReplayResult) -> Path:
    return write_json(path, runtime_map_replay_result_to_dict(item), ensure_parent=False)

def write_runtime_route_replay_items_jsonl(path: Path, items: List[RuntimeRouteReplayItem]) -> Path:
    return write_jsonl(path, (runtime_route_replay_item_to_dict(item) for item in items), mode="a", ensure_parent=False)

def write_seal_integrity_audit_json(path: Path, item: NonExecutionSealIntegrityAudit) -> Path:
    return write_json(path, non_execution_seal_integrity_audit_to_dict(item), ensure_parent=False)

def write_non_execution_board_gates_jsonl(path: Path, items: List[NonExecutionBoardGate]) -> Path:
    return write_jsonl(path, (non_execution_board_gate_to_dict(item) for item in items), mode="a", ensure_parent=False)

def write_non_execution_board_assertions_jsonl(path: Path, items: List[NonExecutionBoardAssertion]) -> Path:
    return write_jsonl(path, (non_execution_board_assertion_to_dict(item) for item in items), mode="a", ensure_parent=False)

def write_non_execution_board_audit_jsonl(path: Path, items: List[NonExecutionBoardAuditEntry]) -> Path:
    return write_jsonl(path, (non_execution_board_audit_entry_to_dict(item) for item in items), mode="a", ensure_parent=False)

def write_non_execution_board_full_review_json(path: Path, item: NonExecutionBoardFullReview) -> Path:
    return write_json(path, non_execution_board_full_review_to_dict(item), ensure_parent=False)

def read_non_execution_board_full_review_json(path: Path) -> Dict[str, Any]:
    return read_json(path)

def list_non_execution_board_full_reviews(data_root: Path) -> List[Path]:
    d = non_execution_board_full_reviews_dir(data_root)
    return list_files(d, "*.json", sort=True)

def get_latest_non_execution_board_full_review(data_root: Path) -> Optional[Path]:
    files = list_non_execution_board_full_reviews(data_root)
    return files[-1] if files else None

def non_execution_board_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "boards": count_files(non_execution_boards_dir(data_root), "*.json"),
        "replay_plans": count_files(runtime_map_replay_plans_dir(data_root), "*.json"),
        "replay_results": count_files(runtime_map_replay_results_dir(data_root), "*.json"),
        "seal_audits": count_files(seal_integrity_audits_dir(data_root), "*.json"),
        "full_reviews": len(list_non_execution_board_full_reviews(data_root))
    }
