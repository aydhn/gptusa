
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_safe_gate.paper_safe_gate_models import (
    BoundaryCertificateReplayPlan, BoundaryCertificateReplayResult,
    FrozenEvidenceIntegrityItem, FrozenEvidenceIntegrityAudit,
    PaperSafeGateRule, PaperSafeGateAssertion, FinalPaperSafeGate,
    PaperSafeGateAuditEntry, PaperSafeGateFullReview
)

def boundary_certificate_replay_plan_to_text(item: BoundaryCertificateReplayPlan) -> str: return f"Plan {item.replay_plan_id}"
def boundary_certificate_replay_result_to_text(item: BoundaryCertificateReplayResult) -> str: return f"Result {item.replay_result_id}"
def frozen_evidence_integrity_item_to_text(item: FrozenEvidenceIntegrityItem) -> str: return f"Item {item.integrity_item_id}"
def frozen_evidence_integrity_audit_to_text(item: FrozenEvidenceIntegrityAudit, limit: int = 100) -> str: return f"Audit {item.audit_id}"
def paper_safe_gate_rule_to_text(item: PaperSafeGateRule) -> str: return f"Rule {item.rule_id}"
def paper_safe_gate_assertion_to_text(item: PaperSafeGateAssertion) -> str: return f"Assertion {item.assertion_id}"
def final_paper_safe_gate_to_text(item: FinalPaperSafeGate, limit: int = 100) -> str: return f"Gate {item.gate_id}"
def paper_safe_gate_audit_entry_to_text(item: PaperSafeGateAuditEntry) -> str: return f"Audit Entry {item.audit_id}"
def paper_safe_gate_full_review_to_text(item: PaperSafeGateFullReview, limit: int = 100) -> str: return f"Full Review {item.review_id}"

def paper_safe_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store summary: {summary}"

def paper_safe_gate_limitations_text() -> str:
    return "Limitations: No broker orders, no paper mutation."
