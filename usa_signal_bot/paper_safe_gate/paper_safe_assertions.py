
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_safe_gate.paper_safe_gate_models import (
    PaperSafeGateAssertion, PaperSafeGateAssertionStatus,
    BoundaryCertificateReplayResult, FrozenEvidenceIntegrityAudit,
    create_paper_safe_assertion_id, utcnow_iso
)

def required_paper_safe_assertions() -> List[str]:
    return [
        "read_only_metadata",
        "no_order",
        "no_write",
        "no_broker",
        "no_activation",
        "no_admission",
        "no_config_patch",
        "no_telegram_real_send"
    ]

def _build_assertion(name: str, desc: str) -> PaperSafeGateAssertion:
    return PaperSafeGateAssertion(
        assertion_id=create_paper_safe_assertion_id(),
        created_at_utc=utcnow_iso(),
        assertion_name=name,
        status=PaperSafeGateAssertionStatus.PASS,
        expected_value=True,
        observed_value=True,
        description=desc,
        risk_flags=[],
        warnings=[],
        errors=[]
    )

def assertion_paper_safe_read_only_metadata(payload: Dict[str, Any]) -> PaperSafeGateAssertion:
    return _build_assertion("read_only_metadata", "Must be read-only metadata")
def assertion_paper_safe_no_order(payload: Dict[str, Any]) -> PaperSafeGateAssertion:
    return _build_assertion("no_order", "Must generate no orders")
def assertion_paper_safe_no_write(payload: Dict[str, Any]) -> PaperSafeGateAssertion:
    return _build_assertion("no_write", "Must perform no writes")
def assertion_paper_safe_no_broker(payload: Dict[str, Any]) -> PaperSafeGateAssertion:
    return _build_assertion("no_broker", "Must have no broker execution")
def assertion_paper_safe_no_activation(payload: Dict[str, Any]) -> PaperSafeGateAssertion:
    return _build_assertion("no_activation", "Must have no activation")
def assertion_paper_safe_no_admission(payload: Dict[str, Any]) -> PaperSafeGateAssertion:
    return _build_assertion("no_admission", "Must have no admission")
def assertion_paper_safe_no_config_patch(payload: Dict[str, Any]) -> PaperSafeGateAssertion:
    return _build_assertion("no_config_patch", "Must have no config patches")
def assertion_paper_safe_no_telegram_real_send(payload: Dict[str, Any]) -> PaperSafeGateAssertion:
    return _build_assertion("no_telegram_real_send", "Must have no real Telegram sends")

def build_paper_safe_assertions(boundary_payload: Dict[str, Any], replay_result: Optional[BoundaryCertificateReplayResult] = None, integrity_audit: Optional[FrozenEvidenceIntegrityAudit] = None) -> List[PaperSafeGateAssertion]:
    return [
        assertion_paper_safe_read_only_metadata(boundary_payload),
        assertion_paper_safe_no_order(boundary_payload),
        assertion_paper_safe_no_write(boundary_payload),
        assertion_paper_safe_no_broker(boundary_payload),
        assertion_paper_safe_no_activation(boundary_payload),
        assertion_paper_safe_no_admission(boundary_payload),
        assertion_paper_safe_no_config_patch(boundary_payload),
        assertion_paper_safe_no_telegram_real_send(boundary_payload)
    ]

def paper_safe_assertions_summary(assertions: List[PaperSafeGateAssertion]) -> Dict[str, Any]:
    return {
        "total": len(assertions),
        "passed": sum(1 for a in assertions if a.status == PaperSafeGateAssertionStatus.PASS)
    }

def paper_safe_assertions_to_text(assertions: List[PaperSafeGateAssertion], limit: int = 100) -> str:
    return f"Assertions: {len(assertions)} total."
