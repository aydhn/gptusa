from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import json
import hashlib
from usa_signal_bot.core.enums import NonExecutionAcceptanceSealStatus, NonExecutionAcceptanceSealDecision, PaperSafeDossierRiskFlag
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import NonExecutionAcceptanceSeal, create_non_execution_seal_id, PaperSafeDossierEvidenceItem
from usa_signal_bot.paper_safe_dossier.paper_safe_ingestion import extract_final_paper_safe_gate, extract_paper_safe_candidate_id

def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def accepted_non_execution_boundaries() -> List[str]:
    return [
        "no_broker_execution",
        "no_active_paper_enable",
        "no_paper_admission",
        "no_order_creation",
        "no_paper_state_write",
        "no_config_patch",
        "no_telegram_real_send",
        "no_external_telemetry",
        "metadata_only_acceptance",
        "not_investment_advice"
    ]

def build_non_execution_acceptance_seal(paper_safe_payload: Dict[str, Any], evidence_items: Optional[List[PaperSafeDossierEvidenceItem]] = None) -> NonExecutionAcceptanceSeal:
    candidate_id = extract_paper_safe_candidate_id(paper_safe_payload)
    gate = extract_final_paper_safe_gate(paper_safe_payload)
    gate_id = gate.get("gate_id") if gate else None

    seal = NonExecutionAcceptanceSeal(
        seal_id=create_non_execution_seal_id(),
        created_at_utc=utcnow_iso(),
        status=NonExecutionAcceptanceSealStatus.SEALED,
        decision=NonExecutionAcceptanceSealDecision.SEAL_NON_EXECUTION_ACCEPTANCE,
        candidate_id=candidate_id,
        source_paper_safe_gate_id=gate_id,
        source_paper_safe_review_id=paper_safe_payload.get("review_id"),
        seal_hash=None,
        accepted_boundaries=accepted_non_execution_boundaries(),
        sealed=True,
        immutable=True,
        non_execution_confirmed=True,
        no_broker_confirmed=True,
        no_active_paper_confirmed=True,
        no_paper_admission_confirmed=True,
        no_order_confirmed=True,
        no_write_confirmed=True,
        no_telegram_real_send_confirmed=True,
        no_config_patch_confirmed=True,
        seal_is_metadata_only=True,
        risk_flags=collect_non_execution_seal_risk_flags(paper_safe_payload),
        required_followups=[],
        warnings=[],
        errors=[]
    )
    seal.seal_hash = stable_non_execution_seal_hash(paper_safe_payload)
    return seal

def build_default_non_execution_acceptance_seal(candidate_id: Optional[str] = None) -> NonExecutionAcceptanceSeal:
    return NonExecutionAcceptanceSeal(
        seal_id=create_non_execution_seal_id(),
        created_at_utc=utcnow_iso(),
        status=NonExecutionAcceptanceSealStatus.SEALED,
        decision=NonExecutionAcceptanceSealDecision.SEAL_NON_EXECUTION_ACCEPTANCE,
        candidate_id=candidate_id,
        source_paper_safe_gate_id=None,
        source_paper_safe_review_id=None,
        seal_hash=None,
        accepted_boundaries=accepted_non_execution_boundaries(),
        sealed=True,
        immutable=True,
        non_execution_confirmed=True,
        no_broker_confirmed=True,
        no_active_paper_confirmed=True,
        no_paper_admission_confirmed=True,
        no_order_confirmed=True,
        no_write_confirmed=True,
        no_telegram_real_send_confirmed=True,
        no_config_patch_confirmed=True,
        seal_is_metadata_only=True,
        risk_flags=[],
        required_followups=[],
        warnings=[],
        errors=[]
    )

def stable_non_execution_seal_hash(payload: Dict[str, Any]) -> str:
    s = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def collect_non_execution_seal_risk_flags(paper_safe_payload: Dict[str, Any]) -> List[PaperSafeDossierRiskFlag]:
    flags = []
    gate = extract_final_paper_safe_gate(paper_safe_payload)
    if gate:
        if gate.get("activation_allowed", False):
            flags.append(PaperSafeDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
        if gate.get("admission_allowed", False):
            flags.append(PaperSafeDossierRiskFlag.ADMISSION_ALLOWED_RISK)
    return flags

def non_execution_acceptance_seal_summary(seal: NonExecutionAcceptanceSeal) -> Dict[str, Any]:
    return {
        "seal_id": seal.seal_id,
        "status": seal.status.value,
        "sealed": seal.sealed,
        "immutable": seal.immutable,
        "non_execution_confirmed": seal.non_execution_confirmed
    }

def non_execution_acceptance_seal_to_text(seal: NonExecutionAcceptanceSeal) -> str:
    lines = [
        f"Non-Execution Acceptance Seal: {seal.seal_id}",
        f"Status: {seal.status.value}",
        f"Sealed: {seal.sealed} | Immutable: {seal.immutable}",
        f"Non-Execution Confirmed: {seal.non_execution_confirmed}",
        f"Boundaries: {', '.join(seal.accepted_boundaries)}"
    ]
    return "\n".join(lines)
