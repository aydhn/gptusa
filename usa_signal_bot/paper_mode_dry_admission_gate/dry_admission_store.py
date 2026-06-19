import json
import functools
from pathlib import Path
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
    d = data_root / "paper_mode_dry_admission_gate"
    d.mkdir(parents=True, exist_ok=True)
    return d

def final_dry_admission_gates_dir(data_root: Path) -> Path:
    d = dry_admission_gate_store_dir(data_root) / "gates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_replay_plans_dir(data_root: Path) -> Path:
    d = dry_admission_gate_store_dir(data_root) / "shadow_replay_plans"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_replay_results_dir(data_root: Path) -> Path:
    d = dry_admission_gate_store_dir(data_root) / "shadow_replay_results"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_replay_items_dir(data_root: Path) -> Path:
    d = dry_admission_gate_store_dir(data_root) / "shadow_replay_items"
    d.mkdir(parents=True, exist_ok=True)
    return d

def board_evidence_freezes_dir(data_root: Path) -> Path:
    d = dry_admission_gate_store_dir(data_root) / "board_evidence_freezes"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_rules_dir(data_root: Path) -> Path:
    d = dry_admission_gate_store_dir(data_root) / "rules"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_assertions_dir(data_root: Path) -> Path:
    d = dry_admission_gate_store_dir(data_root) / "assertions"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_audit_dir(data_root: Path) -> Path:
    d = dry_admission_gate_store_dir(data_root) / "audit"
    d.mkdir(parents=True, exist_ok=True)
    return d

def dry_admission_full_reviews_dir(data_root: Path) -> Path:
    d = dry_admission_gate_store_dir(data_root) / "full_reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_final_dry_admission_gate_json(path: Path, item: FinalPaperModeDryAdmissionGate) -> Path:
    d = final_paper_mode_dry_admission_gate_to_dict(item)
    path.write_text(json.dumps(d, indent=2))
    return path

def write_shadow_replay_plan_json(path: Path, item: ShadowLaunchReplayPlan) -> Path:
    d = shadow_launch_replay_plan_to_dict(item)
    path.write_text(json.dumps(d, indent=2))
    return path

def write_shadow_replay_result_json(path: Path, item: ShadowLaunchReplayResult) -> Path:
    d = shadow_launch_replay_result_to_dict(item)
    path.write_text(json.dumps(d, indent=2))
    return path

def write_shadow_replay_items_jsonl(path: Path, items: List[ShadowLaunchReplayItem]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(shadow_launch_replay_item_to_dict(item)) + "\n")
    return path

def write_board_evidence_freeze_json(path: Path, item: BoardEvidenceFreezeBundle) -> Path:
    d = board_evidence_freeze_bundle_to_dict(item)
    path.write_text(json.dumps(d, indent=2))
    return path

def write_dry_admission_rules_jsonl(path: Path, items: List[DryAdmissionGateRule]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dry_admission_gate_rule_to_dict(item)) + "\n")
    return path

def write_dry_admission_assertions_jsonl(path: Path, items: List[DryAdmissionGateAssertion]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dry_admission_gate_assertion_to_dict(item)) + "\n")
    return path

def write_dry_admission_audit_jsonl(path: Path, items: List[DryAdmissionGateAuditEntry]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(dry_admission_gate_audit_entry_to_dict(item)) + "\n")
    return path

def write_dry_admission_full_review_json(path: Path, item: DryAdmissionGateFullReview) -> Path:
    d = dry_admission_gate_full_review_to_dict(item)
    path.write_text(json.dumps(d, indent=2))
    return path

@functools.lru_cache(maxsize=128)
def _cached_read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())

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
        "gates": len(list(final_dry_admission_gates_dir(data_root).glob("*.json"))),
        "shadow_replay_plans": len(list(shadow_replay_plans_dir(data_root).glob("*.json"))),
        "shadow_replay_results": len(list(shadow_replay_results_dir(data_root).glob("*.json"))),
        "board_evidence_freezes": len(list(board_evidence_freezes_dir(data_root).glob("*.json"))),
        "full_reviews": len(list_dry_admission_full_reviews(data_root))
    }
