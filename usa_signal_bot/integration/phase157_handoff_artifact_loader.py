
from pathlib import Path
from typing import Any, Dict, List
import json
import re

from usa_signal_bot.core.exceptions import Phase158HandoffArtifactLoaderError

FORBIDDEN_FIELDS = [
    "broker_order", "paper_order", "live_order", "sent_to_broker",
    "strategy_active", "deployment_enabled", "production_patch",
    "live_signal", "buy_signal", "sell_signal", "target_weight",
    "portfolio_weight", "actual_target_weight", "allocation",
    "actual_allocation", "capital_allocation", "position_size",
    "order_size", "real_order", "telegram_sent"
]

def _load_json_safe(path: Path) -> Dict[str, Any]:
    if ".." in str(path):
        raise Phase158HandoffArtifactLoaderError("Path traversal attempt detected.")
    if not path.exists():
        raise Phase158HandoffArtifactLoaderError(f"File not found: {path}")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise Phase158HandoffArtifactLoaderError(f"Error loading JSON from {path}: {e}")

def load_phase158_handoff_package_json(path: Path) -> Dict[str, Any]:
    return _load_json_safe(path)

def load_portfolio_band_closure_certificate_json(path: Path) -> Dict[str, Any]:
    return _load_json_safe(path)

def load_phase158_readiness_gate_json(path: Path) -> Dict[str, Any]:
    return _load_json_safe(path)

def validate_phase158_handoff_artifacts(payloads: Dict[str, Any]) -> List[str]:
    violations = []

    # Simple check for forbidden keywords in a string dump of the payload
    payload_str = json.dumps(payloads).lower()
    for field in FORBIDDEN_FIELDS:
        if field.lower() in payload_str:
            violations.append(f"Forbidden field/keyword detected in artifact: {field}")

    # Explicit schema checks
    if payloads.get("live_trading", False):
         violations.append("Live trading flag is set to true.")

    return violations

def phase158_handoff_artifact_loader_summary(payloads: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "keys": list(payloads.keys()),
        "violation_count": len(validate_phase158_handoff_artifacts(payloads))
    }

def phase158_handoff_artifact_loader_to_text(payloads: Dict[str, Any], limit: int = 300) -> str:
    summary = phase158_handoff_artifact_loader_summary(payloads)
    text = f"Artifact Loader Summary: {summary}"
    return text[:limit] + "..." if len(text) > limit else text
