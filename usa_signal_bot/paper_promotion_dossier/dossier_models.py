"""Data models for the non-executing observer promotion dossier (Phase 78).

All ``allowed_*`` / ``*_enabled`` safety flags must stay False: these models are
read-only metadata and never enable paper activation, broker execution, paper
state mutation or config patching.
"""
import dataclasses
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import (
    FinalSafetyBoardDecision,
    FinalSafetyBoardStatus,
    PromotionDossierDecision,
    PromotionDossierReportType,
    PromotionDossierRiskFlag,
    PromotionDossierStatus,
    ReadinessGateStatus,
    ReadinessPackageStatus,
    ReadinessStage,
)


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def create_promotion_evidence_index_id(prefix: str = "promotion_evidence_index") -> str:
    return _new_id(prefix)


def create_observer_promotion_dossier_id(prefix: str = "observer_promotion_dossier") -> str:
    return _new_id(prefix)


def create_final_safety_board_gate_id(prefix: str = "final_safety_board_gate") -> str:
    return _new_id(prefix)


def create_promotion_risk_register_item_id(prefix: str = "promotion_risk") -> str:
    return _new_id(prefix)


def create_final_safety_board_review_id(prefix: str = "final_safety_board_review") -> str:
    return _new_id(prefix)


def create_readiness_stage_plan_id(prefix: str = "readiness_stage_plan") -> str:
    return _new_id(prefix)


def create_staged_readiness_package_id(prefix: str = "staged_readiness_package") -> str:
    return _new_id(prefix)


def create_promotion_dossier_audit_id(prefix: str = "promotion_dossier_audit") -> str:
    return _new_id(prefix)


def create_promotion_dossier_review_id(prefix: str = "promotion_dossier_review") -> str:
    return _new_id(prefix)


@dataclass
class PromotionEvidenceIndex:
    evidence_index_id: str
    created_at_utc: str
    candidate_id: Optional[str] = None
    evidence_refs: List[str] = field(default_factory=list)
    required_evidence_types: List[str] = field(default_factory=list)
    available_evidence_types: List[str] = field(default_factory=list)
    missing_evidence_types: List[str] = field(default_factory=list)
    stale_evidence_types: List[str] = field(default_factory=list)
    evidence_score: Optional[float] = None
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ObserverPromotionDossier:
    dossier_id: str
    created_at_utc: str
    status: PromotionDossierStatus
    candidate_id: Optional[str] = None
    source_observer_governance_review_id: Optional[str] = None
    source_observer_governance_decision: Optional[str] = None
    evidence_index: Optional[PromotionEvidenceIndex] = None
    decision: PromotionDossierDecision = PromotionDossierDecision.INCONCLUSIVE
    safety_flags: List[PromotionDossierRiskFlag] = field(default_factory=list)
    manual_review_required: bool = True
    final_safety_board_required: bool = True
    allowed_for_active_paper: bool = False
    allowed_for_broker_execution: bool = False
    allowed_for_paper_state_mutation: bool = False
    allowed_for_config_patch: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


