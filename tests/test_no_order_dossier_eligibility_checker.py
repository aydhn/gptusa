
from usa_signal_bot.paper_no_order_dossier.eligibility_checker import evaluate_no_order_dossier_eligibility
from usa_signal_bot.core.enums import NoOrderSessionDossierDecision

def test_evaluate_no_order_dossier_eligibility_blocks_on_activation_allowed():
    payload = {"activation_allowed": True}
    decision = evaluate_no_order_dossier_eligibility(payload)
    assert decision == NoOrderSessionDossierDecision.BLOCK
