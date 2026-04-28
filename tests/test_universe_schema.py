import pytest
from usa_signal_bot.universe.schema import (
    get_required_columns, validate_universe_columns, normalize_universe_row
)
from usa_signal_bot.core.exceptions import UniverseValidationError

def test_required_columns():
    cols = get_required_columns()
    assert "symbol" in cols
    assert "asset_type" in cols

def test_validate_universe_columns():
    # Valid
    validate_universe_columns(["symbol", "asset_type", "name"])

    # Invalid
    with pytest.raises(UniverseValidationError, match="Missing required universe columns"):
        validate_universe_columns(["symbol", "name"])

def test_normalize_universe_row():
    row = {"symbol": "AAPL", "asset_type": "STOCK"}
    norm = normalize_universe_row(row)

    assert norm["currency"] == "USD" # Default added
    assert norm["active"] == "true" # Default added
    assert norm["asset_type"] == "stock" # Lowercased
