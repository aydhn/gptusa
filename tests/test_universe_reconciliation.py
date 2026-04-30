import pytest
from usa_signal_bot.universe.reconciliation import reconcile_universe_symbols
from usa_signal_bot.core.enums import UniverseConflictResolution, AssetType
from usa_signal_bot.universe.models import UniverseDefinition, UniverseSymbol
from usa_signal_bot.universe.sources import UniverseSourceLoadResult, UniverseSource, UniverseSourceType, UniverseLayer
from usa_signal_bot.core.exceptions import UniverseReconciliationError

def _make_source_result(name: str, priority: int, symbols: list) -> UniverseSourceLoadResult:
    src = UniverseSource(f"{name}_id", name, UniverseSourceType.PRESET, UniverseLayer.CORE, priority=priority)
    univ = UniverseDefinition(name=name, symbols=symbols)
    return UniverseSourceLoadResult(src, univ, True, len(symbols))

def test_reconciliation_deduplicates():
    s1 = _make_source_result("src1", 10, [UniverseSymbol(symbol="AAPL"), UniverseSymbol(symbol="MSFT")])
    s2 = _make_source_result("src2", 20, [UniverseSymbol(symbol="AAPL"), UniverseSymbol(symbol="GOOG")])

    univ, report = reconcile_universe_symbols([s1, s2])

    assert len(univ.symbols) == 3
    assert report.total_input_symbols == 4
    assert report.total_output_symbols == 3
    assert report.duplicate_count == 1

def test_reconciliation_conflict_resolution():
    sym1 = UniverseSymbol(symbol="AAPL", active=False, name="Apple")
    sym2 = UniverseSymbol(symbol="AAPL", active=True, name="Apple Inc.", sector="Tech")

    s1 = _make_source_result("src1", 10, [sym1])
    s2 = _make_source_result("src2", 20, [sym2])

    # Prefer Active
    univ, report = reconcile_universe_symbols([s1, s2], UniverseConflictResolution.PREFER_ACTIVE)
    assert univ.symbols[0].active is True

    # Prefer Complete Metadata
    univ, report = reconcile_universe_symbols([s1, s2], UniverseConflictResolution.PREFER_COMPLETE_METADATA)
    assert univ.symbols[0].sector == "Tech"

    # Error on conflict (active isn't a conflict in the strict sense, but let's make an asset type conflict)
    sym3 = UniverseSymbol(symbol="AAPL", asset_type=AssetType.ETF)
    s3 = _make_source_result("src3", 30, [sym3])

    with pytest.raises(UniverseReconciliationError):
        reconcile_universe_symbols([s1, s3], UniverseConflictResolution.ERROR_ON_CONFLICT)
