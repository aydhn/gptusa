
from usa_signal_bot.data_providers.provider_reporting import provider_abstraction_limitations_text

def test_provider_reporting():
    txt = provider_abstraction_limitations_text()
    assert "limits" in txt.lower()
