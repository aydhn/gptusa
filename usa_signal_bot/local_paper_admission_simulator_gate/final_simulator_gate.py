from typing import Any
from .simulator_gate_models import FinalLocalPaperAdmissionSimulatorGate, SimulatorGateRule, SimulatorGateAssertion, create_final_simulator_gate_id
from usa_signal_bot.core.enums import LocalPaperAdmissionSimulatorGateStatus, LocalPaperAdmissionSimulatorGateDecision, SimulatorGateRiskFlag
from datetime import datetime, timezone

def build_final_local_paper_admission_simulator_gate(payload: dict[str, Any]) -> FinalLocalPaperAdmissionSimulatorGate:
    return build_default_final_simulator_gate()

def build_default_final_simulator_gate(candidate_id: str | None = None) -> FinalLocalPaperAdmissionSimulatorGate:
    return FinalLocalPaperAdmissionSimulatorGate(
        gate_id=create_final_simulator_gate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=LocalPaperAdmissionSimulatorGateStatus.VALIDATED_SIMULATOR_SAFE,
        decision=LocalPaperAdmissionSimulatorGateDecision.PASS_TO_SIMULATOR_GATE_DOSSIER,
        candidate_id=candidate_id,
        source_dry_admission_dossier_review_id=None,
        source_dry_admission_dossier_id=None,
        source_acceptance_seal_id=None,
        source_rehearsal_replay_result_id=None,
        source_evidence_freeze_id=None,
        sealed=True,
        immutable=True,
        manual_review_required=True,
        activation_denied=True,
        simulator_gate_passed=True,
        dry_admission_dossier_valid=True,
        dry_admission_acceptance_seal_valid=True,
        all_writes_blocked=True
    )

def stable_simulator_gate_hash(payload: dict[str, Any]) -> str:
    return ""

def collect_simulator_gate_safety_flags(payload: dict[str, Any], rules: list[SimulatorGateRule], assertions: list[SimulatorGateAssertion]) -> list[SimulatorGateRiskFlag]:
    return []

def final_simulator_gate_summary(gate: FinalLocalPaperAdmissionSimulatorGate) -> dict[str, Any]:
    return {}

def final_simulator_gate_to_text(gate: FinalLocalPaperAdmissionSimulatorGate, limit: int = 100) -> str:
    return ""
