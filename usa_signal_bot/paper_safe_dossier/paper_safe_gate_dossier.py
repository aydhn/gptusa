from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import json
import hashlib
from usa_signal_bot.core.enums import PaperSafeDossierStatus, PaperSafeDossierDecision, PaperSafeDossierRiskFlag
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import PaperSafeGateDossier, create_paper_safe_dossier_id, PaperSafeDossierEvidenceItem
from usa_signal_bot.paper_safe_dossier.paper_safe_ingestion import (
    extract_final_paper_safe_gate,
    extract_boundary_replay_result,
    extract_frozen_evidence_integrity_audit,
    extract_paper_safe_candidate_id
)
from usa_signal_bot.paper_safe_dossier.dossier_evidence import collect_paper_safe_dossier_evidence

def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def build_paper_safe_gate_dossier(paper_safe_payload: Dict[str, Any]) -> PaperSafeGateDossier:
    candidate_id = extract_paper_safe_candidate_id(paper_safe_payload)
    gate = extract_final_paper_safe_gate(paper_safe_payload)
    replay = extract_boundary_replay_result(paper_safe_payload)
    audit = extract_frozen_evidence_integrity_audit(paper_safe_payload)
    evidence_items = collect_paper_safe_dossier_evidence(paper_safe_payload)

    gate_passed = False
    if gate and gate.get("decision") in ["VALIDATED_PAPER_SAFE", "PASS_TO_PAPER_SAFE_DOSSIER"]:
        gate_passed = True

    dossier = PaperSafeGateDossier(
        dossier_id=create_paper_safe_dossier_id(),
        created_at_utc=utcnow_iso(),
        status=PaperSafeDossierStatus.CREATED,
        decision=PaperSafeDossierDecision.CREATE_PAPER_SAFE_DOSSIER,
        candidate_id=candidate_id,
        source_paper_safe_review_id=paper_safe_payload.get("review_id"),
        source_paper_safe_gate_id=gate.get("gate_id") if gate else None,
        source_boundary_replay_result_id=replay.get("replay_result_id") if replay else None,
        source_integrity_audit_id=audit.get("audit_id") if audit else None,
        evidence_items=evidence_items,
        non_execution_seal=None,
        runtime_map=None,
        evidence_refs=[i.evidence_id for i in evidence_items],
        dossier_hash=None,
        sealed=True,
        immutable=True,
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        admission_allowed=False,
        transition_allowed=False,
        paper_safe_gate_passed=gate_passed,
        all_writes_blocked=True,
        order_created=False,
        mutation_detected=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        safety_flags=collect_paper_safe_dossier_safety_flags(paper_safe_payload, evidence_items),
        required_followups=[],
        warnings=[],
        errors=[]
    )
    dossier.dossier_hash = stable_paper_safe_dossier_hash(paper_safe_payload)
    return dossier

def build_default_paper_safe_dossier(candidate_id: Optional[str] = None) -> PaperSafeGateDossier:
    return PaperSafeGateDossier(
        dossier_id=create_paper_safe_dossier_id(),
        created_at_utc=utcnow_iso(),
        status=PaperSafeDossierStatus.DRAFT,
        decision=PaperSafeDossierDecision.REQUEST_MANUAL_REVIEW,
        candidate_id=candidate_id,
        source_paper_safe_review_id=None,
        source_paper_safe_gate_id=None,
        source_boundary_replay_result_id=None,
        source_integrity_audit_id=None,
        evidence_items=[],
        non_execution_seal=None,
        runtime_map=None,
        evidence_refs=[],
        dossier_hash=None,
        sealed=True,
        immutable=True,
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        admission_allowed=False,
        transition_allowed=False,
        paper_safe_gate_passed=False,
        all_writes_blocked=True,
        order_created=False,
        mutation_detected=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        safety_flags=[],
        required_followups=[],
        warnings=[],
        errors=[]
    )

def stable_paper_safe_dossier_hash(payload: Dict[str, Any]) -> str:
    s = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def collect_paper_safe_dossier_safety_flags(paper_safe_payload: Dict[str, Any], evidence_items: List[PaperSafeDossierEvidenceItem]) -> List[PaperSafeDossierRiskFlag]:
    flags = []
    gate = extract_final_paper_safe_gate(paper_safe_payload)
    if gate:
        if gate.get("activation_allowed", False):
            flags.append(PaperSafeDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
        if gate.get("admission_allowed", False):
            flags.append(PaperSafeDossierRiskFlag.ADMISSION_ALLOWED_RISK)
        if gate.get("order_created", False):
            flags.append(PaperSafeDossierRiskFlag.ORDER_CREATED_RISK)
        if gate.get("mutation_detected", False):
             flags.append(PaperSafeDossierRiskFlag.MUTATION_DETECTED_RISK)

    audit = extract_frozen_evidence_integrity_audit(paper_safe_payload)
    if audit and audit.get("tamper_count", 0) > 0:
        flags.append(PaperSafeDossierRiskFlag.FROZEN_EVIDENCE_TAMPER_RISK)

    for i in evidence_items:
         if i.required and not i.available:
              if PaperSafeDossierRiskFlag.DOSSIER_EVIDENCE_MISSING not in flags:
                   flags.append(PaperSafeDossierRiskFlag.DOSSIER_EVIDENCE_MISSING)
         if i.stale:
              if PaperSafeDossierRiskFlag.DOSSIER_EVIDENCE_STALE not in flags:
                   flags.append(PaperSafeDossierRiskFlag.DOSSIER_EVIDENCE_STALE)
    return flags

def paper_safe_dossier_summary(dossier: PaperSafeGateDossier) -> Dict[str, Any]:
    return {
        "dossier_id": dossier.dossier_id,
        "status": dossier.status.value,
        "sealed": dossier.sealed,
        "paper_safe_gate_passed": dossier.paper_safe_gate_passed,
        "activation_denied": dossier.activation_denied,
        "all_writes_blocked": dossier.all_writes_blocked
    }

def paper_safe_dossier_to_text(dossier: PaperSafeGateDossier, limit: int = 100) -> str:
    lines = [
        f"Paper Safe Dossier: {dossier.dossier_id}",
        f"Status: {dossier.status.value}",
        f"Sealed: {dossier.sealed} | Passed Gate: {dossier.paper_safe_gate_passed}",
        f"Activation Denied: {dossier.activation_denied} | Writes Blocked: {dossier.all_writes_blocked}",
        f"Evidence Items: {len(dossier.evidence_items)}"
    ]
    return "\n".join(lines)
