from typing import Any
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import (
    SandboxRuntimeAdmissionReplayItem,
    SandboxRuntimeAdmissionReplayPlan,
    SandboxRuntimeAdmissionReplayResult,
    SimulatorEvidenceFreezeItem,
    SimulatorEvidenceFreezeBundle,
    HandoffFreezeRule,
    HandoffFreezeAssertion,
    FinalPrePaperHandoffFreezeGate,
    PrePaperHandoffFreezeAuditEntry,
    PrePaperHandoffFreezeFullReview
)
from usa_signal_bot.pre_paper_handoff_freeze_gate.sandbox_replay_plan import sandbox_runtime_admission_replay_plan_to_text
from usa_signal_bot.pre_paper_handoff_freeze_gate.simulator_evidence_freeze import simulator_evidence_freeze_to_text
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_rules import handoff_freeze_rules_to_text
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_assertions import handoff_freeze_assertions_to_text
from usa_signal_bot.pre_paper_handoff_freeze_gate.final_handoff_freeze_gate import final_handoff_freeze_gate_to_text
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_audit import handoff_freeze_audit_to_text
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_report import handoff_freeze_full_review_to_text, handoff_freeze_limitations_text

def sandbox_runtime_admission_replay_item_to_text(item: SandboxRuntimeAdmissionReplayItem) -> str:
    return f"Replay Item: {item.attempt_type} - Blocked: {item.blocked}"

def sandbox_runtime_admission_replay_result_to_text(item: SandboxRuntimeAdmissionReplayResult) -> str:
    return f"Replay Result: Passed={item.passed}, Allowed={item.allowed_attempt_count}, Blocked={item.blocked_attempt_count}"

def simulator_evidence_freeze_item_to_text(item: SimulatorEvidenceFreezeItem) -> str:
    return f"Freeze Item: {item.evidence_type} - Available: {item.available}"

def simulator_evidence_freeze_bundle_to_text(item: SimulatorEvidenceFreezeBundle, limit: int = 100) -> str:
    return simulator_evidence_freeze_to_text(item, limit)

def handoff_freeze_rule_to_text(item: HandoffFreezeRule) -> str:
    return f"Rule: {item.rule_name} - Status: {item.status.value}"

def handoff_freeze_assertion_to_text(item: HandoffFreezeAssertion) -> str:
    return f"Assertion: {item.assertion_name} - Status: {item.status.value}"

def handoff_freeze_audit_entry_to_text(item: PrePaperHandoffFreezeAuditEntry) -> str:
    return f"Audit: {item.action} on {item.entity_type} - Decision: {item.decision}"

def handoff_freeze_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store Summary: {summary}"
