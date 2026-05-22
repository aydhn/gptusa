from pathlib import Path
import json
from typing import Any, List, Optional
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import (
    FirewallReplayPlan, FirewallReplayResult, ZeroMutationBaseline, ZeroMutationAuditReport,
    PrePaperReadinessEvidenceRefresh, ReadinessAuditCheckpoint, FirewallAuditTrailEntry,
    FirewallAuditReview, firewall_replay_plan_to_dict, firewall_replay_result_to_dict,
    zero_mutation_baseline_to_dict, zero_mutation_audit_report_to_dict,
    pre_paper_readiness_evidence_refresh_to_dict, readiness_audit_checkpoint_to_dict,
    firewall_audit_trail_entry_to_dict, firewall_audit_review_to_dict
)

def firewall_audit_store_dir(data_root: Path) -> Path: return data_root / "paper_firewall_audit"
def firewall_replay_plans_dir(data_root: Path) -> Path: return firewall_audit_store_dir(data_root) / "replay_plans"
def firewall_replay_results_dir(data_root: Path) -> Path: return firewall_audit_store_dir(data_root) / "replay_results"
def zero_mutation_baselines_dir(data_root: Path) -> Path: return firewall_audit_store_dir(data_root) / "zero_mutation_baselines"
def zero_mutation_audits_dir(data_root: Path) -> Path: return firewall_audit_store_dir(data_root) / "zero_mutation_audits"
def pre_paper_evidence_refreshes_dir(data_root: Path) -> Path: return firewall_audit_store_dir(data_root) / "evidence_refreshes"
def readiness_audit_checkpoints_dir(data_root: Path) -> Path: return firewall_audit_store_dir(data_root) / "readiness_checkpoints"
def firewall_audit_trail_dir(data_root: Path) -> Path: return firewall_audit_store_dir(data_root) / "audit_trail"
def firewall_audit_reviews_dir(data_root: Path) -> Path: return firewall_audit_store_dir(data_root) / "reviews"

def write_firewall_replay_plan_json(path: Path, item: FirewallReplayPlan) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(firewall_replay_plan_to_dict(item), indent=2))
    return path

def write_firewall_replay_result_json(path: Path, item: FirewallReplayResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(firewall_replay_result_to_dict(item), indent=2))
    return path

def write_zero_mutation_baseline_json(path: Path, item: ZeroMutationBaseline) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(zero_mutation_baseline_to_dict(item), indent=2))
    return path

def write_zero_mutation_audit_json(path: Path, item: ZeroMutationAuditReport) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(zero_mutation_audit_report_to_dict(item), indent=2))
    return path

def write_pre_paper_evidence_refresh_json(path: Path, item: PrePaperReadinessEvidenceRefresh) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(pre_paper_readiness_evidence_refresh_to_dict(item), indent=2))
    return path

def write_readiness_audit_checkpoint_json(path: Path, item: ReadinessAuditCheckpoint) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(readiness_audit_checkpoint_to_dict(item), indent=2))
    return path

def write_firewall_audit_trail_jsonl(path: Path, items: List[FirewallAuditTrailEntry]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        for i in items:
            f.write(json.dumps(firewall_audit_trail_entry_to_dict(i)) + "\n")
    return path

def write_firewall_audit_review_json(path: Path, item: FirewallAuditReview) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(firewall_audit_review_to_dict(item), indent=2))
    return path

def read_firewall_audit_review_json(path: Path) -> dict[str, Any]:
    if not path.exists(): return {}
    return json.loads(path.read_text())

def list_firewall_audit_reviews(data_root: Path) -> List[Path]:
    d = firewall_audit_reviews_dir(data_root)
    if not d.exists(): return []
    return sorted(d.glob("*.json"))

def get_latest_firewall_audit_review(data_root: Path) -> Optional[Path]:
    files = list_firewall_audit_reviews(data_root)
    return files[-1] if files else None

def firewall_audit_store_summary(data_root: Path) -> dict[str, Any]:
    return {"reviews": len(list_firewall_audit_reviews(data_root))}