@dataclass
class FinalSafetyBoardGate:
    gate_id: str
    created_at_utc: str
    gate_name: str
    status: ReadinessGateStatus
    observed_value: Any = None
    threshold: Any = None
    description: str = ""
    risk_flags: List[PromotionDossierRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


@dataclass
class PromotionRiskRegisterItem:
    risk_id: str
    created_at_utc: str
    risk_flag: PromotionDossierRiskFlag
    severity: str = "MEDIUM"
    description: str = ""
    mitigation: str = ""
    blocking: bool = False
    evidence_refs: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


@dataclass
class FinalSafetyBoardReview:
    board_review_id: str
    created_at_utc: str
    status: FinalSafetyBoardStatus
    dossier_id: str
    candidate_id: Optional[str] = None
    gates: List[FinalSafetyBoardGate] = field(default_factory=list)
    risk_register: List[PromotionRiskRegisterItem] = field(default_factory=list)
    decision: FinalSafetyBoardDecision = FinalSafetyBoardDecision.BLOCK_DOSSIER
    rationale: str = ""
    required_followups: List[str] = field(default_factory=list)
    manual_review_required: bool = True
    allowed_for_active_paper: bool = False
    allowed_for_broker_execution: bool = False
    allowed_for_paper_state_mutation: bool = False
    allowed_for_config_patch: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


@dataclass
class ReadinessStagePlan:
    stage_plan_id: str
    created_at_utc: str
    stage: ReadinessStage
    title: str = ""
    description: str = ""
    required_inputs: List[str] = field(default_factory=list)
    required_gates: List[str] = field(default_factory=list)
    output_artifacts: List[str] = field(default_factory=list)
    execution_enabled: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    config_patch_enabled: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


@dataclass
class StagedPaperReadinessPackage:
    package_id: str
    created_at_utc: str
    status: ReadinessPackageStatus
    dossier_id: str
    board_review_id: str
    candidate_id: Optional[str] = None
    stage_plans: List[ReadinessStagePlan] = field(default_factory=list)
    evidence_refs: List[str] = field(default_factory=list)
    safety_flags: List[PromotionDossierRiskFlag] = field(default_factory=list)
    package_summary: Dict[str, Any] = field(default_factory=dict)
    allowed_for_active_paper: bool = False
    allowed_for_broker_execution: bool = False
    allowed_for_paper_state_mutation: bool = False
    allowed_for_config_patch: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


@dataclass
class PromotionDossierAuditEntry:
    audit_id: str
    created_at_utc: str
    entity_type: str
    entity_id: str
    action: str
    decision: Optional[str] = None
    rationale: str = ""
    evidence_refs: List[str] = field(default_factory=list)
    risk_flags: List[PromotionDossierRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


@dataclass
class PromotionDossierReview:
    review_id: str
    created_at_utc: str
    report_type: PromotionDossierReportType = PromotionDossierReportType.FULL_PROMOTION_DOSSIER_REVIEW
    dossiers: List[ObserverPromotionDossier] = field(default_factory=list)
    board_reviews: List[FinalSafetyBoardReview] = field(default_factory=list)
    readiness_packages: List[StagedPaperReadinessPackage] = field(default_factory=list)
    audit_entries: List[PromotionDossierAuditEntry] = field(default_factory=list)
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def _to_plain(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return {f.name: _to_plain(getattr(obj, f.name)) for f in dataclasses.fields(obj)}
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, (list, tuple)):
        return [_to_plain(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _to_plain(v) for k, v in obj.items()}
    return obj


def promotion_evidence_index_to_dict(item: PromotionEvidenceIndex) -> Dict[str, Any]:
    return _to_plain(item)


def observer_promotion_dossier_to_dict(item: ObserverPromotionDossier) -> Dict[str, Any]:
    return _to_plain(item)


def final_safety_board_gate_to_dict(item: FinalSafetyBoardGate) -> Dict[str, Any]:
    return _to_plain(item)


def promotion_risk_register_item_to_dict(item: PromotionRiskRegisterItem) -> Dict[str, Any]:
    return _to_plain(item)


def final_safety_board_review_to_dict(item: FinalSafetyBoardReview) -> Dict[str, Any]:
    return _to_plain(item)


def readiness_stage_plan_to_dict(item: ReadinessStagePlan) -> Dict[str, Any]:
    return _to_plain(item)


def staged_paper_readiness_package_to_dict(item: StagedPaperReadinessPackage) -> Dict[str, Any]:
    return _to_plain(item)


def promotion_dossier_audit_entry_to_dict(item: PromotionDossierAuditEntry) -> Dict[str, Any]:
    return _to_plain(item)


def promotion_dossier_review_to_dict(item: PromotionDossierReview) -> Dict[str, Any]:
    return _to_plain(item)
