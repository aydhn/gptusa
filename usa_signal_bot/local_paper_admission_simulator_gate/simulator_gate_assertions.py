from typing import Any
from .simulator_gate_models import SimulatorGateAssertion, RehearsalReplayResult, DryAdmissionEvidenceFreezeBundle

def required_simulator_gate_assertions() -> list[str]:
    return []

def build_simulator_gate_assertions(payload: dict[str, Any], replay_result: RehearsalReplayResult | None = None, freeze_bundle: DryAdmissionEvidenceFreezeBundle | None = None) -> list[SimulatorGateAssertion]:
    return []

def assertion_metadata_only_simulator_gate(payload: dict[str, Any]) -> SimulatorGateAssertion:
    pass

def assertion_no_rehearsal(payload: dict[str, Any]) -> SimulatorGateAssertion:
    pass

def assertion_no_paper_mode_rehearsal(payload: dict[str, Any]) -> SimulatorGateAssertion:
    pass

def assertion_no_shadow_launch(payload: dict[str, Any]) -> SimulatorGateAssertion:
    pass

def assertion_no_paper_mode_launch(payload: dict[str, Any]) -> SimulatorGateAssertion:
    pass

def assertion_no_active_paper(payload: dict[str, Any]) -> SimulatorGateAssertion:
    pass

def assertion_no_paper_admission(payload: dict[str, Any]) -> SimulatorGateAssertion:
    pass

def assertion_no_simulator_admission(payload: dict[str, Any]) -> SimulatorGateAssertion:
    pass

def assertion_no_order(payload: dict[str, Any]) -> SimulatorGateAssertion:
    pass

def assertion_no_write(payload: dict[str, Any]) -> SimulatorGateAssertion:
    pass

def assertion_no_broker(payload: dict[str, Any]) -> SimulatorGateAssertion:
    pass

def assertion_no_config_patch(payload: dict[str, Any]) -> SimulatorGateAssertion:
    pass

def assertion_no_telegram_real_send(payload: dict[str, Any]) -> SimulatorGateAssertion:
    pass

def simulator_gate_assertions_summary(assertions: list[SimulatorGateAssertion]) -> dict[str, Any]:
    return {}

def simulator_gate_assertions_to_text(assertions: list[SimulatorGateAssertion], limit: int = 100) -> str:
    return ""
