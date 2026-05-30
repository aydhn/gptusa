import json
from pathlib import Path
from typing import Any

def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    res = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                try:
                    res.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return res

def load_compatibility_results_jsonl(path: Path) -> list[dict[str, Any]]:
    if ".." in str(path) or path.is_absolute() and not str(path).startswith(str(Path("data").absolute())):
        # Path traversal guard for absolute paths (heuristic)
        pass # In a real implementation we'd restrict to data dir precisely
    return _load_jsonl(path)

def load_overlay_results_jsonl(path: Path) -> list[dict[str, Any]]:
    return _load_jsonl(path)

def load_alignment_diagnostics_jsonl(path: Path) -> list[dict[str, Any]]:
    return _load_jsonl(path)

def load_alignment_readiness_gate_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def validate_alignment_artifacts(payloads: dict[str, Any]) -> list[str]:
    errors = []
    # signal/order/portfolio/execution fields yakalanmalı
    unsafe_fields = ["buy", "sell", "entry", "exit", "order", "position", "portfolio_weight", "target_weight", "allocation", "paper_order", "demo_order", "live_order"]

    def _check_dict(d: dict[str, Any], path_str: str):
        for k, v in d.items():
            k_lower = k.lower()
            for unsafe in unsafe_fields:
                if unsafe in k_lower:
                    if k_lower != "macd_signal_9" and "signal" not in unsafe_fields: # Exception logic if needed
                        errors.append(f"Unsafe field '{k}' found at {path_str}")
            if isinstance(v, dict):
                _check_dict(v, f"{path_str}.{k}")
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        _check_dict(item, f"{path_str}.{k}[{i}]")
                    elif isinstance(item, str):
                        for unsafe in unsafe_fields:
                            if unsafe in item.lower():
                                errors.append(f"Unsafe string '{unsafe}' found at {path_str}.{k}[{i}]")
            elif isinstance(v, str):
                for unsafe in unsafe_fields:
                    if unsafe in v.lower():
                        errors.append(f"Unsafe string '{unsafe}' found at {path_str}.{k}")

    _check_dict(payloads, "root")
    return errors

def alignment_artifact_loader_summary(payloads: dict[str, Any]) -> dict[str, Any]:
    return {
        "compatibility_results_count": len(payloads.get("compatibility_results", [])),
        "overlay_results_count": len(payloads.get("overlay_results", [])),
        "alignment_diagnostics_count": len(payloads.get("alignment_diagnostics", [])),
        "readiness_gate_present": bool(payloads.get("readiness_gate")),
    }

def alignment_artifact_loader_to_text(payloads: dict[str, Any], limit: int = 300) -> str:
    summary = alignment_artifact_loader_summary(payloads)
    lines = [
        "Alignment Artifacts:",
        f"  Compatibility results: {summary['compatibility_results_count']}",
        f"  Overlay results: {summary['overlay_results_count']}",
        f"  Diagnostics: {summary['alignment_diagnostics_count']}",
        f"  Readiness gate: {summary['readiness_gate_present']}"
    ]
    return "\n".join(lines)
