from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_observer.observer_models import ObserverRuntimeSession

def register_observer_session(session: ObserverRuntimeSession, registry: Optional[List[ObserverRuntimeSession]] = None) -> List[ObserverRuntimeSession]:
    if registry is None:
        registry = []
    # Avoid duplicates
    existing = find_observer_session_by_id(registry, session.session_id)
    if existing:
        return registry
    registry.append(session)
    return registry

def find_observer_session_by_id(registry: List[ObserverRuntimeSession], session_id: str) -> Optional[ObserverRuntimeSession]:
    for s in registry:
        if s.session_id == session_id:
            return s
    return None

def find_observer_sessions_by_candidate_id(registry: List[ObserverRuntimeSession], candidate_id: str) -> List[ObserverRuntimeSession]:
    return [s for s in registry if s.context and s.context.candidate_id == candidate_id]

def latest_observer_session_for_candidate(registry: List[ObserverRuntimeSession], candidate_id: str) -> Optional[ObserverRuntimeSession]:
    sessions = find_observer_sessions_by_candidate_id(registry, candidate_id)
    if not sessions:
        return None
    # Sort by created_at desc
    return sorted(sessions, key=lambda x: x.created_at_utc, reverse=True)[0]

def observer_session_registry_summary(registry: List[ObserverRuntimeSession]) -> Dict[str, Any]:
    return {"total_sessions": len(registry)}

def observer_session_registry_to_text(registry: List[ObserverRuntimeSession], limit: int = 100) -> str:
    return f"Registry contains {len(registry)} sessions."
