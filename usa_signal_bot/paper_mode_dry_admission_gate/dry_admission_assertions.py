from datetime import datetime, timezone
from typing import Any, List
from usa_signal_bot.core.enums import DryAdmissionGateAssertionStatus, DryAdmissionGateRiskFlag
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import (
    DryAdmissionGateAssertion,
    ShadowLaunchReplayResult,
    BoardEvidenceFreezeBundle,
    create_dry_admission_assertion_id
)

def required_dry_admission_assertions() -> List[str]:
    return [
        "metadata_only_dry_admission",
        "no_shadow_launch",
        "no_paper_mode_launch",
        "no_active_paper",
        "no_paper_admission",
        "no_order",
        "no_write",
        "no_broker",
        "no_config_patch",
        "no_telegram_real_send"
    ]

def build_dry_admission_assertions(
    board_payload: dict[str, Any],
    replay_result: ShadowLaunchReplayResult | None = None,
    freeze_bundle: BoardEvidenceFreezeBundle | None = None
) -> List[DryAdmissionGateAssertion]:
    return [
        assertion_metadata_only_dry_admission(board_payload),
        assertion_no_shadow_launch(board_payload),
        assertion_no_paper_mode_launch(board_payload),
        assertion_no_active_paper(board_payload),
        assertion_no_paper_admission(board_payload),
        assertion_no_order(board_payload),
        assertion_no_write(board_payload),
        assertion_no_broker(board_payload),
        assertion_no_config_patch(board_payload),
        assertion_no_telegram_real_send(board_payload)
    ]

def _create_assertion(name: str, passed: bool, risk_flag: DryAdmissionGateRiskFlag | None, desc: str) -> DryAdmissionGateAssertion:
    status = DryAdmissionGateAssertionStatus.PASS if passed else DryAdmissionGateAssertionStatus.FAIL
    flags = [risk_flag] if not passed and risk_flag else []
    errors = ["Assertion failed"] if not passed else []
    return DryAdmissionGateAssertion(
        assertion_id=create_dry_admission_assertion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        assertion_name=name,
        status=status,
        description=desc,
        risk_flags=flags,
        warnings=[],
        errors=errors
    )

def assertion_metadata_only_dry_admission(board_payload: dict[str, Any]) -> DryAdmissionGateAssertion:
    return _create_assertion("metadata_only_dry_admission", True, None, "Admission gate is metadata only")

def assertion_no_shadow_launch(board_payload: dict[str, Any]) -> DryAdmissionGateAssertion:
    passed = not board_payload.get("shadow_launch_allowed", False)
    return _create_assertion("no_shadow_launch", passed, DryAdmissionGateRiskFlag.SHADOW_LAUNCH_RISK, "Asserts no shadow launch")

def assertion_no_paper_mode_launch(board_payload: dict[str, Any]) -> DryAdmissionGateAssertion:
    passed = not board_payload.get("paper_mode_launch_allowed", False)
    return _create_assertion("no_paper_mode_launch", passed, DryAdmissionGateRiskFlag.PAPER_MODE_LAUNCH_RISK, "Asserts no paper mode launch")

def assertion_no_active_paper(board_payload: dict[str, Any]) -> DryAdmissionGateAssertion:
    passed = not board_payload.get("active_paper_enabled", False)
    return _create_assertion("no_active_paper", passed, DryAdmissionGateRiskFlag.ACTIVE_PAPER_ENABLE_RISK, "Asserts no active paper")

def assertion_no_paper_admission(board_payload: dict[str, Any]) -> DryAdmissionGateAssertion:
    passed = not board_payload.get("admission_allowed", False)
    return _create_assertion("no_paper_admission", passed, DryAdmissionGateRiskFlag.PAPER_ADMISSION_RISK, "Asserts no paper admission")

def assertion_no_order(board_payload: dict[str, Any]) -> DryAdmissionGateAssertion:
    passed = not board_payload.get("order_created", False)
    return _create_assertion("no_order", passed, DryAdmissionGateRiskFlag.ORDER_CREATED_RISK, "Asserts no order created")

def assertion_no_write(board_payload: dict[str, Any]) -> DryAdmissionGateAssertion:
    passed = not board_payload.get("mutation_detected", False)
    return _create_assertion("no_write", passed, DryAdmissionGateRiskFlag.PAPER_STATE_MUTATION_RISK, "Asserts no paper state mutation")

def assertion_no_broker(board_payload: dict[str, Any]) -> DryAdmissionGateAssertion:
    passed = not board_payload.get("broker_order_sent", False)
    return _create_assertion("no_broker", passed, DryAdmissionGateRiskFlag.BROKER_ORDER_RISK, "Asserts no broker routing")

def assertion_no_config_patch(board_payload: dict[str, Any]) -> DryAdmissionGateAssertion:
    passed = not board_payload.get("config_patched", False)
    return _create_assertion("no_config_patch", passed, DryAdmissionGateRiskFlag.PRODUCTION_CONFIG_WRITE_RISK, "Asserts no config patch")

def assertion_no_telegram_real_send(board_payload: dict[str, Any]) -> DryAdmissionGateAssertion:
    passed = not board_payload.get("telegram_real_sent", False)
    return _create_assertion("no_telegram_real_send", passed, DryAdmissionGateRiskFlag.TELEGRAM_REAL_SEND_RISK, "Asserts no telegram real send")

def dry_admission_assertions_summary(assertions: List[DryAdmissionGateAssertion]) -> dict[str, Any]:
    passed = sum(1 for a in assertions if a.status == DryAdmissionGateAssertionStatus.PASS)
    failed = sum(1 for a in assertions if a.status == DryAdmissionGateAssertionStatus.FAIL)
    return {
        "total": len(assertions),
        "passed": passed,
        "failed": failed,
        "all_passed": failed == 0
    }

def dry_admission_assertions_to_text(assertions: List[DryAdmissionGateAssertion], limit: int = 100) -> str:
    summary = dry_admission_assertions_summary(assertions)
    return f"Dry Admission Assertions - Total: {summary['total']}, Passed: {summary['passed']}, Failed: {summary['failed']}"
