import pytest
from usa_signal_bot.backtesting.benchmark_comparison.benchmark_safety_validator import (
    benchmark_text_has_trade_or_execution_language,
)


def test_benchmark_text_has_trade_or_execution_language_safe():
    # Test cases that should return False (safe language)
    assert (
        benchmark_text_has_trade_or_execution_language("This is a diagnostic metric.")
        is False
    )
    assert (
        benchmark_text_has_trade_or_execution_language("The performance is good.")
        is False
    )
    assert (
        benchmark_text_has_trade_or_execution_language(
            "We observe high tracking error."
        )
        is False
    )
    assert benchmark_text_has_trade_or_execution_language("") is False


def test_benchmark_text_has_trade_or_execution_language_unsafe():
    # Test cases that should return True (unsafe language)
    assert (
        benchmark_text_has_trade_or_execution_language("I definitely buy this asset.")
        is True
    )
    assert (
        benchmark_text_has_trade_or_execution_language(
            "We definitely buy based on this."
        )
        is True
    )
    assert benchmark_text_has_trade_or_execution_language("DEFINITELY BUY!") is True
    assert (
        benchmark_text_has_trade_or_execution_language(
            "This is a definitely buy signal."
        )
        is True
    )


def test_benchmark_text_has_trade_or_execution_language_edge_cases():
    # Test cases for edge cases
    assert (
        benchmark_text_has_trade_or_execution_language("definitely buying") is False
    )  # not exactly "definitely buy"
    assert (
        benchmark_text_has_trade_or_execution_language("definitely  buy") is False
    )  # double space
    assert (
        benchmark_text_has_trade_or_execution_language("definitely, buy") is False
    )  # punctuation in between
