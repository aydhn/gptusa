from usa_signal_bot.paper_readiness_board_dossier.board_dossier import build_paper_readiness_board_dossier

def test_build_paper_readiness_board_dossier():
    payload = {
        "non_execution_board": {"decision": "PASS_TO_NON_EXECUTION_BOARD_DOSSIER"},
        "runtime_replay_result": {"status": "COMPLETED_ROUTE_SAFE"},
        "seal_integrity_audit": {"status": "VALIDATED"}
    }
    dossier = build_paper_readiness_board_dossier(payload)
    assert dossier.status.name == "VALIDATED_NON_EXECUTION"
    assert dossier.sealed is True
    assert dossier.allows_active_paper is False
