import pytest
from usa_signal_bot.paper_pre_rehearsal.promotion_dossier_adapter import promotion_dossier_supports_pre_paper_rehearsal

def test_dossier():
    supports, _ = promotion_dossier_supports_pre_paper_rehearsal({"dossier_status": "APPROVED_FOR_SANDBOX"})
    assert supports
