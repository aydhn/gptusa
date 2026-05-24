from typing import Any
from .simulator_gate_models import SimulatorGateRule, RehearsalReplayResult, DryAdmissionEvidenceFreezeBundle

def required_simulator_gate_rule_names() -> list[str]:
    return []

def build_simulator_gate_rules(payload: dict[str, Any], replay_result: RehearsalReplayResult | None = None, freeze_bundle: DryAdmissionEvidenceFreezeBundle | None = None) -> list[SimulatorGateRule]:
    return []

def rule_rehearsal_allowed_false(payload: dict[str, Any]) -> SimulatorGateRule:
    pass

def rule_paper_mode_rehearsal_allowed_false(payload: dict[str, Any]) -> SimulatorGateRule:
    pass

def rule_shadow_launch_allowed_false(payload: dict[str, Any]) -> SimulatorGateRule:
    pass

def rule_paper_mode_launch_allowed_false(payload: dict[str, Any]) -> SimulatorGateRule:
    pass

def rule_activation_allowed_false(payload: dict[str, Any]) -> SimulatorGateRule:
    pass

def rule_admission_allowed_false(payload: dict[str, Any]) -> SimulatorGateRule:
    pass

def rule_simulator_admission_allowed_false(payload: dict[str, Any]) -> SimulatorGateRule:
    pass

def rule_order_created_false(payload: dict[str, Any]) -> SimulatorGateRule:
    pass

def rule_mutation_detected_false(payload: dict[str, Any]) -> SimulatorGateRule:
    pass

def rule_dry_admission_acceptance_seal_valid(payload: dict[str, Any]) -> SimulatorGateRule:
    pass

def rule_rehearsal_replay_passed(replay_result: RehearsalReplayResult | None) -> SimulatorGateRule:
    pass

def rule_dry_admission_evidence_freeze_valid(freeze_bundle: DryAdmissionEvidenceFreezeBundle | None) -> SimulatorGateRule:
    pass

def simulator_gate_rules_summary(rules: list[SimulatorGateRule]) -> dict[str, Any]:
    return {}

def simulator_gate_rules_to_text(rules: list[SimulatorGateRule], limit: int = 100) -> str:
    return ""
