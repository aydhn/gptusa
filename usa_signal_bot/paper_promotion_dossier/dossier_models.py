import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, List, Optional, Dict
from usa_signal_bot.core.enums import (
    PromotionDossierStatus,
    PromotionDossierDecision,
    FinalSafetyBoardStatus,
    FinalSafetyBoardDecision,
    ReadinessPackageStatus,
    ReadinessStage,
    ReadinessGateStatus,
    PromotionDossierRiskFlag,
    PromotionDossierReportType
)
from usa_signal_bot.core.exceptions import PromotionDossierValidationError

@dataclass
class PromotionEvidenceIndex:
    evidence_index_id: str
    created_at_utc: str
    candidate_id: Optional[str]
    evidence_refs: List[str]
    required_evidence_types: List[str]
    available_evidence_types: List[str]
    missing_evidence_types: List[str]
    stale_evidence_types: List[str]
    evidence_score: Optional[float]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ObserverPromotionDossier:
    dossier_id: str
    created_at_utc: str
    status: PromotionDossierStatus
    candidate_id: Optional[str]
    source_observer_governance_review_id: Optional[str]
    source_observer_governance_decision: Optional[str]
    evidence_index: Optional[PromotionEvidenceIndex]
    decision: PromotionDossierDecision
    safety_flags: List[PromotionDossierRiskFlag]
    manual_review_required: bool
    final_safety_board_required: bool
    allowed_for_active_paper: bool
    allowed_for_broker_execution: bool
    allowed_for_paper_state_mutation: bool
    allowed_for_config_patch: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FinalSafetyBoardGate:
    gate_id: str
    created_at_utc: str
    gate_name: str
    status: ReadinessGateStatus
    observed_value: Any
    threshold: Any
    description: str
    risk_flags: List[PromotionDossierRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PromotionRiskRegisterItem:
    risk_id: str
    created_at_utc: str
    risk_flag: PromotionDossierRiskFlag
    severity: str
    description: str
    mitigation: str
    blocking: bool
    evidence_refs: List[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FinalSafetyBoardReview:
    board_review_id: str
    created_at_utc: str
    status: FinalSafetyBoardStatus
    dossier_id: Optional[str]
    candidate_id: Optional[str]
    gates: List[FinalSafetyBoardGate]
    risk_register: List[PromotionRiskRegisterItem]
    decision: FinalSafetyBoardDecision
    rationale: str
    required_followups: List[str]
    manual_review_required: bool
    allowed_for_active_paper: bool
    allowed_for_broker_execution: bool
    allowed_for_paper_state_mutation: bool
    allowed_for_config_patch: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReadinessStagePlan:
    stage_plan_id: str
    created_at_utc: str
    stage: ReadinessStage
    title: str
    description: str
    required_inputs: List[str]
    required_gates: List[str]
    output_artifacts: List[str]
    execution_enabled: bool
    active_paper_enabled: bool
    broker_execution_enabled: bool
    paper_state_mutation_enabled: bool
    config_patch_enabled: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StagedPaperReadinessPackage:
    package_id: str
    created_at_utc: str
    status: ReadinessPackageStatus
    dossier_id: Optional[str]
    board_review_id: Optional[str]
    candidate_id: Optional[str]
    stage_plans: List[ReadinessStagePlan]
    evidence_refs: List[str]
    safety_flags: List[PromotionDossierRiskFlag]
    package_summary: Dict[str, Any]
    allowed_for_active_paper: bool
    allowed_for_broker_execution: bool
    allowed_for_paper_state_mutation: bool
    allowed_for_config_patch: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PromotionDossierAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: Optional[str]
    rationale: str
    evidence_refs: List[str]
    risk_flags: List[PromotionDossierRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PromotionDossierReview:
    review_id: str
    created_at_utc: str
    report_type: PromotionDossierReportType
    dossiers: List[ObserverPromotionDossier]
    board_reviews: List[FinalSafetyBoardReview]
    readiness_packages: List[StagedPaperReadinessPackage]
    audit_entries: List[PromotionDossierAuditEntry]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

# Dictionary Converters
def promotion_evidence_index_to_dict(item: PromotionEvidenceIndex) -> dict:
    d = asdict(item)
    return d

def observer_promotion_dossier_to_dict(item: ObserverPromotionDossier) -> dict:
    d = asdict(item)
    if d.get("evidence_index"):
        d["evidence_index"] = promotion_evidence_index_to_dict(item.evidence_index)
    return d

def final_safety_board_gate_to_dict(item: FinalSafetyBoardGate) -> dict:
    return asdict(item)

def promotion_risk_register_item_to_dict(item: PromotionRiskRegisterItem) -> dict:
    return asdict(item)

def final_safety_board_review_to_dict(item: FinalSafetyBoardReview) -> dict:
    d = asdict(item)
    d["gates"] = [final_safety_board_gate_to_dict(g) for g in item.gates]
    d["risk_register"] = [promotion_risk_register_item_to_dict(r) for r in item.risk_register]
    return d

def readiness_stage_plan_to_dict(item: ReadinessStagePlan) -> dict:
    return asdict(item)

def staged_paper_readiness_package_to_dict(item: StagedPaperReadinessPackage) -> dict:
    d = asdict(item)
    d["stage_plans"] = [readiness_stage_plan_to_dict(s) for s in item.stage_plans]
    return d

def promotion_dossier_audit_entry_to_dict(item: PromotionDossierAuditEntry) -> dict:
    return asdict(item)

def promotion_dossier_review_to_dict(item: PromotionDossierReview) -> dict:
    d = asdict(item)
    d["dossiers"] = [observer_promotion_dossier_to_dict(x) for x in item.dossiers]
    d["board_reviews"] = [final_safety_board_review_to_dict(x) for x in item.board_reviews]
    d["readiness_packages"] = [staged_paper_readiness_package_to_dict(x) for x in item.readiness_packages]
    d["audit_entries"] = [promotion_dossier_audit_entry_to_dict(x) for x in item.audit_entries]
    return d

# Validators
def _check_no_execution_language(text: str, context: str):
    lower = text.lower()
    banned = ["live approved", "sent to broker", "kesin al", "garanti", "paper'a uygula", "canlıya al", "gerçek emir", "aktif et", "kesin kâr", "candidate kesin iyi"]
    for b in banned:
        if b in lower:
            raise PromotionDossierValidationError(f"Banned language found in {context}: {b}")

def validate_promotion_evidence_index(item: PromotionEvidenceIndex) -> None:
    if item.evidence_score is not None:
        if not (0 <= item.evidence_score <= 100):
            raise PromotionDossierValidationError("evidence_score must be between 0 and 100 or None")

def validate_observer_promotion_dossier(item: ObserverPromotionDossier) -> None:
    if item.allowed_for_active_paper: raise PromotionDossierValidationError("allowed_for_active_paper must be False")
    if item.allowed_for_broker_execution: raise PromotionDossierValidationError("allowed_for_broker_execution must be False")
    if item.allowed_for_paper_state_mutation: raise PromotionDossierValidationError("allowed_for_paper_state_mutation must be False")
    if item.allowed_for_config_patch: raise PromotionDossierValidationError("allowed_for_config_patch must be False")

def validate_final_safety_board_gate(item: FinalSafetyBoardGate) -> None:
    _check_no_execution_language(item.description, "FinalSafetyBoardGate")

def validate_final_safety_board_review(item: FinalSafetyBoardReview) -> None:
    if item.allowed_for_active_paper: raise PromotionDossierValidationError("allowed_for_active_paper must be False")
    if item.allowed_for_broker_execution: raise PromotionDossierValidationError("allowed_for_broker_execution must be False")
    if item.allowed_for_paper_state_mutation: raise PromotionDossierValidationError("allowed_for_paper_state_mutation must be False")
    if item.allowed_for_config_patch: raise PromotionDossierValidationError("allowed_for_config_patch must be False")
    _check_no_execution_language(item.rationale, "FinalSafetyBoardReview")
    for gate in item.gates:
        validate_final_safety_board_gate(gate)

def validate_readiness_stage_plan(item: ReadinessStagePlan) -> None:
    if item.execution_enabled: raise PromotionDossierValidationError("execution_enabled must be False")
    if item.active_paper_enabled: raise PromotionDossierValidationError("active_paper_enabled must be False")
    if item.broker_execution_enabled: raise PromotionDossierValidationError("broker_execution_enabled must be False")
    if item.paper_state_mutation_enabled: raise PromotionDossierValidationError("paper_state_mutation_enabled must be False")
    if item.config_patch_enabled: raise PromotionDossierValidationError("config_patch_enabled must be False")
    _check_no_execution_language(item.description, "ReadinessStagePlan")

def validate_staged_paper_readiness_package(item: StagedPaperReadinessPackage) -> None:
    if item.allowed_for_active_paper: raise PromotionDossierValidationError("allowed_for_active_paper must be False")
    if item.allowed_for_broker_execution: raise PromotionDossierValidationError("allowed_for_broker_execution must be False")
    if item.allowed_for_paper_state_mutation: raise PromotionDossierValidationError("allowed_for_paper_state_mutation must be False")
    if item.allowed_for_config_patch: raise PromotionDossierValidationError("allowed_for_config_patch must be False")
    for stage in item.stage_plans:
        validate_readiness_stage_plan(stage)

def validate_promotion_dossier_review(item: PromotionDossierReview) -> None:
    for d in item.dossiers:
        validate_observer_promotion_dossier(d)
    for b in item.board_reviews:
        validate_final_safety_board_review(b)
    for p in item.readiness_packages:
        validate_staged_paper_readiness_package(p)

# ID Generators
def create_promotion_evidence_index_id(prefix: str = "promotion_evidence_index") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_observer_promotion_dossier_id(prefix: str = "observer_promotion_dossier") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_final_safety_board_gate_id(prefix: str = "final_safety_gate") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_promotion_risk_register_item_id(prefix: str = "promotion_risk") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_final_safety_board_review_id(prefix: str = "final_safety_board") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_readiness_stage_plan_id(prefix: str = "readiness_stage") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_staged_readiness_package_id(prefix: str = "staged_readiness_package") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_promotion_dossier_audit_id(prefix: str = "promotion_dossier_audit") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
def create_promotion_dossier_review_id(prefix: str = "promotion_dossier_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
