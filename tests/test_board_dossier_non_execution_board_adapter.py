from usa_signal_bot.paper_readiness_board_dossier.non_execution_board_adapter import board_dossier_full_review_from_non_execution_board

def test_board_dossier_full_review_from_non_execution_board():
    payload = {}
    review = board_dossier_full_review_from_non_execution_board(payload)
    assert review is not None
