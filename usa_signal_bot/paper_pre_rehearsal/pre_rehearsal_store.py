from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_common.io import ensure_dir, write_json, write_jsonl, read_json, list_files, count_files

from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import (
    PrePaperDryRehearsalPlan,
    MutationFirewallRule,
    MutationFirewallEvent,
    PrePaperDryRehearsalRun,
    ActivationDeniedCheckpoint,
    PrePaperAuditEntry,
    PrePaperDryRehearsalReview,
    pre_paper_dry_rehearsal_plan_to_dict,
    mutation_firewall_rule_to_dict,
    mutation_firewall_event_to_dict,
    pre_paper_dry_rehearsal_run_to_dict,
    activation_denied_checkpoint_to_dict,
    pre_paper_audit_entry_to_dict,
    pre_paper_dry_rehearsal_review_to_dict
)

def pre_paper_rehearsal_store_dir(data_root: Path) -> Path:
    return ensure_dir(data_root / "paper_pre_rehearsal")

def pre_paper_plans_dir(data_root: Path) -> Path:
    return ensure_dir(pre_paper_rehearsal_store_dir(data_root) / "plans")

def firewall_rules_dir(data_root: Path) -> Path:
    return ensure_dir(pre_paper_rehearsal_store_dir(data_root) / "firewall_rules")

def firewall_events_dir(data_root: Path) -> Path:
    return ensure_dir(pre_paper_rehearsal_store_dir(data_root) / "firewall_events")

def pre_paper_runs_dir(data_root: Path) -> Path:
    return ensure_dir(pre_paper_rehearsal_store_dir(data_root) / "runs")

def activation_checkpoints_dir(data_root: Path) -> Path:
    return ensure_dir(pre_paper_rehearsal_store_dir(data_root) / "activation_checkpoints")

def pre_paper_audit_dir(data_root: Path) -> Path:
    return ensure_dir(pre_paper_rehearsal_store_dir(data_root) / "audit")

def pre_paper_reviews_dir(data_root: Path) -> Path:
    return ensure_dir(pre_paper_rehearsal_store_dir(data_root) / "reviews")

def write_pre_paper_plan_json(path: Path, item: PrePaperDryRehearsalPlan) -> Path:
    file_path = path / f"{item.plan_id}.json"
    write_json(file_path, pre_paper_dry_rehearsal_plan_to_dict(item), ensure_parent=False)
    return file_path

def write_firewall_rules_jsonl(path: Path, items: List[MutationFirewallRule]) -> Path:
    import time
    file_path = path / f"firewall_rules_{int(time.time())}.jsonl"
    write_jsonl(file_path, (mutation_firewall_rule_to_dict(item) for item in items), mode="w", ensure_parent=False)
    return file_path

def write_firewall_events_jsonl(path: Path, items: List[MutationFirewallEvent]) -> Path:
    import time
    file_path = path / f"firewall_events_{int(time.time())}.jsonl"
    write_jsonl(file_path, (mutation_firewall_event_to_dict(item) for item in items), mode="a", ensure_parent=False)
    return file_path

def write_pre_paper_run_json(path: Path, item: PrePaperDryRehearsalRun) -> Path:
    file_path = path / f"{item.run_id}.json"
    write_json(file_path, pre_paper_dry_rehearsal_run_to_dict(item), ensure_parent=False)
    return file_path

def write_activation_denied_checkpoint_json(path: Path, item: ActivationDeniedCheckpoint) -> Path:
    file_path = path / f"{item.checkpoint_id}.json"
    write_json(file_path, activation_denied_checkpoint_to_dict(item), ensure_parent=False)
    return file_path

def write_pre_paper_audit_jsonl(path: Path, items: List[PrePaperAuditEntry]) -> Path:
    import time
    file_path = path / f"audit_{int(time.time())}.jsonl"
    write_jsonl(file_path, (pre_paper_audit_entry_to_dict(item) for item in items), mode="a", ensure_parent=False)
    return file_path

def write_pre_paper_review_json(path: Path, item: PrePaperDryRehearsalReview) -> Path:
    file_path = path / f"{item.review_id}.json"
    write_json(file_path, pre_paper_dry_rehearsal_review_to_dict(item), ensure_parent=False)
    return file_path

def read_pre_paper_review_json(path: Path) -> Dict[str, Any]:
    return read_json(path)

def list_pre_paper_reviews(data_root: Path) -> List[Path]:
    d = pre_paper_reviews_dir(data_root)
    return list_files(d, "*.json", sort=True)

def get_latest_pre_paper_review(data_root: Path) -> Optional[Path]:
    reviews = list_pre_paper_reviews(data_root)
    if not reviews:
        return None
    import os
    return max(reviews, key=os.path.getctime)

def pre_paper_rehearsal_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "plans": count_files(pre_paper_plans_dir(data_root), "*.json"),
        "runs": count_files(pre_paper_runs_dir(data_root), "*.json"),
        "checkpoints": count_files(activation_checkpoints_dir(data_root), "*.json"),
        "reviews": len(list_pre_paper_reviews(data_root))
    }
