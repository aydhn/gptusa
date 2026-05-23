
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
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

def _ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_final_paper_safe_gate_json(path: Path, item: FinalPaperSafeGate) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f: json.dump(final_paper_safe_gate_to_dict(item), f, indent=2)
    return path

def write_boundary_replay_plan_json(path: Path, item: BoundaryCertificateReplayPlan) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f: json.dump(boundary_certificate_replay_plan_to_dict(item), f, indent=2)
    return path

def write_boundary_replay_result_json(path: Path, item: BoundaryCertificateReplayResult) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f: json.dump(boundary_certificate_replay_result_to_dict(item), f, indent=2)
    return path

def write_frozen_integrity_audit_json(path: Path, item: FrozenEvidenceIntegrityAudit) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f: json.dump(frozen_evidence_integrity_audit_to_dict(item), f, indent=2)
    return path

def write_paper_safe_rules_jsonl(path: Path, items: List[PaperSafeGateRule]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        for i in items: f.write(json.dumps(paper_safe_gate_rule_to_dict(i)) + "\n")
    return path

def write_paper_safe_assertions_jsonl(path: Path, items: List[PaperSafeGateAssertion]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        for i in items: f.write(json.dumps(paper_safe_gate_assertion_to_dict(i)) + "\n")
    return path

def write_paper_safe_audit_jsonl(path: Path, items: List[PaperSafeGateAuditEntry]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f:
        for i in items: f.write(json.dumps(paper_safe_gate_audit_entry_to_dict(i)) + "\n")
    return path

def write_paper_safe_full_review_json(path: Path, item: PaperSafeGateFullReview) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w") as f: json.dump(paper_safe_gate_full_review_to_dict(item), f, indent=2)
    return path

def read_paper_safe_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f: return json.load(f)

def list_paper_safe_full_reviews(data_root: Path) -> List[Path]:
    d = paper_safe_full_reviews_dir(data_root)
    if not d.exists(): return []
    return list(d.glob("*.json"))

def get_latest_paper_safe_full_review(data_root: Path) -> Optional[Path]:
    revs = list_paper_safe_full_reviews(data_root)
    if not revs: return None
    return sorted(revs, key=lambda p: p.stat().st_mtime)[-1]

def paper_safe_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"reviews": len(list_paper_safe_full_reviews(data_root))}
