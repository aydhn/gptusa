import pytest
from usa_signal_bot.universe.symbols import (
    normalize_symbol, is_valid_symbol, validate_symbol,
    normalize_asset_type, normalize_exchange, normalize_currency,
    parse_active, sort_symbols, deduplicate_symbols
)
from usa_signal_bot.core.enums import AssetType
from usa_signal_bot.core.exceptions import SymbolValidationError

def test_normalize_symbol():
    assert normalize_symbol("aapl") == "AAPL"
    assert normalize_symbol(" msft ") == "MSFT"
    assert normalize_symbol("") == ""
    assert normalize_symbol(None) == ""

def test_is_valid_symbol():
    assert is_valid_symbol("AAPL") is True
    assert is_valid_symbol("BRK.B") is True
    assert is_valid_symbol("SPY-1") is True

    assert is_valid_symbol("") is False
    assert is_valid_symbol("AA PL") is False
    assert is_valid_symbol("HTTP://A") is False
    assert is_valid_symbol("AAPL/USD") is False
    assert is_valid_symbol("VERYLONGSYMBOLNAME123456") is False # over max length 15

def test_validate_symbol():
    validate_symbol("AAPL")

    with pytest.raises(SymbolValidationError, match="cannot be empty"):
        validate_symbol("")

    with pytest.raises(SymbolValidationError, match="invalid characters"):
        validate_symbol("AAPL USD")

    with pytest.raises(SymbolValidationError, match="exceeds maximum length"):
        validate_symbol("A" * 16)

def test_normalize_asset_type():
    assert normalize_asset_type("stock") == AssetType.STOCK
    assert normalize_asset_type("ETF") == AssetType.ETF
    assert normalize_asset_type("") == AssetType.STOCK # default

    with pytest.raises(SymbolValidationError):
        normalize_asset_type("crypto")

def test_normalize_currency():
    assert normalize_currency("") == "USD"
    assert normalize_currency("eur") == "EUR"

def test_parse_active():
    assert parse_active(True) is True
    assert parse_active(False) is False
    assert parse_active(None) is True
    assert parse_active("") is True
    assert parse_active("true") is True
    assert parse_active("yes") is True
    assert parse_active("1") is True
    assert parse_active("false") is False
    assert parse_active("0") is False

def test_deduplicate_symbols():
    syms = ["AAPL", "MSFT", "AAPL", "GOOG"]
    res = deduplicate_symbols(syms)
    assert res == ["AAPL", "MSFT", "GOOG"]

def test_sort_symbols():
    syms = ["MSFT", "AAPL", "GOOG"]
    res = sort_symbols(syms)
    assert res == ["AAPL", "GOOG", "MSFT"]
