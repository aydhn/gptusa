import json
from pathlib import Path
from typing import Any
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import BehaviorReportDocument

def render_behavior_report_json(document: BehaviorReportDocument) -> dict[str, Any]:
    return document.to_dict()

def write_behavior_report_json(path: Path, document: BehaviorReportDocument, overwrite: bool = False) -> Path:
    if path.exists() and not overwrite:
        return path
    with open(path, "w") as f:
        json.dump(render_behavior_report_json(document), f, indent=2)
    return path

def validate_rendered_behavior_json(payload: dict[str, Any]) -> list[str]:
    return []

def json_behavior_report_renderer_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"keys": list(payload.keys())}
