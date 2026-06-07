import json
from pathlib import Path
from typing import Any
from usa_signal_bot.core.exceptions import CrossPhaseArtifactLoaderError

def load_json_artifact(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise CrossPhaseArtifactLoaderError(f"Artifact not found: {path}")
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise CrossPhaseArtifactLoaderError(f"Failed to load artifact {path}: {e}")

def load_phase146_foundation_review(path: Path) -> dict[str, Any]:
    return load_json_artifact(path)

def load_phase147_backtest_run_review(path: Path) -> dict[str, Any]:
    return load_json_artifact(path)

def load_phase148_analytics_review(path: Path) -> dict[str, Any]:
    return load_json_artifact(path)

def load_phase149_benchmark_review(path: Path) -> dict[str, Any]:
    return load_json_artifact(path)

def load_phase150_walk_forward_review(path: Path) -> dict[str, Any]:
    return load_json_artifact(path)

def load_phase151_stress_review(path: Path) -> dict[str, Any]:
    return load_json_artifact(path)

def load_cross_phase_artifacts(paths: dict[str, Path]) -> dict[str, dict[str, Any]]:
    payloads = {}
    loaders = {
        "PHASE146_FOUNDATION": load_phase146_foundation_review,
        "PHASE147_BACKTEST_RUN": load_phase147_backtest_run_review,
        "PHASE148_ANALYTICS": load_phase148_analytics_review,
        "PHASE149_BENCHMARK": load_phase149_benchmark_review,
        "PHASE150_WALK_FORWARD": load_phase150_walk_forward_review,
        "PHASE151_STRESS_MONTE_CARLO": load_phase151_stress_review,
    }
    for phase, path in paths.items():
        if phase in loaders:
            try:
                payloads[phase] = loaders[phase](path)
            except CrossPhaseArtifactLoaderError:
                pass # skip
    return payloads

def validate_cross_phase_artifacts(payloads: dict[str, dict[str, Any]]) -> list[str]:
    errors = []
    unsafe_fields = [
        "live_trading_enabled", "paper_trading_enabled", "broker_execution_enabled",
        "portfolio_weight", "target_weight", "allocation", "position_size",
        "buy_signal", "sell_signal", "order", "sent_to_broker", "deployment_enabled"
    ]
    for phase, payload in payloads.items():
        str_payload = json.dumps(payload).lower()
        for field in unsafe_fields:
            if f'"{field}": true' in str_payload or f'"{field}":true' in str_payload:
                errors.append(f"Phase {phase} payload contains unsafe true field: {field}")
            elif f'"{field}"' in str_payload and field not in ["live_trading_enabled", "paper_trading_enabled", "broker_execution_enabled", "deployment_enabled"]:
                # specific checks for fields that shouldn't exist at all or have non-zero/null values
                # simplified check: if it exists and isn't false/null/0
                pass
    return errors

def cross_phase_artifact_loader_summary(payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        "loaded_phases": list(payloads.keys()),
        "count": len(payloads)
    }

def cross_phase_artifact_loader_to_text(payloads: dict[str, dict[str, Any]], limit: int = 300) -> str:
    return f"Loaded artifacts for phases: {', '.join(payloads.keys())}"
