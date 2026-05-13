import pytest
from usa_signal_bot.universe_lifecycle.lifecycle_models import SymbolAliasRecord
from usa_signal_bot.core.enums import SymbolAliasType
from usa_signal_bot.universe_lifecycle.symbol_aliases import (
    alias_for_old_symbol, aliases_for_symbol, resolve_symbol_alias,
    apply_aliases_to_symbols
)

def test_alias_for_old_symbol():
    a = SymbolAliasRecord("id", "FB", "META", SymbolAliasType.TICKER_CHANGE)
    res = alias_for_old_symbol([a], "fb")
    assert res == a

def test_aliases_for_symbol():
    a = SymbolAliasRecord("id", "FB", "META", SymbolAliasType.TICKER_CHANGE)
    res = aliases_for_symbol([a], "META")
    assert len(res) == 1

def test_resolve_symbol_alias():
    a1 = SymbolAliasRecord("id1", "FB", "META", SymbolAliasType.TICKER_CHANGE)
    a2 = SymbolAliasRecord("id2", "SQ", "BLOCK", SymbolAliasType.TICKER_CHANGE)

    res = resolve_symbol_alias("FB", [a1, a2])
    assert res == "META"

    res2 = resolve_symbol_alias("AAPL", [a1, a2])
    assert res2 == "AAPL"

def test_resolve_symbol_alias_with_date():
    a1 = SymbolAliasRecord("id1", "FB", "META", SymbolAliasType.TICKER_CHANGE, effective_date="2022-06-09")

    # As of before effective date -> returns old symbol
    res_before = resolve_symbol_alias("FB", [a1], as_of_date="2022-06-08")
    assert res_before == "FB"

    # As of after effective date -> returns new symbol
    res_after = resolve_symbol_alias("FB", [a1], as_of_date="2022-06-10")
    assert res_after == "META"

def test_apply_aliases_to_symbols():
    a1 = SymbolAliasRecord("id1", "FB", "META", SymbolAliasType.TICKER_CHANGE)
    res = apply_aliases_to_symbols(["AAPL", "FB"], [a1])
    assert res == ["AAPL", "META"]
