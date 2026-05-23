
from usa_signal_bot.paper_no_order_dossier.no_order_continuity import validate_no_order_dossier_continuity

def test_validate_no_order_dossier_continuity():
    reasons = validate_no_order_dossier_continuity(None, None, None)
    assert len(reasons) == 0
