
from usa_signal_bot.paper_no_order_dossier.bridge_ingestion import bridge_review_supports_no_order_dossier

def test_bridge_review_supports_no_order_dossier():
    supports, _ = bridge_review_supports_no_order_dossier({
        "activation_allowed": False,
        "dangerous_allowed_count": 0,
        "no_order_session": {"status": "COMPLETED_NO_ORDER"},
        "bridge_replay_result": {"status": "ALL_DANGEROUS_ROUTES_DENIED"}
    })
    assert supports is True
