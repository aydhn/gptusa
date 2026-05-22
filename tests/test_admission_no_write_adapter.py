from usa_signal_bot.paper_admission_review.no_write_adapter import admission_evidence_from_no_write

def test_admission_evidence_from_no_write():
    refs = admission_evidence_from_no_write({"evidence_ref": "ref1"})
    assert "ref1" in refs

    refs = admission_evidence_from_no_write({})
    assert len(refs) == 0
