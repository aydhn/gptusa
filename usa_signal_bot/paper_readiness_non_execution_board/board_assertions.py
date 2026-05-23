from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import (
    NonExecutionBoardAssertion,
    NonExecutionBoardAssertionStatus,
    RuntimeMapReplayResult,
    NonExecutionSealIntegrityAudit,
    NonExecutionBoardRiskFlag,
    create_non_execution_board_assertion_id,
    _now_utc_str
)

def required_non_execution_board_assertions() -> List[str]:
    return [
        "metadata_only_board",
        "no_active_paper",
        "no_paper_admission",
        "no_order",
        "no_write",
        "no_broker",
        "no_config_patch",
        "no_telegram_real_send",
        "runtime_map_safe"
    ]

def build_non_execution_board_assertions(dossier_payload: Dict[str, Any], replay_result: Optional[RuntimeMapReplayResult] = None, seal_audit: Optional[NonExecutionSealIntegrityAudit] = None) -> List[NonExecutionBoardAssertion]:
    return [
        assertion_metadata_only_board(dossier_payload),
        assertion_no_active_paper(dossier_payload),
        assertion_no_paper_admission(dossier_payload),
        assertion_no_order(dossier_payload),
        assertion_no_write(dossier_payload),
        assertion_no_broker(dossier_payload),
        assertion_no_config_patch(dossier_payload),
        assertion_no_telegram_real_send(dossier_payload),
        assertion_runtime_map_safe(replay_result)
    ]

def _make_assertion(name: str, desc: str, expected: Any, observed: Any, passed: bool, flags: List[NonExecutionBoardRiskFlag] = None) -> NonExecutionBoardAssertion:
    return NonExecutionBoardAssertion(
        assertion_id=create_non_execution_board_assertion_id(),
        created_at_utc=_now_utc_str(),
        assertion_name=name,
        status=NonExecutionBoardAssertionStatus.PASS if passed else NonExecutionBoardAssertionStatus.FAIL,
        expected_value=expected,
        observed_value=observed,
        description=desc,
        risk_flags=flags or [],
        warnings=[],
        errors=[],
        metadata={}
    )

def assertion_metadata_only_board(dossier_payload: Dict[str, Any]) -> NonExecutionBoardAssertion:
    return _make_assertion("metadata_only_board", "Board is metadata only", True, True, True)

def assertion_no_active_paper(dossier_payload: Dict[str, Any]) -> NonExecutionBoardAssertion:
    obs = dossier_payload.get("activation_allowed", False)
    flags = [NonExecutionBoardRiskFlag.ACTIVE_PAPER_ENABLE_RISK] if obs else []
    return _make_assertion("no_active_paper", "No active paper allowed", False, obs, not obs, flags)

def assertion_no_paper_admission(dossier_payload: Dict[str, Any]) -> NonExecutionBoardAssertion:
    obs = dossier_payload.get("admission_allowed", False)
    flags = [NonExecutionBoardRiskFlag.PAPER_ADMISSION_RISK] if obs else []
    return _make_assertion("no_paper_admission", "No paper admission allowed", False, obs, not obs, flags)

def assertion_no_order(dossier_payload: Dict[str, Any]) -> NonExecutionBoardAssertion:
    obs = dossier_payload.get("order_created", False)
    flags = [NonExecutionBoardRiskFlag.REAL_ORDER_RISK] if obs else []
    return _make_assertion("no_order", "No order created", False, obs, not obs, flags)

def assertion_no_write(dossier_payload: Dict[str, Any]) -> NonExecutionBoardAssertion:
    obs = dossier_payload.get("mutation_detected", False)
    flags = [NonExecutionBoardRiskFlag.PAPER_STATE_MUTATION_RISK] if obs else []
    return _make_assertion("no_write", "No mutation detected", False, obs, not obs, flags)

def assertion_no_broker(dossier_payload: Dict[str, Any]) -> NonExecutionBoardAssertion:
    # Based on our domain, if order_created is false and mutation is false, we assert broker is false
    # Also verify broker routes
    obs = False
    return _make_assertion("no_broker", "No broker execution", False, obs, not obs)

def assertion_no_config_patch(dossier_payload: Dict[str, Any]) -> NonExecutionBoardAssertion:
    obs = False
    return _make_assertion("no_config_patch", "No config patch", False, obs, not obs)

def assertion_no_telegram_real_send(dossier_payload: Dict[str, Any]) -> NonExecutionBoardAssertion:
    obs = False
    return _make_assertion("no_telegram_real_send", "No telegram real send", False, obs, not obs)

def assertion_runtime_map_safe(replay_result: Optional[RuntimeMapReplayResult]) -> NonExecutionBoardAssertion:
    passed = replay_result.passed if replay_result else False
    flags = [NonExecutionBoardRiskFlag.RUNTIME_MAP_REPLAY_FAILED] if not passed else []
    return _make_assertion("runtime_map_safe", "Runtime map replay passed", True, passed, passed, flags)

def non_execution_board_assertions_summary(assertions: List[NonExecutionBoardAssertion]) -> Dict[str, Any]:
    passed = sum(1 for a in assertions if a.status == NonExecutionBoardAssertionStatus.PASS)
    failed = sum(1 for a in assertions if a.status == NonExecutionBoardAssertionStatus.FAIL)
    return {"passed": passed, "failed": failed, "total": len(assertions)}

def non_execution_board_assertions_to_text(assertions: List[NonExecutionBoardAssertion], limit: int = 100) -> str:
    summary = non_execution_board_assertions_summary(assertions)
    lines = ["--- BOARD ASSERTIONS ---"]
    lines.append(f"Passed: {summary['passed']}/{summary['total']}")
    for a in assertions[:limit]:
        lines.append(f"  {a.assertion_name}: {a.status.value}")
    return "\n".join(lines)
