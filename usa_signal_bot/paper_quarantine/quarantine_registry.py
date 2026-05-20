from typing import Any
from usa_signal_bot.paper_quarantine.quarantine_models import QuarantinedPaperCandidate

def register_quarantined_candidate(candidate: QuarantinedPaperCandidate, registry: list[QuarantinedPaperCandidate] | None = None) -> list[QuarantinedPaperCandidate]:
    reg = registry if registry is not None else []

    # remove existing
    reg = [c for c in reg if c.candidate_id != candidate.candidate_id]
    reg.append(candidate)

    # sort by created descending
    return sorted(reg, key=lambda x: x.created_at_utc, reverse=True)

def find_quarantined_candidate_by_id(registry: list[QuarantinedPaperCandidate], candidate_id: str) -> QuarantinedPaperCandidate | None:
    for c in registry:
        if c.candidate_id == candidate_id:
            return c
    return None

def find_candidates_by_bundle_id(registry: list[QuarantinedPaperCandidate], bundle_id: str) -> list[QuarantinedPaperCandidate]:
    return [c for c in registry if c.source_bundle_id == bundle_id]

def latest_candidate_for_bundle(registry: list[QuarantinedPaperCandidate], bundle_id: str) -> QuarantinedPaperCandidate | None:
    candidates = find_candidates_by_bundle_id(registry, bundle_id)
    if not candidates:
        return None
    return sorted(candidates, key=lambda x: x.created_at_utc, reverse=True)[0]

def quarantine_registry_summary(registry: list[QuarantinedPaperCandidate]) -> dict[str, Any]:
    return {
        "total_candidates": len(registry),
        "enrolled": len([c for c in registry if c.status.value == "enrolled"]),
        "blocked": len([c for c in registry if c.status.value == "blocked"]),
        "waiting_review": len([c for c in registry if c.status.value == "waiting_manual_review"]),
    }

def quarantine_registry_to_text(registry: list[QuarantinedPaperCandidate], limit: int = 100) -> str:
    summary = quarantine_registry_summary(registry)
    lines = [
        "Quarantine Registry Summary",
        f"Total: {summary['total_candidates']}",
        f"Enrolled: {summary['enrolled']}",
        f"Blocked: {summary['blocked']}",
        f"Waiting Review: {summary['waiting_review']}",
        "-" * 20
    ]
    for c in registry[:limit]:
        lines.append(f"{c.candidate_id} | {c.status.value} | {c.source_bundle_id}")
    return "\n".join(lines)
