import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.core.enums import ResearchRunType
from usa_signal_bot.research_execution.execution_models import ConfigSnapshot, create_config_snapshot_id

def stable_config_hash(config_payload: dict[str, Any]) -> str:
    serialized = json.dumps(config_payload, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

def redact_config_secrets(config_payload: dict[str, Any]) -> dict[str, Any]:
    redacted = {}
    secret_terms = ["api_key", "token", "secret", "password", "bearer", "private_key"]
    for k, v in config_payload.items():
        if isinstance(v, dict):
            redacted[k] = redact_config_secrets(v)
        elif isinstance(v, list):
            redacted[k] = [redact_config_secrets(i) if isinstance(i, dict) else i for i in v]
        else:
            if any(term in k.lower() for term in secret_terms):
                redacted[k] = "[REDACTED]"
            else:
                redacted[k] = v
    return redacted

def build_config_snapshot(config_payload: dict[str, Any], snapshot_type: ResearchRunType, source_ref: str | None = None) -> ConfigSnapshot:
    redacted_payload = redact_config_secrets(config_payload)
    return ConfigSnapshot(
        snapshot_id=create_config_snapshot_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        snapshot_type=snapshot_type,
        config_hash=stable_config_hash(redacted_payload),
        config_payload=redacted_payload,
        source_ref=source_ref,
        warnings=[],
        errors=[],
        metadata={}
    )

def build_baseline_config_snapshot(current_config: dict[str, Any]) -> ConfigSnapshot:
    return build_config_snapshot(current_config, ResearchRunType.BASELINE, source_ref="current_app_config")

def build_candidate_config_snapshot(baseline_config: dict[str, Any], overlay: dict[str, Any] | None = None) -> ConfigSnapshot:
    import copy
    candidate_config = copy.deepcopy(baseline_config)
    if overlay:
        # Simple recursive merge for dict overlay
        def merge(a: dict, b: dict) -> dict:
            for key, val in b.items():
                if key in a and isinstance(a[key], dict) and isinstance(val, dict):
                    merge(a[key], val)
                else:
                    a[key] = val
            return a
        merge(candidate_config, overlay)

    return build_config_snapshot(candidate_config, ResearchRunType.CANDIDATE, source_ref="candidate_overlay_applied")

def diff_config_snapshots(baseline: ConfigSnapshot, candidate: ConfigSnapshot) -> dict[str, Any]:
    baseline_keys = set(baseline.config_payload.keys())
    candidate_keys = set(candidate.config_payload.keys())

    diff = {
        "added": list(candidate_keys - baseline_keys),
        "removed": list(baseline_keys - candidate_keys),
        "changed": []
    }

    for k in baseline_keys.intersection(candidate_keys):
        if baseline.config_payload[k] != candidate.config_payload[k]:
            diff["changed"].append({
                "key": k,
                "baseline": baseline.config_payload[k],
                "candidate": candidate.config_payload[k]
            })

    return diff

def config_snapshot_to_text(snapshot: ConfigSnapshot) -> str:
    lines = []
    lines.append(f"--- CONFIG SNAPSHOT: {snapshot.snapshot_id} ---")
    lines.append(f"Type: {snapshot.snapshot_type.value}")
    lines.append(f"Hash: {snapshot.config_hash}")
    lines.append(f"Created: {snapshot.created_at_utc}")
    lines.append("NOTE: Secrets are strictly redacted. Snapshot is local and safe.")
    return "\n".join(lines)
