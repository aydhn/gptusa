
from usa_signal_bot.paper_no_order_dossier.paper_runtime_adapter import build_read_only_paper_snapshot_for_no_order_dossier

def test_build_read_only_paper_snapshot_for_no_order_dossier():
    snap = build_read_only_paper_snapshot_for_no_order_dossier({"test": "data"})
    assert snap["is_read_only"] is True
    assert snap["paper_state_committed"] is False
