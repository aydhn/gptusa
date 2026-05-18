import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.core.enums import ExperimentArtifactType
from usa_signal_bot.research_execution.execution_models import ExperimentArtifact, create_experiment_artifact_id

def artifact_payload_checksum(payload: dict[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

def create_artifact_from_payload(run_id: str, artifact_type: ExperimentArtifactType, payload: dict[str, Any], path: str | None = None) -> ExperimentArtifact:
    from usa_signal_bot.research_execution.config_snapshot import redact_config_secrets
    safe_payload = redact_config_secrets(payload)

    summary = {
        "keys": list(safe_payload.keys()),
        "has_error": "error" in safe_payload,
        "is_redacted_safe": True
    }

    return ExperimentArtifact(
        artifact_id=create_experiment_artifact_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        artifact_type=artifact_type,
        run_id=run_id,
        path=path,
        payload_summary=summary,
        checksum=artifact_payload_checksum(safe_payload),
        warnings=[],
        errors=[],
        metadata={}
    )

def summarize_artifacts(artifacts: list[ExperimentArtifact]) -> dict[str, Any]:
    counts = {}
    for a in artifacts:
        t = a.artifact_type.value
        counts[t] = counts.get(t, 0) + 1

    return {
        "total_artifacts": len(artifacts),
        "type_counts": counts
    }

def filter_artifacts_by_type(artifacts: list[ExperimentArtifact], artifact_type: ExperimentArtifactType) -> list[ExperimentArtifact]:
    return [a for a in artifacts if a.artifact_type == artifact_type]

def artifact_manager_to_text(artifacts: list[ExperimentArtifact], limit: int = 100) -> str:
    summary = summarize_artifacts(artifacts)
    lines = ["--- ARTIFACTS SUMMARY ---"]
    lines.append(f"Total: {summary['total_artifacts']}")
    for k, v in summary['type_counts'].items():
        lines.append(f"  {k}: {v}")

    lines.append("\nRecent Artifacts:")
    for a in artifacts[:limit]:
        lines.append(f"  - {a.artifact_id} ({a.artifact_type.value}) path={a.path}")

    return "\n".join(lines)
