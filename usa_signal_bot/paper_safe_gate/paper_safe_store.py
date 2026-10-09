
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_common.io import (
    ensure_dir, write_json, write_jsonl, read_json, list_files, latest_by_mtime,
)
from usa_signal_bot.paper_safe_gate.paper_safe_gate_models import (
    FinalPaperSafeGate, BoundaryCertificateReplayPlan, BoundaryCertificateReplayResult,
    FrozenEvidenceIntegrityAudit, PaperSafeGateRule, PaperSafeGateAssertion,
    PaperSafeGateAuditEntry, PaperSafeGateFullReview,
    final_paper_safe_gate_to_dict, boundary_certificate_replay_plan_to_dict,
    boundary_certificate_replay_result_to_dict, frozen_evidence_integrity_audit_to_dict,
    paper_safe_gate_rule_to_dict, paper_safe_gate_assertion_to_dict,
    paper_safe_gate_audit_entry_to_dict, paper_safe_gate_full_review_to_dict
)

def paper_safe_gate_store_dir(data_root: Path) -> Path: return data_root / "paper_safe_gate"
def final_paper_safe_gates_dir(data_root: Path) -> Path: return paper_safe_gate_store_dir(data_root) / "gates"
def boundary_replay_plans_dir(data_root: Path) -> Path: return paper_safe_gate_store_dir(data_root) / "boundary_replay_plans"
def boundary_replay_results_dir(data_root: Path) -> Path: return paper_safe_gate_store_dir(data_root) / "boundary_replay_results"
def frozen_integrity_audits_dir(data_root: Path) -> Path: return paper_safe_gate_store_dir(data_root) / "frozen_integrity_audits"
def paper_safe_rules_dir(data_root: Path) -> Path: return paper_safe_gate_store_dir(data_root) / "rules"
def paper_safe_assertions_dir(data_root: Path) -> Path: return paper_safe_gate_store_dir(data_root) / "assertions"
def paper_safe_audit_dir(data_root: Path) -> Path: return paper_safe_gate_store_dir(data_root) / "audit"
def paper_safe_full_reviews_dir(data_root: Path) -> Path: return paper_safe_gate_store_dir(data_root) / "full_reviews"

_ensure_dir = ensure_dir

def write_final_paper_safe_gate_json(path: Path, item: FinalPaperSafeGate) -> Path:
    return write_json(path, final_paper_safe_gate_to_dict(item))

def write_boundary_replay_plan_json(path: Path, item: BoundaryCertificateReplayPlan) -> Path:
    return write_json(path, boundary_certificate_replay_plan_to_dict(item))

def write_boundary_replay_result_json(path: Path, item: BoundaryCertificateReplayResult) -> Path:
    return write_json(path, boundary_certificate_replay_result_to_dict(item))

def write_frozen_integrity_audit_json(path: Path, item: FrozenEvidenceIntegrityAudit) -> Path:
    return write_json(path, frozen_evidence_integrity_audit_to_dict(item))

def write_paper_safe_rules_jsonl(path: Path, items: List[PaperSafeGateRule]) -> Path:
    return write_jsonl(path, (paper_safe_gate_rule_to_dict(i) for i in items))

def write_paper_safe_assertions_jsonl(path: Path, items: List[PaperSafeGateAssertion]) -> Path:
    return write_jsonl(path, (paper_safe_gate_assertion_to_dict(i) for i in items))

def write_paper_safe_audit_jsonl(path: Path, items: List[PaperSafeGateAuditEntry]) -> Path:
    return write_jsonl(path, (paper_safe_gate_audit_entry_to_dict(i) for i in items))

def write_paper_safe_full_review_json(path: Path, item: PaperSafeGateFullReview) -> Path:
    return write_json(path, paper_safe_gate_full_review_to_dict(item))

def read_paper_safe_full_review_json(path: Path) -> Dict[str, Any]:
    return read_json(path)

def list_paper_safe_full_reviews(data_root: Path) -> List[Path]:
    return list_files(paper_safe_full_reviews_dir(data_root), "*.json")

def get_latest_paper_safe_full_review(data_root: Path) -> Optional[Path]:
    revs = list_paper_safe_full_reviews(data_root)
    return latest_by_mtime(revs)

def paper_safe_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"reviews": len(list_paper_safe_full_reviews(data_root))}
