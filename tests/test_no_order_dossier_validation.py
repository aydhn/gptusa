
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_validation import validate_no_active_paper_language_in_no_order

def test_validate_no_active_paper_language_in_no_order():
    rep = validate_no_active_paper_language_in_no_order("We will canlıya al this.")
    assert rep.valid is False
