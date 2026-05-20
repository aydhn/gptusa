from typing import Any, List, Dict

def count_proposals_by_type(sessions: List[dict[str, Any]]) -> Dict[str, int]:
    counts = {}
    for s in sessions:
        for p in s.get("proposals", []):
            t = p.get("type", "UNKNOWN")
            counts[t] = counts.get(t, 0) + 1
    return counts

def count_proposals_by_status(sessions: List[dict[str, Any]]) -> Dict[str, int]:
    counts = {}
    for s in sessions:
        for p in s.get("proposals", []):
            st = p.get("status", "UNKNOWN")
            counts[st] = counts.get(st, 0) + 1
    return counts

def proposal_history_warnings(sessions: List[dict[str, Any]]) -> List[str]:
    warnings = []
    st_counts = count_proposals_by_status(sessions)
    if st_counts.get("BLOCKED", 0) > 0:
        warnings.append(f"{st_counts['BLOCKED']} proposals were blocked.")
    return warnings

def aggregate_proposal_history(sessions: List[dict[str, Any]]) -> dict[str, Any]:
    total = 0
    for s in sessions:
        total += len(s.get("proposals", []))

    return {
        "total_proposals": total,
        "by_type": count_proposals_by_type(sessions),
        "by_status": count_proposals_by_status(sessions),
        "warnings": proposal_history_warnings(sessions)
    }

def proposal_history_to_text(payload: dict[str, Any]) -> str:
    return f"Proposal History\nTotal: {payload.get('total_proposals', 0)}\nWarnings: {len(payload.get('warnings', []))}"
