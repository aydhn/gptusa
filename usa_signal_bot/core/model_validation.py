from enum import Enum
from typing import Any
from .exceptions import DataValidationError

def ensure_non_empty_string(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise DataValidationError(f"'{field_name}' must be a non-empty string.")

def ensure_positive_number(value: int | float, field_name: str) -> None:
    if not isinstance(value, (int, float)):
        raise DataValidationError(f"'{field_name}' must be a number.")
    if value <= 0:
        raise DataValidationError(f"'{field_name}' must be greater than zero.")

def ensure_non_negative_number(value: int | float, field_name: str) -> None:
    if not isinstance(value, (int, float)):
        raise DataValidationError(f"'{field_name}' must be a number.")
    if value < 0:
        raise DataValidationError(f"'{field_name}' must be zero or greater.")

def ensure_ratio(value: float, field_name: str) -> None:
    if not isinstance(value, (int, float)):
        raise DataValidationError(f"'{field_name}' must be a number.")
    if not (0.0 <= float(value) <= 1.0):
        raise DataValidationError(f"'{field_name}' must be between 0.0 and 1.0 inclusive.")

def ensure_enum_value(value: Any, enum_cls: type[Enum], field_name: str) -> None:
    try:
        enum_cls(value)
    except ValueError:
        raise DataValidationError(f"'{field_name}' must be a valid {enum_cls.__name__} value.")

def ensure_list(value: Any, field_name: str) -> None:
    if not isinstance(value, list):
        raise DataValidationError(f"'{field_name}' must be a list.")

def ensure_dict(value: Any, field_name: str) -> None:
    if not isinstance(value, dict):
        raise DataValidationError(f"'{field_name}' must be a dictionary.")

def validate_ohlcv_prices(open_price: float, high: float, low: float, close: float) -> None:
    for price, name in [(open_price, 'open'), (high, 'high'), (low, 'low'), (close, 'close')]:
        ensure_positive_number(price, name)

    if high < low:
        raise DataValidationError("high price cannot be less than low price.")
