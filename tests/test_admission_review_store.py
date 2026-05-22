import tempfile
from pathlib import Path
from usa_signal_bot.paper_admission_review.admission_review_store import write_admission_full_report_json, read_admission_full_report_json
from usa_signal_bot.paper_admission_review.admission_report import build_admission_review_full_report

def test_admission_review_store():
    with tempfile.TemporaryDirectory() as tmpdir:
        data_root = Path(tmpdir)
        payload = {}
        report = build_admission_review_full_report(payload)

        path = data_root / "test.json"
        write_admission_full_report_json(path, report)

        loaded = read_admission_full_report_json(path)
        assert loaded["report_id"] == report.report_id
