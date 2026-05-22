from typing import Any
from usa_signal_bot.paper_no_write_admission.no_write_admission_models import NoWriteAdmissionFullReview

def no_write_evidence_from_firewall_audit(payload: dict[str, Any]) -> list[str]:
    return []

def firewall_audit_supports_no_write_admission(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    return True, []

def attach_no_write_hint_to_firewall_audit_payload(payload: dict[str, Any], review: NoWriteAdmissionFullReview) -> dict[str, Any]:
    return payload

def firewall_audit_no_write_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {}

def firewall_audit_adapter_to_text(payload: dict[str, Any]) -> str:
    return "Firewall Audit Adapter"
