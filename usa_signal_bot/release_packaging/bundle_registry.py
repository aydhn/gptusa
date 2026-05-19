from typing import Any, Dict, List, Optional
from usa_signal_bot.release_packaging.packaging_models import VersionedCandidateBundle

def register_bundle(bundle: VersionedCandidateBundle, registry: Optional[List[VersionedCandidateBundle]] = None) -> List[VersionedCandidateBundle]:
    if registry is None:
        registry = []
    registry.append(bundle)
    return registry

def find_bundle_by_id(registry: List[VersionedCandidateBundle], bundle_id: str) -> Optional[VersionedCandidateBundle]:
    for b in registry:
        if b.bundle_id == bundle_id:
            return b
    return None

def find_bundles_by_candidate_id(registry: List[VersionedCandidateBundle], candidate_id: str) -> List[VersionedCandidateBundle]:
    return [b for b in registry if b.source_candidate_id == candidate_id]

def latest_bundle_for_candidate(registry: List[VersionedCandidateBundle], candidate_id: str) -> Optional[VersionedCandidateBundle]:
    matches = find_bundles_by_candidate_id(registry, candidate_id)
    if not matches:
        return None
    matches.sort(key=lambda x: x.bundle_version, reverse=True)
    return matches[0]

def bundle_registry_summary(registry: List[VersionedCandidateBundle]) -> Dict[str, Any]:
    return {"total_bundles": len(registry)}

def bundle_registry_to_text(registry: List[VersionedCandidateBundle], limit: int = 100) -> str:
    return f"Registry has {len(registry)} bundles."
