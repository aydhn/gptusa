from typing import Any
from datetime import datetime, timezone
import hashlib
import json

from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import (
    PaperSandboxBoundaryCertificate, BoundaryRule, BoundaryAssertion,
    create_boundary_certificate_id
)
from usa_signal_bot.core.enums import PaperSandboxBoundaryCertificateStatus, PaperSandboxBoundaryDecision, PaperSandboxBoundaryRiskFlag

def build_paper_sandbox_boundary_certificate(no_order_payload: dict[str, Any]) -> PaperSandboxBoundaryCertificate:
    return build_default_boundary_certificate(no_order_payload.get("candidate_id"))

def build_default_boundary_certificate(candidate_id: str | None = None) -> PaperSandboxBoundaryCertificate:
    return PaperSandboxBoundaryCertificate(
        certificate_id=create_boundary_certificate_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=PaperSandboxBoundaryCertificateStatus.CREATED,
        decision=PaperSandboxBoundaryDecision.CREATE_BOUNDARY_CERTIFICATE,
        candidate_id=candidate_id,
        source_no_order_review_id=None,
        source_no_order_dossier_id=None,
        source_replay_seal_id=None,
        source_freeze_id=None,
        blocker_replay_result=None,
        evidence_freeze=None,
        boundary_rules=[],
        boundary_assertions=[],
        certificate_hash=None,
        sealed=True,
        immutable=True,
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        admission_allowed=False,
        transition_allowed=False,
        all_writes_blocked=True,
        order_created=False,
        mutation_detected=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        safety_flags=[],
        required_followups=[],
        warnings=[],
        errors=[]
    )

def stable_boundary_certificate_hash(payload: dict[str, Any]) -> str:
    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def collect_boundary_certificate_safety_flags(no_order_payload: dict[str, Any], rules: list[BoundaryRule], assertions: list[BoundaryAssertion]) -> list[PaperSandboxBoundaryRiskFlag]:
    return []

def boundary_certificate_summary(certificate: PaperSandboxBoundaryCertificate) -> dict[str, Any]:
    return {"id": certificate.certificate_id, "status": certificate.status.value, "sealed": certificate.sealed}

def boundary_certificate_to_text(certificate: PaperSandboxBoundaryCertificate, limit: int = 100) -> str:
    return str(boundary_certificate_summary(certificate))
