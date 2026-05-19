from typing import Any, Dict, List, Optional
from usa_signal_bot.release_sandbox.sandbox_models import SandboxPreviewRun

def register_sandbox_preview_run(run: SandboxPreviewRun, registry: Optional[List[SandboxPreviewRun]] = None) -> List[SandboxPreviewRun]:
    if registry is None:
        registry = []
    registry.append(run)
    return registry

def find_sandbox_run_by_id(registry: List[SandboxPreviewRun], run_id: str) -> Optional[SandboxPreviewRun]:
    for run in registry:
        if run.run_id == run_id:
            return run
    return None

def find_sandbox_runs_by_bundle_id(registry: List[SandboxPreviewRun], bundle_id: str) -> List[SandboxPreviewRun]:
    return [run for run in registry if run.bundle_id == bundle_id]

def latest_sandbox_run_for_bundle(registry: List[SandboxPreviewRun], bundle_id: str) -> Optional[SandboxPreviewRun]:
    runs = find_sandbox_runs_by_bundle_id(registry, bundle_id)
    if not runs:
        return None
    # Assuming the registry is appended in order
    return runs[-1]

def sandbox_session_registry_summary(registry: List[SandboxPreviewRun]) -> Dict[str, Any]:
    return {
        "total_runs": len(registry)
    }

def sandbox_session_registry_to_text(registry: List[SandboxPreviewRun], limit: int = 100) -> str:
    summary = sandbox_session_registry_summary(registry)
    return f"Sandbox Session Registry: {summary['total_runs']} runs registered."
