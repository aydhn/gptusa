from typing import Any
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession

def register_shadow_session(session: ShadowRehearsalSession, registry: list[ShadowRehearsalSession] | None = None) -> list[ShadowRehearsalSession]:
    if registry is None:
        registry = []
    registry.append(session)
    return registry

def find_shadow_session_by_id(registry: list[ShadowRehearsalSession], session_id: str) -> ShadowRehearsalSession | None:
    for s in registry:
        if s.session_id == session_id:
            return s
    return None

def find_shadow_sessions_by_bundle_id(registry: list[ShadowRehearsalSession], bundle_id: str) -> list[ShadowRehearsalSession]:
    return [s for s in registry if s.context and s.context.source_bundle_id == bundle_id]

def latest_shadow_session_for_bundle(registry: list[ShadowRehearsalSession], bundle_id: str) -> ShadowRehearsalSession | None:
    sessions = find_shadow_sessions_by_bundle_id(registry, bundle_id)
    if not sessions:
        return None
    return sorted(sessions, key=lambda s: s.created_at_utc, reverse=True)[0]

def shadow_session_registry_summary(registry: list[ShadowRehearsalSession]) -> dict[str, Any]:
    return {
        "total_sessions": len(registry),
        "status_counts": {
             s.status.name: sum(1 for rs in registry if rs.status == s.status) for s in registry
        }
    }

def shadow_session_registry_to_text(registry: list[ShadowRehearsalSession], limit: int = 100) -> str:
    summary = shadow_session_registry_summary(registry)
    text = f"Shadow Session Registry (Total: {summary['total_sessions']})\n"
    for s in registry[:limit]:
        text += f"- {s.session_id} ({s.status.value})\n"
    return text
