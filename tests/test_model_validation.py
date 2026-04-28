import pytest
from enum import Enum
from usa_signal_bot.core.model_validation import (
    ensure_non_empty_string,
    ensure_positive_number,
    ensure_non_negative_number,
    ensure_ratio,
    ensure_enum_value,
    validate_ohlcv_prices
)
from usa_signal_bot.core.exceptions import DataValidationError

def test_ensure_non_empty_string():
    ensure_non_empty_string("valid", "field")
    with pytest.raises(DataValidationError):
        ensure_non_empty_string("", "field")
    with pytest.raises(DataValidationError):
        ensure_non_empty_string("   ", "field")
    with pytest.raises(DataValidationError):
        ensure_non_empty_string(123, "field")

def test_ensure_positive_number():
    ensure_positive_number(1, "field")
    ensure_positive_number(0.1, "field")
    with pytest.raises(DataValidationError):
        ensure_positive_number(0, "field")
    with pytest.raises(DataValidationError):
        ensure_positive_number(-1, "field")

def test_ensure_non_negative_number():
    ensure_non_negative_number(1, "field")
    ensure_non_negative_number(0, "field")
    with pytest.raises(DataValidationError):
        ensure_non_negative_number(-0.1, "field")

def test_ensure_ratio():
    ensure_ratio(0.0, "field")
    ensure_ratio(0.5, "field")
    ensure_ratio(1.0, "field")
    with pytest.raises(DataValidationError):
        ensure_ratio(-0.1, "field")
    with pytest.raises(DataValidationError):
        ensure_ratio(1.1, "field")

class DummyEnum(Enum):
    A = "a"

def test_ensure_enum_value():
    ensure_enum_value("a", DummyEnum, "field")
    ensure_enum_value(DummyEnum.A, DummyEnum, "field")
    with pytest.raises(DataValidationError):
        ensure_enum_value("b", DummyEnum, "field")

def test_validate_ohlcv_prices():
    validate_ohlcv_prices(10, 12, 8, 11)
    with pytest.raises(DataValidationError):
        validate_ohlcv_prices(10, 8, 12, 11)  # high < low
    with pytest.raises(DataValidationError):
        validate_ohlcv_prices(10, 12, -8, 11) # low < 0
