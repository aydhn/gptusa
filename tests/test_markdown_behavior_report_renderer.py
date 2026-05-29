from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    BehaviorReportDocument, BehaviorReportSection
)
from usa_signal_bot.regime_classification.behavior_reporting.markdown_behavior_report_renderer import (
    render_behavior_report_markdown, write_behavior_report_markdown
)

def test_render_behavior_report_markdown():
    doc = BehaviorReportDocument(title="Test Doc")
    sec = BehaviorReportSection(title="Test Sec", body="Sec body")
    doc.sections.append(sec)

    md = render_behavior_report_markdown(doc)
    assert "# Test Doc" in md
    assert "## Test Sec" in md
    assert "Sec body" in md

def test_write_behavior_report_markdown(tmp_path):
    doc = BehaviorReportDocument(title="Test Doc")
    f = tmp_path / "report.md"
    write_behavior_report_markdown(f, doc)
    assert f.exists()
