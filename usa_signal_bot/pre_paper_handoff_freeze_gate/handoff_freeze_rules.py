from typing import Any, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import HandoffFreezeRuleStatus
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import (
    HandoffFreezeRule,
    SandboxRuntimeAdmissionReplayResult,
    SimulatorEvidenceFreezeBundle,
    create_handoff_freeze_rule_id
)

def required_handoff_freeze_rule_names() -> List[str]:
    return [
        "sandbox_runtime_admission_allowed_false",
        "paper_sandbox_runtime_allowed_false",
        "simulator_admission_allowed_false",
        "local_paper_simulator_allowed_false",
        "activation_allowed_false",
        "admission_allowed_false",
        "transition_allowed_false",
        "order_created_false",
        "mutation_detected_false",
        "simulator_acceptance_seal_valid",
        "sandbox_runtime_admission_replay_passed",
        "simulator_evidence_freeze_valid"
    ]

def build_handoff_freeze_rules(payload: dict[str, Any], replay_result: Optional[SandboxRuntimeAdmissionReplayResult] = None, freeze_bundle: Optional[SimulatorEvidenceFreezeBundle] = None) -> List[HandoffFreezeRule]:
    return [
        rule_sandbox_runtime_admission_allowed_false(payload),
        rule_paper_sandbox_runtime_allowed_false(payload),
        rule_simulator_admission_allowed_false(payload),
        rule_local_paper_simulator_allowed_false(payload),
        rule_activation_allowed_false(payload),
        rule_admission_allowed_false(payload),
        rule_transition_allowed_false(payload),
        rule_order_created_false(payload),
        rule_mutation_detected_false(payload),
        rule_simulator_acceptance_seal_valid(payload),
        rule_sandbox_runtime_admission_replay_passed(replay_result),
        rule_simulator_evidence_freeze_valid(freeze_bundle)
    ]

def _create_rule(name: str, passed: bool, expected: Any, observed: Any, desc: str) -> HandoffFreezeRule:
    return HandoffFreezeRule(
        rule_id=create_handoff_freeze_rule_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        rule_name=name,
        status=HandoffFreezeRuleStatus.PASS if passed else HandoffFreezeRuleStatus.FAIL,
        expected_value=expected,
        observed_value=observed,
        required=True,
        description=desc,
        risk_flags=[],
        warnings=[],
        errors=[] if passed else [f"Rule {name} failed"]
    )

def rule_sandbox_runtime_admission_allowed_false(payload: dict[str, Any]) -> HandoffFreezeRule:
    obs = payload.get("sandbox_runtime_admission_allowed", False)
    return _create_rule("sandbox_runtime_admission_allowed_false", not obs, False, obs, "Must not allow sandbox runtime admission")

def rule_paper_sandbox_runtime_allowed_false(payload: dict[str, Any]) -> HandoffFreezeRule:
    obs = payload.get("paper_sandbox_runtime_allowed", False)
    return _create_rule("paper_sandbox_runtime_allowed_false", not obs, False, obs, "Must not allow paper sandbox runtime")

def rule_simulator_admission_allowed_false(payload: dict[str, Any]) -> HandoffFreezeRule:
    obs = payload.get("simulator_admission_allowed", False)
    return _create_rule("simulator_admission_allowed_false", not obs, False, obs, "Must not allow simulator admission")

def rule_local_paper_simulator_allowed_false(payload: dict[str, Any]) -> HandoffFreezeRule:
    obs = payload.get("local_paper_simulator_allowed", False)
    return _create_rule("local_paper_simulator_allowed_false", not obs, False, obs, "Must not allow local paper simulator")

def rule_activation_allowed_false(payload: dict[str, Any]) -> HandoffFreezeRule:
    obs = payload.get("activation_allowed", False)
    return _create_rule("activation_allowed_false", not obs, False, obs, "Must not allow activation")

def rule_admission_allowed_false(payload: dict[str, Any]) -> HandoffFreezeRule:
    obs = payload.get("admission_allowed", False)
    return _create_rule("admission_allowed_false", not obs, False, obs, "Must not allow admission")

def rule_transition_allowed_false(payload: dict[str, Any]) -> HandoffFreezeRule:
    obs = payload.get("transition_allowed", False)
    return _create_rule("transition_allowed_false", not obs, False, obs, "Must not allow transition")

def rule_order_created_false(payload: dict[str, Any]) -> HandoffFreezeRule:
    obs = payload.get("order_created", False)
    return _create_rule("order_created_false", not obs, False, obs, "Must not create order")

def rule_mutation_detected_false(payload: dict[str, Any]) -> HandoffFreezeRule:
    obs = payload.get("mutation_detected", False)
    return _create_rule("mutation_detected_false", not obs, False, obs, "Must not mutate state")

def rule_simulator_acceptance_seal_valid(payload: dict[str, Any]) -> HandoffFreezeRule:
    seal = payload.get("simulator_acceptance_seal")
    obs = seal is not None and seal.get("status") in ["VALIDATED", "SEALED"]
    return _create_rule("simulator_acceptance_seal_valid", obs, True, obs, "Acceptance seal must be valid")

def rule_sandbox_runtime_admission_replay_passed(replay_result: Optional[SandboxRuntimeAdmissionReplayResult]) -> HandoffFreezeRule:
    obs = replay_result.passed if replay_result else False
    return _create_rule("sandbox_runtime_admission_replay_passed", obs, True, obs, "Sandbox replay must pass")

def rule_simulator_evidence_freeze_valid(freeze_bundle: Optional[SimulatorEvidenceFreezeBundle]) -> HandoffFreezeRule:
    obs = freeze_bundle is not None and freeze_bundle.missing_evidence_count == 0
    return _create_rule("simulator_evidence_freeze_valid", obs, True, obs, "Evidence freeze must be valid")

def handoff_freeze_rules_summary(rules: List[HandoffFreezeRule]) -> dict[str, Any]:
    passed = sum(1 for r in rules if r.status == HandoffFreezeRuleStatus.PASS)
    return {
        "total": len(rules),
        "passed": passed,
        "failed": len(rules) - passed
    }

def handoff_freeze_rules_to_text(rules: List[HandoffFreezeRule], limit: int = 100) -> str:
    res = "Handoff Freeze Rules:\n"
    for r in rules[:limit]:
        res += f"- {r.rule_name}: {r.status.value}\n"
    return res
