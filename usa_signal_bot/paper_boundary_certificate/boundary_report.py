from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import BoundaryCertificateFullReview, PaperSandboxBoundaryCertificate, AdmissionBlockerReplayResult, NoOrderEvidenceFreezeBundle, create_boundary_full_review_id
from usa_signal_bot.core.enums import PaperSandboxBoundaryReportType
from usa_signal_bot.paper_boundary_certificate.boundary_certificate import build_default_boundary_certificate
from usa_signal_bot.paper_boundary_certificate.blocker_replay_plan import build_default_blocker_replay_plan

def build_boundary_certificate_full_review(no_order_payload: dict[str, Any]) -> BoundaryCertificateFullReview:
    return build_boundary_review_from_parts(build_default_boundary_certificate(no_order_payload.get("candidate_id")))

def build_boundary_review_from_parts(certificate: PaperSandboxBoundaryCertificate, replay_result: AdmissionBlockerReplayResult | None = None, freeze_bundle: NoOrderEvidenceFreezeBundle | None = None) -> BoundaryCertificateFullReview:
    return BoundaryCertificateFullReview(
        review_id=create_boundary_full_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=PaperSandboxBoundaryReportType.FULL_BOUNDARY_CERTIFICATE_REVIEW,
        certificates=[certificate],
        replay_plans=[build_default_blocker_replay_plan(certificate.candidate_id)],
        replay_results=[replay_result] if replay_result else [],
        evidence_freezes=[freeze_bundle] if freeze_bundle else [],
        boundary_rules=certificate.boundary_rules,
        boundary_assertions=certificate.boundary_assertions,
        audit_entries=[],
        output_paths={},
        warnings=[],
        errors=[]
    )

def boundary_certificate_full_review_summary(review: BoundaryCertificateFullReview) -> dict[str, Any]:
    return {"id": review.review_id, "certificates": len(review.certificates)}

def boundary_certificate_limitations_text() -> str:
    return (
        "Limitations:\n"
        "- no broker/live/demo order\n"
        "- no active paper enable\n"
        "- no paper admission\n"
        "- no real paper mutation\n"
        "- no paper order\n"
        "- no Telegram real send\n"
        "- no production config patch\n"
        "- blocker replay is metadata-only\n"
        "- evidence freeze is metadata-only\n"
        "- boundary certificate is not activation\n"
        "- not investment advice\n"
    )

def boundary_certificate_full_review_to_text(review: BoundaryCertificateFullReview, limit: int = 100) -> str:
    return f"{boundary_certificate_full_review_summary(review)}\n{boundary_certificate_limitations_text()}"
