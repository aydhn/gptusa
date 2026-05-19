from typing import Any, Dict, List, Optional
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewRun

def register_sandbox_preview_run(run: SandboxPreviewRun, registry: Optional[List[SandboxPreviewRun]] = None) -> List[SandboxPreviewRun]:
    if registry is None:
        registry = []
    registry.append(run)
    return registry

def find_sandbox_run_by_id(registry: List[SandboxPreviewRun], run_id: str) -> Optional[SandboxPreviewRun]:
    for r in registry:
        if r.run_id == run_id:
            return r
    return None

def find_sandbox_runs_by_bundle_id(registry: List[SandboxPreviewRun], bundle_id: str) -> List[SandboxPreviewRun]:
    return [r for r in registry if r.bundle_id == bundle_id]

def latest_sandbox_run_for_bundle(registry: List[SandboxPreviewRun], bundle_id: str) -> Optional[SandboxPreviewRun]:
    runs = find_sandbox_runs_by_bundle_id(registry, bundle_id)
    if not runs:
        return None
    # Sort by created_at descending (string comparison works for ISO)
    runs.sort(key=lambda x: x.created_at_utc, reverse=True)
    return runs[0]

def sandbox_session_registry_summary(registry: List[SandboxPreviewRun]) -> Dict[str, Any]:
    return {"total_runs": len(registry)}

def sandbox_session_registry_to_text(registry: List[SandboxPreviewRun], limit: int = 100) -> str:
    return f"Registry has {len(registry)} runs."
