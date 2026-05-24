import pytest
from usa_signal_bot.advanced_runtime.provider_quality_hints import default_provider_quality_hints

def test_hints():
    assert len(default_provider_quality_hints("test")) == 0
