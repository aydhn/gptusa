from typing import Any, List, Optional
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import DryRunBridgeSession

def register_dry_run_bridge_session(session: DryRunBridgeSession, registry: Optional[List[DryRunBridgeSession]] = None) -> List[DryRunBridgeSession]:
    if registry is None:
        registry = []

    existing = find_dry_run_session_by_id(registry, session.session_id)
    if existing:
        registry.remove(existing)

    registry.append(session)
    # Sort descending by creation date
    registry.sort(key=lambda s: s.created_at_utc, reverse=True)
    return registry

def find_dry_run_session_by_id(registry: List[DryRunBridgeSession], session_id: str) -> Optional[DryRunBridgeSession]:
    for session in registry:
        if session.session_id == session_id:
            return session
    return None

def find_dry_run_sessions_by_candidate_id(registry: List[DryRunBridgeSession], candidate_id: str) -> List[DryRunBridgeSession]:
    return [s for s in registry if s.context and s.context.candidate_id == candidate_id]

def latest_dry_run_session_for_candidate(registry: List[DryRunBridgeSession], candidate_id: str) -> Optional[DryRunBridgeSession]:
    sessions = find_dry_run_sessions_by_candidate_id(registry, candidate_id)
    return sessions[0] if sessions else None

def dry_run_session_registry_summary(registry: List[DryRunBridgeSession]) -> dict[str, Any]:
    return {
        "total_sessions": len(registry),
        "candidates": list(set(s.context.candidate_id for s in registry if s.context and s.context.candidate_id))
    }

def dry_run_session_registry_to_text(registry: List[DryRunBridgeSession], limit: int = 100) -> str:
    summary = dry_run_session_registry_summary(registry)
    return f"Session Registry: {summary['total_sessions']} sessions across {len(summary['candidates'])} candidates."
