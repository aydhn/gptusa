from typing import Any
from pathlib import Path
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    BehaviorReportDocument, BehaviorReportSection
)

def render_behavior_report_section_markdown(section: BehaviorReportSection) -> str:
    lines = [f"## {section.title}\n", section.body, ""]
    return "\n".join(lines)

def render_behavior_report_markdown(document: BehaviorReportDocument) -> str:
    lines = [f"# {document.title}\n"]
    for s in document.sections:
        lines.append(render_behavior_report_section_markdown(s))
    return "\n".join(lines)

def write_behavior_report_markdown(path: Path, document: BehaviorReportDocument, overwrite: bool = False) -> Path:
    if path.exists() and not overwrite:
        return path
    with open(path, "w") as f:
        f.write(render_behavior_report_markdown(document))
    return path

def validate_rendered_behavior_markdown(text: str) -> list[str]:
    return []

def markdown_behavior_report_renderer_summary(text: str) -> dict[str, Any]:
    return {"chars": len(text)}
