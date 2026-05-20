from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession

def register_shadow_session(session: ShadowRehearsalSession, registry: Optional[List[ShadowRehearsalSession]] = None) -> List[ShadowRehearsalSession]:
    if registry is None:
        registry = []
    registry.append(session)
    return registry

def find_shadow_session_by_id(registry: List[ShadowRehearsalSession], session_id: str) -> Optional[ShadowRehearsalSession]:
    for s in registry:
        if s.session_id == session_id:
            return s
    return None

def find_shadow_sessions_by_bundle_id(registry: List[ShadowRehearsalSession], bundle_id: str) -> List[ShadowRehearsalSession]:
    return [s for s in registry if s.context and s.context.source_bundle_id == bundle_id]

def latest_shadow_session_for_bundle(registry: List[ShadowRehearsalSession], bundle_id: str) -> Optional[ShadowRehearsalSession]:
    sessions = find_shadow_sessions_by_bundle_id(registry, bundle_id)
    if not sessions:
        return None
    # Sort by created_at_utc desc
    return sorted(sessions, key=lambda s: s.created_at_utc, reverse=True)[0]

def shadow_session_registry_summary(registry: List[ShadowRehearsalSession]) -> Dict[str, Any]:
    return {
        "total_sessions": len(registry),
        "completed_sessions": sum(1 for s in registry if s.status == "COMPLETED"),
        "failed_sessions": sum(1 for s in registry if s.status == "FAILED")
    }

def shadow_session_registry_to_text(registry: List[ShadowRehearsalSession], limit: int = 100) -> str:
    s = shadow_session_registry_summary(registry)
    return f"ShadowRegistry(total={s['total_sessions']}, completed={s['completed_sessions']})"
