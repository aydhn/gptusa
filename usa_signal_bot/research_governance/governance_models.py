from dataclasses import dataclass, field
from typing import Any, Optional
from usa_signal_bot.core.enums import (
    EvidencePackStatus, GovernanceChecklistStatus, GovernanceRiskFlag,
    GovernanceReviewStatus, PromotionEligibility, PromotionDecision,
    ReleaseCandidateStatus, DecisionBoardMode, GovernanceReportType
)
from usa_signal_bot.core.exceptions import GovernanceValidationError
import uuid

@dataclass
class GovernanceEvidencePack:
    evidence_pack_id: str
    created_at_utc: str
    experiment_id: Optional[str]
    hypothesis_id: Optional[str]
    comparison_report_id: Optional[str]
    baseline_run_id: Optional[str]
    candidate_run_id: Optional[str]
    status: EvidencePackStatus
    required_evidence: list[str]
    available_evidence: list[str]
    missing_evidence: list[str]
    metrics_summary: dict[str, Any]
    gate_summary: dict[str, Any]
    attribution_summary: dict[str, Any]
    diagnostics_summary: dict[str, Any]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class GovernanceChecklistItem:
    checklist_id: str
    name: str
    status: GovernanceChecklistStatus
    description: str
    evidence_refs: list[str]
    risk_flags: list[GovernanceRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PromotionReview:
    review_id: str
    created_at_utc: str
    experiment_id: Optional[str]
    hypothesis_id: Optional[str]
    status: GovernanceReviewStatus
    eligibility: PromotionEligibility
    proposed_decision: PromotionDecision
    eligibility_score: Optional[float]
    evidence_pack: Optional[GovernanceEvidencePack]
    checklist_items: list[GovernanceChecklistItem]
    risk_flags: list[GovernanceRiskFlag]
    manual_review_required: bool
    allowed_for_auto_promotion: bool
    allowed_for_config_patch: bool
    allowed_for_order_routing: bool
    rationale: str
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ReleaseCandidatePackage:
    candidate_id: str
    created_at_utc: str
    experiment_id: Optional[str]
    hypothesis_id: Optional[str]
    source_review_id: Optional[str]
    status: ReleaseCandidateStatus
    title: str
    description: str
    candidate_config_ref: Optional[str]
    baseline_config_ref: Optional[str]
    included_artifacts: list[str]
    evidence_pack_id: Optional[str]
    promotion_decision: PromotionDecision
    manual_review_required: bool
    allowed_for_auto_apply: bool
    allowed_for_live_or_demo_execution: bool
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class DecisionBoardResult:
    board_result_id: str
    created_at_utc: str
    mode: DecisionBoardMode
    review_id: Optional[str]
    candidate_id: Optional[str]
    final_decision: PromotionDecision
    eligibility: PromotionEligibility
    passed_check_count: int
    warning_check_count: int
    failed_check_count: int
    risk_flags: list[GovernanceRiskFlag]
    rationale: str
    required_followups: list[str]
    allowed_for_auto_promotion: bool
    allowed_for_config_patch: bool
    allowed_for_order_routing: bool
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class PromotionDecisionLogEntry:
    entry_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    decision: PromotionDecision
    rationale: str
    evidence_refs: list[str]
    risk_flags: list[GovernanceRiskFlag]
    made_by: str
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class GovernanceAuditTrail:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    events: list[dict[str, Any]]
    warning_count: int
    error_count: int
    blocked_count: int
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class GovernanceReview:
    governance_review_id: str
    created_at_utc: str
    report_type: GovernanceReportType
    evidence_packs: list[GovernanceEvidencePack]
    promotion_reviews: list[PromotionReview]
    release_candidates: list[ReleaseCandidatePackage]
    decision_board_results: list[DecisionBoardResult]
    decision_logs: list[PromotionDecisionLogEntry]
    audit_trails: list[GovernanceAuditTrail]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

import json
from dataclasses import asdict

def governance_evidence_pack_to_dict(item: GovernanceEvidencePack) -> dict:
    return asdict(item)

def governance_checklist_item_to_dict(item: GovernanceChecklistItem) -> dict:
    return asdict(item)

def promotion_review_to_dict(item: PromotionReview) -> dict:
    return asdict(item)

def release_candidate_package_to_dict(item: ReleaseCandidatePackage) -> dict:
    return asdict(item)

def decision_board_result_to_dict(item: DecisionBoardResult) -> dict:
    return asdict(item)

def promotion_decision_log_entry_to_dict(item: PromotionDecisionLogEntry) -> dict:
    return asdict(item)

def governance_audit_trail_to_dict(item: GovernanceAuditTrail) -> dict:
    return asdict(item)

def governance_review_to_dict(item: GovernanceReview) -> dict:
    return asdict(item)

def validate_governance_evidence_pack(item: GovernanceEvidencePack) -> None:
    pass

def validate_governance_checklist_item(item: GovernanceChecklistItem) -> None:
    pass

def validate_promotion_review(item: PromotionReview) -> None:
    if item.allowed_for_auto_promotion: raise GovernanceValidationError("allowed_for_auto_promotion must be false")
    if item.allowed_for_config_patch: raise GovernanceValidationError("allowed_for_config_patch must be false")
    if item.allowed_for_order_routing: raise GovernanceValidationError("allowed_for_order_routing must be false")
    if item.eligibility_score is not None and not (0 <= item.eligibility_score <= 100): raise GovernanceValidationError("eligibility_score must be 0-100")

def validate_release_candidate_package(item: ReleaseCandidatePackage) -> None:
    if item.allowed_for_auto_apply: raise GovernanceValidationError("allowed_for_auto_apply must be false")
    if item.allowed_for_live_or_demo_execution: raise GovernanceValidationError("allowed_for_live_or_demo_execution must be false")
    if not item.title: raise GovernanceValidationError("title cannot be empty")

def validate_decision_board_result(item: DecisionBoardResult) -> None:
    if item.allowed_for_auto_promotion: raise GovernanceValidationError("allowed_for_auto_promotion must be false")
    if item.allowed_for_config_patch: raise GovernanceValidationError("allowed_for_config_patch must be false")
    if item.allowed_for_order_routing: raise GovernanceValidationError("allowed_for_order_routing must be false")

def validate_governance_review(item: GovernanceReview) -> None:
    pass

def create_governance_evidence_pack_id(prefix: str = "evidence_pack") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_governance_checklist_item_id(name: str) -> str:
    return f"check_{uuid.uuid4().hex[:8]}"

def create_promotion_review_id(prefix: str = "promotion_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_release_candidate_package_id(prefix: str = "release_candidate") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_decision_board_result_id(prefix: str = "decision_board") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_promotion_decision_log_entry_id(prefix: str = "promotion_decision") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_governance_audit_trail_id(prefix: str = "governance_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_governance_review_id(prefix: str = "governance_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
