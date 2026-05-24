from datetime import datetime, timezone
from typing import Any
from usa_signal_bot.core.enums import SimulatorAcceptanceSealStatus, SimulatorAcceptanceSealDecision, SimulatorDossierRiskFlag
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import (
    SimulatorAcceptanceSeal,
    SimulatorDossierEvidenceItem,
    create_simulator_acceptance_seal_id
)
import hashlib
import json

def accepted_simulator_boundaries() -> list[str]:
    return [
        "simulator_gate_passed",
        "rehearsal_replay_passed",
        "dry_admission_evidence_freeze_valid",
        "no_simulator_admission_permission",
        "no_local_paper_simulator_permission",
        "no_sandbox_runtime_admission_permission",
        "no_paper_sandbox_runtime_permission",
        "no_paper_admission_permission",
        "no_order_creation",
        "no_paper_state_write",
        "no_broker_execution",
        "no_config_patch",
        "no_telegram_real_send",
        "not_investment_advice"
    ]

def stable_simulator_acceptance_seal_hash(payload: dict[str, Any]) -> str:
    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def collect_simulator_acceptance_seal_risk_flags(payload: dict[str, Any]) -> list[SimulatorDossierRiskFlag]:
    flags = []
    if payload.get("allows_active_paper"): flags.append(SimulatorDossierRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
    if payload.get("allows_broker_execution"): flags.append(SimulatorDossierRiskFlag.BROKER_ORDER_RISK)
    if payload.get("allows_paper_state_mutation"): flags.append(SimulatorDossierRiskFlag.PAPER_STATE_MUTATION_RISK)
    if payload.get("allows_config_patch"): flags.append(SimulatorDossierRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
    if payload.get("allows_telegram_real_send"): flags.append(SimulatorDossierRiskFlag.TELEGRAM_REAL_SEND_RISK)
    return flags

def build_default_simulator_acceptance_seal(candidate_id: str | None = None) -> SimulatorAcceptanceSeal:
    return SimulatorAcceptanceSeal(
        seal_id=create_simulator_acceptance_seal_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=SimulatorAcceptanceSealStatus.DRAFT,
        decision=SimulatorAcceptanceSealDecision.UNKNOWN,
        accepted_boundaries=accepted_simulator_boundaries(),
        simulator_gate_passed=True,
        rehearsal_replay_passed=True,
        dry_admission_evidence_freeze_valid=True,
        simulator_rules_passed=True,
        simulator_assertions_passed=True,
        no_simulator_admission_confirmed=True,
        no_local_paper_simulator_confirmed=True,
        no_sandbox_runtime_admission_confirmed=True,
        no_paper_sandbox_runtime_confirmed=True,
        no_rehearsal_confirmed=True,
        no_admission_confirmed=True,
        no_order_confirmed=True,
        no_write_confirmed=True,
        no_broker_confirmed=True,
        no_config_patch_confirmed=True,
        no_telegram_real_send_confirmed=True,
        sealed=False,
        immutable=False,
        seal_is_metadata_only=True,
        allows_simulator_admission=False,
        allows_local_paper_simulator=False,
        allows_sandbox_runtime_admission=False,
        allows_paper_sandbox_runtime=False,
        allows_rehearsal=False,
        allows_paper_mode_rehearsal=False,
        allows_shadow_launch=False,
        allows_paper_mode_launch=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        risk_flags=[],
        required_followups=[],
        warnings=[],
        errors=[],
        candidate_id=candidate_id
    )

def build_simulator_acceptance_seal(payload: dict[str, Any], evidence_items: list[SimulatorDossierEvidenceItem] | None = None) -> SimulatorAcceptanceSeal:
    seal = build_default_simulator_acceptance_seal(payload.get("candidate_id"))
    seal.seal_hash = stable_simulator_acceptance_seal_hash(payload)
    seal.sealed = True
    seal.immutable = True
    seal.status = SimulatorAcceptanceSealStatus.SEALED
    seal.decision = SimulatorAcceptanceSealDecision.SEAL_SIMULATOR_ACCEPTANCE

    seal.risk_flags = collect_simulator_acceptance_seal_risk_flags(payload)
    if seal.risk_flags:
        seal.status = SimulatorAcceptanceSealStatus.BLOCKED
        seal.decision = SimulatorAcceptanceSealDecision.BLOCK

    return seal

def simulator_acceptance_seal_summary(seal: SimulatorAcceptanceSeal) -> dict[str, Any]:
    return {
        "seal_id": seal.seal_id,
        "status": seal.status.value,
        "decision": seal.decision.value,
        "sealed": seal.sealed,
        "immutable": seal.immutable,
        "hash": seal.seal_hash
    }

def simulator_acceptance_seal_to_text(seal: SimulatorAcceptanceSeal) -> str:
    summary = simulator_acceptance_seal_summary(seal)
    return f"--- Simulator Acceptance Seal ---\nStatus: {summary['status']}\nDecision: {summary['decision']}\nSealed: {summary['sealed']}"
