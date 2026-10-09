import functools
from pathlib import Path
from usa_signal_bot.paper_common.io import (ensure_dir, write_json, write_jsonl, read_json, count_files)
from typing import Any, List
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import (
    FinalPaperModeDryAdmissionGate,
    ShadowLaunchReplayPlan,
    ShadowLaunchReplayResult,
    ShadowLaunchReplayItem,
    BoardEvidenceFreezeBundle,
    DryAdmissionGateRule,
    DryAdmissionGateAssertion,
    DryAdmissionGateAuditEntry,
    DryAdmissionGateFullReview,
    final_paper_mode_dry_admission_gate_to_dict,
    shadow_launch_replay_plan_to_dict,
    shadow_launch_replay_result_to_dict,
    shadow_launch_replay_item_to_dict,
    board_evidence_freeze_bundle_to_dict,
    dry_admission_gate_rule_to_dict,
    dry_admission_gate_assertion_to_dict,
    dry_admission_gate_audit_entry_to_dict,
    dry_admission_gate_full_review_to_dict
)

def dry_admission_gate_store_dir(data_root: Path) -> Path:
    return ensure_dir(data_root / "paper_mode_dry_admission_gate")

def final_dry_admission_gates_dir(data_root: Path) -> Path:
    return ensure_dir(dry_admission_gate_store_dir(data_root) / "gates")

def shadow_replay_plans_dir(data_root: Path) -> Path:
    return ensure_dir(dry_admission_gate_store_dir(data_root) / "shadow_replay_plans")

def shadow_replay_results_dir(data_root: Path) -> Path:
    return ensure_dir(dry_admission_gate_store_dir(data_root) / "shadow_replay_results")

def shadow_replay_items_dir(data_root: Path) -> Path:
    return ensure_dir(dry_admission_gate_store_dir(data_root) / "shadow_replay_items")

def board_evidence_freezes_dir(data_root: Path) -> Path:
    return ensure_dir(dry_admission_gate_store_dir(data_root) / "board_evidence_freezes")

def dry_admission_rules_dir(data_root: Path) -> Path:
    return ensure_dir(dry_admission_gate_store_dir(data_root) / "rules")

def dry_admission_assertions_dir(data_root: Path) -> Path:
    return ensure_dir(dry_admission_gate_store_dir(data_root) / "assertions")

def dry_admission_audit_dir(data_root: Path) -> Path:
    return ensure_dir(dry_admission_gate_store_dir(data_root) / "audit")

def dry_admission_full_reviews_dir(data_root: Path) -> Path:
    return ensure_dir(dry_admission_gate_store_dir(data_root) / "full_reviews")


def write_final_dry_admission_gate_json(path: Path, item: FinalPaperModeDryAdmissionGate) -> Path:
    return write_json(path, final_paper_mode_dry_admission_gate_to_dict(item), ensure_parent=False)

def write_shadow_replay_plan_json(path: Path, item: ShadowLaunchReplayPlan) -> Path:
    return write_json(path, shadow_launch_replay_plan_to_dict(item), ensure_parent=False)

def write_shadow_replay_result_json(path: Path, item: ShadowLaunchReplayResult) -> Path:
    return write_json(path, shadow_launch_replay_result_to_dict(item), ensure_parent=False)

def write_shadow_replay_items_jsonl(path: Path, items: List[ShadowLaunchReplayItem]) -> Path:
    return write_jsonl(path, (shadow_launch_replay_item_to_dict(item) for item in items), ensure_parent=False)

def write_board_evidence_freeze_json(path: Path, item: BoardEvidenceFreezeBundle) -> Path:
    return write_json(path, board_evidence_freeze_bundle_to_dict(item), ensure_parent=False)

def write_dry_admission_rules_jsonl(path: Path, items: List[DryAdmissionGateRule]) -> Path:
    return write_jsonl(path, (dry_admission_gate_rule_to_dict(item) for item in items), ensure_parent=False)

def write_dry_admission_assertions_jsonl(path: Path, items: List[DryAdmissionGateAssertion]) -> Path:
    return write_jsonl(path, (dry_admission_gate_assertion_to_dict(item) for item in items), ensure_parent=False)

def write_dry_admission_audit_jsonl(path: Path, items: List[DryAdmissionGateAuditEntry]) -> Path:
    return write_jsonl(path, (dry_admission_gate_audit_entry_to_dict(item) for item in items), ensure_parent=False)

def write_dry_admission_full_review_json(path: Path, item: DryAdmissionGateFullReview) -> Path:
    return write_json(path, dry_admission_gate_full_review_to_dict(item), ensure_parent=False)

@functools.lru_cache(maxsize=128)
def _cached_read_json(path: Path) -> dict[str, Any]:
    return read_json(path)

def read_dry_admission_full_review_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return _cached_read_json(path)

def list_dry_admission_full_reviews(data_root: Path) -> List[Path]:
    d = dry_admission_full_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")), key=lambda p: p.stat().st_mtime, reverse=True)

def get_latest_dry_admission_full_review(data_root: Path) -> Path | None:
    lst = list_dry_admission_full_reviews(data_root)
    return lst[0] if lst else None

def dry_admission_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "gates": count_files(final_dry_admission_gates_dir(data_root), "*.json"),
        "shadow_replay_plans": count_files(shadow_replay_plans_dir(data_root), "*.json"),
        "shadow_replay_results": count_files(shadow_replay_results_dir(data_root), "*.json"),
        "board_evidence_freezes": count_files(board_evidence_freezes_dir(data_root), "*.json"),
        "full_reviews": len(list_dry_admission_full_reviews(data_root))
    }
