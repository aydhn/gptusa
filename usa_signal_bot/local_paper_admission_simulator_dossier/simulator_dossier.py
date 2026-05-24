from datetime import datetime, timezone
from typing import Any
import hashlib
import json

from usa_signal_bot.core.enums import LocalPaperAdmissionSimulatorDossierStatus, LocalPaperAdmissionSimulatorDossierDecision, SimulatorDossierRiskFlag
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import (
    LocalPaperAdmissionSimulatorGateDossier,
    SimulatorDossierEvidenceItem,
    create_simulator_dossier_id
)

def build_default_simulator_dossier(candidate_id: str | None = None) -> LocalPaperAdmissionSimulatorGateDossier:
    return LocalPaperAdmissionSimulatorGateDossier(
        dossier_id=create_simulator_dossier_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=LocalPaperAdmissionSimulatorDossierStatus.DRAFT,
        decision=LocalPaperAdmissionSimulatorDossierDecision.UNKNOWN,
        evidence_items=[],
        sandbox_runtime_admission_blocker_events=[],
        evidence_refs=[],
        sealed=False,
        immutable=False,
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        admission_allowed=False,
        transition_allowed=False,
        simulator_admission_allowed=False,
        local_paper_simulator_allowed=False,
        sandbox_runtime_admission_allowed=False,
        paper_sandbox_runtime_allowed=False,
        rehearsal_allowed=False,
        paper_mode_rehearsal_allowed=False,
        shadow_launch_allowed=False,
        paper_mode_launch_allowed=False,
        simulator_gate_passed=True,
        dry_admission_dossier_valid=True,
        acceptance_seal_valid=True,
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
        errors=[],
        candidate_id=candidate_id
    )

def stable_simulator_dossier_hash(payload: dict[str, Any]) -> str:
    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def collect_simulator_dossier_safety_flags(payload: dict[str, Any], evidence_items: list[SimulatorDossierEvidenceItem]) -> list[SimulatorDossierRiskFlag]:
    flags = []
    if payload.get("order_created"): flags.append(SimulatorDossierRiskFlag.ORDER_CREATED_RISK)
    if payload.get("mutation_detected"): flags.append(SimulatorDossierRiskFlag.MUTATION_DETECTED_RISK)
    if payload.get("activation_allowed"): flags.append(SimulatorDossierRiskFlag.ACTIVATION_ALLOWED_RISK)
    if payload.get("sandbox_runtime_admission_allowed"): flags.append(SimulatorDossierRiskFlag.SANDBOX_RUNTIME_ADMISSION_RISK)
    return flags

def build_local_paper_admission_simulator_gate_dossier(payload: dict[str, Any]) -> LocalPaperAdmissionSimulatorGateDossier:
    dossier = build_default_simulator_dossier(payload.get("candidate_id"))
    dossier.status = LocalPaperAdmissionSimulatorDossierStatus.VALIDATED_SIMULATOR_SAFE
    dossier.decision = LocalPaperAdmissionSimulatorDossierDecision.CREATE_SIMULATOR_DOSSIER
    dossier.dossier_hash = stable_simulator_dossier_hash(payload)
    dossier.sealed = True
    dossier.immutable = True
    dossier.safety_flags = collect_simulator_dossier_safety_flags(payload, [])

    if dossier.safety_flags:
        dossier.status = LocalPaperAdmissionSimulatorDossierStatus.BLOCKED
        dossier.decision = LocalPaperAdmissionSimulatorDossierDecision.BLOCK

    return dossier

def simulator_dossier_summary(dossier: LocalPaperAdmissionSimulatorGateDossier) -> dict[str, Any]:
    return {
        "dossier_id": dossier.dossier_id,
        "status": dossier.status.value,
        "decision": dossier.decision.value,
        "sealed": dossier.sealed,
        "hash": dossier.dossier_hash
    }

def simulator_dossier_to_text(dossier: LocalPaperAdmissionSimulatorGateDossier, limit: int = 100) -> str:
    summary = simulator_dossier_summary(dossier)
    return f"--- Simulator Dossier ---\nStatus: {summary['status']}\nDecision: {summary['decision']}\nSealed: {summary['sealed']}"
