
from usa_signal_bot.paper_no_write_transition.paper_runtime_adapter import build_read_only_paper_snapshot_for_no_write_transition
def test_paper_runtime_adapter():
    res = build_read_only_paper_snapshot_for_no_write_transition({"a": 1})
    assert res["paper_state_committed"] == False
