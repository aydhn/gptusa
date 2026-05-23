
from usa_signal_bot.paper_no_order_dossier.bridge_replay_audit_seal import build_bridge_replay_audit_seal

def test_build_bridge_replay_audit_seal_metadata_only():
    seal = build_bridge_replay_audit_seal({"dangerous_allowed_count": 0, "bridge_replay_result": {"status": "ALL_DANGEROUS_ROUTES_DENIED"}})
    assert seal.sealed is True
    assert seal.immutable is True
    assert seal.dangerous_allowed_count == 0
