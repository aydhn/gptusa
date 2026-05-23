from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import hashlib
import json

from usa_signal_bot.core.enums import AdmissionEvidenceSealStatus
from .admission_review_models import AdmissionEvidenceSeal, create_admission_evidence_seal_id, PaperModeAdmissionReview

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def stable_admission_evidence_seal_hash(payload: Dict[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def build_admission_evidence_seal(admission_review: Optional[PaperModeAdmissionReview] = None, evidence_refs: Optional[List[str]] = None) -> AdmissionEvidenceSeal:
    refs = evidence_refs or []
    if admission_review and admission_review.evidence_refs:
         refs.extend(admission_review.evidence_refs)
    refs = sorted(list(set(refs)))

    status = AdmissionEvidenceSealStatus.SEALED if refs else AdmissionEvidenceSealStatus.FAILED
    seal_hash = stable_admission_evidence_seal_hash({"refs": refs, "review_id": admission_review.admission_review_id if admission_review else None}) if refs else None

    return AdmissionEvidenceSeal(
        seal_id=create_admission_evidence_seal_id(),
        created_at_utc=_now(),
        status=status,
        evidence_refs=refs,
        sealed=True if seal_hash else False,
        immutable=True if seal_hash else False,
        warnings=[],
        errors=[],
        candidate_id=admission_review.candidate_id if admission_review else None,
        source_review_id=admission_review.admission_review_id if admission_review else None,
        seal_hash=seal_hash
    )

def validate_admission_evidence_seal(seal: AdmissionEvidenceSeal) -> List[str]:
    errors = []
    if seal.sealed and not seal.immutable:
        errors.append("If sealed is true, immutable must be true")
    if not seal.seal_hash and seal.sealed:
         errors.append("If sealed is true, seal_hash must be present")
    if seal.status == AdmissionEvidenceSealStatus.FAILED:
         errors.append("Evidence seal failed")
    return errors

def admission_evidence_seal_summary(seal: AdmissionEvidenceSeal) -> Dict[str, Any]:
    return {
        "status": seal.status,
        "sealed": seal.sealed,
        "refs_count": len(seal.evidence_refs),
        "hash_prefix": seal.seal_hash[:8] if seal.seal_hash else None
    }

def admission_evidence_seal_to_text(seal: AdmissionEvidenceSeal) -> str:
    return json.dumps(admission_evidence_seal_summary(seal), indent=2)
