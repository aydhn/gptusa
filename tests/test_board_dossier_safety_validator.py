from usa_signal_bot.paper_readiness_board_dossier.board_dossier_safety_validator import validate_board_dossier_safety

def test_validate_board_dossier_safety():
    issues = validate_board_dossier_safety()
    assert len(issues) == 0
