
from usa_signal_bot.data_providers.provider_schema_mapper import canonical_ohlcv_schema

def test_provider_schema_mapper():
    schema = canonical_ohlcv_schema()
    assert "symbol" in schema
    assert "close" in schema
