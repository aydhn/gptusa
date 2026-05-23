from usa_signal_bot.paper_admission_review.dry_admission_adapter import admission_full_report_from_dry_admission

def test_admission_full_report_from_dry_admission():
    payload = {}
    report = admission_full_report_from_dry_admission(payload)
    assert report is not None
