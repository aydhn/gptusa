
from usa_signal_bot.data_providers.provider_report import build_provider_abstraction_full_review

def test_provider_report():
    rev = build_provider_abstraction_full_review()
    assert rev.context.metadata_only is True
