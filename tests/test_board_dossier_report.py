from usa_signal_bot.paper_readiness_board_dossier.board_dossier_report import build_board_dossier_full_review

def test_build_board_dossier_full_review():
    payload = {
        "non_execution_board": {"decision": "PASS_TO_NON_EXECUTION_BOARD_DOSSIER"},
        "runtime_replay_result": {"status": "COMPLETED_ROUTE_SAFE"},
        "seal_integrity_audit": {"status": "VALIDATED"}
    }
    review = build_board_dossier_full_review(payload)
    assert len(review.dossiers) == 1
    assert len(review.shadow_launch_blocker_events) == 11
