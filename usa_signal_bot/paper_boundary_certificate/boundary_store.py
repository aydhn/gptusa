from typing import Any
import json
from pathlib import Path
from datetime import datetime, timezone

from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import (
    PaperSandboxBoundaryCertificate, AdmissionBlockerReplayPlan, AdmissionBlockerReplayResult,
    NoOrderEvidenceFreezeBundle, BoundaryRule, BoundaryAssertion, BoundaryAuditEntry,
    BoundaryCertificateFullReview, paper_sandbox_boundary_certificate_to_dict,
    admission_blocker_replay_plan_to_dict, admission_blocker_replay_result_to_dict,
    no_order_evidence_freeze_bundle_to_dict, boundary_rule_to_dict, boundary_assertion_to_dict,
    boundary_audit_entry_to_dict, boundary_certificate_full_review_to_dict
)

def boundary_certificate_store_dir(data_root: Path) -> Path:
    d = data_root / "paper_boundary_certificate"
    d.mkdir(parents=True, exist_ok=True)
    return d

def boundary_certificates_dir(data_root: Path) -> Path:
    d = boundary_certificate_store_dir(data_root) / "certificates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def blocker_replay_plans_dir(data_root: Path) -> Path:
    d = boundary_certificate_store_dir(data_root) / "blocker_replay_plans"
    d.mkdir(parents=True, exist_ok=True)
    return d

def blocker_replay_results_dir(data_root: Path) -> Path:
    d = boundary_certificate_store_dir(data_root) / "blocker_replay_results"
    d.mkdir(parents=True, exist_ok=True)
    return d

def evidence_freezes_dir(data_root: Path) -> Path:
    d = boundary_certificate_store_dir(data_root) / "evidence_freezes"
    d.mkdir(parents=True, exist_ok=True)
    return d

def boundary_rules_dir(data_root: Path) -> Path:
    d = boundary_certificate_store_dir(data_root) / "rules"
    d.mkdir(parents=True, exist_ok=True)
    return d

def boundary_assertions_dir(data_root: Path) -> Path:
    d = boundary_certificate_store_dir(data_root) / "assertions"
    d.mkdir(parents=True, exist_ok=True)
    return d

def boundary_audit_dir(data_root: Path) -> Path:
    d = boundary_certificate_store_dir(data_root) / "audit"
    d.mkdir(parents=True, exist_ok=True)
    return d

def boundary_full_reviews_dir(data_root: Path) -> Path:
    d = boundary_certificate_store_dir(data_root) / "full_reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_boundary_certificate_json(path: Path, item: PaperSandboxBoundaryCertificate) -> Path:
    path.write_text(json.dumps(paper_sandbox_boundary_certificate_to_dict(item), indent=2))
    return path

def write_blocker_replay_plan_json(path: Path, item: AdmissionBlockerReplayPlan) -> Path:
    path.write_text(json.dumps(admission_blocker_replay_plan_to_dict(item), indent=2))
    return path

def write_blocker_replay_result_json(path: Path, item: AdmissionBlockerReplayResult) -> Path:
    path.write_text(json.dumps(admission_blocker_replay_result_to_dict(item), indent=2))
    return path

def write_evidence_freeze_json(path: Path, item: NoOrderEvidenceFreezeBundle) -> Path:
    path.write_text(json.dumps(no_order_evidence_freeze_bundle_to_dict(item), indent=2))
    return path

def write_boundary_rules_jsonl(path: Path, items: list[BoundaryRule]) -> Path:
    with path.open('w') as f:
        for i in items:
            f.write(json.dumps(boundary_rule_to_dict(i)) + "\n")
    return path

def write_boundary_assertions_jsonl(path: Path, items: list[BoundaryAssertion]) -> Path:
    with path.open('w') as f:
        for i in items:
            f.write(json.dumps(boundary_assertion_to_dict(i)) + "\n")
    return path

def write_boundary_audit_jsonl(path: Path, items: list[BoundaryAuditEntry]) -> Path:
    with path.open('w') as f:
        for i in items:
            f.write(json.dumps(boundary_audit_entry_to_dict(i)) + "\n")
    return path

def write_boundary_full_review_json(path: Path, item: BoundaryCertificateFullReview) -> Path:
    path.write_text(json.dumps(boundary_certificate_full_review_to_dict(item), indent=2))
    return path

def read_boundary_full_review_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def list_boundary_full_reviews(data_root: Path) -> list[Path]:
    d = boundary_full_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")), reverse=True)

def get_latest_boundary_full_review(data_root: Path) -> Path | None:
    lst = list_boundary_full_reviews(data_root)
    return lst[0] if lst else None

def boundary_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "certificates": len(list(boundary_certificates_dir(data_root).glob("*.json"))),
        "reviews": len(list_boundary_full_reviews(data_root))
    }


# --- Phase 92 ---
# Phase 92