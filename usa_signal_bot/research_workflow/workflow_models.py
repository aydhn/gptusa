from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict
from ..core.enums import (
    RepairItemType,
    RepairPriority,
    RepairStatus,
    HypothesisStatus,
    HypothesisConfidence,
    ExperimentType,
    ExperimentScope,
    ExperimentStatus,
    AcceptanceGateType,
    AcceptanceGateStatus,
    ResearchRiskLevel,
    ResearchWorkflowReportType
)
from ..core.exceptions import ResearchWorkflowValidationError
import uuid
import datetime

@dataclass
class RepairQueueItem:
    item_id: str
    created_at_utc: str
    item_type: RepairItemType
    priority: RepairPriority
    status: RepairStatus
    target_scope: Optional[str]
    target_name: Optional[str]
    title: str
    description: str
    source_failure_modes: List[str]
    evidence_refs: List[str]
    diagnostic_severity: Optional[str]
    evidence_quality: Optional[str]
    suggested_safe_action: str
    linked_hypothesis_ids: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ResearchHypothesis:
    hypothesis_id: str
    created_at_utc: str
    status: HypothesisStatus
    confidence: HypothesisConfidence
    title: str
    hypothesis_statement: str
    target_scope: ExperimentScope
    target_name: Optional[str]
    expected_effect: str
    expected_risk: str
    null_condition: str
    success_criteria: List[str]
    failure_criteria: List[str]
    evidence_refs: List[str]
    linked_repair_item_ids: List[str]
    linked_experiment_ids: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ParameterChangeProposal:
    proposal_id: str
    created_at_utc: str
    target_module: Optional[str]
    target_strategy: Optional[str]
    parameter_name: str
    baseline_value: Any
    candidate_value: Any
    change_reason: str
    expected_effect: str
    risk_notes: List[str]
    allowed_for_auto_apply: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AcceptanceGate:
    gate_id: str
    gate_type: AcceptanceGateType
    status: AcceptanceGateStatus
    threshold: Optional[Any]
    observed_value: Optional[Any]
    description: str
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ExperimentPlan:
    experiment_id: str
    created_at_utc: str
    experiment_type: ExperimentType
    scope: ExperimentScope
    status: ExperimentStatus
    title: str
    description: str
    linked_hypothesis_id: Optional[str]
    baseline_config_ref: Optional[str]
    candidate_config_ref: Optional[str]
    parameter_change_proposals: List[ParameterChangeProposal]
    validation_plan: Dict[str, Any]
    acceptance_gates: List[AcceptanceGate]
    rollback_plan: Dict[str, Any]
    dependency_ids: List[str]
    risk_level: ResearchRiskLevel
    allowed_for_auto_execution: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ResearchDecisionLogEntry:
    entry_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    decision: str
    rationale: str
    evidence_refs: List[str]
    made_by: str
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ResearchWorkflowReview:
    review_id: str
    created_at_utc: str
    report_type: ResearchWorkflowReportType
    repair_items: List[RepairQueueItem]
    hypotheses: List[ResearchHypothesis]
    experiment_plans: List[ExperimentPlan]
    decision_log_entries: List[ResearchDecisionLogEntry]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

