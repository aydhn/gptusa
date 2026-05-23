
from usa_signal_bot.paper_no_order_dossier.dossier_evidence import collect_no_order_dossier_evidence

def test_collect_no_order_dossier_evidence():
    evidence = collect_no_order_dossier_evidence({})
    assert len(evidence) > 0
