
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_report import build_no_order_dossier_full_review

def test_build_no_order_dossier_full_review():
    review = build_no_order_dossier_full_review({})
    assert len(review.dossiers) > 0
