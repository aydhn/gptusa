from usa_signal_bot.paper_admission_review.board_adapter import admission_evidence_from_board

def test_admission_evidence_from_board():
    refs = admission_evidence_from_board({"board_evidence_ref": "ref1"})
    assert "ref1" in refs

    refs = admission_evidence_from_board({})
    assert len(refs) == 0
