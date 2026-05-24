from typing import Any
from .simulator_gate_models import FinalLocalPaperAdmissionSimulatorGate, RehearsalReplayResult, DryAdmissionEvidenceFreezeBundle
from usa_signal_bot.core.enums import SimulatorGateRiskFlag

def collect_simulator_safety_flags(gate: FinalLocalPaperAdmissionSimulatorGate | None = None, replay_result: RehearsalReplayResult | None = None, freeze_bundle: DryAdmissionEvidenceFreezeBundle | None = None) -> list[SimulatorGateRiskFlag]:
    return []

def simulator_has_blocking_flags(flags: list[SimulatorGateRiskFlag]) -> bool:
    return len(flags) > 0

def validate_simulator_safety(gate: FinalLocalPaperAdmissionSimulatorGate | None = None, replay_result: RehearsalReplayResult | None = None, freeze_bundle: DryAdmissionEvidenceFreezeBundle | None = None) -> list[str]:
    return []

def simulator_safety_summary(flags: list[SimulatorGateRiskFlag]) -> dict[str, Any]:
    return {}

def simulator_safety_validator_to_text(payload: dict[str, Any]) -> str:
    return ""
