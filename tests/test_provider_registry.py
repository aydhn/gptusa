
from usa_signal_bot.data_providers.provider_registry import build_provider_registry_entries, provider_registry_summary

def test_provider_registry():
    entries = build_provider_registry_entries()
    assert isinstance(entries, list)
    summary = provider_registry_summary(entries)
    assert "total" in summary
