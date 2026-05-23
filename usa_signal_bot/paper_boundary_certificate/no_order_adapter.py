from typing import Any
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import PaperSandboxBoundaryCertificate, AdmissionBlockerReplayResult, NoOrderEvidenceFreezeBundle, BoundaryCertificateFullReview
from usa_signal_bot.paper_boundary_certificate.boundary_certificate import build_default_boundary_certificate
from usa_signal_bot.paper_boundary_certificate.blocker_replay_engine import PaperAdmissionBlockerReplayEngine
from usa_signal_bot.paper_boundary_certificate.blocker_replay_plan import build_default_blocker_replay_plan
from usa_signal_bot.paper_boundary_certificate.evidence_freeze import build_no_order_evidence_freeze_bundle
from usa_signal_bot.paper_boundary_certificate.boundary_report import build_boundary_review_from_parts

def boundary_certificate_from_no_order(payload: dict[str, Any]) -> PaperSandboxBoundaryCertificate:
    return build_default_boundary_certificate(payload.get("candidate_id"))

def blocker_replay_result_from_no_order(payload: dict[str, Any]) -> AdmissionBlockerReplayResult:
    engine = PaperAdmissionBlockerReplayEngine()
    plan = build_default_blocker_replay_plan(payload.get("candidate_id"))
    events = payload.get("admission_blocker_events", [])
    return engine.replay(plan, events)

def evidence_freeze_from_no_order(payload: dict[str, Any]) -> NoOrderEvidenceFreezeBundle:
    return build_no_order_evidence_freeze_bundle(payload)

def boundary_full_review_from_no_order(payload: dict[str, Any]) -> BoundaryCertificateFullReview:
    cert = boundary_certificate_from_no_order(payload)
    replay = blocker_replay_result_from_no_order(payload)
    freeze = evidence_freeze_from_no_order(payload)
    return build_boundary_review_from_parts(cert, replay, freeze)

def attach_boundary_metadata_to_no_order_payload(payload: dict[str, Any], review: BoundaryCertificateFullReview) -> dict[str, Any]:
    res = dict(payload)
    res["boundary_certificate_review"] = review.review_id
    return res

def no_order_boundary_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"candidate": payload.get("candidate_id")}

def no_order_adapter_to_text(payload: dict[str, Any]) -> str:
    return str(no_order_boundary_summary(payload))
