from usa_signal_bot.paper_readiness_board_dossier.dossier_evidence import collect_board_dossier_evidence

def test_board_dossier_evidence():
    payload = {
        "non_execution_board": {"decision": "PASS_TO_NON_EXECUTION_BOARD_DOSSIER"},
    }
    items = collect_board_dossier_evidence(payload)
    assert len(items) >= 13
