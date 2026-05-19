from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from usa_signal_bot.release_packaging.packaging_models import VersionedCandidateBundle, create_versioned_candidate_bundle_id
from usa_signal_bot.core.enums import ReleaseBundleType, ReleaseBundleStatus

def bundle_from_release_candidate_payload(candidate_payload: Dict[str, Any], governance_payload: Optional[Dict[str, Any]] = None) -> VersionedCandidateBundle:
    b_id = create_versioned_candidate_bundle_id()
    return VersionedCandidateBundle(
        bundle_id=b_id,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        bundle_version="0.1.0",
        bundle_type=ReleaseBundleType.LOCAL_RESEARCH_CANDIDATE,
        status=ReleaseBundleStatus.DRAFT,
        title=candidate_payload.get("title", "Draft Bundle"),
        description=candidate_payload.get("description", "Draft Bundle Description"),
        source_candidate_id=candidate_payload.get("candidate_id"),
        source_experiment_id=candidate_payload.get("experiment_id"),
        source_hypothesis_id=candidate_payload.get("hypothesis_id"),
        source_governance_review_id=governance_payload.get("review_id") if governance_payload else None,
        manifest=None,
        validation_result=None,
        bundle_path=None,
        readme_path=None,
        allowed_for_auto_apply=False,
        allowed_for_live_or_demo_execution=False,
        allowed_for_order_routing=False,
        warnings=[],
        errors=[],
        metadata={}
    )

def bundles_from_governance_review_payload(governance_payload: Dict[str, Any]) -> List[VersionedCandidateBundle]:
    candidates = governance_payload.get("candidates", [])
    bundles = []
    for c in candidates:
        bundles.append(bundle_from_release_candidate_payload(c, governance_payload))
    return bundles

def attach_bundle_metadata_to_governance_review(governance_payload: Dict[str, Any], bundles: List[VersionedCandidateBundle]) -> Dict[str, Any]:
    governance_payload["bundles"] = [{"id": b.bundle_id, "version": b.bundle_version} for b in bundles]
    return governance_payload

def governance_packaging_summary(governance_payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"status": "ok"}

def governance_adapter_to_text(payload: Dict[str, Any]) -> str:
    return "Governance adapter OK."
