from typing import Any
from usa_signal_bot.paper_common.io import ensure_dir, write_json, write_jsonl, read_json, list_files, count_files
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
    ensure_dir(d)
    return d

def boundary_certificates_dir(data_root: Path) -> Path:
    d = boundary_certificate_store_dir(data_root) / "certificates"
    ensure_dir(d)
    return d

def blocker_replay_plans_dir(data_root: Path) -> Path:
    d = boundary_certificate_store_dir(data_root) / "blocker_replay_plans"
    ensure_dir(d)
    return d

def blocker_replay_results_dir(data_root: Path) -> Path:
    d = boundary_certificate_store_dir(data_root) / "blocker_replay_results"
    ensure_dir(d)
    return d

def evidence_freezes_dir(data_root: Path) -> Path:
    d = boundary_certificate_store_dir(data_root) / "evidence_freezes"
    ensure_dir(d)
    return d

def boundary_rules_dir(data_root: Path) -> Path:
    d = boundary_certificate_store_dir(data_root) / "rules"
    ensure_dir(d)
    return d

def boundary_assertions_dir(data_root: Path) -> Path:
    d = boundary_certificate_store_dir(data_root) / "assertions"
    ensure_dir(d)
    return d

def boundary_audit_dir(data_root: Path) -> Path:
    d = boundary_certificate_store_dir(data_root) / "audit"
    ensure_dir(d)
    return d

def boundary_full_reviews_dir(data_root: Path) -> Path:
    d = boundary_certificate_store_dir(data_root) / "full_reviews"
    ensure_dir(d)
    return d

def write_boundary_certificate_json(path: Path, item: PaperSandboxBoundaryCertificate) -> Path:
    return write_json(path, paper_sandbox_boundary_certificate_to_dict(item), ensure_parent=False)

def write_blocker_replay_plan_json(path: Path, item: AdmissionBlockerReplayPlan) -> Path:
    return write_json(path, admission_blocker_replay_plan_to_dict(item), ensure_parent=False)

def write_blocker_replay_result_json(path: Path, item: AdmissionBlockerReplayResult) -> Path:
    return write_json(path, admission_blocker_replay_result_to_dict(item), ensure_parent=False)

def write_evidence_freeze_json(path: Path, item: NoOrderEvidenceFreezeBundle) -> Path:
    return write_json(path, no_order_evidence_freeze_bundle_to_dict(item), ensure_parent=False)

def write_boundary_rules_jsonl(path: Path, items: list[BoundaryRule]) -> Path:
    return write_jsonl(path, (boundary_rule_to_dict(i) for i in items), ensure_parent=False)

def write_boundary_assertions_jsonl(path: Path, items: list[BoundaryAssertion]) -> Path:
    return write_jsonl(path, (boundary_assertion_to_dict(i) for i in items), ensure_parent=False)

def write_boundary_audit_jsonl(path: Path, items: list[BoundaryAuditEntry]) -> Path:
    return write_jsonl(path, (boundary_audit_entry_to_dict(i) for i in items), ensure_parent=False)

def write_boundary_full_review_json(path: Path, item: BoundaryCertificateFullReview) -> Path:
    return write_json(path, boundary_certificate_full_review_to_dict(item), ensure_parent=False)

def read_boundary_full_review_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return read_json(path)

def list_boundary_full_reviews(data_root: Path) -> list[Path]:
    d = boundary_full_reviews_dir(data_root)
    return list_files(d, "*.json", reverse=True)

def get_latest_boundary_full_review(data_root: Path) -> Path | None:
    lst = list_boundary_full_reviews(data_root)
    return lst[0] if lst else None

def boundary_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "certificates": count_files(boundary_certificates_dir(data_root), "*.json"),
        "reviews": len(list_boundary_full_reviews(data_root))
    }


# --- Phase 92 ---
# Phase 92