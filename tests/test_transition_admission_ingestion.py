
from usa_signal_bot.paper_no_write_transition.admission_ingestion import ingest_admission_review_full_report
def test_ingest():
    assert ingest_admission_review_full_report({"a": 1}) == {"a": 1}
