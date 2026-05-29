from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    BehaviorReportDocument, BehaviorReportSection
)
from usa_signal_bot.regime_classification.behavior_reporting.text_behavior_report_renderer import (
    render_behavior_report_text, write_behavior_report_text
)

def test_render_behavior_report_text():
    doc = BehaviorReportDocument(title="Test Doc")
    sec = BehaviorReportSection(title="Test Sec", body="Sec body")
    doc.sections.append(sec)

    txt = render_behavior_report_text(doc)
    assert "REPORT: Test Doc" in txt
    assert "[TEST SEC]" in txt
    assert "Sec body" in txt

def test_write_behavior_report_text(tmp_path):
    doc = BehaviorReportDocument(title="Test Doc")
    f = tmp_path / "report.txt"
    write_behavior_report_text(f, doc)
    assert f.exists()
