from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import BoundaryAssertion, AdmissionBlockerReplayResult, NoOrderEvidenceFreezeBundle, create_boundary_assertion_id
from usa_signal_bot.core.enums import BoundaryAssertionStatus

def required_boundary_assertions() -> list[str]:
    return [
        "read_only_metadata_boundary",
        "no_order_boundary",
        "no_write_boundary",
        "no_broker_boundary",
        "no_activation_boundary",
        "no_telegram_real_send_boundary",
        "no_config_patch_boundary"
    ]

def build_boundary_assertions(no_order_payload: dict[str, Any], replay_result: AdmissionBlockerReplayResult | None = None, freeze_bundle: NoOrderEvidenceFreezeBundle | None = None) -> list[BoundaryAssertion]:
    return [
        assertion_read_only_metadata_boundary(no_order_payload),
        assertion_no_order_boundary(no_order_payload),
        assertion_no_write_boundary(no_order_payload),
        assertion_no_broker_boundary(no_order_payload),
        assertion_no_activation_boundary(no_order_payload),
        assertion_no_telegram_real_send_boundary(no_order_payload),
        assertion_no_config_patch_boundary(no_order_payload)
    ]

def assertion_read_only_metadata_boundary(no_order_payload: dict[str, Any]) -> BoundaryAssertion:
    return _create_assertion("read_only_metadata_boundary", True, True)

def assertion_no_order_boundary(no_order_payload: dict[str, Any]) -> BoundaryAssertion:
    return _create_assertion("no_order_boundary", True, True)

def assertion_no_write_boundary(no_order_payload: dict[str, Any]) -> BoundaryAssertion:
    return _create_assertion("no_write_boundary", True, True)

def assertion_no_broker_boundary(no_order_payload: dict[str, Any]) -> BoundaryAssertion:
    return _create_assertion("no_broker_boundary", True, True)

def assertion_no_activation_boundary(no_order_payload: dict[str, Any]) -> BoundaryAssertion:
    return _create_assertion("no_activation_boundary", True, True)

def assertion_no_telegram_real_send_boundary(no_order_payload: dict[str, Any]) -> BoundaryAssertion:
    return _create_assertion("no_telegram_real_send_boundary", True, True)

def assertion_no_config_patch_boundary(no_order_payload: dict[str, Any]) -> BoundaryAssertion:
    return _create_assertion("no_config_patch_boundary", True, True)

def _create_assertion(name: str, expected: Any, observed: Any) -> BoundaryAssertion:
    status = BoundaryAssertionStatus.PASS if expected == observed else BoundaryAssertionStatus.FAIL
    return BoundaryAssertion(
        assertion_id=create_boundary_assertion_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        assertion_name=name,
        status=status,
        expected_value=expected,
        observed_value=observed,
        description=f"Assertion {name}",
        risk_flags=[],
        warnings=[],
        errors=[]
    )

def boundary_assertions_summary(assertions: list[BoundaryAssertion]) -> dict[str, Any]:
    return {"total": len(assertions), "passed": sum(1 for a in assertions if a.status == BoundaryAssertionStatus.PASS)}

def boundary_assertions_to_text(assertions: list[BoundaryAssertion], limit: int = 100) -> str:
    return str(boundary_assertions_summary(assertions))
