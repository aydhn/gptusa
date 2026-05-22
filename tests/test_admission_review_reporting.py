from usa_signal_bot.paper_admission_review.admission_review_reporting import admission_review_full_report_to_text
from usa_signal_bot.paper_admission_review.admission_report import build_admission_review_full_report

def test_admission_review_reporting():
    report = build_admission_review_full_report({})
    text = admission_review_full_report_to_text(report)
    assert isinstance(text, str)
    assert report.report_id in text
