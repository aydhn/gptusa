from pathlib import Path
from typing import Any, Dict, List, Optional
import json

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
    d = data_root / "paper_pre_rehearsal"
    d.mkdir(parents=True, exist_ok=True)
    return d

def pre_paper_plans_dir(data_root: Path) -> Path:
    d = pre_paper_rehearsal_store_dir(data_root) / "plans"
    d.mkdir(parents=True, exist_ok=True)
    return d

def firewall_rules_dir(data_root: Path) -> Path:
    d = pre_paper_rehearsal_store_dir(data_root) / "firewall_rules"
    d.mkdir(parents=True, exist_ok=True)
    return d

def firewall_events_dir(data_root: Path) -> Path:
    d = pre_paper_rehearsal_store_dir(data_root) / "firewall_events"
    d.mkdir(parents=True, exist_ok=True)
    return d

def pre_paper_runs_dir(data_root: Path) -> Path:
    d = pre_paper_rehearsal_store_dir(data_root) / "runs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def activation_checkpoints_dir(data_root: Path) -> Path:
    d = pre_paper_rehearsal_store_dir(data_root) / "activation_checkpoints"
    d.mkdir(parents=True, exist_ok=True)
    return d

def pre_paper_audit_dir(data_root: Path) -> Path:
    d = pre_paper_rehearsal_store_dir(data_root) / "audit"
    d.mkdir(parents=True, exist_ok=True)
    return d

def pre_paper_reviews_dir(data_root: Path) -> Path:
    d = pre_paper_rehearsal_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_pre_paper_plan_json(path: Path, item: PrePaperDryRehearsalPlan) -> Path:
    file_path = path / f"{item.plan_id}.json"
    with open(file_path, "w") as f:
        json.dump(pre_paper_dry_rehearsal_plan_to_dict(item), f, indent=2)
    return file_path

def write_firewall_rules_jsonl(path: Path, items: List[MutationFirewallRule]) -> Path:
    import time
    file_path = path / f"firewall_rules_{int(time.time())}.jsonl"
    with open(file_path, "w") as f:
        for item in items:
            f.write(json.dumps(mutation_firewall_rule_to_dict(item)) + "\n")
    return file_path

def write_firewall_events_jsonl(path: Path, items: List[MutationFirewallEvent]) -> Path:
    import time
    file_path = path / f"firewall_events_{int(time.time())}.jsonl"
    with open(file_path, "a") as f:
        for item in items:
            f.write(json.dumps(mutation_firewall_event_to_dict(item)) + "\n")
    return file_path

def write_pre_paper_run_json(path: Path, item: PrePaperDryRehearsalRun) -> Path:
    file_path = path / f"{item.run_id}.json"
    with open(file_path, "w") as f:
        json.dump(pre_paper_dry_rehearsal_run_to_dict(item), f, indent=2)
    return file_path

def write_activation_denied_checkpoint_json(path: Path, item: ActivationDeniedCheckpoint) -> Path:
    file_path = path / f"{item.checkpoint_id}.json"
    with open(file_path, "w") as f:
        json.dump(activation_denied_checkpoint_to_dict(item), f, indent=2)
    return file_path

def write_pre_paper_audit_jsonl(path: Path, items: List[PrePaperAuditEntry]) -> Path:
    import time
    file_path = path / f"audit_{int(time.time())}.jsonl"
    with open(file_path, "a") as f:
        for item in items:
            f.write(json.dumps(pre_paper_audit_entry_to_dict(item)) + "\n")
    return file_path

def write_pre_paper_review_json(path: Path, item: PrePaperDryRehearsalReview) -> Path:
    file_path = path / f"{item.review_id}.json"
    with open(file_path, "w") as f:
        json.dump(pre_paper_dry_rehearsal_review_to_dict(item), f, indent=2)
    return file_path

def read_pre_paper_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_pre_paper_reviews(data_root: Path) -> List[Path]:
    d = pre_paper_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")))

def get_latest_pre_paper_review(data_root: Path) -> Optional[Path]:
    reviews = list_pre_paper_reviews(data_root)
    if not reviews:
        return None
    import os
    return max(reviews, key=os.path.getctime)

def pre_paper_rehearsal_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "plans": len(list(pre_paper_plans_dir(data_root).glob("*.json"))),
        "runs": len(list(pre_paper_runs_dir(data_root).glob("*.json"))),
        "checkpoints": len(list(activation_checkpoints_dir(data_root).glob("*.json"))),
        "reviews": len(list_pre_paper_reviews(data_root))
    }
