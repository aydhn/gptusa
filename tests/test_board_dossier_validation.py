from usa_signal_bot.paper_readiness_board_dossier.board_dossier_validation import validate_no_live_execution_language_in_board_dossier

def test_validate_no_live_execution_language_in_board_dossier():
    res = validate_no_live_execution_language_in_board_dossier("sent to broker")
    assert res.valid is False
