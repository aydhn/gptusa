import uuid
from dataclasses import dataclass, field
from typing import Any, List, Optional
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    FirewallReplayStatus,
    FirewallReplayDecision,
    FirewallReplayOutcome,
    ZeroMutationAuditStatus,
    ZeroMutationAuditDecision,
    ReadinessEvidenceRefreshStatus,
    ReadinessAuditCheckpointStatus,
    ReadinessAuditDecision,
    FirewallAuditRiskFlag,
    FirewallAuditReportType
)


@dataclass
class FirewallReplayPlan:
    replay_plan_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    source_pre_rehearsal_review_id: Optional[str]
    source_pre_paper_run_id: Optional[str]
    status: FirewallReplayStatus
    decision: FirewallReplayDecision
    required_attempt_types: List[str]
    replay_event_count: int
    require_all_dangerous_attempts_blocked: bool
    execution_enabled: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    paper_state_mutation_enabled: bool
    config_patch_enabled: bool
    telegram_real_send_enabled: bool
    warnings: List[str]
    errors: List[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FirewallReplayResult:
    replay_result_id: str
    created_at_utc: str
    replay_plan_id: Optional[str]
    status: FirewallReplayStatus
    outcome: FirewallReplayOutcome
    replayed_event_count: int
    blocked_event_count: int
    unblocked_dangerous_event_count: int
    missing_rule_count: int
    risk_flags: List[FirewallAuditRiskFlag]
    passed: bool
    warnings: List[str]
    errors: List[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ZeroMutationBaseline:
    baseline_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    baseline_type: str
    paper_snapshot_hash: Optional[str]
    paper_snapshot_summary: dict[str, Any]
    paper_state_committed: bool
    paper_order_executed: bool
    portfolio_state_mutated: bool
    position_mutated: bool
    cash_mutated: bool
    equity_mutated: bool
    config_patched: bool
    broker_order_sent: bool
    telegram_real_sent: bool
    warnings: List[str]
    errors: List[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ZeroMutationAuditReport:
    audit_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    status: ZeroMutationAuditStatus
    decision: ZeroMutationAuditDecision
    before_baseline: Optional[ZeroMutationBaseline]
    after_baseline: Optional[ZeroMutationBaseline]
    hash_changed: bool
    mutation_detected: bool
    invariant_violations: List[str]
    risk_flags: List[FirewallAuditRiskFlag]
    passed: bool
    warnings: List[str]
    errors: List[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PrePaperReadinessEvidenceItem:
    evidence_id: str
    created_at_utc: str
    evidence_type: str
    source_ref_id: Optional[str]
    source_path: Optional[str]
    status: ReadinessEvidenceRefreshStatus
    required: bool
    available: bool
    fresh: bool
    stale: bool
    summary: dict[str, Any]
    warnings: List[str]
    errors: List[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PrePaperReadinessEvidenceRefresh:
    refresh_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    evidence_items: List[PrePaperReadinessEvidenceItem]
    required_count: int
    available_count: int
    fresh_count: int
    stale_count: int
    missing_count: int
    evidence_score: Optional[float]
    status: ReadinessEvidenceRefreshStatus
    required_followups: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReadinessAuditCheckpoint:
    checkpoint_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    status: ReadinessAuditCheckpointStatus
    decision: ReadinessAuditDecision
    firewall_replay_result_id: Optional[str]
    zero_mutation_audit_id: Optional[str]
    evidence_refresh_id: Optional[str]
    activation_denied: bool
    activation_allowed: bool
    required_followups: List[str]
    risk_flags: List[FirewallAuditRiskFlag]
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    warnings: List[str]
    errors: List[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FirewallAuditTrailEntry:
    audit_entry_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: Optional[str]
    rationale: str
    evidence_refs: List[str]
    risk_flags: List[FirewallAuditRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FirewallAuditReview:
    review_id: str
    created_at_utc: str
    report_type: FirewallAuditReportType
    replay_plans: List[FirewallReplayPlan]
    replay_results: List[FirewallReplayResult]
    zero_mutation_audits: List[ZeroMutationAuditReport]
    evidence_refreshes: List[PrePaperReadinessEvidenceRefresh]
    readiness_checkpoints: List[ReadinessAuditCheckpoint]
    audit_entries: List[FirewallAuditTrailEntry]
    output_paths: dict[str, str]
    warnings: List[str]
    errors: List[str]


def firewall_replay_plan_to_dict(item: FirewallReplayPlan) -> dict:
    return {
        "replay_plan_id": item.replay_plan_id,
        "created_at_utc": item.created_at_utc,
        "candidate_id": item.candidate_id,
        "source_pre_rehearsal_review_id": item.source_pre_rehearsal_review_id,
        "source_pre_paper_run_id": item.source_pre_paper_run_id,
        "status": item.status.value if hasattr(item.status, "value") else item.status,
        "decision": item.decision.value if hasattr(item.decision, "value") else item.decision,
        "required_attempt_types": item.required_attempt_types,
        "replay_event_count": item.replay_event_count,
        "require_all_dangerous_attempts_blocked": item.require_all_dangerous_attempts_blocked,
        "execution_enabled": item.execution_enabled,
        "active_paper_enabled": item.active_paper_enabled,
        "broker_execution_enabled": item.broker_execution_enabled,
        "paper_state_mutation_enabled": item.paper_state_mutation_enabled,
        "config_patch_enabled": item.config_patch_enabled,
        "telegram_real_send_enabled": item.telegram_real_send_enabled,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def firewall_replay_result_to_dict(item: FirewallReplayResult) -> dict:
    return {
        "replay_result_id": item.replay_result_id,
        "created_at_utc": item.created_at_utc,
        "replay_plan_id": item.replay_plan_id,
        "status": item.status.value if hasattr(item.status, "value") else item.status,
        "outcome": item.outcome.value if hasattr(item.outcome, "value") else item.outcome,
        "replayed_event_count": item.replayed_event_count,
        "blocked_event_count": item.blocked_event_count,
        "unblocked_dangerous_event_count": item.unblocked_dangerous_event_count,
        "missing_rule_count": item.missing_rule_count,
        "risk_flags": [f.value if hasattr(f, "value") else f for f in item.risk_flags],
        "passed": item.passed,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def zero_mutation_baseline_to_dict(item: ZeroMutationBaseline) -> dict:
    return {
        "baseline_id": item.baseline_id,
        "created_at_utc": item.created_at_utc,
        "candidate_id": item.candidate_id,
        "baseline_type": item.baseline_type,
        "paper_snapshot_hash": item.paper_snapshot_hash,
        "paper_snapshot_summary": item.paper_snapshot_summary,
        "paper_state_committed": item.paper_state_committed,
        "paper_order_executed": item.paper_order_executed,
        "portfolio_state_mutated": item.portfolio_state_mutated,
        "position_mutated": item.position_mutated,
        "cash_mutated": item.cash_mutated,
        "equity_mutated": item.equity_mutated,
        "config_patched": item.config_patched,
        "broker_order_sent": item.broker_order_sent,
        "telegram_real_sent": item.telegram_real_sent,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def zero_mutation_audit_report_to_dict(item: ZeroMutationAuditReport) -> dict:
    return {
        "audit_id": item.audit_id,
        "created_at_utc": item.created_at_utc,
        "candidate_id": item.candidate_id,
        "status": item.status.value if hasattr(item.status, "value") else item.status,
        "decision": item.decision.value if hasattr(item.decision, "value") else item.decision,
        "before_baseline": zero_mutation_baseline_to_dict(item.before_baseline) if item.before_baseline else None,
        "after_baseline": zero_mutation_baseline_to_dict(item.after_baseline) if item.after_baseline else None,
        "hash_changed": item.hash_changed,
        "mutation_detected": item.mutation_detected,
        "invariant_violations": item.invariant_violations,
        "risk_flags": [f.value if hasattr(f, "value") else f for f in item.risk_flags],
        "passed": item.passed,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def pre_paper_readiness_evidence_item_to_dict(item: PrePaperReadinessEvidenceItem) -> dict:
    return {
        "evidence_id": item.evidence_id,
        "created_at_utc": item.created_at_utc,
        "evidence_type": item.evidence_type,
        "source_ref_id": item.source_ref_id,
        "source_path": item.source_path,
        "status": item.status.value if hasattr(item.status, "value") else item.status,
        "required": item.required,
        "available": item.available,
        "fresh": item.fresh,
        "stale": item.stale,
        "summary": item.summary,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def pre_paper_readiness_evidence_refresh_to_dict(item: PrePaperReadinessEvidenceRefresh) -> dict:
    return {
        "refresh_id": item.refresh_id,
        "created_at_utc": item.created_at_utc,
        "candidate_id": item.candidate_id,
        "evidence_items": [pre_paper_readiness_evidence_item_to_dict(e) for e in item.evidence_items],
        "required_count": item.required_count,
        "available_count": item.available_count,
        "fresh_count": item.fresh_count,
        "stale_count": item.stale_count,
        "missing_count": item.missing_count,
        "evidence_score": item.evidence_score,
        "status": item.status.value if hasattr(item.status, "value") else item.status,
        "required_followups": item.required_followups,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def readiness_audit_checkpoint_to_dict(item: ReadinessAuditCheckpoint) -> dict:
    return {
        "checkpoint_id": item.checkpoint_id,
        "created_at_utc": item.created_at_utc,
        "candidate_id": item.candidate_id,
        "status": item.status.value if hasattr(item.status, "value") else item.status,
        "decision": item.decision.value if hasattr(item.decision, "value") else item.decision,
        "firewall_replay_result_id": item.firewall_replay_result_id,
        "zero_mutation_audit_id": item.zero_mutation_audit_id,
        "evidence_refresh_id": item.evidence_refresh_id,
        "activation_denied": item.activation_denied,
        "activation_allowed": item.activation_allowed,
        "required_followups": item.required_followups,
        "risk_flags": [f.value if hasattr(f, "value") else f for f in item.risk_flags],
        "allows_active_paper": item.allows_active_paper,
        "allows_broker_execution": item.allows_broker_execution,
        "allows_paper_state_mutation": item.allows_paper_state_mutation,
        "allows_config_patch": item.allows_config_patch,
        "allows_telegram_real_send": item.allows_telegram_real_send,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def firewall_audit_trail_entry_to_dict(item: FirewallAuditTrailEntry) -> dict:
    return {
        "audit_entry_id": item.audit_entry_id,
        "created_at_utc": item.created_at_utc,
        "entity_type": item.entity_type,
        "entity_id": item.entity_id,
        "action": item.action,
        "decision": item.decision,
        "rationale": item.rationale,
        "evidence_refs": item.evidence_refs,
        "risk_flags": [f.value if hasattr(f, "value") else f for f in item.risk_flags],
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def firewall_audit_review_to_dict(item: FirewallAuditReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value if hasattr(item.report_type, "value") else item.report_type,
        "replay_plans": [firewall_replay_plan_to_dict(p) for p in item.replay_plans],
        "replay_results": [firewall_replay_result_to_dict(r) for r in item.replay_results],
        "zero_mutation_audits": [zero_mutation_audit_report_to_dict(a) for a in item.zero_mutation_audits],
        "evidence_refreshes": [pre_paper_readiness_evidence_refresh_to_dict(e) for e in item.evidence_refreshes],
        "readiness_checkpoints": [readiness_audit_checkpoint_to_dict(c) for c in item.readiness_checkpoints],
        "audit_entries": [firewall_audit_trail_entry_to_dict(e) for e in item.audit_entries],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }

def validate_firewall_replay_plan(item: FirewallReplayPlan) -> None:
    if item.execution_enabled: raise ValueError("execution_enabled must be False")
    if item.active_paper_enabled: raise ValueError("active_paper_enabled must be False")
    if item.broker_execution_enabled: raise ValueError("broker_execution_enabled must be False")
    if item.paper_state_mutation_enabled: raise ValueError("paper_state_mutation_enabled must be False")
    if item.config_patch_enabled: raise ValueError("config_patch_enabled must be False")
    if item.telegram_real_send_enabled: raise ValueError("telegram_real_send_enabled must be False")
    if not item.require_all_dangerous_attempts_blocked: raise ValueError("require_all_dangerous_attempts_blocked must be True")

def validate_firewall_replay_result(item: FirewallReplayResult) -> None:
    pass

def validate_zero_mutation_baseline(item: ZeroMutationBaseline) -> None:
    pass

def validate_zero_mutation_audit_report(item: ZeroMutationAuditReport) -> None:
    if item.passed and item.mutation_detected: raise ValueError("Zero mutation passed but mutation_detected is true")

def validate_pre_paper_readiness_evidence_refresh(item: PrePaperReadinessEvidenceRefresh) -> None:
    if item.evidence_score is not None and (item.evidence_score < 0 or item.evidence_score > 100):
        raise ValueError("evidence_score must be between 0 and 100")

def validate_readiness_audit_checkpoint(item: ReadinessAuditCheckpoint) -> None:
    if not item.activation_denied: raise ValueError("activation_denied must be True")
    if item.activation_allowed: raise ValueError("activation_allowed must be False")
    if item.allows_active_paper: raise ValueError("allows_active_paper must be False")
    if item.allows_broker_execution: raise ValueError("allows_broker_execution must be False")
    if item.allows_paper_state_mutation: raise ValueError("allows_paper_state_mutation must be False")
    if item.allows_config_patch: raise ValueError("allows_config_patch must be False")
    if item.allows_telegram_real_send: raise ValueError("allows_telegram_real_send must be False")

def validate_firewall_audit_review(item: FirewallAuditReview) -> None:
    pass

def create_firewall_replay_plan_id(prefix: str = "firewall_replay_plan") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_firewall_replay_result_id(prefix: str = "firewall_replay_result") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_zero_mutation_baseline_id(prefix: str = "zero_mutation_baseline") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_zero_mutation_audit_id(prefix: str = "zero_mutation_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_pre_paper_evidence_item_id(prefix: str = "pre_paper_evidence") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_pre_paper_evidence_refresh_id(prefix: str = "pre_paper_evidence_refresh") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_readiness_audit_checkpoint_id(prefix: str = "readiness_audit_checkpoint") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_firewall_audit_trail_entry_id(prefix: str = "firewall_audit_trail") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_firewall_audit_review_id(prefix: str = "firewall_audit_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
