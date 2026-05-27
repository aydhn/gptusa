from pathlib import Path
from typing import Any
from usa_signal_bot.core.exceptions import MarkdownReportRendererError
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import ResearchReportDocument, ResearchReportSection

def validate_rendered_markdown(text: str) -> list[str]:
    errors = []
    # simple checks
    if "buy signal" in text.lower() or "sell signal" in text.lower():
        errors.append("Markdown contains trade signal language")
    return errors

def render_report_section_markdown(section: ResearchReportSection) -> str:
    lines = [f"## {section.title}\n", f"{section.body}\n"]
    if section.bullet_points:
        for bp in section.bullet_points:
            lines.append(f"- {bp}")
        lines.append("")
    return "\n".join(lines)

def render_research_report_markdown(document: ResearchReportDocument) -> str:
    lines = [f"# {document.title}\n"]
    for sec in document.sections:
        lines.append(render_report_section_markdown(sec))
    return "\n".join(lines)

def write_research_report_markdown(path: Path, document: ResearchReportDocument, overwrite: bool = False) -> Path:
    if path.exists() and not overwrite:
        raise MarkdownReportRendererError(f"File {path} exists and overwrite is False")

    text = render_research_report_markdown(document)
    errs = validate_rendered_markdown(text)
    if errs:
        raise MarkdownReportRendererError(f"Validation failed: {errs}")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    return path

def markdown_report_renderer_summary(text: str) -> dict[str, Any]:
    return {"length": len(text)}
