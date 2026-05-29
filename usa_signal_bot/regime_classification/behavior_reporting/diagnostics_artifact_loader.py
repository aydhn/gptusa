import json
from pathlib import Path
from typing import Any

from usa_signal_bot.core.exceptions import DiagnosticsArtifactLoaderError

def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if ".." in str(path):
        raise DiagnosticsArtifactLoaderError("Path traversal not allowed.")
    if not path.exists():
        return []
    res = []
    try:
        with open(path, "r") as f:
            for line in f:
                if line.strip():
                    res.append(json.loads(line))
    except Exception as e:
        raise DiagnosticsArtifactLoaderError(f"Failed to load jsonl from {path}: {e}")
    return res

def load_transition_matrices_jsonl(path: Path) -> list[dict[str, Any]]:
    return _load_jsonl(path)

def load_persistence_profiles_jsonl(path: Path) -> list[dict[str, Any]]:
    return _load_jsonl(path)

def load_duration_profiles_jsonl(path: Path) -> list[dict[str, Any]]:
    return _load_jsonl(path)

def load_churn_diagnostics_jsonl(path: Path) -> list[dict[str, Any]]:
    return _load_jsonl(path)

def load_stability_diagnostics_jsonl(path: Path) -> list[dict[str, Any]]:
    return _load_jsonl(path)

def validate_diagnostics_artifact_payloads(payloads: dict[str, list[dict[str, Any]]]) -> list[str]:
    errs = []
    bad_keys = [
        "api_key", "secret", "token", "password",
        "buy", "sell", "order", "portfolio_weight",
        "target_weight", "allocation", "live_order", "demo_order"
    ]
    for k, vlist in payloads.items():
        for i, v in enumerate(vlist):
            v_str = json.dumps(v).lower()
            for bk in bad_keys:
                if f'"{bk}"' in v_str or f"'{bk}'" in v_str:
                    errs.append(f"Forbidden term '{bk}' found in payload {k} index {i}.")
    return errs

def diagnostics_artifact_loader_summary(payloads: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    return {k: len(v) for k, v in payloads.items()}

def diagnostics_artifact_loader_to_text(payloads: dict[str, list[dict[str, Any]]], limit: int = 200) -> str:
    lines = ["Diagnostics Artifacts:"]
    for k, v in payloads.items():
        lines.append(f"- {k}: {len(v)} items")
    return "\n".join(lines)
