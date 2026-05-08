import tempfile
from pathlib import Path
from usa_signal_bot.paper.paper_analytics_store import write_paper_analytics_bundle_json, list_paper_analytics_reports

def test_paper_analytics_store():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        target = root / "paper" / "analytics" / "test_report" / "bundle.json"

        bundle = {"test": 123}
        write_paper_analytics_bundle_json(target, bundle)

        assert target.exists()
        reports = list_paper_analytics_reports(root)
        assert len(reports) == 1
        assert reports[0].name == "test_report"
