import json
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    BehaviorReportDocument
)
from usa_signal_bot.regime_classification.behavior_reporting.json_behavior_report_renderer import (
    render_behavior_report_json, write_behavior_report_json
)

def test_render_behavior_report_json():
    doc = BehaviorReportDocument(title="Test Doc")
    d = render_behavior_report_json(doc)
    assert d["title"] == "Test Doc"

def test_write_behavior_report_json(tmp_path):
    doc = BehaviorReportDocument(title="Test Doc")
    f = tmp_path / "report.json"
    write_behavior_report_json(f, doc)
    assert f.exists()
