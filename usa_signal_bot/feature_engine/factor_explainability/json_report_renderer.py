import json
from pathlib import Path
from typing import Any
from usa_signal_bot.core.exceptions import JsonReportRendererError
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import (
    ResearchReportDocument,
    research_report_document_to_dict
)

def validate_rendered_json(payload: dict[str, Any]) -> list[str]:
    return []

def render_research_report_json(document: ResearchReportDocument) -> dict[str, Any]:
    return research_report_document_to_dict(document)

def write_research_report_json(path: Path, document: ResearchReportDocument, overwrite: bool = False) -> Path:
    if path.exists() and not overwrite:
        raise JsonReportRendererError(f"File {path} exists and overwrite is False")

    payload = render_research_report_json(document)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)
    return path

def json_report_renderer_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"keys": list(payload.keys())}
