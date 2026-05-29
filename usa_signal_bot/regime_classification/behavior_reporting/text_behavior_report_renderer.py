from pathlib import Path
from typing import Any
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import BehaviorReportDocument

def render_behavior_report_text(document: BehaviorReportDocument) -> str:
    lines = [f"REPORT: {document.title}\n"]
    for s in document.sections:
        lines.append(f"[{s.title.upper()}]\n{s.body}\n")
    return "\n".join(lines)

def write_behavior_report_text(path: Path, document: BehaviorReportDocument, overwrite: bool = False) -> Path:
    if path.exists() and not overwrite:
        return path
    with open(path, "w") as f:
        f.write(render_behavior_report_text(document))
    return path

def validate_rendered_behavior_text(text: str) -> list[str]:
    return []

def text_behavior_report_renderer_summary(text: str) -> dict[str, Any]:
    return {"chars": len(text)}
