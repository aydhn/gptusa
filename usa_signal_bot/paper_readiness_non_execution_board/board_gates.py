from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import (
    NonExecutionBoardGate,
    NonExecutionBoardGateStatus,
    RuntimeMapReplayResult,
    NonExecutionSealIntegrityAudit,
    NonExecutionBoardRiskFlag,
    create_non_execution_board_gate_id,
    _now_utc_str
)
from usa_signal_bot.paper_readiness_non_execution_board.dossier_ingestion import paper_safe_dossier_supports_non_execution_board

def required_non_execution_board_gates() -> List[str]:
    return [
        "paper_safe_dossier_valid",
        "runtime_map_replay_passed",
        "non_execution_seal_integrity_valid",
        "activation_allowed_false",
        "admission_allowed_false",
        "order_created_false",
        "mutation_detected_false",
        "runtime_dangerous_routes_denied"
    ]

def build_non_execution_board_gates(dossier_payload: Dict[str, Any], replay_result: Optional[RuntimeMapReplayResult] = None, seal_audit: Optional[NonExecutionSealIntegrityAudit] = None) -> List[NonExecutionBoardGate]:
    return [
        gate_paper_safe_dossier_valid(dossier_payload),
        gate_runtime_map_replay_passed(replay_result),
        gate_non_execution_seal_integrity_valid(seal_audit),
        gate_activation_allowed_false(dossier_payload),
        gate_admission_allowed_false(dossier_payload),
        gate_order_created_false(dossier_payload),
        gate_mutation_detected_false(dossier_payload),
        gate_runtime_dangerous_routes_denied(replay_result)
    ]

def _make_gate(name: str, desc: str, expected: Any, observed: Any, passed: bool, flags: List[NonExecutionBoardRiskFlag] = None) -> NonExecutionBoardGate:
    return NonExecutionBoardGate(
        gate_id=create_non_execution_board_gate_id(),
        created_at_utc=_now_utc_str(),
        gate_name=name,
        status=NonExecutionBoardGateStatus.PASS if passed else NonExecutionBoardGateStatus.FAIL,
        expected_value=expected,
        observed_value=observed,
        required=True,
        description=desc,
        risk_flags=flags or [],
        warnings=[],
        errors=[],
        metadata={}
    )

def gate_paper_safe_dossier_valid(dossier_payload: Dict[str, Any]) -> NonExecutionBoardGate:
    valid, warnings = paper_safe_dossier_supports_non_execution_board(dossier_payload)
    flags = [NonExecutionBoardRiskFlag.DOSSIER_EVIDENCE_STALE] if not valid else []
    return _make_gate("paper_safe_dossier_valid", "Dossier must be valid for board", True, valid, valid, flags)

def gate_runtime_map_replay_passed(replay_result: Optional[RuntimeMapReplayResult]) -> NonExecutionBoardGate:
    passed = replay_result.passed if replay_result else False
    flags = [NonExecutionBoardRiskFlag.RUNTIME_MAP_REPLAY_FAILED] if not passed else []
    return _make_gate("runtime_map_replay_passed", "Runtime map replay must pass", True, passed, passed, flags)

def gate_non_execution_seal_integrity_valid(seal_audit: Optional[NonExecutionSealIntegrityAudit]) -> NonExecutionBoardGate:
    valid = seal_audit.integrity_valid if seal_audit else False
    flags = [NonExecutionBoardRiskFlag.NON_EXECUTION_SEAL_CONFIRMATION_FAILED] if not valid else []
    return _make_gate("non_execution_seal_integrity_valid", "Seal integrity must be valid", True, valid, valid, flags)

def gate_activation_allowed_false(dossier_payload: Dict[str, Any]) -> NonExecutionBoardGate:
    obs = dossier_payload.get("activation_allowed", False)
    flags = [NonExecutionBoardRiskFlag.ACTIVATION_ALLOWED_RISK] if obs else []
    return _make_gate("activation_allowed_false", "Activation allowed must be false", False, obs, not obs, flags)

def gate_admission_allowed_false(dossier_payload: Dict[str, Any]) -> NonExecutionBoardGate:
    obs = dossier_payload.get("admission_allowed", False)
    flags = [NonExecutionBoardRiskFlag.ADMISSION_ALLOWED_RISK] if obs else []
    return _make_gate("admission_allowed_false", "Admission allowed must be false", False, obs, not obs, flags)

def gate_order_created_false(dossier_payload: Dict[str, Any]) -> NonExecutionBoardGate:
    obs = dossier_payload.get("order_created", False)
    flags = [NonExecutionBoardRiskFlag.ORDER_CREATED_RISK] if obs else []
    return _make_gate("order_created_false", "Order created must be false", False, obs, not obs, flags)

def gate_mutation_detected_false(dossier_payload: Dict[str, Any]) -> NonExecutionBoardGate:
    obs = dossier_payload.get("mutation_detected", False)
    flags = [NonExecutionBoardRiskFlag.MUTATION_DETECTED_RISK] if obs else []
    return _make_gate("mutation_detected_false", "Mutation detected must be false", False, obs, not obs, flags)

def gate_runtime_dangerous_routes_denied(replay_result: Optional[RuntimeMapReplayResult]) -> NonExecutionBoardGate:
    obs = replay_result.dangerous_allowed_count if replay_result else 1
    flags = [NonExecutionBoardRiskFlag.DANGEROUS_RUNTIME_ROUTE_ALLOWED] if obs > 0 else []
    return _make_gate("runtime_dangerous_routes_denied", "Dangerous routes allowed must be 0", 0, obs, obs == 0, flags)

def non_execution_board_gates_summary(gates: List[NonExecutionBoardGate]) -> Dict[str, Any]:
    passed = sum(1 for g in gates if g.status == NonExecutionBoardGateStatus.PASS)
    failed = sum(1 for g in gates if g.status == NonExecutionBoardGateStatus.FAIL)
    return {"passed": passed, "failed": failed, "total": len(gates)}

def non_execution_board_gates_to_text(gates: List[NonExecutionBoardGate], limit: int = 100) -> str:
    summary = non_execution_board_gates_summary(gates)
    lines = ["--- BOARD GATES ---"]
    lines.append(f"Passed: {summary['passed']}/{summary['total']}")
    for g in gates[:limit]:
        lines.append(f"  {g.gate_name}: {g.status.value}")
    return "\n".join(lines)
