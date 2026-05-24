from usa_signal_bot.paper_readiness_board_dossier.paper_runtime_adapter import build_read_only_paper_snapshot_for_board_dossier

def test_build_read_only_paper_snapshot_for_board_dossier():
    snapshot = build_read_only_paper_snapshot_for_board_dossier({})
    assert snapshot["read_only"] is True
    assert snapshot["paper_order_executed"] is False
