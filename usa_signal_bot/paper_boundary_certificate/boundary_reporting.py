from typing import Any
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import (
    AdmissionBlockerReplayPlan, AdmissionBlockerReplayResult, NoOrderEvidenceFreezeItem,
    NoOrderEvidenceFreezeBundle, BoundaryRule, BoundaryAssertion, PaperSandboxBoundaryCertificate,
    BoundaryAuditEntry, BoundaryCertificateFullReview
)
from usa_signal_bot.paper_boundary_certificate.boundary_report import boundary_certificate_limitations_text

def admission_blocker_replay_plan_to_text(item: AdmissionBlockerReplayPlan) -> str:
    return f"Plan ID: {item.replay_plan_id}, Required attempts: {len(item.required_attempt_types)}"

def admission_blocker_replay_result_to_text(item: AdmissionBlockerReplayResult) -> str:
    return f"Result ID: {item.replay_result_id}, Passed: {item.passed}"

def no_order_evidence_freeze_item_to_text(item: NoOrderEvidenceFreezeItem) -> str:
    return f"Item ID: {item.freeze_item_id}, Type: {item.evidence_type}"

def no_order_evidence_freeze_bundle_to_text(item: NoOrderEvidenceFreezeBundle, limit: int = 100) -> str:
    return f"Bundle ID: {item.freeze_id}, Frozen: {item.frozen}"

def boundary_rule_to_text(item: BoundaryRule) -> str:
    return f"Rule: {item.rule_name}, Status: {item.status.value}"

def boundary_assertion_to_text(item: BoundaryAssertion) -> str:
    return f"Assertion: {item.assertion_name}, Status: {item.status.value}"

def paper_sandbox_boundary_certificate_to_text(item: PaperSandboxBoundaryCertificate, limit: int = 100) -> str:
    return f"Certificate ID: {item.certificate_id}, Decision: {item.decision.value}"

def boundary_audit_entry_to_text(item: BoundaryAuditEntry) -> str:
    return f"Audit ID: {item.audit_id}, Action: {item.action}"

def boundary_certificate_full_review_to_text(item: BoundaryCertificateFullReview, limit: int = 100) -> str:
    return f"Review ID: {item.review_id}, Certificates: {len(item.certificates)}\n{boundary_certificate_limitations_text()}"

def boundary_store_summary_to_text(summary: dict[str, Any]) -> str:
    return str(summary)
