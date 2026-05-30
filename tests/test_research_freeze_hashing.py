from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_hashing import compute_text_hash

def test_compute_text_hash():
    h1 = compute_text_hash("hello")
    h2 = compute_text_hash("hello")
    assert h1 == h2
    assert len(h1) == 64
