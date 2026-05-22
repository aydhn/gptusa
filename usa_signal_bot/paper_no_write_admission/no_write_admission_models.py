from dataclasses import dataclass, field
from typing import Any, Optional, List, Dict
from usa_signal_bot.core.enums import (
    NoWriteAdmissionContractStatus,
    NoWriteAdmissionDecision,
    ContractClauseStatus,
    ActivationFirewallReplayStatus,
    ActivationFirewallReplayOutcome,
    PaperModePreflightStatus,
    PaperModePreflightDecision,
    PaperModeSimulationStepStatus,
    NoWriteAdmissionRiskFlag,
    NoWriteAdmissionReportType
)

@dataclass
class NoWriteContractClause:
    clause_id: str
    created_at_utc: str
    clause_name: str
    status: ContractClauseStatus
    expected_value: Any | None
    observed_value: Any | None
    required: bool
    description: str
    risk_flags: list[NoWriteAdmissionRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class NoWritePaperAdmissionContract:
    contract_id: str
    created_at_utc: str
    status: NoWriteAdmissionContractStatus
    decision: NoWriteAdmissionDecision
    candidate_id: str | None
    source_board_review_id: str | None
    source_write_block_proof_id: str | None
    source_activation_firewall_event_refs: list[str]
    clauses: list[NoWriteContractClause]
    evidence_refs: list[str]
    manual_review_required: bool
    activation_denied: bool
    activation_allowed: bool
    all_writes_blocked: bool
    allows_active_paper: bool
    allows_broker_execution: bool
    allows_paper_state_mutation: bool
    allows_config_patch: bool
    allows_telegram_real_send: bool
    safety_flags: list[NoWriteAdmissionRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ActivationReplayPlan:
    replay_plan_id: str
    created_at_utc: str
    candidate_id: str | None
    source_board_review_id: str | None
    required_attempt_types: list[str]
    required_rule_count: int
    require_all_attempts_denied: bool
    execution_enabled: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    paper_state_mutation_enabled: bool
    config_patch_enabled: bool
    telegram_real_send_enabled: bool
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ActivationReplayResult:
    replay_result_id: str
    created_at_utc: str
    replay_plan_id: str | None
    status: ActivationFirewallReplayStatus
    outcome: ActivationFirewallReplayOutcome
    replayed_attempt_count: int
    denied_attempt_count: int
    allowed_attempt_count: int
    missing_rule_count: int
    passed: bool
    risk_flags: list[NoWriteAdmissionRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperModeSimulationStep:
    step_id: str
    created_at_utc: str
    step_name: str
    status: PaperModeSimulationStepStatus
    input_refs: list[str]
    output_refs: list[str]
    write_attempted: bool
    order_attempted: bool
    broker_send_attempted: bool
    config_patch_attempted: bool
    telegram_real_send_attempted: bool
    active_paper_enable_attempted: bool
    risk_flags: list[NoWriteAdmissionRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperModePreflightRun:
    preflight_id: str
    created_at_utc: str
    status: PaperModePreflightStatus
    decision: PaperModePreflightDecision
    candidate_id: str | None
    contract_id: str | None
    activation_replay_result_id: str | None
    simulation_steps: list[PaperModeSimulationStep]
    read_only_snapshot_hash: str | None
    output_summary: dict[str, Any]
    activation_denied: bool
    activation_allowed: bool
    all_writes_blocked: bool
    mutation_detected: bool
    safety_flags: list[NoWriteAdmissionRiskFlag]
    started_at_utc: str | None
    completed_at_utc: str | None
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class NoWriteAdmissionAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: str | None
    rationale: str
    evidence_refs: list[str]
    risk_flags: list[NoWriteAdmissionRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class NoWriteAdmissionFullReview:
    review_id: str
    created_at_utc: str
    report_type: NoWriteAdmissionReportType
    contracts: list[NoWritePaperAdmissionContract]
    activation_replay_plans: list[ActivationReplayPlan]
    activation_replay_results: list[ActivationReplayResult]
    preflight_runs: list[PaperModePreflightRun]
    audit_entries: list[NoWriteAdmissionAuditEntry]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]


def no_write_contract_clause_to_dict(item: NoWriteContractClause) -> dict:
    from dataclasses import asdict
    return asdict(item)

def no_write_paper_admission_contract_to_dict(item: NoWritePaperAdmissionContract) -> dict:
    from dataclasses import asdict
    return asdict(item)

def activation_replay_plan_to_dict(item: ActivationReplayPlan) -> dict:
    from dataclasses import asdict
    return asdict(item)

def activation_replay_result_to_dict(item: ActivationReplayResult) -> dict:
    from dataclasses import asdict
    return asdict(item)

def paper_mode_simulation_step_to_dict(item: PaperModeSimulationStep) -> dict:
    from dataclasses import asdict
    return asdict(item)

def paper_mode_preflight_run_to_dict(item: PaperModePreflightRun) -> dict:
    from dataclasses import asdict
    return asdict(item)

def no_write_admission_audit_entry_to_dict(item: NoWriteAdmissionAuditEntry) -> dict:
    from dataclasses import asdict
    return asdict(item)

def no_write_admission_full_review_to_dict(item: NoWriteAdmissionFullReview) -> dict:
    from dataclasses import asdict
    return asdict(item)

def validate_no_write_contract_clause(item: NoWriteContractClause) -> None:
    pass

def validate_no_write_paper_admission_contract(item: NoWritePaperAdmissionContract) -> None:
    if not item.manual_review_required:
        raise ValueError("manual_review_required must be true")
    if not item.activation_denied:
        raise ValueError("activation_denied must be true")
    if item.activation_allowed:
        raise ValueError("activation_allowed must be false")
    if not item.all_writes_blocked:
        raise ValueError("all_writes_blocked must be true")
    if item.allows_active_paper:
        raise ValueError("allows_active_paper must be false")
    if item.allows_broker_execution:
        raise ValueError("allows_broker_execution must be false")
    if item.allows_paper_state_mutation:
        raise ValueError("allows_paper_state_mutation must be false")
    if item.allows_config_patch:
        raise ValueError("allows_config_patch must be false")
    if item.allows_telegram_real_send:
        raise ValueError("allows_telegram_real_send must be false")

def validate_activation_replay_plan(item: ActivationReplayPlan) -> None:
    if item.execution_enabled:
        raise ValueError("execution_enabled must be false")
    if item.active_paper_enabled:
        raise ValueError("active_paper_enabled must be false")
    if item.broker_execution_enabled:
        raise ValueError("broker_execution_enabled must be false")
    if item.paper_state_mutation_enabled:
        raise ValueError("paper_state_mutation_enabled must be false")
    if item.config_patch_enabled:
        raise ValueError("config_patch_enabled must be false")
    if item.telegram_real_send_enabled:
        raise ValueError("telegram_real_send_enabled must be false")
    if not item.require_all_attempts_denied:
        raise ValueError("require_all_attempts_denied must be true")

def validate_activation_replay_result(item: ActivationReplayResult) -> None:
    pass

def validate_paper_mode_simulation_step(item: PaperModeSimulationStep) -> None:
    if item.write_attempted:
        raise ValueError("write_attempted must be false")
    if item.order_attempted:
        raise ValueError("order_attempted must be false")
    if item.broker_send_attempted:
        raise ValueError("broker_send_attempted must be false")
    if item.config_patch_attempted:
        raise ValueError("config_patch_attempted must be false")
    if item.telegram_real_send_attempted:
        raise ValueError("telegram_real_send_attempted must be false")
    if item.active_paper_enable_attempted:
        raise ValueError("active_paper_enable_attempted must be false")

def validate_paper_mode_preflight_run(item: PaperModePreflightRun) -> None:
    if item.mutation_detected:
        raise ValueError("mutation_detected must be false")

def validate_no_write_admission_full_review(item: NoWriteAdmissionFullReview) -> None:
    pass

import uuid
from datetime import datetime, timezone

def create_no_write_contract_clause_id(prefix: str = "no_write_clause") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_no_write_admission_contract_id(prefix: str = "no_write_contract") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_activation_replay_plan_id(prefix: str = "activation_replay_plan") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_activation_replay_result_id(prefix: str = "activation_replay_result") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_paper_mode_simulation_step_id(prefix: str = "paper_mode_step") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_paper_mode_preflight_id(prefix: str = "paper_mode_preflight") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_no_write_admission_audit_id(prefix: str = "no_write_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_no_write_admission_full_review_id(prefix: str = "no_write_full_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
