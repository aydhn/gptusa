from typing import Any
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import BoundaryCertificateFullReview

def boundary_evidence_from_bridge(payload: dict[str, Any]) -> list[str]:
    return [payload.get("bridge_id", "")]

def bridge_supports_boundary_certificate(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    return True, []

def attach_boundary_hint_to_bridge_payload(payload: dict[str, Any], review: BoundaryCertificateFullReview) -> dict[str, Any]:
    res = dict(payload)
    res["boundary_certificate_hint"] = review.review_id
    return res

def bridge_boundary_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"id": payload.get("bridge_id")}

def bridge_adapter_to_text(payload: dict[str, Any]) -> str:
    return str(bridge_boundary_summary(payload))
