from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_reporting import research_freeze_store_summary_to_text

def test_research_freeze_store_summary_to_text():
    text = research_freeze_store_summary_to_text({"reviews": 5})
    assert "reviews" in text
