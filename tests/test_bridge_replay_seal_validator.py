
from usa_signal_bot.paper_no_order_dossier.bridge_replay_seal_validator import bridge_replay_seal_allows_admission
from usa_signal_bot.paper_no_order_dossier.bridge_replay_audit_seal import build_bridge_replay_audit_seal

def test_bridge_replay_seal_allows_admission_is_false():
    seal = build_bridge_replay_audit_seal({"dangerous_allowed_count": 0})
    assert bridge_replay_seal_allows_admission(seal) is False
