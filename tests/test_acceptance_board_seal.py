from usa_signal_bot.paper_readiness_board_dossier.acceptance_board_seal import build_acceptance_board_seal

def test_build_acceptance_board_seal():
    payload = {
        "non_execution_board": {"decision": "PASS_TO_NON_EXECUTION_BOARD_DOSSIER"},
        "runtime_replay_result": {"status": "COMPLETED_ROUTE_SAFE", "all_dangerous_routes_denied": True},
        "seal_integrity_audit": {"status": "VALIDATED"}
    }
    seal = build_acceptance_board_seal(payload)
    assert seal.sealed is True
    assert seal.immutable is True
    assert seal.allows_shadow_launch is False