def repair_queue_item_to_dict(item: RepairQueueItem) -> dict:
    return {
        "item_id": item.item_id,
        "created_at_utc": item.created_at_utc,
        "item_type": item.item_type.value if hasattr(item.item_type, 'value') else item.item_type,
        "priority": item.priority.value if hasattr(item.priority, 'value') else item.priority,
        "status": item.status.value if hasattr(item.status, 'value') else item.status,
        "target_scope": item.target_scope,
        "target_name": item.target_name,
        "title": item.title,
        "description": item.description,
        "source_failure_modes": item.source_failure_modes,
        "evidence_refs": item.evidence_refs,
        "diagnostic_severity": item.diagnostic_severity,
        "evidence_quality": item.evidence_quality,
        "suggested_safe_action": item.suggested_safe_action,
        "linked_hypothesis_ids": item.linked_hypothesis_ids,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def research_hypothesis_to_dict(item: ResearchHypothesis) -> dict:
    return {
        "hypothesis_id": item.hypothesis_id,
        "created_at_utc": item.created_at_utc,
        "status": item.status.value if hasattr(item.status, 'value') else item.status,
        "confidence": item.confidence.value if hasattr(item.confidence, 'value') else item.confidence,
        "title": item.title,
        "hypothesis_statement": item.hypothesis_statement,
        "target_scope": item.target_scope.value if hasattr(item.target_scope, 'value') else item.target_scope,
        "target_name": item.target_name,
        "expected_effect": item.expected_effect,
        "expected_risk": item.expected_risk,
        "null_condition": item.null_condition,
        "success_criteria": item.success_criteria,
        "failure_criteria": item.failure_criteria,
        "evidence_refs": item.evidence_refs,
        "linked_repair_item_ids": item.linked_repair_item_ids,
        "linked_experiment_ids": item.linked_experiment_ids,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def parameter_change_proposal_to_dict(item: ParameterChangeProposal) -> dict:
    return {
        "proposal_id": item.proposal_id,
        "created_at_utc": item.created_at_utc,
        "target_module": item.target_module,
        "target_strategy": item.target_strategy,
        "parameter_name": item.parameter_name,
        "baseline_value": item.baseline_value,
        "candidate_value": item.candidate_value,
        "change_reason": item.change_reason,
        "expected_effect": item.expected_effect,
        "risk_notes": item.risk_notes,
        "allowed_for_auto_apply": item.allowed_for_auto_apply,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def acceptance_gate_to_dict(item: AcceptanceGate) -> dict:
    return {
        "gate_id": item.gate_id,
        "gate_type": item.gate_type.value if hasattr(item.gate_type, 'value') else item.gate_type,
        "status": item.status.value if hasattr(item.status, 'value') else item.status,
        "threshold": item.threshold,
        "observed_value": item.observed_value,
        "description": item.description,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def experiment_plan_to_dict(item: ExperimentPlan) -> dict:
    return {
        "experiment_id": item.experiment_id,
        "created_at_utc": item.created_at_utc,
        "experiment_type": item.experiment_type.value if hasattr(item.experiment_type, 'value') else item.experiment_type,
        "scope": item.scope.value if hasattr(item.scope, 'value') else item.scope,
        "status": item.status.value if hasattr(item.status, 'value') else item.status,
        "title": item.title,
        "description": item.description,
        "linked_hypothesis_id": item.linked_hypothesis_id,
        "baseline_config_ref": item.baseline_config_ref,
        "candidate_config_ref": item.candidate_config_ref,
        "parameter_change_proposals": [parameter_change_proposal_to_dict(p) for p in item.parameter_change_proposals],
        "validation_plan": item.validation_plan,
        "acceptance_gates": [acceptance_gate_to_dict(g) for g in item.acceptance_gates],
        "rollback_plan": item.rollback_plan,
        "dependency_ids": item.dependency_ids,
        "risk_level": item.risk_level.value if hasattr(item.risk_level, 'value') else item.risk_level,
        "allowed_for_auto_execution": item.allowed_for_auto_execution,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def research_decision_log_entry_to_dict(item: ResearchDecisionLogEntry) -> dict:
    return {
        "entry_id": item.entry_id,
        "created_at_utc": item.created_at_utc,
        "entity_type": item.entity_type,
        "entity_id": item.entity_id,
        "decision": item.decision,
        "rationale": item.rationale,
        "evidence_refs": item.evidence_refs,
        "made_by": item.made_by,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }

def research_workflow_review_to_dict(item: ResearchWorkflowReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": item.report_type.value if hasattr(item.report_type, 'value') else item.report_type,
        "repair_items": [repair_queue_item_to_dict(i) for i in item.repair_items],
        "hypotheses": [research_hypothesis_to_dict(h) for h in item.hypotheses],
        "experiment_plans": [experiment_plan_to_dict(e) for e in item.experiment_plans],
        "decision_log_entries": [research_decision_log_entry_to_dict(d) for d in item.decision_log_entries],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }

def _check_forbidden_language(text: str) -> None:
    forbidden = ["live approved", "sent to broker", "kesin al", "garanti",
                 "otomatik optimize et", "parametreyi otomatik değiştir",
                 "kesin uygula", "kesin kâr"]
    text_lower = text.lower()
    for word in forbidden:
        if word in text_lower:
            raise ResearchWorkflowValidationError(f"Forbidden language used: {word}")

def validate_repair_queue_item(item: RepairQueueItem) -> None:
    if not item.title:
        raise ResearchWorkflowValidationError("Title cannot be empty")
    _check_forbidden_language(item.title)
    _check_forbidden_language(item.description)
    _check_forbidden_language(item.suggested_safe_action)

def validate_research_hypothesis(item: ResearchHypothesis) -> None:
    if not item.title:
        raise ResearchWorkflowValidationError("Title cannot be empty")
    if not item.hypothesis_statement:
        raise ResearchWorkflowValidationError("Hypothesis statement cannot be empty")
    _check_forbidden_language(item.title)
    _check_forbidden_language(item.hypothesis_statement)
    _check_forbidden_language(item.expected_effect)
    _check_forbidden_language(item.expected_risk)

def validate_parameter_change_proposal(item: ParameterChangeProposal) -> None:
    if not item.parameter_name:
        raise ResearchWorkflowValidationError("Parameter name cannot be empty")
    if item.allowed_for_auto_apply:
        raise ResearchWorkflowValidationError("allowed_for_auto_apply must be false")
    _check_forbidden_language(item.change_reason)
    _check_forbidden_language(item.expected_effect)

def validate_acceptance_gate(item: AcceptanceGate) -> None:
    _check_forbidden_language(item.description)

def validate_experiment_plan(item: ExperimentPlan) -> None:
    if not item.title:
        raise ResearchWorkflowValidationError("Title cannot be empty")
    if item.allowed_for_auto_execution:
        raise ResearchWorkflowValidationError("allowed_for_auto_execution must be false")
    _check_forbidden_language(item.title)
    _check_forbidden_language(item.description)

def validate_research_workflow_review(item: ResearchWorkflowReview) -> None:
    for i in item.repair_items: validate_repair_queue_item(i)
    for h in item.hypotheses: validate_research_hypothesis(h)
    for e in item.experiment_plans: validate_experiment_plan(e)

def create_repair_queue_item_id(prefix: str = "repair_item") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_research_hypothesis_id(prefix: str = "hypothesis") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_parameter_change_proposal_id(parameter_name: str) -> str:
    return f"proposal_{parameter_name}_{uuid.uuid4().hex[:8]}"

def create_acceptance_gate_id(gate_type: AcceptanceGateType) -> str:
    return f"gate_{gate_type.value}_{uuid.uuid4().hex[:8]}"

def create_experiment_plan_id(prefix: str = "experiment_plan") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_research_decision_log_entry_id(prefix: str = "decision") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_research_workflow_review_id(prefix: str = "research_workflow_review") -> str:
    return f"{prefix}_{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
